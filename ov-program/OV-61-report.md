# OV-61: versioned cross-repository integration (2026-11-09)

**State: PASSED.** The exit asks for an integration matrix at pinned commits and for BLUX off to still work.
Both are recorded in [`ecosystem/integration-matrix.md`](../ecosystem/integration-matrix.md):
- every BLUX boundary ran from fresh clones at one pin set, with missing targets treated as errors;
- every engine, and `ax`, ran without the BLUX runtime.

Not covered, by decision:
- the real-provider paths (D-02);
- VoidForge on a device (D-03);
- hosted CI (D-01).

| Repository | Before | After |
|---|---|---|
| blux | `60ddc76` | `5995419` |
| docs | `7a06090` | this commit |
| engines (blux-system, dat, lrc, god, blux-coga, blux-ca, blux-gpt, jadis.toolbox, axiom) | unchanged | pinned as they are |

## Owner decisions (2026-11-09)

- **F114:** external and destructive capabilities check the receipt store before they act.
- **F96:** LRC recovery stays a CLI command (`lrc recover`). No `repo.recover` capability; no contract change.

## Delta review (rule 11)

| Item | Result |
|---|---|
| Stage 42 contract checks | Reused. `check_contracts.py --workspace ~/ov` still passes: no invariant failure, no breaking change, only commit moves (INFO). The lock in `ecosystem/compatibility.json` now holds the current commits |
| Integration tests in blux | They existed, but they skip silently when a target is missing. blux's CI pinned engine commits from Stages 02–09, 2 to 5 commits behind each engine and before the OV-51/52 fixes; it also installed BluxGPT at one commit and checked out another (F133) |
| Engines' own boundary tests | DAT, LRC, CogA, cA and GOD already assert that they never import the BLUX runtime. They were rerun here without it |
| F114, F96 | Decided by the owner (above) |

## Changes (blux `5995419`)

- **Store preflight (F114):**
  - Before an `external` or `destructive` capability acts, `BluxSystemSink.preflight()` runs `blux-system verify`.
  - A damaged store, or a refusal-class error, stops the run with `EXECUTION_FAILED`
    (`details.reason = receipt_store_preflight`); nothing runs.
  - An unavailable store still lets the capability run, and its receipt is spooled as before.
  - `read` and `write` capabilities keep the OV-52 behaviour.
- **One pin set (F133):**
  - `integrations/targets.lock.json` pins BLUX System, DAT, LRC, GOD, CogA, cA and BluxGPT.
  - `tools/integration_targets.py` installs, checks out and requires exactly those commits. Its `env` output sets
    every `BLUX_REQUIRE_*` flag, so a missing target fails instead of skipping.
  - CI now uses the tool. `integration_targets.py check` fails if a commit is hard-coded again.
- **Docs:** the integrations README (the store situations, the SDK pin blux-system really uses, the lock) and
  the CHANGELOG.

## Evidence (executed 2026-11-09)

| Check | Result |
|---|---|
| New tests | `test_receipt_preflight.py` 8 (one against a real `blux-system` store damaged on disk): 4 fail on `60ddc76`, the 4 "still runs" cases pass there too. `test_integration_targets.py` 4: the check fails on the old `ci.yml` |
| blux, dev environment | 660 passed, 15 skipped with every `BLUX_REQUIRE_*` set (skips: real-provider paths, D-02; BLHermes characterization) |
| BLUX on, fresh clones | 656 passed, 19 skipped, 0 failed (26 min). Boundaries: BLUX System 23, DAT 5, LRC 6, GOD 3, CogA 4, cA 3, BluxGPT and the direct CLI 18. Extra skips versus the dev run: the archived BLHermes fork checks and the VoidForge adapter test, which need sibling checkouts |
| BLUX off | each from a fresh clone in its own venv; the run is refused if any BLUX runtime piece is present. CogA 346, cA 116, DAT 87, LRC 136, GOD 102 (with blux-sdk only), BLUX System 103, BluxGPT 41, JADIS Toolbox 79 passed, 0 failed. Skips: the `.blux` checks that need the SDK, cross-engine checks needing DAT, BluxGPT's paid provider test, and LRC's archived BLHermes inventory check |
| `ax` with BLUX absent | every engine route works (DAT, CogA, cA, LRC, GOD, BLUX System); `ax ask`/`ax agent` exit 69 and name BLUX; a real `ax audit` completes; `ax capabilities` lists DAT and LRC capabilities through GOD. axiom `run_tests.sh` 14 passed; `test_ax_router` 14 passed, including the 3 VoidForge client tests against a VoidForge `671349e` checkout |
| Products | No product manifest depends on BLUX (roughin, vigyl, resolver, void.os, void.sys, void.game, voidforge, termux-background, theresolver, bluxai.app); their suites ran in OV-55 to OV-60. blux-app is a BLUX front end by design |
| Contracts | `check_contracts.py`: ok, 0 breaking, 0 invariant failures; lock written; `integration_matrix.py --check --workspace ~/ov` passes |
| Lint and types | blux `ruff check`, `ruff format --check`, `mypy` (63 files) clean |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 |

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F114 | blux | RESOLVED_VERIFIED | store preflight for external/destructive capabilities |
| F133 | blux | RESOLVED_VERIFIED | stale and inconsistent CI integration pins |
| F96 | lrc | RESOLVED_VERIFIED (unchanged) | owner kept recovery CLI-only |

## Stage output

```yaml
stage_id: OV-61
implementation:
  changes: [receipt-store preflight for external/destructive capabilities, single integration pin set and
            installer used by CI, compatibility lock at the current commits, integration matrix]
  excluded: [real model providers (D-02), VoidForge device operations (D-03), hosted CI (D-01)]
validation:
  integration: [blux integration tests from fresh clones with every BLUX_REQUIRE_* set]
  blux_off: [CogA, cA, DAT, LRC, GOD, BLUX System, BluxGPT, JADIS Toolbox own suites without the BLUX runtime;
             ax routes and suites]
  contracts: [check_contracts.py ok, lock written]
disposition: {state: PASSED, blockers: [], next_actions: [OV-62 needs authorization]}
```
