# Implementation findings from documentation synchronization

Documentation passes record real implementation gaps here. They do not silently fix them. Each entry
gives the repository, the issue, its severity, how the documentation exposed it, the recommended stage, and
whether it blocks a release. Entries leave this register only when the fix is merged, with the fixing commit
noted. History stays in git.

## Pass of 2026-10-26 (after Stage 23)

| # | Repo | Issue | Severity | How documentation exposed it | Recommended stage | Blocking |
|---|---|---|---|---|---|---|
| F1 | void.os | Paid-app entitlement, Play Integrity and product-signature verification are `TODO` stubs (`EntitlementManager`, `IntegrityGate`, `SignatureVerifier`). Release paths fail closed. | Critical | The README claimed a "signed AXIOM-to-VOID.GAME launch contract" | Stage 24 (needs the owner's Play/backend decisions) | Yes: paid release |
| F2 | void.game | `SignatureVerifier` leaves cryptographic verification as `TODO` (Stage 26 replaced `LaunchGate` with `StandaloneEntitlementGate`; still fails closed). Release fails closed; debug builds bypass. | Critical | `docs/security.md` said "protected by a launch contract and runtime module signature gate" | Stage 26 | Yes: paid release |
| F3 | void.os ↔ void.game | ~~No single source of truth for Shooter~~ **Resolved in Stage 24:** `void.game/core` is authoritative (void.game `ad7e0ab`); AXIOM vendors it byte-for-byte at a locked commit, and `tools/components.py check` fails CI on drift (void.os `097f50d`). | High | Status audit | Stage 24 | No longer |
| F4 | void.game | ~~Two versions (root 0.1.0 vs versionName 2.0.0-dev)~~ **Resolved in Stage 24:** one version, 2.1.0-dev (void.game `ad7e0ab`) | Low | Version-consistency audit | Stage 24 | No |
| F5 | voidforge | No local confirmation UI. The app's authorizer declines every write, and the production write barrier is locked. File pull/push, backup capture, install, sideload, flash and the root/module workflows exist only in `:core`. | High (by design until hardware qualification) | Four-state status audit (core / app / mock / hardware) | After real-device acceptance | Yes: write features |
| F6 | voidforge | No real-device evidence. The Stage 23 probe was BLOCKED: no USB in the build container, no attached target, app not installed. | High | Hardware column of the status matrix | Owner-run acceptance (`tools/device_acceptance.py`) | Yes: release |
| F7 | voidforge, void.os, void.sys, void.game, roughin, vigyl | Proprietary, paid or members-only product source sits in **public** repositories (unauthenticated GitHub API returns 200). VoidForge's members-only policy is therefore not met for source. | High (policy) | Distribution-status audit | Owner action (repository visibility) | Yes: VoidForge distribution policy |
| F8 | dat | README install command pinned tag `v4.0.0`, which does not exist (tags: `v1.0.0`, `v2.0.0-alpha.1`, `v2.0.0-Stable`). The README is now corrected. | Medium | Command verification | Owner: tag 4.0.0, or keep installing from `main` | No |
| F9 | blux | No release tag or published package. Termux APT on-device installation not run. | Medium | Package and release status | Owner steps in `packaging/termux/ACCEPTANCE.md` | Yes: BLUX release |
| F10 | blux, blux-gpt | No real-provider Model API evidence (provider accounts without balance). Hard-coded provider model IDs are not checked against current catalogs. | Medium | Evidence-model audit (mock vs real-provider) | When provider access exists | No |
| F11 | .github | `docs/ecosystem-diagram.md` described five repositories that do not exist (`blux-core`, `blux-orbit`, `blux-design-system`, `blux-experience-kit`, `blux-governance`). Now replaced by a pointer to this map. | Medium (docs) | Cross-reference audit | Fixed in this pass | No |
| F12 | theresolver | ~~`next` 16.1.6 critical advisory~~ **Resolved in Stage 31:** `next` 16.4.3; `npm audit`: 0 vulnerabilities (theresolver `49dbeff`) | High (security) | Status matrix; full reconciliation | Stage 31 | No longer |
| F13 | roughin | ~~Stage 00 baseline: missing `greenlet` dependency~~ **Resolved in Stage 28:** reproduced (import error), fixed with `sqlalchemy[asyncio]` in `backend/requirements.txt` (roughin `9e5cf12`). | Medium | Status matrix | Stage 28 | No longer |
| F14 | termux-background | README said "v1.0.0 Not Operational" while `VERSION` is 1.1.0; no device has passed its checklist. README corrected. | Low | Version-consistency audit | Owner device run | Yes: release |
| F15 | jadis.toolbox | The README was an operating checklist and did not describe the repository's scripts. An identity section was added. | Low (docs) | Identity audit | Fixed in this pass | No |
| F16 | blux10k | `dotfiles/.zshrc` exports `BLUX10K_VERSION="2.0.0"`, while `VERSION` and `bin/blux10k --version` report 3.0.0 | Low | Version-consistency audit | Next blux10k change | No |
| F17 | void.sys | `security/SignatureVerifier.kt` also leaves signature verification as `TODO`: the standalone icon-pack signature gate is scaffolding | High | TODO/FIXME source audit | Stage 25 | Yes: paid release |

## Stage 24 incremental sync (2026-10-26)

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F18 | void.os | CI uploaded the debug APK from a public repository. Debug builds bypass entitlement, so unlocked builds of a paid product were downloadable. **Contained in Stage 24:** upload limited to private repositories (`097f50d`). The unauthenticated API lists no current void.os artifacts (2026-10-26), so none remain to clean up. | High | CI workflow review | Distribution blocker | **Resolved** |
| F19 | void.os | No crash-loop guard: a startup crash repeats until the user changes the default Home app | Medium (P1) | Stage 24 release matrix | Future-stage work, needs device verification | Yes: paid release |
| F20 | void.os | Backup is disabled (`allowBackup="false"`); customization is lost on device transfer | Low (P2) | Release matrix | Product decision (open question) | No |
| F21 | void.os | No release keystore or protected signing job; environment-only signing exists | High (P0) | Release matrix | Release blocker (owner) | Yes |
| F22 | void.game | ~~Standalone packaging only build-verified~~ **Mostly resolved in Stage 26:** release/R8 build and 16 KB audit pass (`6f6c85b`); device runs remain (see F31) | Medium | Stage 24 build | Stage 26 | No longer (device part: F31) |

## Stage 25 incremental sync (2026-10-26)

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F23 | void.os ↔ void.sys | VOID.SYS work had been authored only inside AXIOM: 7 vector glyphs, their mappings, and the generic-drawable classification, so the standalone pack lacked them. **Resolved:** promoted to void.sys (`09cf56f`); AXIOM vendors the versioned bundle through its component lock (`4964895`). | Medium | Byte comparison of both repositories | Stage 25 | No longer |
| F24 | void.sys | The VOID.SYS app icon was a plain vector, not an adaptive icon. **Resolved:** adaptive background/foreground/monochrome layers inside the safe zone (`09cf56f`). | Low | Adaptive-icon audit | Stage 25 | No longer |
| F25 | void.sys | The standalone pack has not been device-tested in third-party launchers (Nova, Lawnchair); appfilter resolution is verified only statically | Medium | Stage 25 tests are static | Hardware pending | Yes: standalone release |

## Stage 26 incremental sync (2026-10-26)

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F26 | void.game | Tracked libGDX **1.12.1** natives were packaged with the **1.14.2** Java backend (JNI mismatch risk, 4 KB alignment). **Resolved:** natives extracted from Maven 1.14.2 at build time; `.so` files untracked (`6f6c85b`) | Critical | APK native audit (hash and alignment differed from AXIOM's) | Stage 26 | No longer |
| F27 | void.game | The standalone app had no `LAUNCHER` entry, label or icon, so buyers could not launch it. **Resolved:** "AXIOM Shooter" launcher entry with adaptive icon (`6f6c85b`). Supersedes the earlier development-only design | Critical | Manifest audit; `aapt2 dump badging` | Stage 26 | No longer |
| F28 | void.game | The standalone release gate required an AXIOM launch payload that AXIOM never sends, so a standalone purchase could never unlock. **Resolved:** `StandaloneEntitlementGate` (verification still TODO, F2) | High | Code review of both hosts | Stage 26 | No longer (crypto: F2) |
| F29 | void.game | No audio: no sound assets or synthesis exist | Medium | Asset and code audit | Future-stage product work (needs licensed or synthesized audio and device verification) | Yes: product polish |
| F30 | void.game | An interrupted run is not resumed; only campaign progress, scores and settings persist | Medium | Persistence audit | Future-stage work | No |
| F31 | void.game, void.os | No device playthroughs, GL context-loss, frame-time or battery evidence on either surface | High | Status matrix | Hardware pending | Yes: release |
| F32 | void.game, void.os | The default font (libGDX `lsans-15`) has no confirmed upstream licence (credits UNR-020) | Medium | Asset-licensing audit | Unresolved attribution | Yes: legal review |

## Stage 28 incremental sync (2026-10-27)

Roughin release-readiness audit (roughin `9e5cf12`). Fixed in the stage, with tests: the Stripe webhook had no
idempotency and never recorded payments or linked subscriptions; the checkout customer id was never committed;
refresh tokens were plaintext, never rotated, and `/auth/refresh` returned 500; CORS was a wildcard with
credentials; the default JWT secret and `create_all` were allowed in production; invoice numbers were globally
unique; invoice status was freely patchable; a voided invoice's payment link stayed payable; account deletion
failed on foreign keys and left stored files; uploads had no type or size limit; search did not escape LIKE
wildcards; two list routes answered 200 instead of 404 across tenants; Tailwind never ran (no PostCSS config),
so the production CSS was empty. Open items:

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F33 | roughin | Migration 0001 never matched the models: 32 columns nullable that the models declare NOT NULL, and no unique PaymentIntent id. Databases built by the 1.0 `create_all` have the model schema and no `alembic_version`. **Resolved for migrated databases:** migration 0003 and `test_migrations.py` (SQLite). `create_all` databases need `alembic stamp 0001` (docs/deployment.md) | High | `compare_metadata` test | Stage 28 | No longer (stamping documented) |
| F34 | roughin | The PostgreSQL migration run and the backup/restore round-trip are defined in CI (`postgres` job) but have no evidence. Every job in CI runs 40437004032 (`6a63057`) and 40438085335 (`f3599d3`) failed before starting: "The job was not started because your account is locked due to a billing issue." There is no PostgreSQL in the build environment | High | Stage 28 hard gate | **BLOCKED** (Appendix B): the owner clears the GitHub billing lock, then re-runs `ci` on `main`; acceptance = `backend`, `postgres` and `frontend` jobs green. Local alternative: `make test` with `MIGRATION_TEST_URL` pointing at a scratch PostgreSQL 16, plus the `postgres` job's backup steps | Yes: release |
| F35 | roughin | No production deployment, no Stripe test-mode run, no real R2 bucket test: Stripe and R2 are faked at the network edge in tests (webhook signatures are real) | High | Stage 28 hard gate | Environment-blocked: needs owner accounts and a host; steps in `docs/release-checklist.md` | Yes: release |
| F36 | roughin | Dependency advisories. Python: python-jose and ecdsa (unfixed upstream; not exploitable, HS256 pinned) **resolved** by switching to PyJWT (roughin `f3599d3`); `pip-audit` is clean. GitHub reported 11 Dependabot alerts at push time; they could not be itemized (`gh` unauthenticated in this session) and may lag the PyJWT fix. Frontend (`npm audit`: 1 high, 4 moderate): vite ≤6.4.3 and esbuild ≤0.24.2 (dev server only, not in the bundle); react-router 6.x open redirect via `<Link>`/`navigate` (shipped, but every navigation target is a constant or a server UUID, so it is not reachable today). Fixes need majors: react-router-dom 7, vite 8, vite-plugin-pwa 2 | Medium | `npm audit`; Dependabot on push | Future stage: upgrade with UI smoke tests | No (not exploitable as used); yes before adding user-controlled navigation |
| F37 | roughin | No frontend tests and no real-device mobile or poor-network testing; the UI was changed (refresh interceptor, invoice actions, Settings) and verified only by `vite build` | Medium | Stage 28 audit | Future stage (Roughin UI) | Yes: release confidence |
| F38 | roughin | Auth rate limiting is in process memory (one instance only); no email verification, password reset, 2FA or account lockout; tokens in `localStorage` | Medium | `docs/security.md` | Future stage | No (documented) |
| F39 | roughin | Partial payments and refunds are not modelled (audited for manual review); estimates are PDFs, not stored entities; `datetime.utcnow()` naive timestamps (deprecated in Python 3.12+) | Low | Stage 28 audit | Future stage | No |
| F40 | roughin | Production PWA icons (192/512 PNG) are deliberately kept out of git; only a placeholder SVG ships | Low | `vite build` audit | Owner/brand pipeline (Void.Sys icons) | Yes: store-quality install |
| F41 | roughin | Optional BLUX features (drafting, scope extraction, summaries) were not started: the brief allows them only after the deterministic core is solid, and the core's hard gate still has F34/F35 open | Info | Stage 28 brief | After F34/F35 | No |

## Stage 29 incremental sync (2026-10-27)

Vigyl core rebuild (vigyl `a01497d`, `a0816a4`). Fixed in the stage, with tests: Stage 1 had no
authentication. `GET /users` and `GET /care-groups` listed every account's email and every group's join
code to anyone, and every write trusted a client-supplied `user_id`. Join codes never expired and could be
reused. Tasks had no verification, missed state or history. The pinned `fastapi==0.116.1` pulled in
starlette 0.47.3 (7 advisories). Open items:

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F42 | vigyl | Stage 1 SQLite development databases are not migrated (no accounts existed; Alembic starts at 0001 = the Stage 29 models) | Low | Migration design | Documented in the 0001 docstring and roadmap | No (nothing was deployed) |
| F43 | vigyl | No app UI: the master plan's "see task, tap done" and "see status instantly" flows exist only as API endpoints | High | `frontend/` holds only `.gitkeep` | Future stage (Vigyl UI) | Yes: release |
| F44 | vigyl | Notifications and escalations are in-app records only; no push, email or SMS delivery, so an escalation reaches nobody who is not in the app | High | `docs/notifications.md` | Future stage | Yes: release (must not be described as alerting until fixed) |
| F45 | vigyl | The PostgreSQL migration test and backup round-trip are CI-defined but CI run 40445574378 (`a01497d`) never started: "account is locked due to a billing issue" (same as F34) | High | GitHub check-run annotation | **BLOCKED** (Appendix B): the owner clears the billing lock; acceptance = `backend` and `postgres` jobs green | Yes: release |
| F46 | vigyl | No recurring tasks, password reset, email verification or 2FA; subscriptions (master plan §VI) and location are not built; the privacy policy is a corrected draft needing legal review (health-adjacent data) | Medium | Stage 29 audit | Future stages + owner legal review | Yes: release |
| F47 | vigyl | Optional BLUX assistance not started; the boundary (suggest-only, never completes/reassigns/verifies, no medical decisions) is documented in `docs/architecture.md#blux-boundary` | Info | Stage 29 brief | After F43/F44 | No |

## Full ecosystem reconciliation after Stage 30 (2026-10-27)

Stage 30 has no brief of its own: the owner's prompts cover Stages 20–29 and 31–45. It is recorded as the
checkpoint that closes the 21–29 wave and triggers this mandatory reconciliation. All 28 repositories
(26 under `~/ov` plus `.github` and `.github-private`) were fetched; every one is clean and level with
`origin/main`. Excluded: `secret-project` (owner exclusion) and `blhermes-agent` (archived, read-only).

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F48 | resolver | Version mismatch: git tag `v4.0` (on `73abe3e`) versus `app/__init__.py` `__version__ = "1.0.0"`. Neither is documented as the release version | Medium | Reconciliation | Owner decision on the versioning scheme | Yes: release labelling |
| F49 | all repositories with CI (18 use `ubuntu-latest`) | **No CI has run organization-wide.** The latest run of every checked repository (voidforge, void.os, void.sys, void.game, blux, axiom, dat, jadis.toolbox, termux-background, credits, docs, blux-ca, roughin, vigyl) failed before starting: "The job was not started because your account is locked due to a billing issue." Every CI-based evidence claim therefore rests on local runs only. GitHub also warns that `ubuntu-latest` moves to Ubuntu 26 | Critical (process) | GitHub check-run annotations, 2026-10-27 | **BLOCKED** (Appendix B): the owner clears the billing lock, then re-runs CI; pin runner images in Stage 42 (cross-repo CI) | Yes: every release |
| F50 | .github | The owner-written banner says "Stage 21 - 30 of 44"; the queued plan ends at Stage 45, and Stage 30 has no brief | Low | Profile versus the stage queue | Owner decision (owner text was not edited) | No |
| F51 | dat | `snapshot.md` (2026-01-21, `f735057`) still described DAT as MIT-licensed and "enterprise-grade", and holds the only broken relative link in the organization. **Resolved:** a historical-snapshot banner (dat `8898290`); the content is kept as history | Low | Link check; claim search | Docs | No longer |
| F52 | .github | The profile listed Vigyl's stack as SQLite and described the jadis.toolbox overhaul as only scheduled. **Resolved** (.github `7c9ad5a`) | Low | Profile versus matrix | Docs | No longer |

Checked with no contradiction found: versions in the matrix against package metadata (every row matches);
stage references in every repository; obsolete names (BLHermes references are historical and accurate; no
`blux-web` claims); release-sounding claims (none unqualified outside the DAT snapshot); the repository
visibility list in F7 (unchanged: 6 proprietary product repositories are still public; resolver,
theresolver, bluxai.app, ivrp, operationrestore and .github-private are private); a secret and personal-path
scan of every file changed since 2026-10-26 (clean); and credits `validate.py --org-root` (OK).

## Stage 31 incremental sync (2026-10-27)

Resolver website overhaul (theresolver `49dbeff`). Fixed in the stage, with tests:
- The status page and the footer of every page claimed "All Systems Operational", with a build-time "Last
  checked" timestamp.
- Pricing sold a RAG add-on the bot no longer offers.
- The privacy page said AI-provider data is "anonymized"; `llm.py` and `rag.py` send text and user IDs.
- Canonical URLs pointed at a redirecting `www` host.
- There was no CSP, and builds were not reproducible.

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F53 | resolver | Tracked `cloudflared/config.yml` names tunnel `thetheresolverbotbot` and routes `admin.thetheresolverbotbot.net` / `hq.thetheresolverbotbot.net`; the site and bot docs use `admin.theresolverbot.net` (looks like a doubled find-and-replace) | Medium | Stage 31 domain check | Bot maintenance (separate lifecycle; not changed here) | Possibly: admin cockpit routing |
| F54 | theresolver | `https://theresolverbot.net/` and `www` return HTTP 530, Cloudflare error 1033 (tunnel unreachable), on 2026-10-27; the Pages deployment `theresolver.pages.dev` serves the current build. The apex hostname is routed to a tunnel instead of the Pages project | High | `curl` against both hosts | Owner action in Cloudflare (attach the custom domain to the Pages project, or fix the tunnel route) | Yes: site launch |
| F55 | theresolver | GitHub reported 86 Dependabot alerts on push while `npm audit` of the pushed lockfile reports 0; the private repository's alerts cannot be listed here (`gh` unauthenticated) | Low | Push output versus `npm audit` | Re-check once `gh` is authenticated | No |

## Stage 32 incremental sync (2026-10-27)

Termux Background release checks (termux-background `75cfb97`). Fixed: three negative CLI test assertions
(`! grep …` under `set -e`) could never fail; the README lacked uninstall steps (the package does not revert
`termux.properties`) and still cloned from `Justadudeinspace/`. Local release checks pass
(`docs/RELEASE_CHECKS.md`); the standalone release gate still needs a device and CI.

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F56 | termux-background | Targets SDK 35 while 36 is available (lint `OldTargetApi`); raising it needs a behaviour review and a device re-test | Low | `./gradlew lint` | Future maintenance | Only for Play distribution |
| F57 | termux-background | `set` installs the image before rewriting properties; a failure in the last step leaves the new image with the old properties (benign: same file name) | Low | CLI review | Tech debt | No |

## Stage 33 incremental sync (2026-10-27)

jadis.toolbox standalone scripts (jadis.toolbox `253c386`). Every retained utility now has a stated purpose and
tests (`scripts/README.md`, `tests/test_scripts.py`). Fixed:
- `github_backup` would commit and push in **plaintext** from a cloned-but-locked repository; it now unlocks
  with the exported key or refuses (mutation-tested).
- `timelog` invoice totals silently failed on mawk/busybox.
- Commas corrupted the timelog CSV.
- The timelog invoice path ignored `TMPDIR`.

Nothing was deleted (personal tools; use cannot be ruled out). No capability adapters were added (the scripts
write data).

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F58 | jadis.toolbox | `master_log` writes the home-tree listing, `logcat` and `ps aux` to shared storage by default (readable by apps with storage permission), and pings 8.8.8.8. Documented, and `MASTER_LOG_DIR` added; the default was kept because the widget workflow relies on it | Medium (privacy) | Script audit | Owner decision on the default | No |
| F59 | jadis.toolbox | `newproject` overlaps LRC's repository-creation role and defaults to the MIT licence (the organization's default is proprietary); kept as a personal tool and documented | Low | Script audit | Owner decision | No |

## Stages 34–36 incremental sync (2026-10-27)

BLUX AI pipeline (blux `7bdd076`, `8ef10d5`, `ba160c3`):
- **Stage 34:** the `blux_training` trajectory → dataset pipeline. Its hard gate passed (22 tests).
- **Stage 35:** the Generation 0 harness and its committed, reproducible baseline.
- **Stage 36:** a register of all eight specialist candidates. None is integrated. Capability routing, risk
  and verdict classification are rejected with evidence; the rest are blocked on data.

The Gen 0 policy suite found a real gap: `adb shell recovery --wipe_data` went undetected. It was fixed in
the rule and covered by a regression test.

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F60 | blux | Model-dependent Gen 0 suites (intent, tool selection, repository diagnosis) are BLOCKED: no provider credentials (same cause as F10); the harness has no live model runner yet | High | `evals/reports/gen0/` | Owner action (provider balance) + harness work | Yes: a complete Gen 0 baseline |
| F61 | blux | Engine "task success" is replay determinism against records the same pinned engine produced; it detects regressions, not answer quality. No human-reviewed quality labels exist | Medium | `evals/README.md` | Future evaluation work | No |
| F62 | blux | A second session committed native-router work to `blux/training/` concurrently (a107205…0e4b4f6) and replaced `training/README.md`; the Stage 34 commit had to be rebased (README merged, nothing overwritten). Tooling behind those commits is undeclared (credits UNR-021) | Medium (process) | Rejected push, then rebase | Owner coordination of parallel sessions | No |
| F63 | blux | Native specialists need owner-authored, rights-cleared data: 694 independent routing families (training/research/WAKE_UP_REPORT.md section 39); repair and patch ranking need multi-candidate outcome data that cA does not produce | High | `training/SPECIALISTS.md` | Owner data collection | Yes: Generation 1 |

## Stage 38 incremental sync (2026-10-27)

BLUX App 2.0 (blux-app `6c8e8dd`): local mission control over the real BLUX tools. The hard gate passed: a
real operation recorded in a real BLUX System store is inspected end to end through the app, and the only
controls are read-only BLUX System checks.

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F64 | blux-app | The page was syntax-checked (`node --check`) but not exercised in a browser; there are no UI or accessibility tests yet | Medium | Stage 38 test inventory | Future (UI testing) | Yes: release |
| F65 | blux-gpt (local shells) | BluxGPT 1.0's shell overlay defined a `blux()` function that shadows BLUX's `blux` command. BluxGPT already fixed this (its installer ships `bluxgpt` and runs `unfunction blux`; `docs/AUDIT-1.0.md` item 1, tested), but a stale copy can survive in a user's own startup file and was observed in one. BLUX App resolves tools to absolute paths, so it is unaffected | Low | A `blux` function observed in a local shell profile; `blux-gpt/scripts/install_shell.sh` | Owner action: remove the old function, or re-run BluxGPT's `install_shell.sh` | No |

## TODO / FIXME source audit (2026-10-26)

`git grep -E '\b(TODO|FIXME|XXX|HACK)\b'` over every repository except archived BLHermes, excluding Markdown,
JSON and vendored licences, found 17 hits:

| Classification | Hits | Where |
|---|---|---|
| Genuine unfinished implementation (release blocker) | 6 | Cryptographic verification in void.os (`EntitlementManager`, `IntegrityGate`, `SignatureVerifier`), void.game (`LaunchGate`, `SignatureVerifier`) and void.sys (`SignatureVerifier`): F1, F2, F17 |
| Tool rule definition or test fixture (intentional) | 10 | blux-ca `validator/validators.py` and test; dat `analyzers/quality.py` and three tests; blux-ca-dataset legacy fixture |
| Third-party template content | 1 | blux10k `dotfiles/.p10k.zsh` (powerlevel10k generated config comment) |

One broken relative link remains by design: `dat/snapshot.md` is a historical repository snapshot dated
2026-01-21 that links to `docs/ROADMAP.md`, which was removed in Stage 03.
