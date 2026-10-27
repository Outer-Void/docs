# Release, deprecation, incident and recovery

## Release policy

- **Independent lifecycles.** Each repository versions and releases on its own (semantic versioning, or Android
  `versionName`/`versionCode`). A bot release never forces a website release, a BLUX release never forces a
  product release.
- **A release needs evidence, not intent.** Before a component is tagged as released:
  1. its status-matrix row shows the evidence its gate requires (tests; hardware for device or Android work;
     security);
  2. its release checklist passes (for example Roughin `docs/release-checklist.md`, Vigyl
     `docs/release-checklist.md`, Termux Background `docs/RELEASE_CHECKS.md`);
  3. CI ran green on the release commit. As of 2026-10-27, no Outer-Void CI job starts (billing lock, findings
     F49), so **no component can satisfy this rule today**;
  4. its notices and credits records are current;
  5. Android artifacts are signed with an offline key and verified (`apksigner verify`).
- Nothing is called released, stable, production-ready or a release candidate without a matrix status that says
  so. Package metadata must not claim more (for example a "Production/Stable" classifier on an unreleased package).

## Deprecation

- Deprecate in the open: mark the item deprecated in its repository docs and CHANGELOG, name the replacement,
  and keep the old path working for at least one release where it is cheap (examples: BLUX System's
  `[legacy]` commands, `blux-app legacy-view`).
- History is never deleted. Retired repositories are archived, not deleted (BLHermes). Superseded documents get
  a dated historical banner, not a rewrite (DAT `snapshot.md`).
- Removing an interface other repositories use requires updating every consumer first, with the compatibility
  matrix (contracts.md) and the cross-repository contract checks (Stage 42) as the guard.

## Incident and recovery

| Incident | First steps |
|---|---|
| Leaked credential or signing key | Revoke or rotate at the provider; treat any build signed with it as compromised; record it in the repository's README and findings; never rewrite git history to hide it |
| Product data loss | Restore from the product's backups (Roughin and Vigyl `scripts/restore.sh` into an empty database), then compare counts and migration revisions |
| BLUX System store damage | `blux-system verify --store …` (hash chain); restore from `blux-system export` or a filesystem backup; `replay-check` affected operations |
| Security finding in a component | Record in findings with severity; fix in the owning repository; add a regression test (for example the adb wipe rule, Stage 36) |
| Public exposure of private source | Make the repository private (owner), delete public artifacts, record it (VoidForge F7) |

Contacts: outervoid.blux@gmail.com (main), theoutervoid@outlook.com (fallback).
