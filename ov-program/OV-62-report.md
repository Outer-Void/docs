# OV-62: adversarial and fault-injection drills (2026-11-09)

**State: PASSED.** The exit asks for no unauthorized change, no false success and no hidden data loss under
attack and faults. The drills found six defects: two unauthorized changes, one false success and three
failures that were hidden although no data was lost:

| Kind | Defect | Finding |
|---|---|---|
| Unauthorized change | `shell.exec` ran escapes outside the workspace without approval | F95 |
| Unauthorized change | a race let `fs.write` follow a symlink swapped in after its check | F136 |
| False success | DAT passed its gate over a file it could not read | F134 |
| Hidden failure, no data lost | BLUX System died without a document on a full disk | F135 |
| Hidden failure, no data lost | LRC did the same during `scaffold` | F137 |
| Hidden failure, no data lost | the OV-61 receipt-store preflight blocked on damage the next write repairs | F138 |

Each is fixed, with a test that fails on the previous commit, and every drill now holds. Not drilled here:
- physical devices (D-03);
- PostgreSQL, Stripe and R2 (D-05; `BLOCKED_LOCAL_ENVIRONMENT`);
- real providers (D-02).

Their earlier mock-level evidence is listed under "Reused".

| Repository | Before | After |
|---|---|---|
| blux | `5995419` | `b56d06c` |
| dat | `57c8099` | `24a7290` (owner bypass: protected `main`) |
| lrc | `ea82afc` | `3765215` (owner bypass: protected `main`) |
| blux-system | `26f2240` | `9392449` |

## Owner decisions (2026-11-09)

- **F95:** every `shell.exec` command needs the person's approval of that exact command (or YOLO, which only
  the person can switch on for a session). This holds until an OS sandbox exists; none works on Android/PRoot.
- **F103:** LRC reports stale `.lrc-stage-*` directories and never deletes them.

## Drills

All drills ran against the OV-61 pin set from fresh clones, unless the line says otherwise.

| # | Drill | Before | After |
|---|---|---|---|
| 1 | `shell.exec`, no approvals, 9 escape attempts | 5 took effect outside the workspace: `echo x > ../f`, an absolute path, shell variables, an obfuscated `rm -r` of an outside folder, a home dotfile | every command is refused without a one-time approval or YOLO; a session approval of a rule no longer opens the shell; an outside `cwd` is refused first (F95) |
| 2 | `fs.read`/`fs.write` through symlinks, `..`, absolute and dangling links (8 calls) | all refused, nothing outside changed | unchanged |
| 3 | A separate process swaps a workspace directory for a symlink to outside while `fs.write` runs | 1 file written outside in 584 tries, reported as success | every path component is opened with `O_NOFOLLOW` relative to its checked parent: 0 in 621; a deterministic test swaps right after the check (F136) |
| 4 | DAT audit of a repository with an unreadable file holding a secret, `--fail-on critical` | gate **pass**, exit 0; the file appears only in `target.skipped` | `TARGET_UNREADABLE`, outcome `incomplete`, exit 3 (F134) |
| 5 | `blux-system ingest` under a file-size limit (disk-full stand-in), as an error and as a kill | exit 1 with a traceback and nothing on stdout; the store keeps a torn tail, repaired by the next ingest | `STORE_IO_ERROR` document (`EFBIG`); `SIGXFSZ` ignored so a limit never kills it silently; BLUX treats the code as retryable and spools the receipt (F135) |
| 6 | Receipt-store preflight (F114) right after drill 5 | `verify` reports `torn_tail`, so a destructive capability would have been refused although the next write repairs it | a torn tail alone passes; other damage still blocks (F138) |
| 7 | `lrc create` under a size limit | exit 3, no target, no leftovers | unchanged |
| 8 | `lrc scaffold` under a size limit | exit 1 with an `OSError` traceback even with `--json`; files unchanged; the next scaffold works | `IO_ERROR` document (F137) |
| 9 | `lrc create` killed while staging (F103) | a `.lrc-stage-*` directory is left, silently | `create` and `recover` report it as `STALE_STAGE_DIRECTORY` with the removal command |
| 10 | `ca modify` under a size limit | `APPLY_FAILED`, exit 3, workspace unchanged, `status` and `recover` clean | unchanged |
| 11 | Destructive capability against a damaged store (from OV-61) | stopped before acting | unchanged |

## Reused (rule 11)

| Area | Evidence |
|---|---|
| BLUX System crash and tamper | OV-52: crash at every byte, edited, cut or reordered logs, retention and import interruption (`test_evidence_authority.py`) |
| Receipts under outage and refusal | OV-52: spool, set aside, flush races, agent fails closed (`test_receipt_durability.py`, `test_agent_cmd.py`) |
| LRC and cA interruption | OV-51: killed `migrate`/`scaffold` recover; cA committed-change recovery (`test_interrupted.py`, `test_interrupted_commit.py`) |
| Hostile project metadata | `.blux/` hostile inputs (blux `test_dot_blux_hostile.py`); GOD hostile input (`test_hostile_input.py`) |
| Policy and hooks | hooks cannot turn a deny into an allow; device commands need a one-time approval even under YOLO (`test_core_migration.py`, `test_runtime_hooks.py`) |
| Payments | Roughin and Vigyl webhook replay and forgery (OV-55/56), Resolver charged-but-failed payments (F125, OV-57), mock level only (D-05, D-07) |
| Devices | VoidForge write barrier and confirmation broker (OV-59, JVM tests; D-03) |
| Termux Background | `set` rolls back a failed image change (F57, OV-59) |

## Evidence (executed 2026-11-09)

| Check | Result |
|---|---|
| Old-code check | new tests fail on the previous commits: blux 6 (`test_tool_hardening.py`, `test_receipt_preflight.py`), DAT 1, LRC 2, blux-system 1; DAT's size-limit test passes on both (it guards the documented skip) |
| Suites | DAT 91, LRC 140 (1 skipped), blux-system 104 passed; blux 663 passed with every `BLUX_REQUIRE_*` set; its 3 Termux package tests at first failed because the installed-package check expected `echo hi` to run unapproved; the check now approves the command once, and the 4 package tests pass; ruff, format and mypy clean in all four |
| Integration matrix | pins bumped for dat, lrc and blux-system; fresh-clone rerun: blux 662 passed, 19 skipped, 0 failed at pin set `b56d06c`; BLUX off reruns DAT 89, LRC 138, BLUX System 104 passed; `ax` routes and its 14+14 tests pass with the new engines (`ecosystem/integration-matrix.md`) |
| Contracts | `check_contracts.py`: ok, 0 breaking, 0 invariant failures; lock rewritten |
| DAT gate | before commit only `release.dirty-worktree` (run with the fixed DAT); after commit exit 0 |

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F95 | blux | RESOLVED_VERIFIED | every shell command needs approval (owner decision) |
| F103 | lrc | RESOLVED_VERIFIED | stale stage directories reported (owner decision) |
| F134 | dat | RESOLVED_VERIFIED | unreadable file no longer passes the gate |
| F135 | blux-system | RESOLVED_VERIFIED | I/O failure is a `STORE_IO_ERROR` document |
| F136 | blux | RESOLVED_VERIFIED | `fs.read`/`fs.write` check-then-use race |
| F137 | lrc | RESOLVED_VERIFIED | `scaffold` I/O failure is an `IO_ERROR` document |
| F138 | blux | RESOLVED_VERIFIED | preflight tolerates a torn tail alone |

## Stage output

```yaml
stage_id: OV-62
implementation:
  changes: [per-command shell approval, O_NOFOLLOW component walk for file tools, DAT unreadable target,
            STORE_IO_ERROR, LRC IO_ERROR and stale-stage report, preflight torn-tail tolerance, pin bump]
  excluded: [devices (D-03), PostgreSQL/Stripe/R2 (D-05), real providers (D-02)]
validation:
  drills: [11 drills; before and after recorded]
  regression: [new tests fail on the previous commits]
  integration: [fresh-clone matrix rerun at the new pins]
disposition: {state: PASSED, blockers: [], next_actions: [OV-63 needs authorization]}
```
