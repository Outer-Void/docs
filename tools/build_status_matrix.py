#!/usr/bin/env python3
"""Source of the Outer Void component status matrix (docs/ecosystem/status-matrix.json + .md).

Edit COMPONENTS below, then run `python3 tools/build_status_matrix.py` (writes both files) or
`--check` (fails if the committed files differ from this source, or if a status is outside the vocabulary).
Commit SHAs are what each repository's main was at `last_verified`; they are evidence anchors, not live state.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUSES = {
    "NOT_STARTED", "PLANNED", "IMPLEMENTED", "MOCK_TESTED", "INTEGRATION_TESTED", "HARDWARE_PENDING", "BLOCKED",
    "RELEASE_CANDIDATE", "RELEASED", "ARCHIVED",
    # Additions, defined in ecosystem/README.md:
    "NOT_APPLICABLE", "NOT_RELEASED", "UNVERIFIED", "OPTIONAL", "EXCLUDED", "REQUIRED",
}
STATUS_FIELDS = ("standalone_status", "blux_status", "ax_status", "test_status", "hardware_status", "security_status",
                 "package_status", "distribution_status", "release_status")
DATE = "2026-10-26"


def c(component, repo, version, sha, role, standalone, blux, ax, test, hardware, security, package, distribution, release,
      blockers, evidence, verified=DATE):
    return {"component": component, "repo": repo, "version": version, "commit_sha": sha, "role": role,
            "standalone_status": standalone, "blux_status": blux, "ax_status": ax, "test_status": test,
            "hardware_status": hardware, "security_status": security, "package_status": package,
            "distribution_status": distribution, "release_status": release, "known_blockers": blockers,
            "evidence": evidence, "last_verified": verified}


NA = "NOT_APPLICABLE"
COMPONENTS = [
    c("BLUX (runtime, SDK, contracts, `blux` CLI)", "blux", "outervoid-blux 0.4.0; blux-sdk 0.2.0; Contract v1 / Model API v1 / Hook System v1 = 1.0",
      "f491524", "Intelligence/runtime/integration platform: contracts, capability registry, Model API, routing, Hook System, direct `blux` CLI",
      "IMPLEMENTED", NA, "INTEGRATION_TESTED", "INTEGRATION_TESTED", "BLOCKED", "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag or published package", "Termux APT on-device install not run (owner steps in packaging/termux/ACCEPTANCE.md)",
       "No real-provider Model API evidence (provider accounts without balance)"],
      "make ci at f491524: 563 passed, 15 skipped; schema lock, ruff, mypy, wheel OK (Stage 22)"),
    c("AXIOM control plane (`ax`)", "axiom", "2.0.0", "a276744", "Developer control plane; routes to authoritative engines, reimplements none",
      "IMPLEMENTED", "OPTIONAL", NA, "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["Engines must be installed separately; missing engines exit 69 by design"],
      "tests/test_ax_router.py 12 passed and tests/run_tests.sh 14/14 at a276744 (Stage 22); `ax devices` chain also exercised from VoidForge's integration test"),
    c("blux10k", "blux10k", "3.0.0", "fcb127d", "Environment and toolchain authority (`ax env`) plus dotfiles",
      "IMPLEMENTED", "EXCLUDED", "INTEGRATION_TESTED", "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED", [],
      "pytest: 10 passed at fcb127d (re-run 2026-10-26)"),
    c("CogA", "blux-coga", "2.0.0", "3dc86fa", "Deterministic structured reasoning; no model, no hidden chain-of-thought",
      "IMPLEMENTED", "INTEGRATION_TESTED", "IMPLEMENTED", "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag for 2.0.0"], "pytest: 343 passed at 3dc86fa (re-run 2026-10-26)"),
    c("cA", "blux-ca", "2.0.1", "7cb953a", "Construction/modification/repair; never certifies its own work (DAT validates)",
      "IMPLEMENTED", "INTEGRATION_TESTED", "IMPLEMENTED", "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag for 2.0.1"], "pytest: 117 passed at 7cb953a (re-run 2026-10-26; needs the declared `hypothesis` dev dependency)"),
    c("DAT", "dat", "4.0.0", "76d0a01", "Independent audit/security/quality/release authority; may reject any component's work",
      "IMPLEMENTED", "INTEGRATION_TESTED", "IMPLEMENTED", "INTEGRATION_TESTED", NA, "IMPLEMENTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["README previously pinned a v4.0.0 tag that does not exist (tags: v1.0.0, v2.0.0-alpha.1, v2.0.0-Stable)"],
      "pytest: 88 passed at 76d0a01 (re-run 2026-10-26)"),
    c("LRC", "lrc", "2.0.0", "34b6a04", "Deterministic repository creation/scaffolding/migration; does not certify itself",
      "IMPLEMENTED", "INTEGRATION_TESTED", "IMPLEMENTED", "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag for 2.0.0"], "pytest: 133 passed, 1 skipped at 34b6a04 (re-run 2026-10-26)"),
    c("GOD", "god", "2.0.0", "a329d89", "Capability/project/command discovery; never execution authority",
      "IMPLEMENTED", "INTEGRATION_TESTED", "IMPLEMENTED", "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag for 2.0.0"], "pytest: 94 passed at a329d89 (re-run 2026-10-26)"),
    c("BLUX System", "blux-system", "2.0.0", "f0ba3a1", "Intelligence-free execution truth: receipts, operation graph, provenance, replay metadata",
      "IMPLEMENTED", "INTEGRATION_TESTED", "IMPLEMENTED", "INTEGRATION_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag for 2.0.0"], "pytest: 74 passed at f0ba3a1 (re-run 2026-10-26)"),
    c("BluxGPT", "blux-gpt", "2.0.0", "4609cd9", "Provider/model gateway behind Model API v1; no agent loop, no tool execution, no authority",
      "IMPLEMENTED", "INTEGRATION_TESTED", NA, "MOCK_TESTED", NA, NA, "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["Real-provider runs not recorded; hard-coded provider model IDs not verified against current catalogs"],
      "pytest: 49 passed, 1 skipped at 4609cd9 (re-run 2026-10-26), deterministic mock and fake transports"),
    c("BLUX App", "blux-app", None, "386e81f", "Read-only observability viewer of artifacts and receipts",
      "IMPLEMENTED", "OPTIONAL", NA, "UNVERIFIED", NA, NA, "NOT_STARTED", "NOT_STARTED", "NOT_RELEASED", ["Phase 1 CLI viewer only"],
      "Not re-run in the 2026-10-26 documentation pass"),
    c("cA dataset", "blux-ca-dataset", "dynamic (pyproject)", "662ec33", "Deterministic cA evaluation/training dataset (Hugging Face card layout)",
      "IMPLEMENTED", "OPTIONAL", NA, "INTEGRATION_TESTED", NA, NA, NA, "NOT_STARTED", "NOT_RELEASED", [],
      "pytest: 36 passed, 2 skipped at 662ec33 (re-run 2026-10-26)"),
    c("CogA dataset", "blux-coga-dataset", "dynamic (pyproject)", "9331f73", "Deterministic CogA evaluation/training dataset",
      "IMPLEMENTED", "OPTIONAL", NA, "INTEGRATION_TESTED", NA, NA, NA, "NOT_STARTED", "NOT_RELEASED", [],
      "pytest: 38 passed at 9331f73 (re-run 2026-10-26)"),
    c("VoidForge", "voidforge", "0.1.0-dev", "463b921", "Standalone Android-to-Android device-engineering workstation (members-only, free for now)",
      "IMPLEMENTED", "OPTIONAL", "INTEGRATION_TESTED", "MOCK_TESTED", "BLOCKED", "MOCK_TESTED", "IMPLEMENTED", "BLOCKED", "NOT_RELEASED",
      ["Production write barrier locked; no local confirmation UI", "No real-device acceptance (2026-10-26 probe BLOCKED)",
       "Repository is public, conflicting with members-only policy (owner action in docs/DISTRIBUTION.md)",
       "No production release key or keystore configured"],
      "Stage 22/23: :core 86, :integration 9, tools 24 tests passed; app assembleDebug OK; all mock/synthetic"),
    c("AXIOM Launcher", "void.os", "2.0.0-dev", "24b07cd", "Paid Android launcher product (bundles VOID.SYS and hidden AXIOM Shooter)",
      "IMPLEMENTED", "EXCLUDED", NA, "MOCK_TESTED", "HARDWARE_PENDING", "BLOCKED", "IMPLEMENTED", "BLOCKED", "NOT_RELEASED",
      ["Stage 24 hard gate NOT passed (docs/release/release-matrix.md)",
       "Entitlement, Play Integrity and product-signature verification are TODO stubs (release paths fail closed)",
       "No device matrix run", "No release keystore / protected signing job (env-only signing exists)",
       "No crash-loop guard", "Public repository for a paid product", "Legal/asset notice review"],
      "testDebugUnitTest 78 passed, assembleDebug OK, tool tests OK, components check with both upstreams OK, 16 KB native QA OK at 24b07cd (Stage 26)"),
    c("VOID.SYS", "void.sys", "2.1.0-dev", "09cf56f", "Icon system: one lineage for the standalone icon pack and the versioned bundle consumed by AXIOM Launcher",
      "IMPLEMENTED", "EXCLUDED", NA, "MOCK_TESTED", "HARDWARE_PENDING", "BLOCKED", "IMPLEMENTED", "BLOCKED", "NOT_RELEASED",
      ["Standalone signature verification is a TODO stub (fails closed)", "2,903 asset variants pending individual visual review",
       "No device test of the standalone pack in third-party launchers", "Public repository for a paid product"],
      "tools tests 8 passed, verify_drawables OK, assembleDebug + assembleRelease OK, release APK keeps all 587 drawable names (Stage 25); AXIOM vendors release/manifest.json bundle byte-for-byte"),
    c("AXIOM Shooter", "void.game", "2.1.0-dev", "b56c1ae",
      "Standalone game product; core/ is the authoritative gameplay source bundled in AXIOM Launcher as a hidden Easter egg",
      "IMPLEMENTED", "EXCLUDED", NA, "MOCK_TESTED", "HARDWARE_PENDING", "BLOCKED", "IMPLEMENTED", "BLOCKED", "NOT_RELEASED",
      ["Purchase/signature verification is TODO (release fails closed)", "No audio", "Interrupted runs are not resumed",
       "No device playthroughs, GL context-loss, frame-time or battery evidence", "Default font licence unresolved (credits UNR-020)",
       "Public repository for a paid product"],
      "core:test 21 passed; android assembleDebug + assembleRelease OK; tools/check_apk_natives.py passes both APKs (libGDX 1.14.2, 16 KB); aapt2: launchable 'AXIOM Shooter' (Stage 26)"),
    c("Resolver (Telegram runtime)", "resolver", "1.0.0 (app/__init__.py); git tag v4.0", "bf7f26a", "Telegram moderation bot runtime with a paid intelligence layer",
      "IMPLEMENTED", "UNVERIFIED", NA, "MOCK_TESTED", NA, "UNVERIFIED", NA, "IMPLEMENTED", "UNVERIFIED",
      ["Version mismatch: tag v4.0 (73abe3e) vs __version__ 1.0.0 (F48)", "Release gate steps install_resolver.sh / run_resolver.sh need live secrets: not run",
       "CI blocked org-wide by the GitHub billing lock (F49)"],
      "Release gate offline steps at bf7f26a: compileall OK, unittest 173 OK, scripts/smoke_check.py OK (2026-10-27 reconciliation)", "2026-10-27"),
    c("Resolver website", "ov-webpages/theresolver", "0.2.0", "49dbeff", "Marketing/acquisition site for the Resolver bot (separate from the runtime)",
      "IMPLEMENTED", "EXCLUDED", NA, "INTEGRATION_TESTED", NA, "IMPLEMENTED", NA, "IMPLEMENTED", "NOT_RELEASED",
      ["Custom domain theresolverbot.net (and www) returns Cloudflare error 1033 (tunnel), not the Pages site (F54)",
       "GitHub Actions blocked org-wide by the billing lock (F49)"],
      "npm run check at 49dbeff: lint, build, 9 node:test checks over the export incl. HTTP smoke; npm audit 0; two builds byte-identical; "
      "deployed theresolver.pages.dev serves this build (pages 200, deep links, CSP/HSTS headers) (Stage 31)", "2026-10-27"),
    c("Roughin", "roughin", "1.1.0 (API); frontend 1.0.0", "f3599d3", "Standalone contractor SaaS (FastAPI + React PWA)",
      "IMPLEMENTED", "PLANNED", NA, "MOCK_TESTED", NA, "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["PostgreSQL migration + backup/restore CI BLOCKED: GitHub account billing lock, jobs never started (F34)", "No deployment, Stripe test-mode or real R2 run (F35)",
       "No frontend tests or device testing (F37)", "Frontend dependency advisories need major upgrades; Python deps pip-audit clean (F36)", "Public repository for proprietary SaaS source"],
      "pytest: 91 passed at f3599d3 (SQLite; Stripe/R2 faked at the edge, real webhook signature verification); ruff clean; vite build OK (Stage 28)",
      "2026-10-27"),
    c("Vigyl", "vigyl", "API 0.2.0", "a0816a4", "Standalone caregiving/accountability product; backend API only (no UI yet)",
      "IMPLEMENTED", "PLANNED", NA, "MOCK_TESTED", NA, "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No app UI (F43)", "Notifications are in-app only: no push/email delivery (F44)", "PostgreSQL migration + backup CI BLOCKED: GitHub billing lock (F45)",
       "No recurring tasks, password reset or legal review (F46)", "Public repository for privacy-sensitive product source"],
      "pytest: 78 passed at a0816a4 (SQLite; role, access, privacy, task-history and failure-path suites); ruff clean; pip-audit clean (Stage 29)",
      "2026-10-27"),
    c("Termux Background", "termux-background", "1.1.0", "75cfb97", "Standalone Android companion + Termux CLI for Termux Monet wallpapers",
      "IMPLEMENTED", "EXCLUDED", NA, "MOCK_TESTED", "HARDWARE_PENDING", NA, "IMPLEMENTED", "BLOCKED", "NOT_RELEASED",
      ["No device has passed docs/DEVICE_RC_CHECKLIST.md", "No signing key in CI; CI blocked org-wide (F49)", "Targets SDK 35; 36 available (F56)"],
      "docs/RELEASE_CHECKS.md at 75cfb97: shellcheck, cli_test.sh, build-deb + package_test, gradle test (10 per variant), lint 0 errors, debug+release APKs (Stage 32)",
      "2026-10-27"),
    c("JADIS Toolbox (`jadis`)", "jadis.toolbox", "0.1.0", "253c386",
      "Portable workstation tool: environment classification, doctor, safe journaled repair, bootstrap, snapshots (Termux, PRoot Debian, Debian)",
      "IMPLEMENTED", "OPTIONAL", NA, "INTEGRATION_TESTED", "HARDWARE_PENDING", "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["Not run in native Termux (fixture-tested only)", "Native Debian 13 evidence pending the CI container job's first run",
       "No published package (install from source)", "Small repair catalogue (4 repairs)", "CI blocked org-wide (F49)"],
      "75 tests at 253c386 (CLI suite plus 8 for the standalone scripts, incl. a mutation-checked git-crypt plaintext guard), ruff/mypy clean; "
      "earlier: real PRoot Debian 13 run, real BLUX subprocess call; GOD discovers its 4 read-only capabilities (Stage 33)", "2026-10-27"),
    c("Credits ledger", "credits", None, "18240ba", "Canonical attribution, licensing and provenance ledger",
      "IMPLEMENTED", NA, NA, "INTEGRATION_TESTED", NA, NA, NA, NA, NA, [], "validate.py --org-root and 39 tests OK at 18240ba (Stage 29 sync)",
      "2026-10-27"),
    c("Central docs", "docs", None, "6cfbd70", "Legal/policy baselines and ecosystem governance documentation (this repository)",
      "IMPLEMENTED", NA, NA, "IMPLEMENTED", NA, NA, NA, NA, NA, [], "tools/build_status_matrix.py --check OK; full reconciliation 2026-10-27", "2026-10-27"),
    c("Organization profile", ".github", None, "7c9ad5a", "Public organization profile and doctrine", "IMPLEMENTED", NA, NA, NA, NA, NA, NA, NA, NA,
      ["Owner banner says 'Stage 21 - 30 of 44'; the queued plan ends at Stage 45 (F50, owner decision)"], "Contents reconciled 2026-10-27", "2026-10-27"),
    c("Private organization profile", ".github-private", None, "bc32b7a", "Members-only organization profile", "IMPLEMENTED", NA, NA, NA, NA, NA, NA, NA, NA, [],
      "Contents inspected 2026-10-27 (logo and doctrine line only)", "2026-10-27"),
    c("BLHermes (archived fork)", "blhermes-agent", "upstream metadata only", "dc8abc1db0",
      "Historical/reference fork of Nous Research hermes-agent (MIT); replaced by BLUX",
      "ARCHIVED", "ARCHIVED", NA, "ARCHIVED", NA, NA, NA, "ARCHIVED", "ARCHIVED", [],
      "GitHub API archived=true; credits LIN-001 archival facts"),
    c("Operation: Restore website", "ov-webpages/operationrestore", None, "126453f", "Static site for operationrestore.net",
      "IMPLEMENTED", "EXCLUDED", NA, NA, NA, NA, NA, "UNVERIFIED", "UNVERIFIED", [], "README inspected 2026-10-26"),
    c("bluxai.app", "ov-webpages/bluxai.app", None, "a8d127a", "Reserved BLUX website repository; contains only README and LICENSE",
      "NOT_STARTED", NA, NA, NA, NA, NA, NA, NA, NA, [], "File list inspected 2026-10-26"),
    c("IVRP website", "ov-webpages/ivrp", None, "0e2b75e", "Reserved Inner Void Recovery Program website repository; README and LICENSE only",
      "NOT_STARTED", NA, NA, NA, NA, NA, NA, NA, NA, [], "File list inspected 2026-10-26"),
]


def render_md(rows):
    lines = ["# Component status matrix", "",
             "Generated from `tools/build_status_matrix.py`; do not edit by hand. Statuses are defined in",
             "[README.md](README.md#status-vocabulary). `commit_sha` is the evidence anchor at `last_verified`.", "",
             "| Component | Repo | Version | Commit | Standalone | BLUX | ax | Tests | Hardware | Security | Package | Distribution | Release | Last verified |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| " + " | ".join([r["component"], f"`{r['repo']}`", r["version"] or "-", f"`{r['commit_sha']}`",
                                          *[r[f] for f in STATUS_FIELDS], r["last_verified"]]) + " |")
    lines += ["", "## Evidence and blockers", ""]
    for r in rows:
        lines.append(f"- **{r['component']}** (`{r['repo']}`): {r['role']}. Evidence: {r['evidence']}.")
        for b in r["known_blockers"]:
            lines.append(f"  - Blocker: {b}")
    return "\n".join(lines) + "\n"


def main(argv):
    for r in COMPONENTS:
        bad = [f for f in STATUS_FIELDS if r[f] not in STATUSES]
        if bad:
            print(f"{r['repo']}: unknown status in {bad}", file=sys.stderr)
            return 1
    data = json.dumps({"format": "outer-void-status-matrix v1", "generated_from": "tools/build_status_matrix.py",
                       "statuses": sorted(STATUSES), "components": COMPONENTS}, indent=1) + "\n"
    md = render_md(COMPONENTS)
    targets = {ROOT / "ecosystem" / "status-matrix.json": data, ROOT / "ecosystem" / "status-matrix.md": md}
    if "--check" in argv:
        stale = [str(p.relative_to(ROOT)) for p, text in targets.items() if not p.exists() or p.read_text() != text]
        if stale:
            print("stale: " + ", ".join(stale) + " (run tools/build_status_matrix.py)", file=sys.stderr)
            return 1
        print("status matrix OK")
        return 0
    for p, text in targets.items():
        p.write_text(text)
    print("wrote ecosystem/status-matrix.json and ecosystem/status-matrix.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
