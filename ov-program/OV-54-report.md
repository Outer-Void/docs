# OV-54: `ax`, blux10k, JADIS Toolbox, BLUX App, bluxai.app (2026-11-07 to 2026-11-08)

**State: PASSED for its exit (clean install, exit 69, tenant isolation, no second runtime).** The delta review
found one serious defect: `ax` could not work from any clean clone, because `cockpit/bin/ax-route` had never
been committed (F120). It is fixed and verified from a fresh GitHub clone. The rest of the stage:
- implemented the owner's two decisions on JADIS Toolbox defaults (F58, F59);
- ran BLUX App's first browser accessibility pass and fixed what it found (F64, F123);
- fixed a broken `newproject` Node template (F122) and an `ax` crash on broken overrides (F121);
- re-verified bluxai.app's tenant boundary (no defect found).

bluxai.app deployment stays an owner decision (D-08, F66 DEFERRED). No real provider was called.

| Repository | Before | After |
|---|---|---|
| axiom (`ax`) | `ed079e8` | `1272d75` |
| blux10k | `e2e9f58` | `e2e9f58` (no change) |
| jadis.toolbox | `253c386` | `e3f25a5` |
| blux-app | `dca88bf` | `4bdb899` |
| ov-webpages/bluxai.app | `e894ac6` | `32e988d` |

## Delta review (rule 11)

None of the five components had changed since OV-48/OV-49. Their last verified results came from working
checkouts. This stage added clean-install checks, which is how F120 surfaced.

| Exit item | Result |
|---|---|
| Clean install | blux10k: `bootstrap --apply` into a scratch HOME links all 5 dotfiles and backs up an existing `.bashrc`; probes leave HOME untouched. JADIS Toolbox, BLUX App, bluxai.app: `pip install` into fresh venvs, entry points and packaged data work. **`ax`: failed on a clean clone (F120)**; after the fix a fresh GitHub clone routes correctly |
| Exit 69 | All 12 routes exit 69 with a clear message when their engine is missing. Engine arguments and exit codes pass through unchanged. **Gap (F121):** an override pointing at a directory or an unstartable file crashed |
| Tenant isolation | bluxai.app: membership on every org route (non-members get 404); per-org BLUX System stores; read-only, org-bound API tokens. New probes all held: another org cannot revoke a token; an operation id asked of another org's store reveals nothing; `alg=none`, wrong-key and refresh tokens get 401; a deactivated user gets 401. Remote runs cannot reach server files, because `blux run` exposes only `echo.test` and `model.*` (`fs.read` gives UNKNOWN_CAPABILITY) |
| No second runtime | bluxai.app imports no BLUX package (test). BLUX App imports only BLUX's redaction function. `ax` imports no engine and execs the engine (test). JADIS Toolbox and blux10k call tools by command |

## Changes

- **axiom (F120, F121):**
  - `.gitignore` re-includes `cockpit/bin/`, and `ax-route` is committed.
  - An `AX_BIN_*` override pointing at a directory is "not installed" (exit 69).
  - An engine that exists but can't be started exits 126 with a message.
- **JADIS Toolbox, owner decisions of 2026-11-07:**
  - **F58:** `master_log` writes to owner-only `~/.local/state/jadis/master_log/logs`. Shared storage needs
    `MASTER_LOG_DIR`, and the 8.8.8.8 ping needs `MASTER_LOG_PING=1`.
  - **F59:** `newproject` defaults to a proprietary licence, with the holder from `DEFAULT_COPYRIGHT_HOLDER`. MIT
    and the others are available with `-l`, an unknown licence is refused, and the docs point to LRC for
    organization repositories.
  - **F122:** the Node template is written with `printf` and JSON escaping instead of `eval`, and the MIT
    licence names its holder.
- **BLUX App (F64, F123):** new `scripts/a11y-pass.mjs`, which needs Playwright and axe-core installed outside
  the package. Fixes:
  - light-scheme colours now meet 4.5:1 contrast;
  - a `:focus-visible` outline;
  - wide tables scroll in a labelled, keyboard-focusable region;
  - long ids wrap.

  `tests/test_ui_accessibility.py` guards these without a browser.
- **bluxai.app:** a tenant-boundary regression test.
- **Docs:** toolbox `scripts/README.md`, `master_log` and `newproject` READMEs; BLUX App README; bluxai.app
  README; the `ax` router docstring.

## Evidence (executed 2026-11-07 and 2026-11-08)

| Check | Result |
|---|---|
| New tests on the old code | `ax` override test fails on `ed079e8` (traceback); toolbox: 3 new behaviour tests fail on `253c386`, and the opt-in test passes on both, as intended; BLUX App: 3 of 3 fail on `dca88bf`. bluxai.app's new test records probes that already held |
| Fresh GitHub clone of axiom | before: `ax audit` exit 127 and 9 router tests failed; after (`1272d75`): `ax audit` exit 69, 11 passed and 3 skipped (the skips need the sibling VoidForge checkout) |
| axiom (working checkout) | router 14 passed; `tests/run_tests.sh` 14/14; `cockpit/tests/smoke.sh` passed; run with a scratch HOME (the owner's shell files untouched) |
| blux10k | 10 passed; `detect`, `inventory`, `check`, `verify`, `report`, `doctor`, `bootstrap` leave HOME unchanged |
| JADIS Toolbox | 79 passed; `ruff check`, `ruff format --check` and `mypy` clean (the test file was reformatted; it already failed the documented gate) |
| BLUX App | 14 passed; `ruff check .` (the CI gate) clean; browser pass: 44 states (9 views, operation, verify result × light/dark × 1280/320 px), 0 axe violations, focus visible on all controls, no 320 px reflow, targets ≥ 24 px; the store had the same 3 records before and after |
| bluxai.app | 14 passed with BLUX; 10 passed and 4 skipped without (the 503 path); `ruff check` clean |
| DAT gate | before each commit only `release.dirty-worktree`; after each commit exit 0 (4 repositories) |
| Pushes | fast-forward to `main`; none of these repositories has branch rules |

**Disclosures:**
- BLUX App's `ruff format --check` reports unformatted files that already existed, which I left alone;
  formatting is not that repository's gate.
- In this shell, `blux` resolves to the stale `blux()` function in the owner's `~/.zshrc.local` (D-12, F65).
  I used the venv's executable by full path and changed nothing in the shell files.
- With `blux-system` off PATH, `blux run` queued its receipts in the outbox, and `blux receipts flush`
  recorded them (OV-52 behaviour seen working).

## Findings

| ID | Repository | Severity | State | Note |
|---|---|---|---|---|
| F120 | axiom | High | RESOLVED_VERIFIED | `ax-route` never committed; `ax` failed on clean clones |
| F121 | axiom | Low | RESOLVED_VERIFIED | broken overrides crashed |
| F122 | jadis.toolbox | Medium | RESOLVED_VERIFIED | `newproject -t node` aborted; empty MIT holder |
| F123 | blux-app | Medium | RESOLVED_VERIFIED | contrast, focus, keyboard scroll, reflow |
| F58 | jadis.toolbox | Medium | RESOLVED_VERIFIED | owner decision implemented: private, offline default |
| F59 | jadis.toolbox | Low | RESOLVED_VERIFIED | owner decision implemented: proprietary default |
| F64 | blux-app | Medium | RESOLVED_VERIFIED | browser and accessibility tests exist and pass |
| F124 | blux10k | Low | OPEN | `verify` exits 0 with every dotfile missing |
| F66 | bluxai.app | Medium | DEFERRED (D-08) | not deployed; no web front end |

**Lesson carried forward (F120):** release evidence must come from clean clones. A working checkout can hold
files git never saw. OV-63 (release machinery) should build and test from fresh clones.

## Stage output

```yaml
stage_id: OV-54
implementation:
  changes: [ax-route committed and override handling, master_log private default, newproject proprietary default
            and node template fix, BLUX App accessibility pass and fixes, bluxai.app tenant-boundary test]
  excluded: [bluxai.app deployment and front end (D-08), blux10k verify semantics (F124), screen-reader and device
             checks]
validation:
  clean_install: [axiom from a fresh GitHub clone, blux10k bootstrap into scratch HOME, pip installs of jadis-toolbox,
                  blux-app, bluxai.app into fresh venvs]
  exit_69: [12 of 12 routes; overrides 69 or 126]
  tenant_isolation: [bluxai.app 14 passed incl. new boundary test; no defect]
  no_second_runtime: [import checks in bluxai.app, blux-app, ax]
  security: [DAT gate exit 0 in 4 repositories]
disposition: {state: PASSED, blockers: [], deferred: [D-08], next_actions: [OV-57+ need authorization]}
```
