# OV-53: native BLUX research (2026-11-07)

**State: PARTIAL.** The exit's fallback branch holds: nothing was promoted, and native BLUX models stay
**EXPERIMENTAL**. The research itself cannot proceed. There is no eligible corpus (F63, D-09), no independent
evaluation custodian and no compute budget (new owner decision D-15), so no candidate was trained or evaluated
against Gen 0. What could be done without those inputs was done:
- the data controls were probed and three defects fixed (F115–F117);
- the Gen 0 baseline and the Router 0.1 evidence were re-verified;
- BLUX lint (F94) and a router test gap (F119) were fixed.

No model was downloaded, no provider was called, and no protected split was opened outside its dataset's
process.

| Repository | Before | After |
|---|---|---|
| blux | `cfd7470` | `60ddc76` |

## Delta review (rule 11)

The training tree had not changed since `8d989de` (dataset program, 2026-11-04). The Gen 0 baseline was last
produced at Stage 35 (`8ef10d5`).

| Plan item | Result |
|---|---|
| Eligible corpus | **None.** All families in `training/dataset-program/families.json` are `source_acquisition_pending`; F63 stays EXTERNAL_BLOCKED (D-09). The engine datasets (`blux-coga-dataset`, `blux-ca-dataset`, 127 train/validation records) are specialist regression material, not a corpus |
| Provenance | Source schema, eligibility (owner approval, no private data), licences and receipts: sound. The dataset-program preflight (family locks, digests, eligibility) passes its 3 tests |
| PII screening | **Gaps (F116):** 11 of 14 probed forms passed unredacted |
| Hidden reasoning | **Gap (F115, High):** `<think>`, harmony analysis channels and `reasoning`-style fields were accepted as training data. Related: bluxgpt passes inline `<think>` from OpenAI-compatible servers into answers (F118, OPEN, provider layer) |
| Independent holdout | **Gap (F117):** reworded siblings of holdout items reached train, in one build and across versions. Independence of authorship needs a custodian (D-15); I cannot be one, since I write the training tooling |
| Compute | Host: aarch64 Android/PRoot, 6 cores, 5.3 GiB RAM (1.6 GiB available), no GPU, 36 GB free disk. No training of the shortlisted bases (0.135–1.7 B parameters) is qualified here; a budget is D-15 |
| Evaluation against Gen 0 | Gen 0 re-run: deterministic results **match** the Stage 35 baseline (exit 0). Router 0.1: evidence chain verifies (8 receipts, protected order intact); its own gate **failed**, so it stays historical EXPERIMENTAL evidence. No new candidate exists to compare |

## Changes (blux)

- **F115:** the hidden-reasoning gate rejects `<think>`/`<thought>` tags, harmony `analysis` channels and the
  fields `reasoning`, `reasoning_details|summary|items|text`, `thought_process` and `thinking_blocks|content|text`.
  `reasoning_structure`, CogA's `reflection` and prose mentioning reasoning are kept.
- **F116:** the personal-data gate redacts:
  - look-alike e-mail domains;
  - phone numbers with separators or a `+` code;
  - IPv6 with at least three groups (so `xs[1::2]` is kept);
  - `/root` and `C:\Users\<name>` home paths;
  - Luhn-valid card numbers starting 2–6;
  - US SSNs.
- **F117:** a train or validation record whose input is ≥ 80% contained in a protected record of the same build is
  rejected, and `--lock` pointing at a previous dataset protects that dataset's test, holdout and regression splits
  automatically. `blux_training` pipeline version 1.1.0.
- **F94:** `training/dataset-program` formatted and lint-clean. The preflight's syntax tree is unchanged; only
  imports in its test were reordered.
- **F119:** router integrity tests take `BLUX_COGA_DATASET` and `BLUX_COGA_DATASET_PYTHON`.
- **Docs:** `training/blux_training/README.md` gate table and the CHANGELOG ("Unreleased: OV-53").

## Evidence (executed 2026-11-07)

| Check | Result |
|---|---|
| New tests on the old code | 17 of 28 in `tests/training/test_ov53_gates.py` fail on `cfd7470`; the 11 that pass are preservation and false-positive guards |
| False positives | none on the 127 train/validation records of both engine datasets (aggregate counts only); slices, times, MACs, hashes, ids and documentation addresses kept (tests) |
| Training pipeline tests | 53 passed; `make training-example` builds and validates |
| Router tests | 50 passed (previously 46 + 4 always skipped), with sklearn 1.7.2 / scipy 1.16.3 / numpy 2.3.4 as pinned, in a separate scratch venv; positive control: the unmutated dataset passes the probe |
| Dataset-program tests | 3 passed |
| Gen 0 | `python -m evals.blux_eval.run ... --check evals/reports/gen0/report.json`: deterministic results match, exit 0. Model suites (intent, tool selection, repository diagnosis) BLOCKED (D-02) |
| Router 0.1 evidence | `verify_experiment`: 8 receipt entries verified, protected order verified, gate_passed false |
| BLUX full suite, every `BLUX_REQUIRE_*=1` | 648 passed, 15 skipped (620 + 28 new; skips as OV-52), exit 0 |
| `ruff check .`, `ruff format --check .`, `mypy` | clean for the whole repository (F94 resolved) |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 |
| Push | fast-forward to `main`; blux has no branch rules |

## Findings

| ID | Repository | Severity | State | Note |
|---|---|---|---|---|
| F115 | blux | High | RESOLVED_VERIFIED | reasoning-model output passed the hidden-reasoning gate |
| F116 | blux | Medium | RESOLVED_VERIFIED | common personal data passed unredacted |
| F117 | blux | Medium | RESOLVED_VERIFIED | holdout siblings could enter training |
| F94 | blux | Low | RESOLVED_VERIFIED | `training/dataset-program` lint |
| F119 | blux | Low | RESOLVED_VERIFIED | router integrity tests always skipped off-cloud |
| F118 | blux-gpt | Medium | OPEN (OV-64 scope) | inline `<think>` from OpenAI-compatible servers reaches answers and sessions |
| F63 | blux | High | EXTERNAL_BLOCKED (D-09) | no eligible corpus |
| F61 | blux | Medium | EXTERNAL_BLOCKED (D-15) | no independent, human-reviewed evaluation |

## Owner decisions needed

- **D-09 / F63:** a rights-cleared corpus (owner-authored or licensed with permission evidence).
- **D-15 (new):** an independent evaluation custodian, who authors and holds protected items. The authors of
  the training tooling and templates, including this assistant, cannot fill the role. Also a compute budget:
  hardware, or a paid service that no stage may choose.
- **F118:** whether to authorize a small blux-gpt fix now (fake-provider tests suffice) rather than waiting for
  OV-64.

## Stage output

```yaml
stage_id: OV-53
implementation:
  changes: [hidden-reasoning gate (think, harmony, reasoning fields), PII gate (emails, phones, IPv6, homes,
            cards, SSNs), sibling protection within and across versions, dataset-program lint, router test paths]
  excluded: [corpus acquisition (D-09), custodian and protected items (D-15), compute (D-15), training,
             model downloads, provider calls (D-02), bluxgpt inline reasoning (F118)]
validation:
  unit_and_integration: [training 53, router 50, dataset-program 3, BLUX 648 passed 15 skipped with every BLUX_REQUIRE_*=1]
  regression: [17 of 28 new tests fail on cfd7470; 11 are preservation and false-positive guards]
  evaluation: [Gen 0 deterministic results match the Stage 35 baseline; Router 0.1 gate failed, history only]
  security: [ruff and mypy clean, DAT gate exit 0]
disposition: {state: PARTIAL, native_models: EXPERIMENTAL, blockers: [D-09, D-15], next_actions: [owner decisions D-09 and D-15; F118 authorization; OV-54 needs authorization]}
```
