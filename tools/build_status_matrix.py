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
      "83ded6f", "Intelligence/runtime/integration platform: contracts, capability registry, Model API, routing, Hook System, direct `blux` CLI, training data pipeline, Gen 0 evaluation",
      "IMPLEMENTED", NA, "INTEGRATION_TESTED", "INTEGRATION_TESTED", "BLOCKED", "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No release tag or published package", "Termux APT on-device install not run (owner steps in packaging/termux/ACCEPTANCE.md)",
       "No real-provider Model API evidence (provider accounts without balance)", "Gen 0 model suites BLOCKED (F60); no native specialist integrated (F63)"],
      "make ci at ba160c3: 594 passed, 15 skipped; schema lock, ruff, strict mypy, wheel OK; Gen 0 baseline evals/reports/gen0 reproduces (--check) (Stages 34-36). Stage 43 at 83ded6f (agent receipts fix, F71): 597 passed, 15 skipped with the network disconnected; integration hard gates with every engine required 45 passed; from a clean clone without BLHermes 568 passed and the wheels build (ecosystem/release-candidate.md)",
      "2026-10-27"),
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
    c("BLUX App", "blux-app", "2.0.0", "6c8e8dd", "Local mission control over the real BLUX tools (read-only views; only read-only BLUX System checks as controls)",
      "IMPLEMENTED", "INTEGRATION_TESTED", NA, "INTEGRATION_TESTED", NA, "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["Not browser-tested (page script syntax-checked only)", "CI blocked org-wide (F49)", "VoidForge devices need the device app running"],
      "11 tests at 6c8e8dd incl. end-to-end: real blux run operations recorded in a real BLUX System store, inspected through the HTTP API; "
      "Host/token/origin/id-validation and secret-redaction tests (Stage 38)", "2026-10-27"),
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
       "No frontend tests or device testing (F37)", "Frontend dependency advisories need major upgrades; Python deps pip-audit clean (F36)", "boto3 probes instance metadata when R2 settings are empty outside production (F73)", "Public repository for proprietary SaaS source"],
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
    c("bluxai.app", "ov-webpages/bluxai.app", "0.1.0", "9fdb0a2", "Private BLUX workspace service over the BLUX executables (orgs, roles, runs/receipts, API tokens, audit, opt-in remote runs)",
      "IMPLEMENTED", "INTEGRATION_TESTED", NA, "INTEGRATION_TESTED", NA, "MOCK_TESTED", "IMPLEMENTED", "NOT_STARTED", "NOT_RELEASED",
      ["No web front end (F66)", "Not deployed; rate limits are per process (F66)", "CI blocked org-wide (F49)"],
      "12 tests at 9fdb0a2 incl. a real remote run into the organization's own BLUX System store, tenant isolation, roles, read-only API tokens; "
      "no BLUX runtime imports and local BLUX works without it (Stage 39)", "2026-10-27"),
    c("IVRP website", "ov-webpages/ivrp", None, "0e2b75e", "Reserved Inner Void Recovery Program website repository; README and LICENSE only",
      "NOT_STARTED", NA, NA, NA, NA, NA, NA, NA, NA, [], "File list inspected 2026-10-26"),
]


# Stage 44 (2026-10-27): final repository-by-repository Definition of Done pass. Each row is re-anchored to the commit
# that was verified, with the evidence of that run (ecosystem/definition-of-done.md). Statuses are not raised by it.
STAGE44 = {
    "blux": ("51134af", "unit+integration 597 passed (network off), hard gates 45 passed, ruff+mypy clean"),
    "blux-system": ("f0ba3a1", "74 passed (network off)"),
    "blux-gpt": ("4609cd9", "49 passed, 1 skipped (network off)"),
    "blux-coga": ("3dc86fa", "343 passed (network off)"),
    "blux-ca": ("7cb953a", "117 passed (network off)"),
    "dat": ("487e1d4", "88 passed (BLUX disabled)"),
    "lrc": ("443e532", "134 passed (network off), 133 with BLUX disabled"),
    "god": ("ad6f0c4", "94 passed (BLUX disabled and network off)"),
    "blux-app": ("0de2d9a", "11 passed; ruff fixed and now in CI"),
    "blux-ca-dataset": ("662ec33", "36 passed, 2 skipped"),
    "blux-coga-dataset": ("9331f73", "38 passed"),
    "axiom": ("2d3e4ef", "router tests 12 passed, shell suite and smoke passed"),
    "blux10k": ("80a7465", "10 passed"),
    "jadis.toolbox": ("253c386", "75 passed"),
    "voidforge": ("59b6d67", ":core 86 + :integration 9 passed (forced rerun)"),
    "void.os": ("24b07cd", "unit 78 passed, debug APK built (BLUX-free core)"),
    "void.sys": ("09cf56f", "debug APK built; no automated tests"),
    "void.game": ("b56c1ae", "core 21 passed, debug APK built"),
    "roughin": ("97921fc", "backend 91 passed (BLUX disabled, network off); frontend npm audit 5 advisories, not exploitable as used (F36 open)"),
    "vigyl": ("a0816a4", "backend 78 passed (BLUX disabled, network off)"),
    "resolver": ("bf7f26a", "173 unit tests passed"),
    "ov-webpages/theresolver": ("49dbeff", "lint, build and 9 tests passed; npm audit clean"),
    "termux-background": ("75cfb97", "unit 10+10 passed, CLI and package suites passed, shellcheck clean"),
    "ov-webpages/bluxai.app": ("9e5706a", "13 passed with BLUX, 10 + 3 skipped without; BLUX-absent 503 fix"),
    "ov-webpages/operationrestore": ("126453f", "DAT audit pass (static site)"),
    "ov-webpages/ivrp": ("68dbad7", "DAT audit pass (README only)"),
    "credits": ("8a0c52a", "validate, org-root check and 39 tests passed"),
    "docs": ("ef7d357", "13 tests, matrix, constitution and contract checks passed"),
    ".github": ("be5221d", "DAT audit pass; links checked"),
    ".github-private": ("5ea59da", "DAT audit pass"),
}
for _row in COMPONENTS:
    if _row["repo"] in STAGE44:
        _row["commit_sha"], _note = STAGE44[_row["repo"]]
        _row["evidence"] += f". Stage 44 DoD at {_row['commit_sha']} (2026-10-27): {_note}; DAT audit triaged"
        _row["last_verified"] = "2026-10-27"


# Forward execution is additive; Stage 44/45 evidence above stays historical.
_forward = ROOT / "OV-scaffold" / "component-updates.json"
if _forward.exists():
    _updates = json.loads(_forward.read_text())
    for _component in COMPONENTS:
        _component.update(_updates.get(_component["repo"], {}))
    if "secret-project/er" in _updates:
        COMPONENTS.append(c(
            "Eden Recovery", "secret-project/er", "Phase 0 draft", "4622037",
            "Institutional architecture, IVRP workups and Restore integration; no clinical authority",
            "IMPLEMENTED", "OPTIONAL", NA, "INTEGRATION_TESTED", NA, "UNVERIFIED",
            NA, "NOT_RELEASED", "NOT_RELEASED",
            ["Independent clinical/medical/legal/finance/lived-experience review pending",
             "Jurisdiction, market, workforce, payer and capital studies not commissioned",
             "Curriculum approval and institutional phase gates remain open"],
            "281 source references verified; three illustrative financial-model tests pass; no institutional approval",
            "2026-10-27"))
        COMPONENTS[-1].update(_updates["secret-project/er"])


# OV-48 (2026-11-04): suites affected by post-freeze commits re-run at the tested commit (ov-program/OV-48-report.md).
# Rows not listed keep their earlier evidence and date. Statuses are not raised by it.
OV48 = {
    "blux": ("8d989de", "training/dataset-program 3 passed; runtime unchanged since 51134af (Stage 44 evidence reused)"),
    "blux-system": ("77173f2", "74 passed against blux-sdk 0.2.0"),
    "axiom": ("ed079e8", "13 router tests passed; an executed `ax` routes through ax-route"),
    "blux10k": ("e2e9f58", "10 passed; `zsh -n` clean; `--version` 3.0.0"),
    "roughin": ("a4410a1", "backend 93 passed; frontend 4 passed and built; npm audit 6 build-time advisories (F78)"),
    "vigyl": ("f7ce8f3", "frontend 8 passed, built, npm audit clean; backend unchanged since a0816a4 (78 passed, 2026-10-27)"),
    "resolver": ("aae88c2", "173 passed"),
}
OV48_VERSION = {  # verified against the manifests in OV-47
    "resolver": "4.0.0 (app/__init__.py); git tag v4.0 (historical)",
    "vigyl": "API 0.2.0; frontend 0.1.0 (development preview)",
}
OV48_BLOCKERS = {
    "roughin": ["Build-time npm advisories through vite-plugin-pwa (F78)"],
    "termux-background": ["Four unsupported 2025 GitHub releases still offer APKs (F77, owner decision D-13)",
                          "Compromised release keystore and passwords remain in public git history; never sign with it (F81)",
                          "Four untriaged user issues report that the app closes or doesn't work (F79)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV48:
        _row["commit_sha"], _note = OV48[_row["repo"]]
        _row["evidence"] += f". OV-48 re-run at {_row['commit_sha']} (2026-11-04): {_note}"
        _row["last_verified"] = "2026-11-04"
    _row["known_blockers"] = _row["known_blockers"] + OV48_BLOCKERS.get(_row["repo"], [])
    _row["version"] = OV48_VERSION.get(_row["repo"], _row["version"])


# OV-55 / OV-56 (2026-11-05): auth hardening and UI flows, run at the commit shown (ov-program/OV-55-report.md,
# OV-56-report.md). SQLite-backed local runs only; PostgreSQL, Stripe, R2 and notification delivery stay blocked.
# Statuses are not raised by it.
OV55 = {
    "roughin": ("61c4b47", "OV-55: backend 100 passed at 0a794ac and auth suite 23 at 61c4b47 (SQLite); full backend 100 passed again at 61c4b47 in the deep audit (SQLite, 2026-11-06); frontend 10 passed and built; npm audit --omit=dev 0; DAT gate pass"),
    "vigyl": ("5637f3d", "OV-56: backend 108 passed at 875b006 (SQLite, 2026-11-06; backend unchanged since); frontend 40 passed and built; browser accessibility pass (headless Chromium, axe-core) 12 states 0 violations; npm audit 0; DAT gate pass"),
}
OV55_DATES = {"vigyl": "2026-11-06", "roughin": "2026-11-06"}  # the latest re-run per row
OV55_BLOCKERS = {
    "roughin": ["Password reset and email verification need an email provider (D-14)"],
    "vigyl": ["Password reset and email verification need an email provider (D-14)",
              "Alerts are in-app only; receipts show seen or not seen, never delivered elsewhere (F44, D-06)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV55:
        _row["commit_sha"], _note = OV55[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = OV55_DATES.get(_row["repo"], "2026-11-05")
    _row["known_blockers"] = _row["known_blockers"] + OV55_BLOCKERS.get(_row["repo"], [])

# OV-50 (2026-11-07): BLUX runtime and model routing (ov-program/OV-50-report.md). Deterministic and mock suites
# only; real providers stay BLOCKED until OV-64. Statuses are not raised by it.
OV50 = {
    "blux": ("4163637", "OV-50: tool-layer fixes F89-F93; full suite 604 passed, 15 skipped at 4163637 (2026-11-07), engines installed so the integration hard gates ran; ruff and mypy clean on changed code; DAT gate pass"),
}
OV50_BLOCKERS = {
    "blux": ["Receipts can be lost while BLUX System is down (F83-F85, OV-52)",
             "shell.exec is not an OS sandbox (F95, OV-62)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV50:
        _row["commit_sha"], _note = OV50[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-07"
    _row["known_blockers"] = _row["known_blockers"] + OV50_BLOCKERS.get(_row["repo"], [])

# OV-51 (2026-11-07): engine reliability (ov-program/OV-51-report.md): interrupted transactions, replay, malformed
# input. Engine suites and the BLUX hard gates (BLUX_REQUIRE_*=1) at the commits shown. Statuses are not raised by it.
OV51 = {
    "blux": ("9cd53ef", "OV-51: SDK .blux loader hardening F98-F99; full suite 611 passed, 15 skipped with every BLUX_REQUIRE_*=1 (2026-11-07); integration hard gates 45 passed, 2 skipped (real-provider) at the final engine commits; ruff and mypy clean; DAT gate pass"),
    "blux-coga": ("c94dc9c", "OV-51: replay of damaged artifacts F101; 347 passed; eval suite identical under PYTHONHASHSEED 0, 1 and 999; ruff and mypy clean; DAT gate pass"),
    "blux-ca": ("689ec70", "OV-51: interrupted-commit recovery F97; 119 passed; CogA -> cA -> DAT forced-rejection hard gate passed through BLUX; ruff and mypy clean; DAT gate pass"),
    "dat": ("57c8099", "OV-51: nested policy F102; 89 passed; FIFO, device and symlinked target policies ignored for the default; ruff and mypy clean; DAT gate pass"),
    "lrc": ("ea82afc", "OV-51: lrc recover, interruption guard and lock F96; 139 passed; ruff and mypy clean; DAT gate pass"),
    "god": ("613b800", "OV-51: malformed input and damaged cache F100; 102 passed; workspace check identical before and after; ruff and mypy clean; DAT gate pass"),
}
OV51_BLOCKERS = {
    "lrc": ["A killed create leaves a .lrc-stage-* directory beside the target (F103, OV-62)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV51:
        _row["commit_sha"], _note = OV51[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-07"
    _row["known_blockers"] = _row["known_blockers"] + OV51_BLOCKERS.get(_row["repo"], [])


# OV-52 (2026-11-07): BLUX System as the evidence authority (ov-program/OV-52-report.md): store crash repair,
# head anchor, payload and blob verification, retention, import; receipt durability F83-F85. Statuses unchanged.
OV52 = {
    "blux-system": ("26f2240", "OV-52: crash repair, head anchor, payload and blob verification, atomic retention, all-or-nothing import, lock wait F104-F110; 103 passed (also with the pinned SDK 0.2.0); ruff and mypy clean; DAT gate pass"),
    "blux": ("cfd7470", "OV-52: receipt durability F83-F85, refused receipts set aside F111, agent fails closed F112; full suite 620 passed, 15 skipped with every BLUX_REQUIRE_*=1 (2026-11-07); ruff and mypy clean; DAT gate pass"),
}
OV52_BLOCKERS = {
    "blux-system": ["Store heads are unsigned; a consistent rewrite needs an external head to detect (F113, OV-63)"],
    "blux": ["One-shot commands act before learning a receipt is refused (F114, OV-61)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV52:
        _row["commit_sha"], _note = OV52[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-07"
    _row["known_blockers"] = [b for b in _row["known_blockers"] if "F83-F85" not in b] + OV52_BLOCKERS.get(_row["repo"], [])

# OV-53 (2026-11-07): native BLUX research (ov-program/OV-53-report.md). PARTIAL: data controls hardened, Gen 0
# re-verified; no corpus (D-09), custodian or compute (D-15), so native models stay EXPERIMENTAL. Statuses unchanged.
OV53 = {
    "blux": ("60ddc76", "OV-53: training gates F115-F117, lint F94, router tests F119; full suite 648 passed, 15 skipped with every BLUX_REQUIRE_*=1 (2026-11-07); Gen 0 deterministic results match the Stage 35 baseline; ruff and mypy clean for the whole repository; DAT gate pass"),
}
OV53_BLOCKERS = {
    "blux": ["Native models EXPERIMENTAL: no eligible corpus (F63, D-09), no evaluation custodian or compute budget (F61, D-15)"],
    "blux-gpt": ["Inline <think> from OpenAI-compatible servers reaches answers and sessions (F118, OV-64)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV53:
        _row["commit_sha"], _note = OV53[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-07"
    _row["known_blockers"] = _row["known_blockers"] + OV53_BLOCKERS.get(_row["repo"], [])

# OV-54 (2026-11-08): ax, blux10k, JADIS Toolbox, BLUX App, bluxai.app (ov-program/OV-54-report.md). Clean installs,
# exit 69, tenant isolation and no second runtime verified; bluxai.app deployment stays D-08. Statuses unchanged.
OV54 = {
    "axiom": ("1272d75", "OV-54: ax-route committed (F120: it was never tracked, so `ax` failed on clean clones), broken overrides explained F121; router 14 passed here and 11 passed, 3 skipped from a fresh GitHub clone; run_tests.sh 14/14; smoke passed; every route exits 69 without its engine; DAT gate pass"),
    "blux10k": ("e2e9f58", "OV-54 re-run (2026-11-07): 10 passed; probes leave HOME untouched; bootstrap --apply into a scratch HOME links all dotfiles and backs up existing ones"),
    "jadis.toolbox": ("e3f25a5", "OV-54: master_log private and offline by default (F58), newproject proprietary by default (F59), node template fix F122; 79 passed; ruff, format and mypy clean; clean install into a fresh venv; DAT gate pass"),
    "blux-app": ("4bdb899", "OV-54: browser accessibility pass (F64) and fixes F123: 44 states, 0 axe violations, focus/reflow/target probes pass; 14 passed; clean install; DAT gate pass"),
    "ov-webpages/bluxai.app": ("32e988d", "OV-54: tenant-boundary test added (no defect found); 14 passed with BLUX, 10 passed and 4 skipped without (503); clean install of .[dev]; DAT gate pass"),
}
OV54_BLOCKERS = {
    "blux10k": ["`verify` exits 0 with every managed dotfile missing (F124)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV54:
        _row["commit_sha"], _note = OV54[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-08" if _row["repo"] != "blux10k" else "2026-11-07"
    _row["known_blockers"] = _row["known_blockers"] + OV54_BLOCKERS.get(_row["repo"], [])

# OV-57 (2026-11-08): Resolver and website (ov-program/OV-57-report.md). PARTIAL: payment and recovery fixes, root cause
# of 530/1033 found from outside; domain, tunnel, live bot and live recovery need the owner's access (D-07).
OV57 = {
    "resolver": ("63cce8b", "OV-57: charged Stars payments never dropped F125, database backup/restore and recovery runbook F126; 184 tests, smoke check, run_resolver.sh proof mode from a clean copy; DAT gate pass"),
    "ov-webpages/theresolver": ("49dbeff", "OV-57 re-run (2026-11-08): lint, build, 9 tests, pricing matches the bot (5 plans); theresolver.pages.dev serves this build; npm audit --omit=dev clean"),
}
OV57_BLOCKERS = {
    "resolver": ["Mini App hostnames admin./hq. have no DNS (F127, D-07)", "Bot not verified live against Telegram (F128, D-07)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV57:
        _row["commit_sha"], _note = OV57[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-08"
    _row["known_blockers"] = _row["known_blockers"] + OV57_BLOCKERS.get(_row["repo"], [])

# OV-58 (2026-11-08): Launcher family (ov-program/OV-58-report.md). PARTIAL: signature v1, crash-loop guard, layout-only
# backup and synthesized Shooter SFX; signing (D-04), devices (D-03) and Play licensing/Integrity (D-11) still block.
OV58 = {
    "void.os": ("d4c3dc9", "OV-58: product signature v1 F1 (partial: Play licensing/Integrity still TODO), crash-loop guard F19, layout-only backup F20, Shooter core re-vendored with SFX; 93 unit tests; assembleDebug and assembleRelease OK (unsigned); 16 KB native check; components check vs both upstreams OK; DAT gate pass"),
    "void.sys": ("af0050b", "OV-58: product signature v1 F17; 8 unit tests (first in this repository); assembleRelease OK (unsigned); DAT gate pass"),
    "void.game": ("0839bcd", "OV-58: product signature v1 F2, synthesized SFX with a SOUND setting F29; core 24 tests, android 8; assembleRelease OK (unsigned); 16 KB native check; DAT gate pass"),
}
OV58_BLOCKERS = {
    "void.os": ["No device run of safe mode, backup/restore or sound (D-03)"],
    "void.game": ["Sound not heard on a device (D-03)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV58:
        _row["commit_sha"], _note = OV58[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-08"
    _row["known_blockers"] = _row["known_blockers"] + OV58_BLOCKERS.get(_row["repo"], [])

# OV-59 (2026-11-08): VoidForge and Termux Background (ov-program/OV-59-report.md). PARTIAL: confirmation screen,
# graduated write classes (all locked), Termux signer pinning, set rollback; device evidence per class needs D-03.
OV59 = {
    "voidforge": ("671349e", "OV-59: local confirmation screen F5 (partial), graduated write classes (none qualified, all locked), Termux signer pinning F87, private-state docs F86; core 96 and integration 13 tests; assembleDebug/Release, lintDebug, detekt, spotless, source policy, tools tests OK; DAT gate pass"),
    "termux-background": ("49164f6", "OV-59: set rolls back the image on a failed properties write F57; cli and package tests pass (rebuilt .deb); issue triage F79; DAT gate pass"),
}
OV59_BLOCKERS = {
    "voidforge": ["Every write class locked until per-class device evidence (F5, D-03)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV59:
        _row["commit_sha"], _note = OV59[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-08"
    _row["known_blockers"] = _row["known_blockers"] + OV59_BLOCKERS.get(_row["repo"], [])

# OV-60 (2026-11-08): institutional and support repositories (ov-program/OV-60-report.md). PASSED: explicit state
# and safe next action for each; ER by GitHub metadata only.
OV60 = {
    "void.game": ("c5ce555", "OV-60: lsans-15 font notice (OFL-1.1, F32), notices at libGDX 1.14.2 (F129), tools/check_notices.py in CI (fails on the old notices); release APK rebuilt; DAT gate pass"),
    "void.os": ("d009469", "OV-60: lsans-15 font notice (OFL-1.1, F32), tools/check_notices.py in CI; release APK rebuilt; components check OK; DAT gate pass"),
    ".github": ("6e8083f", "OV-60: banner names the OV-46-70 program (owner decision, F50); VoidForge, Vigyl and private-product facts corrected (F132); DAT gate pass"),
    ".github-private": ("dbe0b6f", "OV-60: private repository list matches the GitHub API; per-class VoidForge write locks (F132); DAT gate pass"),
    "credits": ("c0d4565", "OV-60: UNR-020 resolved (lsans-15 is OFL-1.1 Liberation Sans), UNR-014 narrowed to six public repositories, libGDX 1.14.2 natives; validate, acknowledgments and unresolved checks, pytest 39 pass"),
    "ov-webpages/operationrestore": ("126453f", "OV-60: live operationrestore.net matches 126453f file for file; security headers present; README.md and .gitignore are served publicly (F130); impact text and privacy notice need the owner (F131, D-10); no change (owner decision)"),
    "ov-webpages/ivrp": ("68dbad7", "OV-60: reserved repository (README and licence only); policies in docs/legal/ivrp are drafts, not legal advice; next action waits for the owner (D-10)"),
    "secret-project/er": ("ac4b89a", "OV-60: GitHub metadata only (private, main ac4b89a, last push 2026-10-27, no releases or tags); content EXCLUDED_BY_OWNER_POLICY; independent review is D-10"),
}
OV60_BLOCKERS = {
    "ov-webpages/operationrestore": ["The site serves README.md and .gitignore (F130, owner)", "Impact text and privacy notice need owner review (F131, D-10)"],
}
for _row in COMPONENTS:
    if _row["repo"] in OV60:
        _row["commit_sha"], _note = OV60[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-08"
    _row["known_blockers"] = _row["known_blockers"] + OV60_BLOCKERS.get(_row["repo"], [])

# OV-61 (2026-11-09): versioned cross-repository integration (ov-program/OV-61-report.md, ecosystem/integration-matrix.md).
# PASSED: every BLUX boundary from fresh clones at one pin set; every engine and ax without the BLUX runtime.
OV61 = {
    "blux": ("5995419", "OV-61: receipt-store preflight for external/destructive capabilities (F114, owner decision), single integration pin set integrations/targets.lock.json used by CI (F133); integration matrix from fresh clones with every BLUX_REQUIRE_* set; DAT gate pass"),
}
OV61_OFF = {
    "blux-coga": "OV-61: own suite passes without the BLUX runtime (fresh clone at c94dc9c)",
    "blux-ca": "OV-61: own suite passes without the BLUX runtime (fresh clone at 689ec70)",
    "dat": "OV-61: own suite passes without the BLUX runtime (fresh clone at 57c8099)",
    "lrc": "OV-61: own suite passes without the BLUX runtime (fresh clone at ea82afc)",
    "god": "OV-61: own suite passes with blux-sdk only, no BLUX runtime (fresh clone at 613b800)",
    "blux-system": "OV-61: own suite passes without the BLUX runtime (fresh clone at 26f2240)",
    "blux-gpt": "OV-61: own suite passes without the BLUX runtime (fresh clone at 0175196)",
    "jadis.toolbox": "OV-61: own suite passes without the BLUX runtime (fresh clone at e3f25a5)",
    "axiom": "OV-61: ax routes work with BLUX absent (ask/agent exit 69 naming BLUX); run_tests.sh 14 and test_ax_router 14 pass, VoidForge client tests included",
}
for _row in COMPONENTS:
    if _row["repo"] in OV61:
        _row["commit_sha"], _note = OV61[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-09"
    if _row["repo"] in OV61_OFF:
        _row["evidence"] += f". {OV61_OFF[_row['repo']]}"
        _row["last_verified"] = "2026-11-09"
    if _row["repo"] == "blux-gpt":
        _row["commit_sha"] = "0175196"

# OV-62 (2026-11-09): adversarial and fault-injection drills (ov-program/OV-62-report.md). PASSED.
OV62 = {
    "blux": ("b56d06c", "OV-62: every shell.exec command needs approval (F95, owner decision); file tools never follow a symlink swapped in after the check (F136); STORE_IO_ERROR retryable and torn tail tolerated by the preflight (F138); integration pins bumped; drills and fresh-clone matrix pass"),
    "dat": ("24a7290", "OV-62: an unreadable file makes the audit incomplete (exit 3) instead of passing the gate (F134); suite 91 passed; BLUX off passes; DAT gate pass"),
    "lrc": ("3765215", "OV-62: stale staging directories reported (F103, owner decision); a full disk is an IO_ERROR document (F137); suite 140 passed; BLUX off passes"),
    "blux-system": ("9392449", "OV-62: an I/O failure is a STORE_IO_ERROR document, SIGXFSZ ignored (F135); suite 104 passed; BLUX off passes"),
}
for _row in COMPONENTS:
    if _row["repo"] in OV62:
        _row["commit_sha"], _note = OV62[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-09"

# OV-63 (2026-11-09): DAT pilot and shared release machinery (ov-program/OV-63-report.md, releases/). PARTIAL:
# a signed, reproducible, independently checked and installable DAT build exists; no release while CI cannot run.
OV63 = {
    "dat": ("eff11ee", "OV-63: pilot 4.0.0-pilot.1 built from two fresh clones byte-identically, tests 98, lint, wheel and sdist installed into empty environments with smoke checks, bandit/detect-secrets/pip-audit pass, signed with the release key (releases/dat/4.0.0-pilot.1); unparsed Android manifests block the security gate (F139); the tag workflow only verifies (F140)"),
}
OV63_STATUS = {"dat": {"package_status": "INTEGRATION_TESTED", "distribution_status": "BLOCKED"}}
OV63_BLOCKERS = {"dat": ["D-01: CI cannot run, and the release policy needs green CI on the release commit; the pilot stays local (owner decision 2026-11-09)"]}
for _row in COMPONENTS:
    if _row["repo"] in OV63:
        _row["commit_sha"], _note = OV63[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-09"
        _row.update(OV63_STATUS.get(_row["repo"], {}))
        _row["known_blockers"] = _row["known_blockers"] + OV63_BLOCKERS.get(_row["repo"], [])

# OV-64 (2026-11-09): real services and providers (ov-program/OV-64-report.md). BLOCKED: every provider account is
# unfunded (D-02); D-05, D-06 and D-07 kept blocked by the owner. Local fixes only.
OV64 = {
    "blux-gpt": ("11b83a4", "OV-64: inline <think> reasoning dropped from OpenAI-compatible answers and streams (F118); API-key config created 0600 (F141); suite 62 passed; metered real run: keys valid, every account PROVIDER_QUOTA_EXCEEDED, spend US$0"),
}
OV64_BLOCKERS = {"blux-gpt": ["D-02: OpenAI, Anthropic and DeepSeek accounts have no balance (2026-11-09); the authorized US$1 real run repeats once one is funded"]}
for _row in COMPONENTS:
    if _row["repo"] in OV64:
        _row["commit_sha"], _note = OV64[_row["repo"]]
        _row["evidence"] += f". {_note}"
        _row["last_verified"] = "2026-11-09"
        _row["known_blockers"] = _row["known_blockers"] + OV64_BLOCKERS.get(_row["repo"], [])

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
