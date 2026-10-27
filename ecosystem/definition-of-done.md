# Final repository-by-repository Definition of Done pass (Stage 44, 2026-10-27)

**What was checked.** All 30 active repositories in [the constitution](../constitution/repositories.md), at the
commits in the final matrix. BLHermes (archived) is listed for completeness only.

**The final matrix** is the regenerated [status-matrix.md](status-matrix.md), with each row re-anchored to the commit
verified here and dated 2026-10-27.

**Status rules.** Statuses were not raised by this pass. Release and distribution remain gated by CI (blocked
org-wide, F49), real providers (F10) and hardware. Evidence from Stage 43 ([release-candidate.md](release-candidate.md))
is reused where the repository has not changed since.

## How each item was checked

| Item | How it was checked |
|---|---|
| Tests passing | Each repository's own suite, run on 2026-10-27 (Stage 43 or 44): pytest, unittest, Gradle unit tests with a forced rerun, node tests and shell suites |
| Lint / static | `ruff check` in every Python repository that configures it; mypy (blux); eslint (theresolver); shellcheck (termux-background) |
| Security review | `dat audit` over all 30 repositories, with every critical and high finding triaged by hand (below); `npm audit` for the Node frontends |
| Dependencies | The DAT package analyzer and `npm audit`. Python dependencies of Roughin and Vigyl were pip-audited in Stages 28–29 |
| Stale branding, obsolete upstream hooks | Tracked files searched for the fictional repositories, upstream Hermes/Nous references and "Production/Stable", and every workflow and hook file checked for third-party repository references |
| `.blux` metadata, capability contracts | `blux project` for the 7 repositories with `.blux/` (all valid); `tools/check_contracts.py --workspace` (no breaking change) |
| Machine output, receipts, failure paths, permissions, BLUX integration, AX routing | The Stage 43 runs: integration hard gates with every engine required, the receipt store and its graph, provider failure, VoidForge authorization, and the `ax` router tests with exit 69 |
| Credentials protected | Secret findings triaged (no real secret in any repository); production configuration guards reject development secrets (Roughin, Vigyl, bluxai.app) |
| Build / package artifacts | BLUX wheels built and installed from a clean clone; Android debug APKs built (void.os, void.sys, void.game); theresolver static build; termux-background package suite |
| Compatibility matrix, release ledger | The lock was re-recorded at the final commits (`ecosystem/compatibility.json`). No new tag was made, so the ledger stands |
| Clean tree, committed, pushed | Every repository clean and level with `origin/main` after this stage's commits |

## Per repository

| Repository | Tests (2026-10-27) | Lint / static | Security (DAT, triaged) | Notes |
|---|---|---|---|---|
| blux | 597 passed, 15 skipped, network off; hard gates 45 passed | ruff, mypy clean | pass after triage | F71 fixed (Stage 43); Stage 00 baseline marked historical |
| blux-system | 74 passed | ruff clean | pass after triage | |
| blux-gpt | 49 passed, 1 skipped | ruff clean | pass after triage | |
| blux-coga | 343 passed | ruff clean | pass | |
| blux-ca | 117 passed | ruff clean | pass | |
| dat | 88 passed | ruff clean | pass | |
| lrc | 134 passed | ruff clean | pass after triage | |
| god | 94 passed | ruff clean | pass | |
| blux-app | 11 passed | ruff **fixed** (17 issues), now in CI | pass after triage | |
| blux-ca-dataset | 36 passed, 2 skipped | ruff clean | pass after triage | |
| blux-coga-dataset | 38 passed | ruff clean | pass after triage | |
| axiom | router 12 passed; shell suite and smoke passed | | pass | F72 |
| blux10k | 10 passed | | pass | |
| jadis.toolbox | 75 passed | ruff clean | pass | |
| voidforge | :core 86 and :integration 9 passed | | pass after triage | Public repository (F7, owner) |
| void.os (AXIOM Launcher) | 78 passed; debug APK built | | pass after triage | BLUX optional (boundary test); on-device BLOCKED |
| void.sys | debug APK built; no automated tests | | pass | BLUX-free; on-device BLOCKED |
| void.game (AXIOM Shooter) | 21 passed; debug APK built | | pass | BLUX-free; on-device BLOCKED |
| roughin | backend 91 passed | ruff clean | pass after triage | F36 open (frontend advisories), F73 |
| vigyl | backend 78 passed | ruff clean | pass after triage | No UI yet |
| resolver | 173 passed | | pass | |
| ov-webpages/theresolver | 9 passed; lint and build | eslint: 0 errors, 3 warnings | pass; `npm audit` clean | Custom domain error 1033 (F54) |
| termux-background | unit 10+10 passed; CLI and package suites | shellcheck clean | pass | |
| ov-webpages/bluxai.app | 13 passed with BLUX; 10 passed + 3 skipped without | ruff clean | pass after triage | BLUX-absent fix (below) |
| ov-webpages/operationrestore | static site | | pass | Outside the BLUX path |
| ov-webpages/ivrp | README only | | pass | Outside the BLUX path |
| credits | validate, org-root check, 39 tests | | pass | |
| docs | 13 tests; matrix, constitution and contract checks | | pass | |
| .github, .github-private | links checked | | pass | |

## Security triage

DAT's raw gate fails for 11 repositories. Every critical and high finding was opened and classified. **No real
secret was found anywhere.**

| Class | Where | Why it is not a secret |
|---|---|---|
| Deliberately fake secrets in redaction tests | voidforge (`CoreTest`, `RedactionTest`, redaction corpus, distribution test); blux-system and blux-app tests; blux-gpt (`providers/mock.py`, `tests/conftest.py`); blux training test; dataset tests | Each is a marked fake used to prove scrubbing or rejection |
| Documented placeholder URLs | roughin and vigyl docs and `scripts/backup.sh`; `.env.example`; lrc example spec; blux-ca-dataset seeds and data (`user:password@db.example.com`) | Placeholders, not credentials |
| CI-local service credentials | roughin and vigyl `.github/workflows/ci.yml` (Postgres service at `localhost`) | Only reachable inside the CI job |
| Development defaults | `DEV_SECRET` in vigyl and bluxai.app | Refused by each production configuration check |
| False positive | void.os `components.lock.json` | An icon file hash (`onepassword.png`) |
| Historical | dat `snapshot.md` | Historical document (banner since Stage 30) |

**Follow-up (F76):** commit DAT target policies that suppress these, with justification, so the raw gate passes. Every
suppression is counted in the report. This was not done in this stage.

## Special boundaries

| Boundary | Result | Evidence |
|---|---|---|
| resolver and theresolver remain separate | PASS | No code dependency in either direction. theresolver's optional `check:pricing` reads a resolver checkout in development only |
| Shooter and VOID.SYS remain BLUX-free | PASS | No BLUX reference in their source or build files |
| AXIOM Launcher BLUX remains optional | PASS | `ProductBoundaryTest.launcherCoreDoesNotRequireBlux` passes |
| VoidForge remains standalone and restricted to authorized Org Members | Standalone PASS · restriction **BLOCKED** | `:core` has no dependency on any client (tested). The repository is still public (F7): the owner must make it private |
| BLHermes is no longer an active dependency | PASS | Decoupling tests pass; BLUX builds, tests and runs from a clean clone without it (Stage 43) |
| blux-web is retired | PASS (never existed) | Re-verified absent in Stage 39 |
| ivrp and operationrestore stay outside the BLUX critical path | PASS | No BLUX code or calls; the only mention is the contact address |

## Fixed in this stage

- **bluxai.app (`9e5706a`).** Without `blux-system` on the server, creating an organization committed the org and
  then answered 500, so a retry hit 409. The BLUX System store is now created on first use, and a missing BLUX
  answers 503 with a clear message. Accounts, organizations, roles, tokens and audit keep working. A regression
  test runs without BLUX and fails on the old code.
- **blux-app (`0de2d9a`).** 17 ruff issues fixed; CI now runs `ruff check .`.
- **blux (`51134af`).** The Stage 00 baseline under `docs/ecosystem/` carries a dated historical banner and a README.

## Not met, with next steps

| Item | Why | Next step |
|---|---|---|
| CI green on the release commit | Billing lock (F49) | The owner clears the lock, then re-runs every workflow |
| Real-provider paths | Provider accounts without balance (F10) | Fund a provider; `BLUX_REAL_MODELS=1` integration tests |
| On-device behaviour (launcher, VOID.SYS, Shooter, VoidForge, Termux Background) | No hardware here | Each repository's `docs/device-testing.md` |
| VoidForge members-only | Public repository (F7) | The owner makes it private |
| DAT raw gate | Test fixtures are flagged | DAT target policies with justified suppressions |
| Roughin frontend advisories | Major upgrades needed (F36) | Upgrade to vite 8 and react-router 7, then add frontend tests (F37) |
