# Contracts, SDK, integration and compatibility

Canonical sources are in `Outer-Void/blux`; this page states the rules and links to them.

## BLUX Contract v1

- **Kinds:** `blux.capability`, `blux.capability-set`, `blux.execution`, `blux.result`, `blux.receipt`,
  `blux.artifact`, `blux.model`, `blux.project`, `blux.policy`, `blux.error`. JSON Schemas are in
  [`contracts/v1/`](https://github.com/Outer-Void/blux/tree/main/contracts/v1), with a checksum lock.
- **Version:** contract version `1.0`. The SDK supports exactly `("1.0",)` (`blux_sdk/versions.py`). Version
  negotiation: [ADR-0005](https://github.com/Outer-Void/blux/blob/main/docs/adr/0005-version-negotiation.md);
  a document with an unsupported version is refused, never guessed at.
- **Errors:** typed error codes ([ADR-0006](https://github.com/Outer-Void/blux/blob/main/docs/adr/0006-error-model.md)).
- **Envelopes:** operation, result and receipt envelopes
  ([ADR-0004](https://github.com/Outer-Void/blux/blob/main/docs/adr/0004-operation-result-envelope.md)).
- **Identifiers:** prefixed ULIDs (`op_`, `rcpt_`, `art_`, `ses_` + 26 Crockford base32 characters); capability
  ids such as `reason.plan` (`blux_sdk/ids.py`, matching `common.schema.json`).

## SDK policy

- `blux-sdk` (`blux/sdk/python`, version 0.2.0) is the only implementation of Contract v1 validation. Its
  packaged schemas are a byte-identical copy of `contracts/v1` (`packaging/sync_schemas.py --check` fails on drift).
- No other repository copies schemas. Consumers depend on the SDK, pinned deliberately (see the compatibility
  matrix below).
- The SDK is not on PyPI; it is installed from the BLUX repository (`#subdirectory=sdk/python`).

## Capability policy

- A repository integrates by declaring a `.blux/` directory: `manifest.yaml` (`blux.project`: `project_id`,
  `name`, `role`, `capabilities`, `policy`), `capabilities.yaml` and `policy.yaml`
  ([ADR-0003](https://github.com/Outer-Void/blux/blob/main/docs/adr/0003-capability-contract.md)).
- The manifest's `role` is `standalone` (usable without BLUX) or `integrated` (requires the BLUX runtime);
  both are first-class ([ADR-0002](https://github.com/Outer-Void/blux/blob/main/docs/adr/0002-standalone-vs-integrated-boundary.md)).
  This is a contract field, separate from the BLUX column of [repositories.md](repositories.md).
- `.blux/` exists today in blux, blux-coga, blux-ca, dat, lrc, god and jadis.toolbox (checked 2026-10-27).
  A missing `.blux/` is valid wherever BLUX integration is deliberately excluded.
- Policies have a `default_effect` and rules; authorization and authority:
  [ADR-0007](https://github.com/Outer-Void/blux/blob/main/docs/adr/0007-authority-authorization-model.md).
  Device-destructive operations need the person at the device (VoidForge).
- GOD discovers capabilities by reading `.blux/` through the SDK; it never runs them.

## Hook System v1

- Version `1.0` (`blux_runtime/hooks/catalog.py`), 37 events across agent, artifact, capability, credential,
  model, reasoning, receipt, request, runtime, security, session, tool and training families. Each event declares
  whether it is vetoable, mutable and sensitive. Mutations may only add (`superset`) or narrow (`decrease`).
- Spec: [docs/hooks/v1.md](https://github.com/Outer-Void/blux/blob/main/docs/hooks/v1.md),
  [ADR-0012](https://github.com/Outer-Void/blux/blob/main/docs/adr/0012-hook-system.md).
- The `training.eligible` / `training.rejected` events exist in the catalogue; the Stage 34 pipeline does not
  emit them yet.

## BLUX Model API v1

- Version `1.0`. Applications address four **logical models**: `blux-main`, `blux-fast`, `blux-reason`,
  `blux-code`. Route capabilities: `streaming`, `tools`, `structured_output`, `deterministic`, `long_context`,
  `local_only`. Spec: [docs/model-api/v1.md](https://github.com/Outer-Void/blux/blob/main/docs/model-api/v1.md),
  [ADR-0010](https://github.com/Outer-Void/blux/blob/main/docs/adr/0010-model-api.md).
- Physical provider models appear only in the routing table (`default_routes.json`). Code naming a physical model
  fails `tests/models/test_logical_model_isolation.py`, and every logical model keeps a fallback route, so a new
  backend (including a future native model) is added and rolled back by editing routes.
- Providers are reached through BluxGPT as a subprocess backend. Fallback is explicit and marked degraded;
  excluded and non-allowed providers are never used (Gen 0 routing suite).

## Receipt and provenance spec

- Every capability execution produces a `blux.receipt`: `receipt_id`, `operation_id`, `parent_operation_id`,
  `session_id`, `project_id`, `capability_id` and version, `actor`, `status`, `error_code`, `policy_decision`,
  `input_sha256`, `output_sha256`, `artifact_ids`, `started_at`, `finished_at`, `issuer`.
- BLUX System is the persistence authority. It derives statuses `SUCCESS`, `FAILURE`, `DENIED` (policy),
  `CANCELLED`, and `PARTIAL` (aggregate: the operation succeeded, something in its subtree did not). It exposes
  `show`, `list`, `graph` (parent → child), `timeline`, `verify` (hash chain), `replay-check` and
  `artifact-verify`.
- Training records carry provenance in the same spirit: source hash, receipt ids, eligibility, pipeline version
  and redactions (`blux_training`).

## Integration standard

A component integrates with the ecosystem by:
1. a CLI whose machine commands print exactly one JSON document, with exit code 0 (ok), 1 (failure, with an
   error document) and 2 (usage); routers use 69 for "engine unavailable"
   ([ADR-0008](https://github.com/Outer-Void/blux/blob/main/docs/adr/0008-no-arbitrary-stdout-protocol.md));
2. optionally a `.blux/` declaration (capabilities and policy) validated by the SDK;
3. being invoked as a subprocess provider, never imported
   ([ADR-0009](https://github.com/Outer-Void/blux/blob/main/docs/adr/0009-subprocess-provider.md));
4. emitting or accepting Contract v1 documents only;
5. staying usable when every other component is absent.

## Compatibility matrix (2026-10-27)

| Component | Contract | SDK dependency | Notes |
|---|---|---|---|
| blux (runtime, CLI) | 1.0 | ships blux-sdk 0.2.0 | Model API 1.0, Hook System 1.0 |
| blux-system | 1.0 | blux-sdk pinned to commit `0b09a46` (tag `blux-sdk-v0.1.0`) | one release behind the SDK; same contract |
| god | 1.0 | `blux-sdk>=0.1.0,<0.3` | reads `.blux/` only through the SDK |
| blux-coga, blux-ca, dat, lrc, jadis.toolbox | 1.0 (`.blux/`) | none | declare capabilities; called as subprocesses |
| blux-gpt | Model API 1.0 backend | none | invoked by the Model API router |
| blux-app, bluxai.app | consume CLI output | none | call executables only |

The accepted baseline with exact commits is the generated [compatibility matrix](../ecosystem/compatibility.md)
(from `ecosystem/compatibility.json`). `python3 tools/check_contracts.py --fetch` re-reads each boundary's few defining
files from GitHub (no clones) and fails on any breaking change: a removed capability, a changed capability schema, Contract
v1 schemas changed without a version change, an unsupported contract version or SDK pin, a VoidForge catalogue copy that
drifted, an `ax` route without its executable or subcommand, or an unrecorded release tag
(`ecosystem/release-ledger.json`). Docs CI runs it on every push and daily. Accepting a change is an explicit, reviewed
`--write-lock`.
