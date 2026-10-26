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
| AXIOM Launcher | `void.os` | 2.0.0-dev | `097f50d` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| VOID.SYS | `void.sys` | 2.0.0-dev | `26d91b9` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | UNVERIFIED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| AXIOM Shooter | `void.game` | 2.1.0-dev | `ad7e0ab` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | MOCK_TESTED | HARDWARE_PENDING | BLOCKED | IMPLEMENTED | BLOCKED | NOT_RELEASED | 2026-10-26 |
| Resolver (Telegram runtime) | `resolver` | 1.0.0 (app/__init__.py) | `9c66aaf` | IMPLEMENTED | UNVERIFIED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | IMPLEMENTED | UNVERIFIED | 2026-10-24 |
| Resolver website | `ov-webpages/theresolver` | 0.1.0 | `75a6352` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | BLOCKED | NOT_APPLICABLE | UNVERIFIED | UNVERIFIED | 2026-10-24 |
| Roughin | `roughin` | frontend 1.0.0 | `7bd7125` | IMPLEMENTED | PLANNED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | NOT_STARTED | NOT_RELEASED | 2026-10-24 |
| Vigyl | `vigyl` | - | `2af2717` | IMPLEMENTED | PLANNED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | NOT_STARTED | NOT_RELEASED | 2026-10-24 |
| Termux Background | `termux-background` | 1.1.0 | `c375c7e` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | UNVERIFIED | HARDWARE_PENDING | NOT_APPLICABLE | IMPLEMENTED | UNVERIFIED | NOT_RELEASED | 2026-10-26 |
| Jadis Toolbox | `jadis.toolbox` | - | `0981ab5` | IMPLEMENTED | EXCLUDED | NOT_APPLICABLE | UNVERIFIED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |
| Credits ledger | `credits` | - | `9fb3fbf` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | INTEGRATION_TESTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |
| Central docs | `docs` | - | `636decb` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |
| Organization profile | `.github` | - | `71f58e0` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |
| Private organization profile | `.github-private` | - | `8707173` | IMPLEMENTED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | 2026-10-26 |
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
- **AXIOM Launcher** (`void.os`): Paid Android launcher product (bundles VOID.SYS and hidden AXIOM Shooter). Evidence: testDebugUnitTest 75 passed (incl. ProductBoundaryTest), assembleDebug OK, tools/components.py check --upstream OK at 097f50d (Stage 24).
  - Blocker: Stage 24 hard gate NOT passed (docs/release/release-matrix.md)
  - Blocker: Entitlement, Play Integrity and product-signature verification are TODO stubs (release paths fail closed)
  - Blocker: No device matrix run
  - Blocker: No release keystore / protected signing job (env-only signing exists)
  - Blocker: No crash-loop guard
  - Blocker: Public repository for a paid product
  - Blocker: Legal/asset notice review
- **VOID.SYS** (`void.sys`): Icon system: bundled AXIOM Launcher component and separate icon-pack product. Evidence: 590 SVG sources, 609 appfilter entries counted 2026-10-26; tests not run in this pass.
  - Blocker: Standalone signature verification is a TODO stub (fails closed)
  - Blocker: 2,903 asset variants pending individual visual review
  - Blocker: No versioned release consumed by AXIOM yet (Stage 25)
  - Blocker: Public repository for a paid product
- **AXIOM Shooter** (`void.game`): Standalone game product; core/ is the authoritative gameplay source bundled in AXIOM Launcher as a hidden Easter egg. Evidence: core:test 18 passed and android:assembleDebug OK at ad7e0ab (Stage 24); AXIOM vendors core byte-for-byte (components lock).
  - Blocker: Signature/launch verification is TODO (fails closed)
  - Blocker: No device playthroughs, GL context-loss or audio evidence (Stage 26)
  - Blocker: Public repository for a paid product
- **Resolver (Telegram runtime)** (`resolver`): Telegram moderation bot runtime with a paid intelligence layer. Evidence: Stage 00 baseline (2026-10-24) classified it RELEASE_CANDIDATE; not re-run in this pass.
  - Blocker: Release tag status not re-verified in this pass
- **Resolver website** (`ov-webpages/theresolver`): Marketing/acquisition site for the Resolver bot (separate from the runtime). Evidence: Stage 00 baseline (2026-10-24).
  - Blocker: Stage 00 baseline: next 16.1.6 critical advisory, upgrade to >=16.4.3 (not re-verified)
- **Roughin** (`roughin`): Standalone contractor SaaS (FastAPI + React PWA). Evidence: Stage 00 baseline (2026-10-24); release readiness is Stage 28.
  - Blocker: Stage 00 baseline: missing greenlet dependency (not re-verified)
  - Blocker: Public repository for proprietary SaaS source
- **Vigyl** (`vigyl`): Standalone caregiving/accountability product; Stage 1 backend foundation only. Evidence: Stage 00 baseline (2026-10-24); release readiness is Stage 29.
  - Blocker: Only the Stage 1 core loop exists
  - Blocker: Public repository for privacy-sensitive product source
- **Termux Background** (`termux-background`): Standalone Android companion + Termux CLI for Termux Monet wallpapers. Evidence: Repository docs; not re-run in this pass.
  - Blocker: No device has passed docs/DEVICE_RC_CHECKLIST.md
- **Jadis Toolbox** (`jadis.toolbox`): Personal utility scripts (GitHub backup, master log) and Termux notes. Evidence: Repository contents inspected 2026-10-26.
- **Credits ledger** (`credits`): Canonical attribution, licensing and provenance ledger. Evidence: validate.py --org-root and 39 tests OK (Stage 23 update).
- **Central docs** (`docs`): Legal/policy baselines and ecosystem governance documentation (this repository). Evidence: tools/build_status_matrix.py --check.
- **Organization profile** (`.github`): Public organization profile and doctrine. Evidence: Contents inspected 2026-10-26.
- **Private organization profile** (`.github-private`): Members-only organization profile. Evidence: Contents inspected 2026-10-26.
- **BLHermes (archived fork)** (`blhermes-agent`): Historical/reference fork of Nous Research hermes-agent (MIT); replaced by BLUX. Evidence: GitHub API archived=true; credits LIN-001 archival facts.
- **Operation: Restore website** (`ov-webpages/operationrestore`): Static site for operationrestore.net. Evidence: README inspected 2026-10-26.
- **bluxai.app** (`ov-webpages/bluxai.app`): Reserved BLUX website repository; contains only README and LICENSE. Evidence: File list inspected 2026-10-26.
- **IVRP website** (`ov-webpages/ivrp`): Reserved Inner Void Recovery Program website repository; README and LICENSE only. Evidence: File list inspected 2026-10-26.
