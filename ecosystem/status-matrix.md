# Component status matrix

Generated from `tools/build_status_matrix.py`; do not edit by hand. Statuses are defined in
[README.md](README.md#status-vocabulary). `commit_sha` is the evidence anchor at `last_verified`.

| Component | Repo | Version | Commit | Standalone | BLUX | ax | Tests | Hardware | Security | Package | Distribution | Release | Last verified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BLUX (runtime, SDK, contracts, `blux` CLI) | `blux` | outervoid-blux 0.4.0; blux-sdk 0.2.0; Contract v1 / Model API v1 / Hook System v1 = 1.0 | `51134af` | IMPLEMENTED | NOT_APPLICABLE | INTEGRATION_TESTED | INTEGRATION_TESTED | BLOCKED | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| AXIOM control plane (`ax`) | `axiom` | 2.0.0 | `2d3e4ef` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| blux10k | `blux10k` | 3.0.0 | `80a7465` | IMPLEMENTED | EXCLUDED | INTEGRATION_TESTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| CogA | `blux-coga` | 2.0.0 | `3dc86fa` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| cA | `blux-ca` | 2.0.1 | `7cb953a` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| DAT | `dat` | 4.0.0 | `487e1d4` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | IMPLEMENTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| LRC | `lrc` | 2.0.0 | `443e532` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| GOD | `god` | 2.0.0 | `ad6f0c4` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| BLUX System | `blux-system` | 2.0.0 | `f0ba3a1` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| BluxGPT | `blux-gpt` | 2.0.0 | `4609cd9` | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| BLUX App | `blux-app` | 2.0.0 | `0de2d9a` | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| cA dataset | `blux-ca-dataset` | dynamic (pyproject) | `662ec33` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| CogA dataset | `blux-coga-dataset` | dynamic (pyproject) | `9331f73` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| VoidForge | `voidforge` | 0.1.0-dev | `59b6d67` | IMPLEMENTED | OPTIONAL | INTEGRATION_TESTED | MOCK_TESTED | BLOCKED | MOCK_TESTED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-27 |
| AXIOM Launcher | `void.os` | 2.0.0-dev | `24b07cd` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-27 |
| VOID.SYS | `void.sys` | 2.1.0-dev | `09cf56f` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-27 |
| AXIOM Shooter | `void.game` | 2.1.0-dev | `b56c1ae` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-27 |
| Resolver (Telegram runtime) | `resolver` | 1.0.0 (app/__init__.py); git tag v4.0 | `bf7f26a` | IMPLEMENTED | UNVERIFIED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | IMPLEMENTED | UNVERIFIED | 2026-10-27 |
| Resolver website | `ov-webpages/theresolver` | 0.2.0 | `49dbeff` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | IMPLEMENTED | NOT_APPLICABLE | IMPLEMENTED | NOT_RELEASED | 2026-10-27 |
| Roughin | `roughin` | 1.1.0 (API); frontend 1.0.0 | `97921fc` | IMPLEMENTED | PLANNED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| Vigyl | `vigyl` | API 0.2.0 | `a0816a4` | IMPLEMENTED | PLANNED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| Termux Background | `termux-background` | 1.1.0 | `75cfb97` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | NOT_APPLICABLE | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-27 |
| JADIS Toolbox (`jadis`) | `jadis.toolbox` | 0.1.0 | `253c386` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | HARDWARE_PENDING | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| Credits ledger | `credits` | - | `8a0c52a` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| Central docs | `docs` | - | `ef7d357` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| Organization profile | `.github` | - | `be5221d` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| Private organization profile | `.github-private` | - | `5ea59da` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| BLHermes (archived fork) | `blhermes-agent` | upstream metadata only | `dc8abc1db0` | ARCHIVED | ARCHIVED | NOT_APPLICABLE | ARCHIVED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | ARCHIVED | ARCHIVED | 2026-10-26 |
| Operation: Restore website | `ov-webpages/operationrestore` | - | `126453f` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | UNVERIFIED | UNVERIFIED | 2026-10-27 |
| bluxai.app | `ov-webpages/bluxai.app` | 0.1.0 | `9e5706a` | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| IVRP website | `ov-webpages/ivrp` | - | `68dbad7` | NOT_STARTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |

## Evidence and blockers

- **BLUX (runtime, SDK, contracts, `blux` CLI)** (`blux`): Intelligence/runtime/integration platform: contracts, capability registry, Model API, routing, Hook System, direct `blux` CLI, training data pipeline, Gen 0 evaluation. Evidence: make ci at ba160c3: 594 passed, 15 skipped; schema lock, ruff, strict mypy, wheel OK; Gen 0 baseline evals/reports/gen0 reproduces (--check) (Stages 34-36). Stage 43 at 83ded6f (agent receipts fix, F71): 597 passed, 15 skipped with the network disconnected; integration hard gates with every engine required 45 passed; from a clean clone without BLHermes 568 passed and the wheels build (ecosystem/release-candidate.md). Stage 44 DoD at 51134af (2026-10-27): unit+integration 597 passed (network off), hard gates 45 passed, ruff+mypy clean; DAT audit triaged.
  - Blocker: No release tag or published package
  - Blocker: Termux APT on-device install not run (owner steps in packaging/termux/ACCEPTANCE.md)
  - Blocker: No real-provider Model API evidence (provider accounts without balance)
  - Blocker: Gen 0 model suites BLOCKED (F60); no native specialist integrated (F63)
- **AXIOM control plane (`ax`)** (`axiom`): Developer control plane; routes to authoritative engines, reimplements none. Evidence: tests/test_ax_router.py 12 passed and tests/run_tests.sh 14/14 at a276744 (Stage 22); `ax devices` chain also exercised from VoidForge's integration test. Stage 44 DoD at 2d3e4ef (2026-10-27): router tests 12 passed, shell suite and smoke passed; DAT audit triaged.
  - Blocker: Engines must be installed separately; missing engines exit 69 by design
- **blux10k** (`blux10k`): Environment and toolchain authority (`ax env`) plus dotfiles. Evidence: pytest: 10 passed at fcb127d (re-run 2026-10-26). Stage 44 DoD at 80a7465 (2026-10-27): 10 passed; DAT audit triaged.
- **CogA** (`blux-coga`): Deterministic structured reasoning; no model, no hidden chain-of-thought. Evidence: pytest: 343 passed at 3dc86fa (re-run 2026-10-26). Stage 44 DoD at 3dc86fa (2026-10-27): 343 passed (network off); DAT audit triaged.
  - Blocker: No release tag for 2.0.0
- **cA** (`blux-ca`): Construction/modification/repair; never certifies its own work (DAT validates). Evidence: pytest: 117 passed at 7cb953a (re-run 2026-10-26; needs the declared `hypothesis` dev dependency). Stage 44 DoD at 7cb953a (2026-10-27): 117 passed (network off); DAT audit triaged.
  - Blocker: No release tag for 2.0.1
- **DAT** (`dat`): Independent audit/security/quality/release authority; may reject any component's work. Evidence: pytest: 88 passed at 76d0a01 (re-run 2026-10-26). Stage 44 DoD at 487e1d4 (2026-10-27): 88 passed (BLUX disabled); DAT audit triaged.
  - Blocker: README previously pinned a v4.0.0 tag that does not exist (tags: v1.0.0, v2.0.0-alpha.1, v2.0.0-Stable)
- **LRC** (`lrc`): Deterministic repository creation/scaffolding/migration; does not certify itself. Evidence: pytest: 133 passed, 1 skipped at 34b6a04 (re-run 2026-10-26). Stage 44 DoD at 443e532 (2026-10-27): 134 passed (network off), 133 with BLUX disabled; DAT audit triaged.
  - Blocker: No release tag for 2.0.0
- **GOD** (`god`): Capability/project/command discovery; never execution authority. Evidence: pytest: 94 passed at a329d89 (re-run 2026-10-26). Stage 44 DoD at ad6f0c4 (2026-10-27): 94 passed (BLUX disabled and network off); DAT audit triaged.
  - Blocker: No release tag for 2.0.0
- **BLUX System** (`blux-system`): Intelligence-free execution truth: receipts, operation graph, provenance, replay metadata. Evidence: pytest: 74 passed at f0ba3a1 (re-run 2026-10-26). Stage 44 DoD at f0ba3a1 (2026-10-27): 74 passed (network off); DAT audit triaged.
  - Blocker: No release tag for 2.0.0
- **BluxGPT** (`blux-gpt`): Provider/model gateway behind Model API v1; no agent loop, no tool execution, no authority. Evidence: pytest: 49 passed, 1 skipped at 4609cd9 (re-run 2026-10-26), deterministic mock and fake transports. Stage 44 DoD at 4609cd9 (2026-10-27): 49 passed, 1 skipped (network off); DAT audit triaged.
  - Blocker: Real-provider runs not recorded; hard-coded provider model IDs not verified against current catalogs
- **BLUX App** (`blux-app`): Local mission control over the real BLUX tools (read-only views; only read-only BLUX System checks as controls). Evidence: 11 tests at 6c8e8dd incl. end-to-end: real blux run operations recorded in a real BLUX System store, inspected through the HTTP API; Host/token/origin/id-validation and secret-redaction tests (Stage 38). Stage 44 DoD at 0de2d9a (2026-10-27): 11 passed; ruff fixed and now in CI; DAT audit triaged.
  - Blocker: Not browser-tested (page script syntax-checked only)
  - Blocker: CI blocked org-wide (F49)
  - Blocker: VoidForge devices need the device app running
- **cA dataset** (`blux-ca-dataset`): Deterministic cA evaluation/training dataset (Hugging Face card layout). Evidence: pytest: 36 passed, 2 skipped at 662ec33 (re-run 2026-10-26). Stage 44 DoD at 662ec33 (2026-10-27): 36 passed, 2 skipped; DAT audit triaged.
- **CogA dataset** (`blux-coga-dataset`): Deterministic CogA evaluation/training dataset. Evidence: pytest: 38 passed at 9331f73 (re-run 2026-10-26). Stage 44 DoD at 9331f73 (2026-10-27): 38 passed; DAT audit triaged.
- **VoidForge** (`voidforge`): Standalone Android-to-Android device-engineering workstation (members-only, free for now). Evidence: Stage 22/23: :core 86, :integration 9, tools 24 tests passed; app assembleDebug OK; all mock/synthetic. Stage 44 DoD at 59b6d67 (2026-10-27): :core 86 + :integration 9 passed (forced rerun); DAT audit triaged.
  - Blocker: Production write barrier locked; no local confirmation UI
  - Blocker: No real-device acceptance (2026-10-26 probe BLOCKED)
  - Blocker: Repository is public, conflicting with members-only policy (owner action in docs/DISTRIBUTION.md)
  - Blocker: No production release key or keystore configured
- **AXIOM Launcher** (`void.os`): Paid Android launcher product (bundles VOID.SYS and hidden AXIOM Shooter). Evidence: testDebugUnitTest 78 passed, assembleDebug OK, tool tests OK, components check with both upstreams OK, 16 KB native QA OK at 24b07cd (Stage 26). Stage 44 DoD at 24b07cd (2026-10-27): unit 78 passed, debug APK built (BLUX-free core); DAT audit triaged.
  - Blocker: Stage 24 hard gate NOT passed (docs/release/release-matrix.md)
  - Blocker: Entitlement, Play Integrity and product-signature verification are TODO stubs (release paths fail closed)
  - Blocker: No device matrix run
  - Blocker: No release keystore / protected signing job (env-only signing exists)
  - Blocker: No crash-loop guard
  - Blocker: Public repository for a paid product
  - Blocker: Legal/asset notice review
- **VOID.SYS** (`void.sys`): Icon system: one lineage for the standalone icon pack and the versioned bundle consumed by AXIOM Launcher. Evidence: tools tests 8 passed, verify_drawables OK, assembleDebug + assembleRelease OK, release APK keeps all 587 drawable names (Stage 25); AXIOM vendors release/manifest.json bundle byte-for-byte. Stage 44 DoD at 09cf56f (2026-10-27): debug APK built; no automated tests; DAT audit triaged.
  - Blocker: Standalone signature verification is a TODO stub (fails closed)
  - Blocker: 2,903 asset variants pending individual visual review
  - Blocker: No device test of the standalone pack in third-party launchers
  - Blocker: Public repository for a paid product
- **AXIOM Shooter** (`void.game`): Standalone game product; core/ is the authoritative gameplay source bundled in AXIOM Launcher as a hidden Easter egg. Evidence: core:test 21 passed; android assembleDebug + assembleRelease OK; tools/check_apk_natives.py passes both APKs (libGDX 1.14.2, 16 KB); aapt2: launchable 'AXIOM Shooter' (Stage 26). Stage 44 DoD at b56c1ae (2026-10-27): core 21 passed, debug APK built; DAT audit triaged.
  - Blocker: Purchase/signature verification is TODO (release fails closed)
  - Blocker: No audio
  - Blocker: Interrupted runs are not resumed
  - Blocker: No device playthroughs, GL context-loss, frame-time or battery evidence
  - Blocker: Default font licence unresolved (credits UNR-020)
  - Blocker: Public repository for a paid product
- **Resolver (Telegram runtime)** (`resolver`): Telegram moderation bot runtime with a paid intelligence layer. Evidence: Release gate offline steps at bf7f26a: compileall OK, unittest 173 OK, scripts/smoke_check.py OK (2026-10-27 reconciliation). Stage 44 DoD at bf7f26a (2026-10-27): 173 unit tests passed; DAT audit triaged.
  - Blocker: Version mismatch: tag v4.0 (73abe3e) vs __version__ 1.0.0 (F48)
  - Blocker: Release gate steps install_resolver.sh / run_resolver.sh need live secrets: not run
  - Blocker: CI blocked org-wide by the GitHub billing lock (F49)
- **Resolver website** (`ov-webpages/theresolver`): Marketing/acquisition site for the Resolver bot (separate from the runtime). Evidence: npm run check at 49dbeff: lint, build, 9 node:test checks over the export incl. HTTP smoke; npm audit 0; two builds byte-identical; deployed theresolver.pages.dev serves this build (pages 200, deep links, CSP/HSTS headers) (Stage 31). Stage 44 DoD at 49dbeff (2026-10-27): lint, build and 9 tests passed; npm audit clean; DAT audit triaged.
  - Blocker: Custom domain theresolverbot.net (and www) returns Cloudflare error 1033 (tunnel), not the Pages site (F54)
  - Blocker: GitHub Actions blocked org-wide by the billing lock (F49)
- **Roughin** (`roughin`): Standalone contractor SaaS (FastAPI + React PWA). Evidence: pytest: 91 passed at f3599d3 (SQLite; Stripe/R2 faked at the edge, real webhook signature verification); ruff clean; vite build OK (Stage 28). Stage 44 DoD at 97921fc (2026-10-27): backend 91 passed (BLUX disabled, network off); frontend npm audit 5 advisories, not exploitable as used (F36 open); DAT audit triaged.
  - Blocker: PostgreSQL migration + backup/restore CI BLOCKED: GitHub account billing lock, jobs never started (F34)
  - Blocker: No deployment, Stripe test-mode or real R2 run (F35)
  - Blocker: No frontend tests or device testing (F37)
  - Blocker: Frontend dependency advisories need major upgrades; Python deps pip-audit clean (F36)
  - Blocker: boto3 probes instance metadata when R2 settings are empty outside production (F73)
  - Blocker: Public repository for proprietary SaaS source
- **Vigyl** (`vigyl`): Standalone caregiving/accountability product; backend API only (no UI yet). Evidence: pytest: 78 passed at a0816a4 (SQLite; role, access, privacy, task-history and failure-path suites); ruff clean; pip-audit clean (Stage 29). Stage 44 DoD at a0816a4 (2026-10-27): backend 78 passed (BLUX disabled, network off); DAT audit triaged.
  - Blocker: No app UI (F43)
  - Blocker: Notifications are in-app only: no push/email delivery (F44)
  - Blocker: PostgreSQL migration + backup CI BLOCKED: GitHub billing lock (F45)
  - Blocker: No recurring tasks, password reset or legal review (F46)
  - Blocker: Public repository for privacy-sensitive product source
- **Termux Background** (`termux-background`): Standalone Android companion + Termux CLI for Termux Monet wallpapers. Evidence: docs/RELEASE_CHECKS.md at 75cfb97: shellcheck, cli_test.sh, build-deb + package_test, gradle test (10 per variant), lint 0 errors, debug+release APKs (Stage 32). Stage 44 DoD at 75cfb97 (2026-10-27): unit 10+10 passed, CLI and package suites passed, shellcheck clean; DAT audit triaged.
  - Blocker: No device has passed docs/DEVICE_RC_CHECKLIST.md
  - Blocker: No signing key in CI; CI blocked org-wide (F49)
  - Blocker: Targets SDK 35; 36 available (F56)
- **JADIS Toolbox (`jadis`)** (`jadis.toolbox`): Portable workstation tool: environment classification, doctor, safe journaled repair, bootstrap, snapshots (Termux, PRoot Debian, Debian). Evidence: 75 tests at 253c386 (CLI suite plus 8 for the standalone scripts, incl. a mutation-checked git-crypt plaintext guard), ruff/mypy clean; earlier: real PRoot Debian 13 run, real BLUX subprocess call; GOD discovers its 4 read-only capabilities (Stage 33). Stage 44 DoD at 253c386 (2026-10-27): 75 passed; DAT audit triaged.
  - Blocker: Not run in native Termux (fixture-tested only)
  - Blocker: Native Debian 13 evidence pending the CI container job's first run
  - Blocker: No published package (install from source)
  - Blocker: Small repair catalogue (4 repairs)
  - Blocker: CI blocked org-wide (F49)
- **Credits ledger** (`credits`): Canonical attribution, licensing and provenance ledger. Evidence: validate.py --org-root and 39 tests OK at 18240ba (Stage 29 sync). Stage 44 DoD at 8a0c52a (2026-10-27): validate, org-root check and 39 tests passed; DAT audit triaged.
- **Central docs** (`docs`): Legal/policy baselines and ecosystem governance documentation (this repository). Evidence: tools/build_status_matrix.py --check OK; full reconciliation 2026-10-27. Stage 44 DoD at ef7d357 (2026-10-27): 13 tests, matrix, constitution and contract checks passed; DAT audit triaged.
- **Organization profile** (`.github`): Public organization profile and doctrine. Evidence: Contents reconciled 2026-10-27. Stage 44 DoD at be5221d (2026-10-27): DAT audit pass; links checked; DAT audit triaged.
  - Blocker: Owner banner says 'Stage 21 - 30 of 44'; the queued plan ends at Stage 45 (F50, owner decision)
- **Private organization profile** (`.github-private`): Members-only organization profile. Evidence: Contents inspected 2026-10-27 (logo and doctrine line only). Stage 44 DoD at 5ea59da (2026-10-27): DAT audit pass; DAT audit triaged.
- **BLHermes (archived fork)** (`blhermes-agent`): Historical/reference fork of Nous Research hermes-agent (MIT); replaced by BLUX. Evidence: GitHub API archived=true; credits LIN-001 archival facts.
- **Operation: Restore website** (`ov-webpages/operationrestore`): Static site for operationrestore.net. Evidence: README inspected 2026-10-26. Stage 44 DoD at 126453f (2026-10-27): DAT audit pass (static site); DAT audit triaged.
- **bluxai.app** (`ov-webpages/bluxai.app`): Private BLUX workspace service over the BLUX executables (orgs, roles, runs/receipts, API tokens, audit, opt-in remote runs). Evidence: 12 tests at 9fdb0a2 incl. a real remote run into the organization's own BLUX System store, tenant isolation, roles, read-only API tokens; no BLUX runtime imports and local BLUX works without it (Stage 39). Stage 44 DoD at 9e5706a (2026-10-27): 13 passed with BLUX, 10 + 3 skipped without; BLUX-absent 503 fix; DAT audit triaged.
  - Blocker: No web front end (F66)
  - Blocker: Not deployed; rate limits are per process (F66)
  - Blocker: CI blocked org-wide (F49)
- **IVRP website** (`ov-webpages/ivrp`): Reserved Inner Void Recovery Program website repository; README and LICENSE only. Evidence: File list inspected 2026-10-26. Stage 44 DoD at 68dbad7 (2026-10-27): DAT audit pass (README only); DAT audit triaged.
