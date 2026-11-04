"""GitHub Actions workflow audit (OV-48): inventory/workflow-audit.json.

    python3 tools/audit_workflows.py --workspace ~/ov            # audit every checkout at its HEAD, record the SHAs
    python3 tools/audit_workflows.py --workspace ~/ov --check    # re-read the recorded SHAs and compare

Workflow files are read with `git show <sha>:<path>`, never from the working tree. For each file it records:
- whether the YAML parses;
- the triggers;
- the workflow and job `permissions`;
- runner labels;
- each `uses:` reference, and whether it is pinned to a full commit SHA;
- the names (never the values) of referenced secrets;
- risky constructs: `pull_request_target`, write-all permissions, untrusted `${{ github.event.* }}` text inside
  `run:`.

The archived fork (blhermes-agent) and secret-project/ are out of scope.
Requires PyYAML.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

DOCS = Path(__file__).resolve().parents[1]
OUT = DOCS / "inventory/workflow-audit.json"
SKIP = ("blhermes-agent",)
SHA40 = re.compile(r"@[0-9a-f]{40}$")
UNTRUSTED = re.compile(r"\$\{\{\s*github\.event\.(issue|pull_request|comment|review|head_commit|commits)[^}]*\}\}")


def git(path, *args):
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, check=True).stdout


def repos():
    c = json.loads((DOCS / "constitution/repositories.json").read_text())
    return [r["repo"] for r in (c["repositories"] if isinstance(c, dict) else c)
            if not r["repo"].startswith("secret-project/") and r["repo"] not in SKIP]


def audit_file(text):
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return {"parses": False, "error": str(e).splitlines()[0]}
    if not isinstance(doc, dict):
        return {"parses": False, "error": "not a mapping"}
    on = doc.get("on", doc.get(True))  # YAML 1.1 reads a bare `on:` key as True
    triggers = sorted(on) if isinstance(on, dict) else sorted(on) if isinstance(on, list) else [on]
    jobs = doc.get("jobs") or {}
    uses, runners, job_perms = [], set(), {}
    for name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        ro = job.get("runs-on")
        runners.update(ro if isinstance(ro, list) else [str(ro)] if ro else [])
        if "permissions" in job:
            job_perms[name] = job["permissions"]
        if "uses" in job:
            uses.append(job["uses"])
        uses += [s["uses"] for s in job.get("steps") or [] if isinstance(s, dict) and "uses" in s]
    perms = doc.get("permissions")
    return {
        "parses": True, "name": doc.get("name"), "triggers": [str(t) for t in triggers],
        "permissions": perms, "job_permissions": job_perms,
        "least_privilege": perms is not None or (bool(jobs) and len(job_perms) == len(jobs)),
        "write_all": perms == "write-all" or any(p == "write-all" for p in job_perms.values()),
        "runners": sorted(runners),
        "uses": sorted(set(uses)),
        "unpinned_actions": sorted({u for u in uses if not u.startswith("./") and not SHA40.search(u)}),
        "secrets": sorted(set(re.findall(r"secrets\.([A-Za-z0-9_]+)", text))),
        "pull_request_target": "pull_request_target" in [str(t) for t in triggers],
        "untrusted_in_run": bool(UNTRUSTED.search(text))}


def build(ws, shas):
    rows = {}
    for repo in repos():
        path = ws / repo
        if not (path / ".git").exists():
            continue
        sha = shas.get(repo) or git(path, "rev-parse", "HEAD").strip()
        files = [f for f in git(path, "ls-tree", "-r", "--name-only", sha).splitlines()
                 if f.startswith(".github/workflows/") and f.endswith((".yml", ".yaml"))]
        rows[repo] = {"sha": sha, "workflows": {f: audit_file(git(path, "show", f"{sha}:{f}")) for f in files}}
    wf = [w for r in rows.values() for w in r["workflows"].values()]
    ok = [w for w in wf if w["parses"]]
    summary = {
        "repositories_with_workflows": sum(bool(r["workflows"]) for r in rows.values()),
        "workflow_files": len(wf), "parse_failures": len(wf) - len(ok),
        "without_least_privilege": sum(not w["least_privilege"] for w in ok),
        "write_all": sum(w["write_all"] for w in ok),
        "files_with_unpinned_actions": sum(bool(w["unpinned_actions"]) for w in ok),
        "distinct_unpinned_actions": sorted({u for w in ok for u in w["unpinned_actions"]}),
        "pull_request_target": sum(w["pull_request_target"] for w in ok),
        "untrusted_in_run": sum(w["untrusted_in_run"] for w in ok),
        "runner_labels": sorted({x for w in ok for x in w["runners"]}),
        "secret_names": sorted({s for w in ok for s in w["secrets"]})}
    return json.dumps({"format": "outer-void-workflow-audit v1", "stage": "OV-48", "summary": summary,
                       "repositories": rows}, indent=1) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace", required=True, type=Path)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        old = json.loads(OUT.read_text())
        text = build(args.workspace, {r: v["sha"] for r, v in old["repositories"].items()})
        same = OUT.read_text() == text
        print("workflow audit:", "OK" if same else "DRIFT")
        return 0 if same else 1
    text = build(args.workspace, {})
    OUT.write_text(text)
    print(json.dumps(json.loads(text)["summary"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
