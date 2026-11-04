"""Current repository inventory (OV-46): inventory/*.json, kept apart from the Stage 45 freeze in reassessment/.

    python3 tools/build_inventory.py --workspace ~/ov --refresh   # record today's SHAs and GitHub metadata, rebuild
    python3 tools/build_inventory.py --workspace ~/ov             # rebuild inventory-current.json from the record
    python3 tools/build_inventory.py --workspace ~/ov --check     # rebuild and compare; verify the record

`--refresh` is the only mode that touches the network. It writes:
- baseline-commits.json, with each checkout's HEAD, remote main, and whether they are level and clean;
- visibility-attestation.json, from the authenticated GitHub API through `gh`.

Everything else in inventory-current.json is computed from each repository's tree at its recorded commit
(`git ls-tree` / `git show`), so the file can be reproduced later even after the repositories have moved on.

Repositories under secret-project/ are inventoried from GitHub metadata only. Their checkout is never opened;
content inspection is EXCLUDED_BY_OWNER_POLICY.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]
OUT = DOCS / "inventory"
ORG = "Outer-Void"
EXCLUDED_PREFIX = "secret-project/"
ARCHIVED_EXTRA = [{"repo": "blhermes-agent", "kind": "archived", "blux": "none", "visibility": "public",
                   "owns": "Historical BLHermes fork (read-only)", "never_owns": "Any runtime role"}]

MANIFESTS = ("pyproject.toml", "setup.py", "setup.cfg", "package.json", "build.gradle.kts", "build.gradle",
             "settings.gradle.kts", "VERSION", "Cargo.toml", "go.mod", "Makefile")
LOCKS = ("package-lock.json", "poetry.lock", "uv.lock", "Pipfile.lock", "gradle/libs.versions.toml",
         "gradle.lockfile", "yarn.lock", "pnpm-lock.yaml")
SKIP_DIRS = ("node_modules/", "vendor/", "third_party/", "dist/", "build/")


def run(*args, cwd=None, check=True):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=check).stdout.strip()


def gh_api(path):
    return json.loads(run("gh", "api", path))


def load(name):
    return json.loads((OUT / name).read_text())


def dump(name, doc):
    return json.dumps(doc, indent=1) + "\n"


def repositories():
    """Constitution repositories plus the archived fork, each with its GitHub name."""
    c = json.loads((DOCS / "constitution/repositories.json").read_text())
    repos = (c["repositories"] if isinstance(c, dict) else c) + ARCHIVED_EXTRA
    return [dict(r, github=r["repo"].split("/")[-1]) for r in repos]


def excluded(repo):
    return repo["repo"].startswith(EXCLUDED_PREFIX)


def refresh(ws):
    today = datetime.date.today().isoformat()
    attest, base = {}, {}
    for r in repositories():
        meta = gh_api(f"repos/{ORG}/{r['github']}")
        branch = meta["default_branch"]
        attest[r["github"]] = {
            "visibility": meta["visibility"], "archived": meta["archived"], "default_branch": branch,
            "pushed_at": meta["pushed_at"], "open_issues": meta["open_issues_count"],
            "releases": len(gh_api(f"repos/{ORG}/{r['github']}/releases?per_page=100"))}
        remote = gh_api(f"repos/{ORG}/{r['github']}/commits/{branch}")["sha"]
        if excluded(r):
            base[r["repo"]] = {"branch": branch, "remote_sha": remote, "local": "EXCLUDED_BY_OWNER_POLICY"}
            continue
        path = ws / r["repo"]
        if not (path / ".git").exists():
            base[r["repo"]] = {"branch": branch, "remote_sha": remote, "local": "NO_CHECKOUT"}
            continue
        run("git", "fetch", "-q", "origin", cwd=path)
        head = run("git", "rev-parse", "HEAD", cwd=path)
        base[r["repo"]] = {"branch": run("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=path), "head": head,
                           "remote_sha": remote, "level_with_origin": head == remote,
                           "clean": run("git", "status", "--porcelain", cwd=path) == "", "local": "CHECKOUT"}
    (OUT / "baseline-commits.json").write_text(dump("", {
        "format": "outer-void-baseline-commits v1", "recorded_at": today, "stage": "OV-46",
        "note": "docs is recorded at its HEAD before the OV-46 commit", "repositories": base}))
    (OUT / "visibility-attestation.json").write_text(dump("", {
        "format": "outer-void-visibility-attestation v1", "recorded_at": today,
        "source": f"authenticated GitHub REST API (gh api repos/{ORG}/<name>)", "repositories": attest}))


def tree_facts(path, sha):
    files = [f for f in run("git", "ls-tree", "-r", "--name-only", sha, cwd=path).splitlines()
             if not any(f.startswith(d) or f"/{d}" in f for d in SKIP_DIRS)]

    def show(f):
        return run("git", "show", f"{sha}:{f}", cwd=path, check=False)

    manifests = {}
    for f in files:
        name = f.rsplit("/", 1)[-1]
        if name not in MANIFESTS or f.count("/") > 2:
            continue
        text, version = show(f), None
        if name == "package.json":
            try:
                version = json.loads(text).get("version")
            except ValueError:
                version = "UNPARSABLE"
        elif name == "VERSION":
            version = text.splitlines()[0].strip() if text else None
        else:
            m = re.search(r'^\s*(?:version|versionName)\s*=\s*"([^"]+)"', text, re.M)
            version = m.group(1) if m else None
        manifests[f] = version
    tags = run("git", "tag", "--merged", sha, "--sort=-creatordate", cwd=path).splitlines()
    licence = show("LICENSE").splitlines()[:1] if "LICENSE" in files else []
    locks = sorted(f for f in files if f.endswith(LOCKS) or re.search(r"(^|/)requirements[^/]*\.txt$", f))
    toolchains = sorted({t for f in manifests for t, keys in (
        ("python", ("pyproject.toml", "setup.py", "setup.cfg")), ("node", ("package.json",)),
        ("gradle", ("build.gradle.kts", "build.gradle", "settings.gradle.kts"))) if f.rsplit("/", 1)[-1] in keys}
                        | ({"python"} if any("requirements" in f for f in locks) else set()))
    return {"tracked_files": len(files), "manifests": manifests, "lock_files": locks,
            "workflows": sorted(f for f in files if f.startswith(".github/workflows/") and f.endswith((".yml", ".yaml"))),
            "toolchains": toolchains, "tags": {"count": len(tags), "latest": tags[:3]},
            "licence_first_line": licence[0][:100] if licence else None}


def build(ws):
    base, attest = load("baseline-commits.json"), load("visibility-attestation.json")
    matrix = {r["repo"]: r for r in json.loads((DOCS / "ecosystem/status-matrix.json").read_text())["components"]}
    frozen = {r["repo"]: r.get("sha") for r in json.loads((DOCS / "reassessment/inventory.json").read_text())["repositories"]}
    rows = []
    for r in repositories():
        b, a, m = base["repositories"][r["repo"]], attest["repositories"][r["github"]], matrix.get(r["repo"], {})
        row = {"repo": r["repo"], "github": f"{ORG}/{r['github']}", "component": m.get("component"), "kind": r["kind"],
               "blux": r["blux"], "declared_visibility": r.get("visibility"), "github_visibility": a["visibility"],
               "visibility_matches": (r.get("visibility") or "").lower() == a["visibility"].lower(),
               "archived": a["archived"], "default_branch": a["default_branch"], "remote_sha": b["remote_sha"],
               "matrix_version": m.get("version"), "owns": r.get("owns"), "never_owns": r.get("never_owns"),
               "depends_on": r.get("depends_on") or []}
        if b["local"] != "CHECKOUT":
            row.update(content_inspection=b["local"])
        else:
            path = ws / r["repo"]
            fsha = frozen.get(r["repo"])
            row.update(content_inspection="INSPECTED", head=b["head"], level_with_origin=b["level_with_origin"],
                       clean=b["clean"], frozen_sha=fsha,
                       commits_since_freeze=int(run("git", "rev-list", "--count", f"{fsha}..{b['head']}", cwd=path))
                       if fsha else None,
                       **tree_facts(path, b["head"]))
        rows.append(row)
    edges = {(r["repo"], d) for r in repositories() for d in (r.get("depends_on") or [])}
    fedges = {(e["from"], e["to"]) for e in json.loads((DOCS / "reassessment/dependency-graph.json").read_text())["edges"]}
    return dump("", {
        "format": "outer-void-inventory-current v1", "recorded_at": base["recorded_at"], "stage": "OV-46",
        "counts": {"repositories": len(rows), "github": len(attest["repositories"]),
                   "archived": sum(r["archived"] for r in rows),
                   "excluded_by_owner_policy": sum(r["content_inspection"] == "EXCLUDED_BY_OWNER_POLICY" for r in rows),
                   "inspected": sum(r["content_inspection"] == "INSPECTED" for r in rows)},
        "dependency_graph": {"source": "constitution/repositories.json (depends_on)",
                             "frozen": "reassessment/dependency-graph.json",
                             "unchanged_since_freeze": edges == fedges,
                             "added": sorted(map(list, edges - fedges)), "removed": sorted(map(list, fedges - edges))},
        "repositories": rows})


def check(ws, text):
    problems = []
    base, attest = load("baseline-commits.json"), load("visibility-attestation.json")
    names = [r["github"] for r in repositories()]
    if sorted(names) != sorted(attest["repositories"]) or len(set(names)) != len(names):
        problems.append(f"repository sets differ: constitution+archived {sorted(set(names) ^ set(attest['repositories']))}")
    for r in repositories():
        b = base["repositories"].get(r["repo"])
        if b is None:
            problems.append(f"{r['repo']}: no baseline")
        elif b["local"] == "CHECKOUT" and subprocess.run(
                ["git", "merge-base", "--is-ancestor", b["head"], "HEAD"], cwd=ws / r["repo"]).returncode:
            problems.append(f"{r['repo']}: recorded head {b['head'][:7]} is not an ancestor of the checkout's HEAD")
    if (OUT / "inventory-current.json").read_text() != text:
        problems.append("inventory-current.json differs from a rebuild")
    for p in problems:
        print("FAIL", p)
    print(f"inventory: {'OK' if not problems else f'{len(problems)} problem(s)'}")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace", required=True, type=Path)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="record SHAs and GitHub metadata (network)")
    mode.add_argument("--check", action="store_true", help="rebuild and compare; write nothing")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.refresh:
        refresh(args.workspace)
    text = build(args.workspace)
    if args.check:
        return check(args.workspace, text)
    (OUT / "inventory-current.json").write_text(text)
    print("wrote inventory/inventory-current.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
