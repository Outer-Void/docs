"""Current findings projection (OV-47): ecosystem/findings-current.json.

It joins two inputs:
- the frozen open findings (reassessment/open-findings.json, never edited);
- the hand-authored current dispositions and new findings (ecosystem/findings-dispositions.json).

    python3 tools/build_findings_current.py           # write ecosystem/findings-current.json
    python3 tools/build_findings_current.py --check   # validate and compare; write nothing

Validation rules:
- every frozen finding has exactly one disposition, and no unknown ids;
- statuses and priorities come from the vocabulary;
- RESOLVED_VERIFIED and PARTIAL need dated evidence;
- new findings use fresh ids above the frozen range.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]
FROZEN = DOCS / "reassessment/open-findings.json"
SOURCE = DOCS / "ecosystem/findings-dispositions.json"
OUT = DOCS / "ecosystem/findings-current.json"
STATUSES = ("OPEN", "RESOLVED_VERIFIED", "PARTIAL", "EXTERNAL_BLOCKED", "BLOCKED_LOCAL_ENVIRONMENT", "SUPERSEDED",
            "DEFERRED", "UNKNOWN")
PRIORITIES = ("P0", "P1", "P2")
CURRENT = ("status", "owner", "priority", "stage", "decision", "evidence", "next_action")
DATED = re.compile(r"\b20\d\d-\d\d-\d\d\b")


def build():
    frozen = json.loads(FROZEN.read_text())
    src = json.loads(SOURCE.read_text())
    disp, problems = src["dispositions"], []
    ids = [f["id"] for f in frozen["findings"]]
    problems += [f"{i}: no disposition" for i in ids if i not in disp]
    problems += [f"{i}: not a frozen open finding" for i in disp if i not in ids]
    top = max(int(i[1:]) for i in ids)
    rows = []
    for f in frozen["findings"]:
        d = disp.get(f["id"], {})
        rows.append({"id": f["id"], "origin": "frozen", "frozen": f, **{k: d.get(k) for k in CURRENT}})
    for n in src["new_findings"]:
        if int(n["id"][1:]) <= top or n["id"] in ids:
            problems.append(f"{n['id']}: new finding id must be above F{top}")
        rows.append({"id": n["id"], "origin": "new", "frozen": None,
                     "found": n["found"], "repo": n["repo"], "severity": n["severity"], "source": n["source"],
                     "issue": n["issue"], **{k: n.get(k) for k in CURRENT}})
    for r in rows:
        if r["status"] not in STATUSES:
            problems.append(f"{r['id']}: status {r['status']!r}")
        if r["priority"] not in PRIORITIES:
            problems.append(f"{r['id']}: priority {r['priority']!r}")
        if not r["evidence"] or not r["next_action"] or not r["owner"]:
            problems.append(f"{r['id']}: evidence, owner and next_action are required")
        elif r["status"] in ("RESOLVED_VERIFIED", "PARTIAL") and not any(DATED.search(e) for e in r["evidence"]):
            problems.append(f"{r['id']}: {r['status']} needs dated evidence")
    sev = lambda r: (r["frozen"]["severity"] if r["frozen"] else r["severity"] or "").split()[0]
    still = [r for r in rows if r["status"] not in ("RESOLVED_VERIFIED", "SUPERSEDED")]
    doc = {"format": "outer-void-findings-current v1", "as_of": src["as_of"],
           "sources": {"frozen": "reassessment/open-findings.json (2026-10-27, unchanged)",
                       "dispositions": "ecosystem/findings-dispositions.json"},
           "counts": {"frozen_open": len(ids), "new": len(src["new_findings"]),
                      "by_status": dict(collections.Counter(r["status"] for r in rows)),
                      "unresolved_by_severity": dict(collections.Counter(sev(r) for r in still))},
           "findings": rows}
    return json.dumps(doc, indent=1) + "\n", problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text, problems = build()
    if args.check and (not OUT.exists() or OUT.read_text() != text):
        problems.append("ecosystem/findings-current.json differs from a rebuild")
    for p in problems:
        print("FAIL", p)
    if problems:
        return 1
    if not args.check:
        OUT.write_text(text)
    print("findings-current:", json.loads(text)["counts"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
