# OV-50: BLUX runtime and model routing (2026-11-07)

**State: PASSED for its exit (deterministic and mock suites), with provider claims BLOCKED until OV-64.** The delta
review found and reproduced five defects in the tool layer and the agent, all fixed in blux `4163637` with tests that
fail on the previous commit. One residual risk is recorded rather than fixed: `shell.exec` is not an OS sandbox
(F95). No real provider was called; the receipt-durability defects F83–F85 stay with OV-52.

## Delta review (rule 11)

The review started from blux `56c9b76` (OV-49). The runtime had not changed since `51134af` (Stage 44).
- **Re-run first.** The full suite at `56c9b76`: 597 passed, 15 skipped (2 real-provider paths, 12 that need the
  BLHermes interpreter, 1 because the fork moved past the inventoried commit). Same counts as Stage 44.
- **Read in full:** approvals, command detection, path confinement, child environment, the built-in tools, the
  executor (timeouts, hook guards, receipts), the model router, the subprocess backend, `model.generate`, the
  hook catalogue and bus rules, the agent loop and `blux agent`, and `blux doctor`.
- **Probed** with a scratch script against a fictional workspace and with the CLI in an empty environment (no
  config, no provider keys).

| Area | Result at `56c9b76` |
|---|---|
| Tool approvals | Session, one-time and YOLO semantics match the BLHermes goldens; device rules are never covered by a session approval or YOLO. **Gap:** shell commands reached credential and start-up files that the file tools refuse or gate (F89) |
| Path confinement | `fs.*` resolve symlinks and refuse paths outside the workspace. **Gap:** `fs.write` could plant `.git/hooks/*` and change `.git/config` or `.blux/` (F90) |
| Timeouts | The executor uses the smaller of request and descriptor timeouts; hooks can only shorten them; a hung command is killed at its deadline. **Gaps:** output was buffered in full before it was cut (F91); cancellation was ignored (F92) |
| Structured output | The router validates JSON output against the requested schema and tool-call arguments against declared tools; a violation moves to the next route. Sound (existing tests) |
| Fallback | Explicit, recorded attempt by attempt, `degraded` when not the primary route; refusals (`CONTENT_FILTERED`) are never routed around; fallback can be disabled. Sound |
| Offline and no-model use | Deterministic capabilities run with no model (`blux run echo.test`, exit 0). `blux ask` with no keys lists every route, hints `blux doctor` and exits 3. **Gap:** `blux agent` printed only `EXECUTION_FAILED` and exited 1 (F93) |
| Hooks | Hooks can observe, veto and narrow but never allow; a vetoable event fails closed when emission breaks. Sound (existing tests; 21 bus tests, 10 runtime-hook tests) |

## Changes (blux `4163637`)

- **Shell matches the file tools (F89).** Two new command rules, ordinary approvals rather than device rules:
  - `credential.path`: any mention of a file `fs.read` refuses. The pattern is built from `paths.DENY_HOME`, so
    the two lists cannot drift apart.
  - `autorun.write`: a redirect, `tee`, `cp`/`mv`/`ln`/`install`/`rsync` target or `sed -i` on a shell start-up
    file, `~/.local/bin`, a git hook, `.git/config` or `.blux/`. Reading those files stays unrestricted.
  - None of the BLHermes approval goldens change; 15 everyday commands stay safe (for example `cat ~/.bashrc`,
    `grep url .git/config`, `echo x > my.profile`).
- **Workspace writes (F90).** `fs.write` into `.git/` or `.blux/` anywhere in the workspace needs an approval.
  `.gitignore` and `.github/` are unaffected.
- **Bounded output (F91).** Each stream is drained on its own thread and only 64 KiB is kept. The probe that
  produced 400 MB used about 765 MB of memory before and about 1 MB now.
- **Cancellation (F92).** A cancelled `shell.exec` kills the command's process group and fails with reason
  `cancelled`; the probe returned in 0.5 s instead of running for 6 s and reporting success.
- **No-model agent (F93).** `blux agent` reports a failed model call as `blux ask` does (routes, hints,
  receipt) and uses the same exit codes: 3 configuration, 4 timeout, 130 cancelled, 1 otherwise.
- **Docs:** ADR-0013 (stricter-than-BLHermes list, and that detection is not a sandbox) and the changelog.

## Evidence (executed 2026-11-06 and 2026-11-07)

| Check | Result |
|---|---|
| New tests on the old code | `tests/runtime/test_tool_hardening.py` and the new agent test: 6 fail on `56c9b76`; the 7th (output order and exit codes) passes on both, as intended |
| Full suite at `4163637` | 604 passed, 15 skipped (597 before plus 7 new; skips: 2 real-provider paths, 12 need the BLHermes interpreter, 1 fork moved), exit 0 |
| Hard gates | Included in the full suite: every engine was installed, so the integration tests ran (no integration skips apart from the 2 real-provider paths) |
| Probes after the fix | 5/5 credential and start-up commands need approval; git hook and `.git/config` writes need approval; cancel 0.5 s; output memory +1 MB |
| `ruff` (runtime, cli, sdk, tests) and `mypy` | clean |
| `ruff` on the whole repository | fails in `training/dataset-program/` only, unchanged from `56c9b76` (F94, OV-53) |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 |
| Real providers | **not run**: BLOCKED until OV-64 (D-02). The 2 real-provider tests skip |

A first full run reported one failure: the fork-decoupling guard rejected a literal legacy path in the new command
rule. Building the rule from `paths.DENY_HOME` fixed it without adding an allow-list exception. That run also
overlapped a brief `git stash` of the working tree, so it was discarded and the suite was run again from the
start.

## Findings

| ID | Severity | State | Note |
|---|---|---|---|
| F89 | High | RESOLVED_VERIFIED | shell reached what the file tools refuse |
| F90 | Medium | RESOLVED_VERIFIED | git hooks and `.blux/` writable without approval |
| F91 | Medium | RESOLVED_VERIFIED | unbounded output buffering |
| F92 | Medium | RESOLVED_VERIFIED | cancellation ignored |
| F93 | Low | RESOLVED_VERIFIED | agent hid why the model failed |
| F94 | Low | OPEN (OV-53) | `make lint` fails in `training/dataset-program/` |
| F95 | Medium | DEFERRED (OV-62) | `shell.exec` is not an OS sandbox; a process that leaves the group survives |
| F83–F85 | | OPEN (OV-52) | receipt durability; unchanged by this stage |

## Stage output

```yaml
stage_id: OV-50
implementation:
  changes: [credential.path and autorun.write command rules, .git/.blux write approval, bounded shell output,
            shell cancellation, agent no-model reporting]
  excluded: [receipt durability F83-F85 (OV-52), OS sandbox for shell.exec (F95, OV-62), real providers (OV-64)]
validation:
  unit_and_integration: [604 passed, 15 skipped at 4163637]
  regression: [6 new tests fail on 56c9b76 and pass on 4163637]
  security: [ruff and mypy clean on changed code, DAT gate exit 0]
  external: [real providers BLOCKED (D-02), CI EXTERNAL_BLOCKED (D-01)]
disposition: {state: PASSED, blockers: [], next_actions: [OV-51 engine reliability, then OV-52 receipt durability]}
```
