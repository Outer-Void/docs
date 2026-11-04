# OV-48: CI, builds, reproducibility (2026-11-04)

**State: BLOCKED for hosted CI and PostgreSQL; local verification done.**
- **Hosted CI.** It cannot start: EXTERNAL_BLOCKED, D-01.
- **PostgreSQL.** It cannot run here: BLOCKED_LOCAL_ENVIRONMENT.
- **Local work.** Everything that can run locally ran: the affected suites, the builds, the workflow audit and the
  environment record. Nothing blocked is reported as green.

## 1. Hosted CI (F49)

The check used the latest CI workflow run of every repository, read from the GitHub API. **No job was triggered.**
Runs started by this stage's own pushes are included.

| Result | Repositories |
|---|---|
| Failed before start: *"The job was not started because your account is locked due to a billing issue."* | 18: blux, blux-system, blux-gpt, blux-coga, blux-ca, dat, lrc, god, blux-app, blux-ca-dataset, blux-coga-dataset, jadis.toolbox, voidforge, void.os, void.game, termux-background, credits, docs |
| `startup_failure`, 0 jobs, no annotation | 5 private: vigyl, roughin, void.sys, resolver, theresolver |
| Passing CI run at current HEAD | **none** |

Notes:
- **The private repositories.** All 26 workflow files parse (section 3), so their `startup_failure` is not a broken
  workflow file. It is consistent with the account lock; GitHub gives no annotation to prove it.
  - void.sys is the clearest case. Its workflow is unchanged since 2026-10-26, when it failed with the billing
    annotation while the repository was still public.
- **blux-gpt.** Its green run at `4609cd9` is GitHub's dependency-graph job (`dynamic/dependabot/update-graph`), not
  CI. Its CI run at that commit has the billing annotation.
- **Disposition.** F49 and F70 stay EXTERNAL_BLOCKED (D-01). Release gates cannot be promoted, and local runs remain
  supplementary evidence.

## 2. PostgreSQL (F34, F45)

| Item | State |
|---|---|
| Roughin and Vigyl migration, backup and restore round-trips | **BLOCKED_LOCAL_ENVIRONMENT.** PostgreSQL 17 `initdb` stalled for over an hour under PRoot (forward run, 2026-10-27). It was not retried, per the owner's decision |
| Leftover processes from that attempt | None running (`ps`, 2026-11-04) |
| Acceptance path | The CI `postgres` jobs in both repositories, or the same commands on a suitable external machine |
| Substitutes | None accepted. SQLite and mocked PostgreSQL results are not PostgreSQL qualification |

## 3. Workflow audit (`tools/audit_workflows.py`, `inventory/workflow-audit.json`)

Every file is read at a recorded commit with `git show`. `--check` re-reads those commits and compares.

| Check | Result |
|---|---|
| Repositories with workflows / files | 23 / 26 |
| YAML parses | 26/26 |
| `permissions` declared (workflow or every job) | 24/26. **Missing:** void.os `android-ci.yml`, resolver `ci.yml` |
| `write-all`, `pull_request_target`, untrusted `github.event.*` text in `run:` | 0 / 0 / 0 |
| Actions pinned to a commit SHA | 0/26 files. All use tags (10 distinct: checkout@v4, setup-python@v5, setup-node@v4, setup-java@v4, upload- and download-artifact@v4, setup-android@v3, setup-gradle@v4, android-emulator-runner@v2, action-gh-release@v2) |
| Runners | `ubuntu-latest` in 17 files (moving to Ubuntu 26), `ubuntu-24.04` in 6, `matrix.os` in 1 (god) |
| Secrets referenced (names only) | GPG signing (dat, lrc release); the VoidForge members signing set; the termux-background keystore set |

**F80, the hardening backlog, is recorded but not applied.** The locked plan defers changes that only hosted CI can
validate. SHA pinning, least-privilege `permissions` and pinned runner images go in together with the first CI run
after D-01, so that run verifies them.

## 4. Fresh local runs (current HEAD, 2026-11-04)

These are the suites affected by post-freeze commits, run once and used for both the OV-47 dispositions and this
stage.

| Repository @ tested commit | Suite | Result |
|---|---|---|
| axiom @ ed079e8 | unittest (all) | 13 passed |
| blux10k @ e2e9f58 | unittest; `zsh -n`; `--version` | 10 passed; clean; 3.0.0 |
| blux @ 8d989de | `training/dataset-program` unittest | 3 passed |
| blux-system @ 77173f2 | pytest | 74 passed |
| resolver @ aae88c2 | unittest | 173 passed |
| roughin @ a4410a1 | backend pytest | 93 passed (938 deprecation warnings, F39) |
| roughin @ a4410a1 | frontend `npm ci`, `npm test`, `npm run build`, `npm audit` | 4 passed; built (PWA worker); **audit exit 1**: 6 advisories (F78) |
| vigyl @ f7ce8f3 | frontend `npm ci`, `npm test`, `npm run build`, `npm audit --omit=optional` | 8 passed; built; 0 vulnerabilities |

**Current-HEAD governance gates.** All pass:
- docs `build_status_matrix --check`, `build_constitution --check`, `build_inventory --check`,
  `export_reassessment --check` (9/9), `build_findings_current --check`, `audit_workflows --check`, and the 13
  contract mutation tests;
- credits `validate`, `--org-root` and 39 tests.

**Reused with their original date and commit, not re-run.** Their repositories have not changed since:

| Evidence | Date | Commit |
|---|---|---|
| blux runtime: 597 unit and integration, 45 hard gates | 2026-10-27 | 51134af |
| blux-gpt 49 (+1 skipped); CogA 343; cA 117; DAT 88; LRC 134; GOD 94; BLUX App 11; datasets 36 and 38; JADIS Toolbox 75 | 2026-10-27 | Stage 44 anchors in `ecosystem/status-matrix.json` |
| VoidForge :core 86 and :integration 9; void.os unit 78 with debug APK; void.game core 21 with APK; void.sys APK | 2026-10-26 / 27 | 59b6d67, 24b07cd, b56c1ae, 09cf56f. void.sys's later commit 3f2b7aa changes only its README |
| termux-background unit, CLI and package suites; theresolver lint, build and 9 tests; bluxai.app 13 | 2026-10-27 | 75cfb97, 49dbeff, 9e5706a |
| Vigyl backend: 78 passed | 2026-10-27 | a0816a4. Backend unchanged since; f7ce8f3 and ee34852 touch only the frontend, CI and README |

The Gradle suites were not re-run: no Android source changed since their anchors.

## 5. Environment (reproducibility record)

| Item | Version |
|---|---|
| OS | Debian GNU/Linux 13 (trixie) under PRoot-Distro on Android, kernel 6.17.0, aarch64 |
| Python | 3.13.5 (system and venvs); pytest 9.1.1 |
| Node / npm | v20.19.2 / 11.21.1. CI declares Node 22, so local results are on 20 |
| Java | OpenJDK 21.0.12.1 |
| git / gh / zsh / bash | 2.47.3 / 2.46.0 / 5.9 / 5.2.37 |

## 6. D-12: owner shell configuration (diagnosis only; nothing edited)

| File | Lines | What is there | Effect | Recommended correction |
|---|---|---|---|---|
| `~/.zshrc.local` | 16–44 | The `### >>> BLUXGPT OVERLAY >>>` block from BluxGPT 1.0 (`BLUXGPT_VERSION="1.0.0"`), defining `blux()` at line 22 | An interactive zsh resolves `blux` to that function (`whence -w blux` → `function`), so the BLUX CLI is shadowed (F65) | Run `~/ov/blux-gpt/scripts/install_shell.sh`, which replaces exactly that marker block with the current overlay (it ships `bluxgpt`, not `blux`). Or delete lines 16–44. Then `exec zsh` and confirm `whence -w blux` reports `command` |
| `~/.zshrc` | 163–164 | `export ANDROID_HOME=/opt/android-sdk` and `export ANDROID_SDK_ROOT=/opt/android-sdk` | `/opt/android-sdk` does not exist, so Gradle and adb lookups by name fail | Set both to `$HOME/android-sdk`, which exists and contains `platform-tools` |

## 7. Status matrix

`tools/build_status_matrix.py` has an OV-48 overlay, which:
- re-anchors the seven re-run rows to their tested commits with `last_verified` 2026-11-04;
- corrects the Resolver version (4.0.0) and the Vigyl version (frontend 0.1.0 preview) from the manifests;
- adds the F77, F78 and F79 blockers.

**No status is raised.**

## Stage output

```yaml
stage_id: OV-48
validation:
  unit: [axiom 13, blux10k 10, dataset-program 3, blux-system 74, resolver 173, roughin 93+4, vigyl 8]
  build: [roughin frontend, vigyl frontend]
  security: [workflow audit: 0 critical constructs; F80 backlog]
  external: [hosted CI EXTERNAL_BLOCKED (D-01)]
  integration: [PostgreSQL BLOCKED_LOCAL_ENVIRONMENT (F34, F45)]
  hardware: [not applicable this stage]
disposition:
  state: BLOCKED (hosted CI, PostgreSQL); local verification done
  blockers: [D-01, PostgreSQL host]
  next_actions: [OV-49; apply F80 with the first CI run after D-01; owner applies D-12]
```
