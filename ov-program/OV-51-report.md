# OV-51: engine reliability (2026-11-07)

**State: PASSED for its exit (engines work standalone and with BLUX).** The delta review found and reproduced
seven defects in interrupted transactions, replay and malformed-input handling across the five engines and the
SDK loader they share with BLUX; all are fixed with tests that fail on the previous commits. One low residual is
deferred (F103). No real provider was called.

| Repository | Before | After |
|---|---|---|
| lrc | `443e532` | `ea82afc` |
| blux-ca | `7cb953a` | `689ec70` |
| blux (SDK) | `4163637` | `9cd53ef` |
| god | `ad6f0c4` | `613b800` |
| blux-coga | `3dc86fa` | `c94dc9c` |
| dat | `487e1d4` | `57c8099` |

## Delta review (rule 11)

No engine had changed since the deep audit (2026-11-06), which re-ran the BLUX hard gates (45 passed). The
OV-51 scope (replay, rollback, interrupted transactions, LRC atomicity, GOD on malformed input) had not been
probed by fault injection before, so this stage did that rather than repeating verified runs.
- **Re-run first** (2026-11-07, at the "before" commits): CogA 343, cA 117, DAT 88, LRC 133 passed (1 skipped:
  `dat` not on PATH), GOD 94. All exit 0.
- **Read in full:** LRC's engine (create, journal, rollback), cA's workspace transactions, CogA's replay, GOD's
  index, scan and loader, the SDK's `.blux/` loader and YAML parser, DAT's policy loading.
- **Probed** with scratch scripts: processes killed with `os._exit` at chosen points, 13 malformed `.blux/`
  projects, 7 damaged GOD caches, YAML alias bombs, tampered CogA artifacts, hostile DAT targets and policies.

| Area | Result at the "before" commits |
|---|---|
| LRC atomicity, interrupted transactions | `create` is all-or-nothing (staged, verified, renamed). **Gap:** a killed `scaffold`/`migrate` left the repository part-way with no way back (F96) |
| cA rollback and recovery | Journal, lock, `ca recover` and rollback are sound for kills during writing (existing test). **Gap:** a kill after the ledger write made `recover` undo a committed change (F97) |
| CogA replay | Deterministic: the eval suite is byte-identical under `PYTHONHASHSEED` 0, 1 and 999; tampered results fail replay (exit 1). **Gap:** a damaged artifact crashed replay (F101) |
| GOD on malformed input | 10 of 13 malformed projects became problem records. **Gaps:** a pipe hung the scan, a link was followed, deep nesting crashed it (F98, F100); damaged caches crashed every query (F100); alias bombs (F99) |
| DAT on hostile input | FIFOs and symlinks in the target, and non-regular target policies, are handled (the stricter default policy applies). **Gap:** a deeply nested policy was `INTERNAL_ERROR` (F102) |
| CogA → cA → DAT with a forced rejection | Verified through BLUX: DAT fails cA's build, cA repairs within its limit, only DAT passes it, BLUX System reconstructs the chain (`tests/integration/test_ca.py`) |

## Changes

- **LRC (F96).** New `lrc recover DIR` restores every journaled path to its before-state after a killed
  `scaffold`/`migrate` (or a `rollback_failed` journal), removes temporary files and marks the journal
  `recovered`. Until then `scaffold`, `migrate` and `rollback` refuse with `INTERRUPTED_TRANSACTION` (exit 3).
  Recovery refuses (`ROLLBACK_CONFLICT`) if a path changed after the interruption. Backups are fsynced before
  the journal; an advisory lock (`TARGET_LOCKED`) stops two LRC processes changing one repository, and the plan
  is re-checked under it.
- **cA (F97).** `ca recover` keeps a change the ledger already records (`"completed": true`) and only removes
  the journal; rollback links lost to a kill are restored, so a repeated rollback is `ALREADY_ROLLED_BACK`, not
  a false `CONFLICT`.
- **SDK `.blux/` loader (F98, F99)**, shared by GOD and the BLUX runtime: only regular files are opened
  (`O_NOFOLLOW`, non-blocking, `fstat`), reads stop at 1 MiB, nesting too deep is `nesting_too_deep`, and alias
  expansion is bounded by the byte limit. No alias-free document within the limit is affected.
- **GOD (F100).** `.blux/` entries that are not regular files or directories are problems before anything is
  opened, also with older SDKs (GOD allows `<0.3`); cache entries carry a record digest and are re-read when
  damaged.
- **CogA (F101)** and **DAT (F102):** damaged artifacts and over-nested policies are `INVALID_ARTIFACT` and
  `INVALID_POLICY`.
- **Docs:** changelogs of all six repositories; LRC `USAGE`, `ENGINE`, `troubleshooting` and README; cA
  `CONSTRUCTION`; GOD `INDEX` and README; CogA `USAGE`; BLUX `docs/spec/dot-blux.md`.
- **Versions unchanged:** engine versions are part of plan ids, artifact ids and pinned fixtures, so the
  changes are listed under "Unreleased".

## Evidence (executed 2026-11-07)

| Check | Result |
|---|---|
| New tests on the old code | LRC 5/5, cA 2/2, GOD 8/8, CogA 4/4, DAT 1/1 fail on the "before" commits. SDK: 6 of 7 fail on `4163637`; the 7th (large alias-free documents still load) passes alone on the old code, as intended (in the combined old run it timed out behind the old code's runaway alias-bomb thread) |
| GOD with the old SDK | the new GOD passes all 8 new tests with the SDK from `4163637` |
| Engine suites (final) | CogA 347, cA 119, DAT 89, LRC 139, GOD 102 passed, 0 skipped, exit 0 |
| BLUX full suite, every `BLUX_REQUIRE_*=1` | 611 passed, 15 skipped (604 + 7 new; skips: 2 real-provider, 12 need the BLHermes interpreter, 1 fork moved), exit 0 |
| BLUX hard gates at the final engine commits | 45 passed, 2 skipped (real-provider), exit 0. Re-run because DAT's one-line fix landed while the full suite was running |
| Probes after the fixes | killed migration recovered byte-for-byte (the owner's edit kept); 13/13 malformed projects are problems; 7/7 damaged caches re-read; 442-byte alias bomb refused in 0.7 s |
| False positives | `god check` over the 26 workspace repositories (secret-project excluded) identical before and after: 8 projects, 0 problems |
| `ruff` and `mypy` (each repository's configured gates) | clean in all six |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 in all six |
| Pushes | lrc, blux-ca, blux-coga and dat protect `main`; the fast-forward pushes logged "Bypassed rule violations" (owner bypass), as in earlier stages. blux and god have no rules |
| Real providers | not run: BLOCKED until OV-64 (D-02) |

## Findings

| ID | Repository | Severity | State | Note |
|---|---|---|---|---|
| F96 | lrc | High | RESOLVED_VERIFIED | interrupted scaffold/migrate had no recovery; no lock |
| F97 | blux-ca | Medium | RESOLVED_VERIFIED | recover undid a committed change |
| F98 | blux | Medium | RESOLVED_VERIFIED | `.blux/` loader followed links, blocked on pipes, unbounded reads, RecursionError |
| F99 | blux | Medium | RESOLVED_VERIFIED | YAML alias bombs |
| F100 | god | Medium | RESOLVED_VERIFIED | hostile project or damaged cache stopped discovery |
| F101 | blux-coga | Low | RESOLVED_VERIFIED | replay crashed on a damaged artifact |
| F102 | dat | Low | RESOLVED_VERIFIED | nested policy was INTERNAL_ERROR |
| F103 | lrc | Low | DEFERRED (OV-62) | a killed `create` leaves `.lrc-stage-*` beside the target |

`lrc recover` is a CLI command, not a BLUX capability; through BLUX the `INTERRUPTED_TRANSACTION` error names
it. A `repo.recover` capability would be a versioned contract change (OV-61).

## Stage output

```yaml
stage_id: OV-51
implementation:
  changes: [lrc recover + interruption guard + lock, cA committed-change recovery, SDK .blux/ loader hardening,
            GOD malformed input and cache digests, CogA replay validation, DAT nested policy]
  excluded: [stale create stage directories (F103, OV-62), repo.recover BLUX capability (OV-61),
             real providers (OV-64)]
validation:
  unit_and_integration: [engine suites 347/119/89/139/102 passed, BLUX 611 passed 15 skipped,
                         hard gates 45 passed 2 skipped]
  regression: [new tests fail on the previous commits (SDK 6 of 7; the 7th is a preservation test)]
  security: [ruff and mypy clean, DAT gate exit 0 in six repositories]
  external: [real providers BLOCKED (D-02), CI EXTERNAL_BLOCKED (D-01)]
disposition: {state: PASSED, blockers: [], next_actions: [OV-52 receipt durability (F83-F85)]}
```
