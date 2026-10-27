# Policies

## AI and model policy

- Applications use **logical models** only (`blux-main`, `blux-fast`, `blux-reason`, `blux-code`); physical
  models live in the routing table (contracts.md). Model output is assistance, never authority. It does not
  certify work (DAT does), authorize device writes (the person at VoidForge does), or own product truth.
- **Provider hidden reasoning is never stored.** CogA keeps only explicit structure. The dataset builders and
  `blux_training` reject records with reasoning-named fields or markers.
- AI tools used to build Outer Void are attributed per repository in
  [credits `provenance/ai-assistance.yaml`](https://github.com/Outer-Void/credits/blob/main/provenance/ai-assistance.yaml),
  from commit trailers or other evidence. Undeclared tooling becomes an unresolved record (for example UNR-021),
  never a guess.
- Native models are integrated only if they beat the Generation 0 baseline on a permanent holdout
  (`blux/evals/reports/gen0/`, `blux/training/SPECIALISTS.md`). None is integrated today.

## Training and data policy

Implemented in `blux/training/blux_training` (Stage 34) and the dataset repositories (`dstool`):
- **Private user or project data is never training data**, even when approved.
- Secrets mean rejection, never partial redaction. Personal data is redacted and the record marked.
- Every source needs an allowed licence; every record carries provenance (source hash, receipt ids, eligibility,
  pipeline version).
- Protected splits (test, holdout, regression, adversarial) are locked: a record never moves, and contamination
  against them is checked.
- Builds are deterministic and re-validatable from their files.

## Privacy

- Each product publishes its own privacy policy under [`legal/`](../legal/README.md), or in its repository
  (Vigyl `docs/privacy-policy.md`, Resolver website `/privacy/`). Privacy policies describe what the code does.
  Factual corrections are made against source (for example the Resolver website's AI-provider section,
  Stage 31).
- Tool output shown to people passes through redaction (BLUX's `redact()`; BLUX System's redaction module).
  jadis never uploads diagnostics and redacts secrets everywhere.
- Products keep personal data in their own stores; BLUX does not collect it.

## Credentials

- Credentials come from the environment or an OS secret store, never from repositories, logs, receipts or
  datasets. Model API routes name only the variable (`credential_env`), never a value.
- Apps store tokens only as hashes: refresh tokens (Roughin, Vigyl, bluxai.app), invitation codes (Vigyl) and
  API tokens (bluxai.app).
- Signing keys stay offline. CI receives them only as protected secrets. A key that was ever committed is
  treated as compromised (Termux Background precedent).
- Every documentation pass scans added files for secrets and personal paths.

## Device operations

- **VoidForge is the device authority**
  ([ADR-0016](https://github.com/Outer-Void/blux/blob/main/docs/adr/0016-voidforge-devices.md)). BLUX and
  `ax devices` can only ask, through the `voidforge` integration client (`ping`, `describe`, `devices`, `call`).
  Every write is confirmed by the person at the VoidForge device.
- Destructive command patterns (flash, erase, unlock, adb destructive commands including `recovery --wipe_data`)
  are classified as device operations by `blux_runtime.security.commands` and need approval.
- No component flashes, wipes or unlocks a device on its own.

## VoidForge restricted distribution

From [voidforge `docs/DISTRIBUTION.md`](https://github.com/Outer-Void/voidforge/blob/main/docs/DISTRIBUTION.md):
- VoidForge is free and only for authorized Outer-Void organization members. It is not a public binary.
- The members-only release path: an offline signing key, a manual workflow that runs only in a private repository
  under a reviewer-protected environment, a manifest signed with an offline organization key, and a private update
  channel.
- **Open:** the repository is still public (owner action; findings F7). Until it is private, the source is not
  members-only, though binaries are kept off public surfaces.

## Licensing and provenance

- **Proprietary by default.** Every repository changed on or after 2026-10-25 is under its Outer-Void, BLUX or
  product proprietary licence. Copies released earlier under MIT or Apache-2.0 stay under those licences, as each
  README states.
- Third-party components keep their licences. Licence texts are copied verbatim and checksummed in
  [Outer-Void/credits](https://github.com/Outer-Void/credits). Notices travel with distributed artifacts
  (`THIRD_PARTY_NOTICES.md` and `licenses/`).
- Attribution goes beyond the legal minimum where provenance is known, and distinguishes dependency, lineage,
  inspiration, tool and AI assistance ([credits GOVERNANCE](https://github.com/Outer-Void/credits/blob/main/GOVERNANCE.md)).
