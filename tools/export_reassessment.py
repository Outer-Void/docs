"""Stage 45 freeze exports: reassessment/*.json, rebuilt from the frozen commits.

Recovered from the Stage 45 session (it originally read working trees on 2026-10-27). Every input is now read
with `git show <frozen sha>:<path>`, so the exports can be reproduced at any later time:

    python3 tools/export_reassessment.py --workspace ~/ov --check   # rebuild and compare, write nothing
    python3 tools/export_reassessment.py --workspace ~/ov           # rewrite reassessment/ (historical: avoid)

The frozen SHAs come from reassessment/inventory.json itself. Files that live in this docs repository are read at
DOCS_FREEZE, the commit that added the exports. The capability registry is rebuilt by running GOD over
`git archive` copies of the seven repositories at their frozen SHAs (`--god` names the executable).
"""

import argparse
import collections
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]
OUT = DOCS / "reassessment"
DOCS_FREEZE = "43d9a6c"  # docs commit "Stage 45: freeze for reassessment"
CAPABILITY_REPOS = ("blux", "blux-coga", "blux-ca", "dat", "lrc", "god", "jadis.toolbox")


class Frozen:
    def __init__(self, workspace):
        self.ws = Path(workspace)
        inv = json.loads(self.show("docs", DOCS_FREEZE, "reassessment/inventory.json"))
        self.date = inv["frozen_at"]
        self.sha = {r["repo"]: r["sha"] for r in inv["repositories"] if r.get("sha")}

    def path(self, repo):
        return DOCS if repo == "docs" else self.ws / repo

    def show(self, repo, sha, path):
        return subprocess.run(["git", "-C", str(self.path(repo)), "show", f"{sha}:{path}"],
                              capture_output=True, check=True).stdout

    def read(self, repo, path):
        return self.show(repo, DOCS_FREEZE if repo == "docs" else self.sha[repo], path)

    def json(self, repo, path):
        return json.loads(self.read(repo, path))

    def archive(self, repo, dest):
        data = subprocess.run(["git", "-C", str(self.path(repo)), "archive", self.sha[repo]],
                              capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(dest, filter="data")


def build(fz, god):
    docs = {}
    # The frozen SHAs are the anchor: the inventory's SHA fields are carried over, everything else is rebuilt.
    shas = {r["repo"]: {k: r[k] for k in ("branch", "sha", "level_with_origin", "clean", "fetched")}
            for r in fz.json("docs", "reassessment/inventory.json")["repositories"] if r.get("sha")}

    # 1-4: inventory
    constitution = fz.json("docs", "constitution/repositories.json")
    repos = constitution["repositories"] if isinstance(constitution, dict) else constitution
    matrix = {r["repo"]: r for r in fz.json("docs", "ecosystem/status-matrix.json")["components"]}
    inventory = []
    for r in repos:
        m = matrix.get(r["repo"], {})
        inventory.append({"repo": r["repo"], "component": m.get("component"), "kind": r["kind"], "blux": r["blux"],
                          "visibility": r.get("visibility"), "version": m.get("version"), **shas.get(r["repo"], {}),
                          "owns": r.get("owns"), "never_owns": r.get("never_owns")})
    inventory.append({"repo": "blhermes-agent", "component": "BLHermes (archived fork)", "kind": "archived",
                      "blux": "none", **shas.get("blhermes-agent", {})})
    docs["inventory.json"] = {"format": "outer-void-freeze-inventory v1", "frozen_at": fz.date,
                              "repositories": inventory}

    # 5: dependency graph (declared in the constitution)
    edges = [{"from": r["repo"], "to": d} for r in repos for d in (r.get("depends_on") or [])]
    docs["dependency-graph.json"] = {"format": "outer-void-freeze-dependency-graph v1", "frozen_at": fz.date,
                                     "source": "docs/constitution/repositories.json (depends_on)",
                                     "nodes": [r["repo"] for r in repos], "edges": edges}

    # 6: capability registry, discovered by GOD from the repositories' .blux/ declarations
    with tempfile.TemporaryDirectory() as tmp:
        roots = []
        for repo in CAPABILITY_REPOS:
            dest = Path(tmp) / repo
            fz.archive(repo, dest)
            roots += ["-r", str(dest)]
        proc = subprocess.run([god, "capabilities", *roots, "--no-cache", "--json"],
                              capture_output=True, text=True, check=True)
    caps = json.loads(proc.stdout)["capabilities"]
    docs["capability-registry.json"] = {
        "format": "outer-void-freeze-capabilities v1", "frozen_at": fz.date,
        "discovered_by": "god capabilities over the seven repositories with .blux/", "count": len(caps),
        "capabilities": [{k: c.get(k) for k in ("capability_id", "project_id", "contract_versions", "labels", "provider")}
                         for c in caps]}

    # 7-8: compatibility lock and release ledger (snapshots with their source hashes)
    for name, src in (("compatibility.json", "ecosystem/compatibility.json"),
                      ("release-ledger.json", "ecosystem/release-ledger.json")):
        raw = fz.read("docs", src)
        docs[name] = {"frozen_at": fz.date, "source": "docs/" + src, "source_sha256": hashlib.sha256(raw).hexdigest(),
                      "content": json.loads(raw)}

    # 9: BLUX runtime migration / parity status (BLHermes -> BLUX)
    pm = fz.json("blux", "migration/blhermes/parity-matrix.json")
    docs["blux-migration-parity.json"] = {
        "frozen_at": fz.date, "source": "blux/migration/blhermes/parity-matrix.json", "states_defined": pm["states"],
        "by_state": dict(collections.Counter(f["migration_state"] for f in pm["features"])), "total": len(pm["features"]),
        "features": [{k: f.get(k) for k in ("id", "feature", "classification", "target", "migration_state", "blocker")}
                     for f in pm["features"]],
        "decoupling_evidence": fz.json("blux", "migration/blhermes/decoupling-evidence.json")}

    # 10: models, datasets, evaluations
    routes = fz.json("blux", "runtime/blux_runtime/models/default_routes.json")
    gen0 = fz.json("blux", "evals/reports/gen0/report.json")
    spec = fz.json("blux", "training/specialists.json")
    datasets = {}
    for d in ("blux-ca-dataset", "blux-coga-dataset"):
        cfg = fz.json(d, "dataset.json")
        raw = fz.read(d, "splits.lock.json")
        lock = json.loads(raw)
        datasets[d] = {"version": cfg.get("version"), "release_date": cfg.get("release_date"),
                       "splits_lock_sha256": hashlib.sha256(raw).hexdigest(), "records": len(lock["records"]),
                       "by_split": dict(collections.Counter(r["split"] for r in lock["records"].values()
                                                            if r.get("status") == "active"))}
    docs["models-datasets-evals.json"] = {
        "frozen_at": fz.date,
        "model_api": {"version": routes["model_api_version"], "routes_id": routes["routes_id"],
                      "logical_models": {m: [{"route_id": r["route_id"], "provider": r["provider"], "tier": r["tier"]}
                                             for r in v["routes"]] for m, v in routes["models"].items()}},
        "native_models_integrated": [],
        "specialists": {"as_of": spec.get("as_of"), "items": spec["items"], "candidates": spec["candidates"]},
        "datasets": datasets,
        "evaluation_gen0": {"source": "blux/evals/reports/gen0/report.json", "summary": gen0["summary"],
                            "models": gen0["models"], "suites": gen0["suites"]}}

    # 11: product release states (the final matrix)
    keys = ("component", "repo", "version", "commit_sha", "standalone_status", "blux_status", "ax_status",
            "test_status", "hardware_status", "security_status", "package_status", "distribution_status",
            "release_status", "known_blockers", "last_verified")
    docs["release-states.json"] = {"frozen_at": fz.date, "source": "docs/ecosystem/status-matrix.json",
                                   "components": [{k: r[k] for k in keys} for r in matrix.values()]}

    # 12: open findings (blockers and deferred items); fixed or resolved rows are left out
    rows, seen = [], set()
    for line in fz.read("docs", "ecosystem/findings.md").decode().splitlines():
        if not re.match(r"^\| (F\d+) \| (.*)$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] in seen:
            continue
        seen.add(cells[0])
        text = " | ".join(cells)
        if re.search(r"\b(Fixed|Resolved|RESOLVED|FIXED)\b", text) and not re.search(r"\bOpen\b", text):
            continue
        rows.append({"id": cells[0], "repo": cells[1], "issue": cells[2], "severity": cells[3] if len(cells) > 3 else None,
                     "class": cells[5] if len(cells) > 5 else None, "blocking": cells[6] if len(cells) > 6 else None})
    docs["open-findings.json"] = {"frozen_at": fz.date, "source": "docs/ecosystem/findings.md",
                                  "note": "rows whose class or text says Fixed/Resolved are excluded",
                                  "count": len(rows), "findings": rows}
    return {name: json.dumps(doc, indent=1, sort_keys=False) + "\n" for name, doc in docs.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workspace", required=True, help="directory holding the repository checkouts")
    ap.add_argument("--god", default="god", help="GOD executable")
    ap.add_argument("--check", action="store_true", help="compare with reassessment/ and write nothing")
    args = ap.parse_args()
    out = build(Frozen(args.workspace), args.god)
    if args.check:
        bad = [n for n, text in out.items() if not (OUT / n).exists() or (OUT / n).read_text() != text]
        for n in bad:
            print(f"DRIFT {n}")
        print(f"reassessment exports: {len(out) - len(bad)}/{len(out)} reproduced byte for byte")
        return 1 if bad else 0
    for n, text in out.items():
        (OUT / n).write_text(text)
    print(f"wrote {len(out)} exports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
