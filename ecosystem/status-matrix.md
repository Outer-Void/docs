# Component status matrix

Generated from `tools/build_status_matrix.py`; do not edit by hand. Statuses are defined in
[README.md](README.md#status-vocabulary). `commit_sha` is the evidence anchor at `last_verified`.

| Component | Repo | Version | Commit | Standalone | BLUX | ax | Tests | Hardware | Security | Package | Distribution | Release | Last verified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BLUX (runtime, SDK, contracts, `blux` CLI) | `blux` | outervoid-blux 0.4.0; blux-sdk 0.2.0; Contract v1 / Model API v1 / Hook System v1 = 1.0 | `f491524` | IMPLEMENTED | NOT_APPLICABLE | INTEGRATION_TESTED | INTEGRATION_TESTED | BLOCKED | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| AXIOM control plane (`ax`) | `axiom` | 2.0.0 | `a276744` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| blux10k | `blux10k` | 3.0.0 | `fcb127d` | IMPLEMENTED | EXCLUDED | INTEGRATION_TESTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| CogA | `blux-coga` | 2.0.0 | `3dc86fa` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| cA | `blux-ca` | 2.0.1 | `7cb953a` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| DAT | `dat` | 4.0.0 | `76d0a01` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | IMPLEMENTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| LRC | `lrc` | 2.0.0 | `34b6a04` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| GOD | `god` | 2.0.0 | `a329d89` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| BLUX System | `blux-system` | 2.0.0 | `f0ba3a1` | IMPLEMENTED | INTEGRATION_TESTED | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| BluxGPT | `blux-gpt` | 2.0.0 | `4609cd9` | IMPLEMENTED | INTEGRATION_TESTED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| BLUX App | `blux-app` | - | `386e81f` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_STARTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| cA dataset | `blux-ca-dataset` | dynamic (pyproject) | `662ec33` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| CogA dataset | `blux-coga-dataset` | dynamic (pyproject) | `9331f73` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| VoidForge | `voidforge` | 0.1.0-dev | `463b921` | IMPLEMENTED | OPTIONAL | INTEGRATION_TESTED | MOCK_TESTED | BLOCKED | MOCK_TESTED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| AXIOM Launcher | `void.os` | 2.0.0-dev | `24b07cd` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| VOID.SYS | `void.sys` | 2.1.0-dev | `09cf56f` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| AXIOM Shooter | `void.game` | 2.1.0-dev | `b56c1ae` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| Resolver (Telegram runtime) | `resolver` | 1.0.0 (app/__init__.py); git tag v4.0 | `bf7f26a` | IMPLEMENTED | UNVERIFIED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | IMPLEMENTED | UNVERIFIED | 2026-10-27 |
| Resolver website | `ov-webpages/theresolver` | 0.2.0 | `49dbeff` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | IMPLEMENTED | NOT_APPLICABLE | IMPLEMENTED | NOT_RELEASED | 2026-10-27 |
| Roughin | `roughin` | 1.1.0 (API); frontend 1.0.0 | `f3599d3` | IMPLEMENTED | PLANNED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| Vigyl | `vigyl` | API 0.2.0 | `a0816a4` | IMPLEMENTED | PLANNED | NOT_APPLICABLE | MOCK_TESTED | NOT_APPLICABLE | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-27 |
| Termux Background | `termux-background` | 1.1.0 | `75cfb97` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | NOT_APPLICABLE | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-27 |
| JADIS Toolbox (`jadis`) | `jadis.toolbox` | 0.1.0 | `64f5d08` | IMPLEMENTED | OPTIONAL | NOT_APPLICABLE | INTEGRATION_TESTED | HARDWARE_PENDING | MOCK_TESTED | IMPLEMENTED | NOT_STARTED | NOT_RELEASED | 2026-10-26 |
| Credits ledger | `credits` | - | `18240ba` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| Central docs | `docs` | - | `6cfbd70` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| Organization profile | `.github` | - | `7c9ad5a` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| Private organization profile | `.github-private` | - | `bc32b7a` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-27 |
| BLHermes (archived fork) | `blhermes-agent` | upstream metadata only | `dc8abc1db0` | ARCHIVED | ARCHIVED | NOT_APPLICABLE | ARCHIVED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | ARCHIVED | ARCHIVED | 2026-10-26 |
| Operation: Restore website | `ov-webpages/operationrestore` | - | `126453f` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | UNVERIFIED | UNVERIFIED | 2026-10-26 |
| bluxai.app | `ov-webpages/bluxai.app` | - | `a8d127a` | NOT_STARTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |
| IVRP website | `ov-webpages/ivrp` | - | `0e2b75e` | NOT_STARTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |

## Evidence and blockers

- **BLUX (runtime, SDK, contracts, `blux` CLI)** (`blux`): Intelligence/runtime/integration platform: contracts, capability registry, Model API, routing, Hook System, direct `blux` CLI. Evidence: make ci at f491524: 563 passed, 15 skipped; schema lock, ruff, mypy, wheel OK (Stage 22).
  - Blocker: No release tag or published package
  - Blocker: Termux APT on-device install not run (owner steps in packaging/termux/ACCEPTANCE.md)
  - Blocker: No real-provider Model API evidence (provider accounts without balance)
- **AXIOM control plane (`ax`)** (`axiom`): Developer control plane; routes to authoritative engines, reimplements none. Evidence: tests/test_ax_router.py 12 passed and tests/run_tests.sh 14/14 at a276744 (Stage 22); `ax devices` chain also exercised from VoidForge's integration test.
  - Blocker: Engines must be installed separately; missing engines exit 69 by design
- **blux10k** (`blux10k`): Environment and toolchain authority (`ax env`) plus dotfiles. Evidence: pytest: 10 passed at fcb127d (re-run 2026-10-26).
- **CogA** (`blux-coga`): Deterministic structured reasoning; no model, no hidden chain-of-thought. Evidence: pytest: 343 passed at 3dc86fa (re-run 2026-10-26).
  - Blocker: No release tag for 2.0.0
- **cA** (`blux-ca`): Construction/modification/repair; never certifies its own work (DAT validates). Evidence: pytest: 117 passed at 7cb953a (re-run 2026-10-26; needs the declared `hypothesis` dev dependency).
  - Blocker: No release tag for 2.0.1
- **DAT** (`dat`): Independent audit/security/quality/release authority; may reject any component's work. Evidence: pytest: 88 passed at 76d0a01 (re-run 2026-10-26).
  - Blocker: README previously pinned a v4.0.0 tag that does not exist (tags: v1.0.0, v2.0.0-alpha.1, v2.0.0-Stable)
- **LRC** (`lrc`): Deterministic repository creation/scaffolding/migration; does not certify itself. Evidence: pytest: 133 passed, 1 skipped at 34b6a04 (re-run 2026-10-26).
  - Blocker: No release tag for 2.0.0
- **GOD** (`god`): Capability/project/command discovery; never execution authority. Evidence: pytest: 94 passed at a329d89 (re-run 2026-10-26).
  - Blocker: No release tag for 2.0.0
- **BLUX System** (`blux-system`): Intelligence-free execution truth: receipts, operation graph, provenance, replay metadata. Evidence: pytest: 74 passed at f0ba3a1 (re-run 2026-10-26).
  - Blocker: No release tag for 2.0.0
- **BluxGPT** (`blux-gpt`): Provider/model gateway behind Model API v1; no agent loop, no tool execution, no authority. Evidence: pytest: 49 passed, 1 skipped at 4609cd9 (re-run 2026-10-26), deterministic mock and fake transports.
  - Blocker: Real-provider runs not recorded; hard-coded provider model IDs not verified against current catalogs
- **BLUX App** (`blux-app`): Read-only observability viewer of artifacts and receipts. Evidence: Not re-run in the 2026-10-26 documentation pass.
  - Blocker: Phase 1 CLI viewer only
- **cA dataset** (`blux-ca-dataset`): Deterministic cA evaluation/training dataset (Hugging Face card layout). Evidence: pytest: 36 passed, 2 skipped at 662ec33 (re-run 2026-10-26).
- **CogA dataset** (`blux-coga-dataset`): Deterministic CogA evaluation/training dataset. Evidence: pytest: 38 passed at 9331f73 (re-run 2026-10-26).
- **VoidForge** (`voidforge`): Standalone Android-to-Android device-engineering workstation (members-only, free for now). Evidence: Stage 22/23: :core 86, :integration 9, tools 24 tests passed; app assembleDebug OK; all mock/synthetic.
  - Blocker: Production write barrier locked; no local confirmation UI
  - Blocker: No real-device acceptance (2026-10-26 probe BLOCKED)
  - Blocker: Repository is public, conflicting with members-only policy (owner action in docs/DISTRIBUTION.md)
  - Blocker: No production release key or keystore configured
- **AXIOM Launcher** (`void.os`): Paid Android launcher product (bundles VOID.SYS and hidden AXIOM Shooter). Evidence: testDebugUnitTest 78 passed, assembleDebug OK, tool tests OK, components check with both upstreams OK, 16 KB native QA OK at 24b07cd (Stage 26).
  - Blocker: Stage 24 hard gate NOT passed (docs/release/release-matrix.md)
  - Blocker: Entitlement, Play Integrity and product-signature verification are TODO stubs (release paths fail closed)
  - Blocker: No device matrix run
  - Blocker: No release keystore / protected signing job (env-only signing exists)
  - Blocker: No crash-loop guard
  - Blocker: Public repository for a paid product
  - Blocker: Legal/asset notice review
- **VOID.SYS** (`void.sys`): Icon system: one lineage for the standalone icon pack and the versioned bundle consumed by AXIOM Launcher. Evidence: tools tests 8 passed, verify_drawables OK, assembleDebug + assembleRelease OK, release APK keeps all 587 drawable names (Stage 25); AXIOM vendors release/manifest.json bundle byte-for-byte.
  - Blocker: Standalone signature verification is a TODO stub (fails closed)
  - Blocker: 2,903 asset variants pending individual visual review
  - Blocker: No device test of the standalone pack in third-party launchers
  - Blocker: Public repository for a paid product
- **AXIOM Shooter** (`void.game`): Standalone game product; core/ is the authoritative gameplay source bundled in AXIOM Launcher as a hidden Easter egg. Evidence: core:test 21 passed; android assembleDebug + assembleRelease OK; tools/check_apk_natives.py passes both APKs (libGDX 1.14.2, 16 KB); aapt2: launchable 'AXIOM Shooter' (Stage 26).
  - Blocker: Purchase/signature verification is TODO (release fails closed)
  - Blocker: No audio
  - Blocker: Interrupted runs are not resumed
  - Blocker: No device playthroughs, GL context-loss, frame-time or battery evidence
  - Blocker: Default font licence unresolved (credits UNR-020)
  - Blocker: Public repository for a paid product
- **Resolver (Telegram runtime)** (`resolver`): Telegram moderation bot runtime with a paid intelligence layer. Evidence: Release gate offline steps at bf7f26a: compileall OK, unittest 173 OK, scripts/smoke_check.py OK (2026-10-27 reconciliation).
  - Blocker: Version mismatch: tag v4.0 (73abe3e) vs __version__ 1.0.0 (F48)
  - Blocker: Release gate steps install_resolver.sh / run_resolver.sh need live secrets: not run
  - Blocker: CI blocked org-wide by the GitHub billing lock (F49)
- **Resolver website** (`ov-webpages/theresolver`): Marketing/acquisition site for the Resolver bot (separate from the runtime). Evidence: npm run check at 49dbeff: lint, build, 9 node:test checks over the export incl. HTTP smoke; npm audit 0; two builds byte-identical; deployed theresolver.pages.dev serves this build (pages 200, deep links, CSP/HSTS headers) (Stage 31).
  - Blocker: Custom domain theresolverbot.net (and www) returns Cloudflare error 1033 (tunnel), not the Pages site (F54)
  - Blocker: GitHub Actions blocked org-wide by the billing lock (F49)
- **Roughin** (`roughin`): Standalone contractor SaaS (FastAPI + React PWA). Evidence: pytest: 91 passed at f3599d3 (SQLite; Stripe/R2 faked at the edge, real webhook signature verification); ruff clean; vite build OK (Stage 28).
  - Blocker: PostgreSQL migration + backup/restore CI BLOCKED: GitHub account billing lock, jobs never started (F34)
  - Blocker: No deployment, Stripe test-mode or real R2 run (F35)
  - Blocker: No frontend tests or device testing (F37)
  - Blocker: Frontend dependency advisories need major upgrades; Python deps pip-audit clean (F36)
  - Blocker: Public repository for proprietary SaaS source
- **Vigyl** (`vigyl`): Standalone caregiving/accountability product; backend API only (no UI yet). Evidence: pytest: 78 passed at a0816a4 (SQLite; role, access, privacy, task-history and failure-path suites); ruff clean; pip-audit clean (Stage 29).
  - Blocker: No app UI (F43)
  - Blocker: Notifications are in-app only: no push/email delivery (F44)
  - Blocker: PostgreSQL migration + backup CI BLOCKED: GitHub billing lock (F45)
  - Blocker: No recurring tasks, password reset or legal review (F46)
  - Blocker: Public repository for privacy-sensitive product source
- **Termux Background** (`termux-background`): Standalone Android companion + Termux CLI for Termux Monet wallpapers. Evidence: docs/RELEASE_CHECKS.md at 75cfb97: shellcheck, cli_test.sh, build-deb + package_test, gradle test (10 per variant), lint 0 errors, debug+release APKs (Stage 32).
  - Blocker: No device has passed docs/DEVICE_RC_CHECKLIST.md
  - Blocker: No signing key in CI; CI blocked org-wide (F49)
  - Blocker: Targets SDK 35; 36 available (F56)
- **JADIS Toolbox (`jadis`)** (`jadis.toolbox`): Portable workstation tool: environment classification, doctor, safe journaled repair, bootstrap, snapshots (Termux, PRoot Debian, Debian). Evidence: 67 tests (unit, fixture, real-filesystem integration, adversarial redaction), 7 deliberate breaks caught, ruff/mypy/hygiene clean, wheel smoke test; real PRoot Debian 13 run; real BLUX subprocess call (2026-10-26).
  - Blocker: Not run in native Termux (fixture-tested only)
  - Blocker: Native Debian 13 evidence pending the CI container job's first run
  - Blocker: No published package (install from source)
  - Blocker: Small repair catalogue (4 repairs)
- **Credits ledger** (`credits`): Canonical attribution, licensing and provenance ledger. Evidence: validate.py --org-root and 39 tests OK at 18240ba (Stage 29 sync).
- **Central docs** (`docs`): Legal/policy baselines and ecosystem governance documentation (this repository). Evidence: tools/build_status_matrix.py --check OK; full reconciliation 2026-10-27.
- **Organization profile** (`.github`): Public organization profile and doctrine. Evidence: Contents reconciled 2026-10-27.
  - Blocker: Owner banner says 'Stage 21 - 30 of 44'; the queued plan ends at Stage 45 (F50, owner decision)
- **Private organization profile** (`.github-private`): Members-only organization profile. Evidence: Contents inspected 2026-10-27 (logo and doctrine line only).
- **BLHermes (archived fork)** (`blhermes-agent`): Historical/reference fork of Nous Research hermes-agent (MIT); replaced by BLUX. Evidence: GitHub API archived=true; credits LIN-001 archival facts.
- **Operation: Restore website** (`ov-webpages/operationrestore`): Static site for operationrestore.net. Evidence: README inspected 2026-10-26.
- **bluxai.app** (`ov-webpages/bluxai.app`): Reserved BLUX website repository; contains only README and LICENSE. Evidence: File list inspected 2026-10-26.
- **IVRP website** (`ov-webpages/ivrp`): Reserved Inner Void Recovery Program website repository; README and LICENSE only. Evidence: File list inspected 2026-10-26.
