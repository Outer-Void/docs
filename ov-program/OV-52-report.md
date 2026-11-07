# OV-52: BLUX System as the evidence authority (2026-11-07)

**State: PASSED for its exit (tampering and corruption are detected, and required receipts fail closed).** The
deep-audit receipt defects F83–F85 are fixed, and the delta review found and reproduced nine more defects in
BLUX System's store and BLUX's receipt path (F104–F112); all are fixed with tests that fail on the previous
commits. Two residuals are deferred with owners (F113, F114). No real provider was called.

| Repository | Before | After |
|---|---|---|
| blux-system | `f7f8ede` | `26f2240` |
| blux | `9cd53ef` | `cfd7470` |

## Delta review (rule 11)

BLUX System had not changed since OV-49 (`f7f8ede`); its suite last ran at Stage 43/44 baselines. The deep audit
(2026-11-06) found F83–F85 in BLUX's sink but did not probe the store itself, so this stage did.
- **Re-run first** (2026-11-07, at the "before" commits): blux-system 74 passed, ruff and mypy clean; BLUX sink,
  System integration and agent tests 14 passed.
- **Read in full:** the store (`store.py`: log, lock, torn-tail repair, ingest, import/export, retention), the
  graph and statuses, the CLI, BLUX's `system_sink.py`, the executor's emit path, the agent loop and the CLI
  commands that report unrecorded receipts.
- **Probed** with scratch scripts: crashes at chosen bytes, records cut from the end, re-hashed forgeries,
  damaged metadata, hostile bundles, tampered blobs, 16 simultaneous writers, retention killed mid-run, and
  F83–F85 against BLUX.

| Area (plan) | Result at the "before" commits |
|---|---|
| Hash chain | Edits, gaps, reordering and garbage were detected. **Gaps:** a record missing only its newline bricked the store at the next append (F104); a shortened or stale log verified as ok (F105); re-hashed malformed records and damaged metadata crashed readers (F106) |
| Graph and partial failure | `PARTIAL`, `DENIED`, `CANCELLED`, missing-parent placeholders and cycles were correct. **Gaps:** an unknown status crashed the graph (F106); an import could stop part-way (F108) |
| Retention | Compaction was atomic, but its record was appended afterwards, so a kill in between left an unrecorded removal (F107); blobs could be pruned before their record existed (F109) |
| Migrations | A newer store format was refused, but as unexplained corruption (F106). Format 1 is unchanged: `head.json` is an addition that older stores gain at their next write, and a writer from before OV-52 is accepted |
| Required receipts | **Gaps:** F83 (an outage lost receipts of operations with artifacts), F84 (flush deleted concurrently spooled receipts), F85 (nothing flushed; `SINK_REFUSED` retried for ever), refused receipts were dropped (F111), `blux agent` kept acting after a refused receipt (F112), 15 of 16 simultaneous writers were refused (F110) |

## Changes

- **blux-system store.**
  - Crash repair: a complete record missing its newline is completed and recorded (`unterminated_record`); a
    long-lived writer also repairs a torn tail another process left.
  - `head.json` anchors the last record; `truncated` and `anchor_mismatch` are `STORE_CORRUPT`.
    `verify --expect-head` checks a head kept elsewhere.
  - Every open checks each payload's structure (`invalid_payload`); `verify` also checks receipts and artifacts
    against Contract v1 and checks every blob (`blob_mismatch`, `blob_missing`).
  - Damaged `retention.json` and `store.json` are `STORE_CORRUPT` with a reason; a newer format is
    `unsupported_version`.
  - Retention writes its record (with `previous_head` and `previous_records`) inside the new chain, installed
    with one rename.
  - Import checks payloads and conflicts before any write; a failing import imports nothing.
  - Writers wait up to 10 s for the lock; blobs are written under it, fsynced, and repaired on re-ingest.
- **BLUX receipt path.**
  - The receipt is always attempted; artifacts are spooled with their bytes; `sink_error.missing_artifacts`
    (F83).
  - Spool and flush are serialized with a lock file; a flush works from `<outbox>.flushing.jsonl` (F84).
  - `blux receipts status|flush [--include-refused]`; `blux doctor` warns while receipts wait; `SINK_REFUSED` is
    a refusal (F85).
  - Refused documents are set aside in `<outbox>.refused.jsonl`; outbox files are owner-only (F111).
  - `blux agent` stops before its next step when a receipt is neither recorded nor queued (`ReceiptNotRecorded`,
    exit 5); `Outcome.receipt_not_queued` (F112).
- **Docs:** blux-system `docs/STORE.md` (corruption table, what the chain proves and does not, import, retention,
  locking), README and CHANGELOG; BLUX `docs/cli.md`, `interfaces.py`, `agent_cmd.py` and CHANGELOG.
- **Behaviour change disclosed:** a Stage 43 test expected `blux agent` to finish after a failing sink. It now
  covers both cases: queued receipts let the agent finish (exit 5); a receipt that is not even queued stops it
  before the tool call (exit 5, no answer).
- **Versions unchanged** (blux-system 2.0.0, store format 1): changes are listed under "Unreleased".

## Evidence (executed 2026-11-07)

| Check | Result |
|---|---|
| New tests on the old code | blux-system: 27 of 29 fail on `f7f8ede`; the 2 that pass are a preservation test (retention killed before its rename) and the null-`capability_id` false-positive guard. 3 of the 27 test new interfaces (lock wait, anchor compatibility). BLUX: all 10 new or changed tests fail on `9cd53ef` (8 sink tests, the real-System outage/flush test, the agent test) |
| False positive caught during the stage | the first payload check required `capability_id`; the BLUX integration suite showed that receipts rejected before their capability is known have it null. Fixed and covered by a test before any commit |
| blux-system suite | 103 passed (74 + 29), exit 0; also 103 passed against its pinned SDK (`6ee4c80`, 0.2.0) |
| BLUX full suite, every `BLUX_REQUIRE_*=1` | 620 passed, 15 skipped (611 + 9 new; the skips are OV-51's: 2 real-provider, 12 need the BLHermes interpreter, 1 fork moved), exit 0, including every engine hard gate. One later edit split a long string in a test's fake script for lint; that test file was re-run (8 passed) |
| Probes after the fixes | newline-less record completed, then 2 more appends verified; shortened log `truncated`; re-hashed malformed records, unknown status, damaged metadata all `STORE_CORRUPT` documents (no tracebacks); malformed events and conflicting bundles import nothing; tampered blob `blob_mismatch`, repaired by re-ingest; 16 of 16 simultaneous writers stored |
| `ruff` and `mypy` | clean in both repositories |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 in both |
| Pushes | fast-forward to `main`; blux and blux-system have no branch rules (no bypass) |
| Real providers | not run: BLOCKED until OV-64 (D-02) |

## Findings

| ID | Repository | Severity | State | Note |
|---|---|---|---|---|
| F83 | blux | Medium | RESOLVED_VERIFIED | outage lost receipts of operations with artifacts |
| F84 | blux | Medium | RESOLVED_VERIFIED | flush deleted concurrently spooled receipts |
| F85 | blux | Low | RESOLVED_VERIFIED | nothing flushed the outbox; `SINK_REFUSED` retried for ever |
| F104 | blux-system | High | RESOLVED_VERIFIED | a record missing its newline bricked the store |
| F105 | blux-system | Medium | RESOLVED_VERIFIED | shortened or stale log verified as ok |
| F106 | blux-system | Medium | RESOLVED_VERIFIED | corruption crashed readers |
| F107 | blux-system | Medium | RESOLVED_VERIFIED | retention could remove records unrecorded |
| F108 | blux-system | Medium | RESOLVED_VERIFIED | import could stop part-way; malformed events imported |
| F109 | blux-system | Low | RESOLVED_VERIFIED | blob tampering not verified; blobs written outside the lock |
| F110 | blux-system | Medium | RESOLVED_VERIFIED | simultaneous writers refused |
| F111 | blux | Medium | RESOLVED_VERIFIED | refused receipts dropped |
| F112 | blux | Medium | RESOLVED_VERIFIED | `blux agent` kept acting after a refused receipt |
| F113 | blux-system | Low | DEFERRED (OV-63) | chain is unsigned; a consistent rewrite needs an external head to detect |
| F114 | blux | Low | DEFERRED (OV-61) | one-shot commands act before learning a receipt is refused |

## Stage output

```yaml
stage_id: OV-52
implementation:
  changes: [store crash repair, head anchor and expect-head, payload and blob verification, metadata errors,
            atomic recorded retention, all-or-nothing import, writer lock wait, receipt always attempted,
            artifact spooling, outbox locking, blux receipts status/flush, refused receipts set aside,
            agent fails closed]
  excluded: [signed store heads (F113, OV-63), pre-execution store check (F114, OV-61), real providers (OV-64)]
validation:
  unit_and_integration: [blux-system 103 passed, BLUX 620 passed 15 skipped with every BLUX_REQUIRE_*=1]
  regression: [new tests fail on the previous commits (blux-system 27 of 29, BLUX 10 of 10)]
  security: [ruff and mypy clean, DAT gate exit 0 in both repositories]
  external: [real providers BLOCKED (D-02), CI EXTERNAL_BLOCKED (D-01)]
disposition: {state: PASSED, blockers: [], next_actions: [OV-53 native BLUX research (needs authorization)]}
```
