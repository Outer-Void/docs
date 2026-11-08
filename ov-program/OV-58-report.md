# OV-58: Launcher family (2026-11-08)

**State: PARTIAL.** The exit asks for each repository and the combination to qualify, with signed artifacts and a
device matrix. Signed artifacts need signing custody (D-04, F21), and the device matrix needs physical devices
(D-03), so the exit can't be met here. The engineering the plan put first is done, using the owner's four
decisions of 2026-11-08:
- product signature verification in all three apps (F1, F2, F17);
- a crash-loop guard (F19);
- layout-only backup (F20);
- synthesized Shooter sound (F29), bundled into AXIOM Launcher;
- F30 closed as decided.

Stage 27 stays **BLOCKED**: its gate (Stage 24's standalone release gate) still fails.

| Repository | Before | After |
|---|---|---|
| void.os (AXIOM Launcher) | `4ae9b33` | `d4c3dc9` |
| void.sys (VOID.SYS) | `3f2b7aa` | `af0050b` |
| void.game (AXIOM Shooter) | `b56c1ae` | `0839bcd` |

## Owner decisions (2026-11-08)

| Question | Decision |
|---|---|
| Signature verification (F1/F2/F17) | Implement v1 now: ECDSA P-256 over a documented canonical payload, keys pinned at build time, fail closed with none |
| Backup (F20) | Back up layout/customization settings only |
| Interrupted runs (F30) | Keep as is: a run is not resumed |
| Shooter audio (F29) | Synthesized sound effects with a mute setting; no music |

## Delta review (rule 11)

None of the three repositories had changed since OV-47/49. Baselines re-run on 2026-11-08: void.os 78 unit tests.
The Android builds need Termux's native `aapt2` 2.20. The Debian `aapt2` 2.19 used before cannot read the
installed API 36 platform jar, and the SDK's own `aapt2` is x86-64. That is an environment note, not a product
defect.

| Plan item | Result |
|---|---|
| F1, F2, F17: signature verification | All three `SignatureVerifier`s stopped at a `TODO`. Now each checks the install's signing certificate and the issuer's signature (`docs/product-signature-v1.md` in each repository). With no key pinned, release builds stay locked as before. In AXIOM Launcher, Play licensing and Play Integrity remain `TODO` pending D-11, so F1 is PARTIAL |
| F21: signing | Blocked (D-04). All release APKs build unsigned. The exposed termux-background key was never used |
| Crash-loop guard (F19) | Added and unit-tested; not exercised on a device |
| Icon work | VOID.SYS icon QA (individual visual review of generated variants) needs human review; not part of this run |
| Shooter work | Synthesized sound (F29) added and re-vendored into AXIOM through `tools/components.py sync` |
| Device matrix | Blocked (D-03) |

## Changes

- **Product signature v1 (all three).**
  - New pure-JVM `ProductSignatureCrypto`.
  - `PackageSignatureVerifier` added to VOID.SYS and the Shooter.
  - Keys come from a Gradle property or environment variable per app; a malformed value fails the build.
  - The reference issuer is `void.os/tools/product_signature.py` (`keygen`, `sign`, `verify`). Each app's tests
    check a vector it produced with a test-only key whose private half was never committed and which must never
    be pinned.
- **AXIOM Launcher (F19, F20).**
  - `AxiomApplication` installs the crash-loop guard.
  - Three crashes without a healthy 10 s session lead to a plain-view safe mode. It offers to try again, reset
    AXIOM's layout settings, or choose another Home app.
  - Backup includes only `datastore/axiom_settings.preferences_pb`, through both `fullBackupContent` and
    `dataExtractionRules`. Feed notes and tasks, signatures, entitlement, crash state and caches are excluded.
    Unknown widget IDs after a restore show the existing "widget unavailable" placeholder.
- **AXIOM Shooter (F29).**
  - Seven effects are synthesized in code: shot, hit, explosion, damage, patch, missile, bomb.
  - They are rendered once to private local storage and played as libGDX sounds.
  - Settings has SOUND on/off (default on), and any audio failure turns audio off for the session.
  - The core was re-vendored into AXIOM (component lock now at `0839bcd`).
- **Docs:** each repository's README and security docs no longer call verification `TODO`. Also updated: the
  AXIOM v1 checklist, and the Shooter's design and integration contract.

## Evidence (executed 2026-11-08)

| Check | Result |
|---|---|
| void.os | 93 unit tests (78 + 15 new: 8 signature, 4 crash/backup, 3 vendored SFX); `assembleDebug` and `assembleRelease` OK (unsigned); `check_apk_natives.py` passes both APKs. One release compile first failed on a stale incremental Kotlin cache; a non-incremental rebuild and a final normal rebuild passed |
| void.sys | 8 unit tests passed (new); `assembleRelease` OK |
| void.game | core 24 tests (21 + 3); android 8 tests (new); `assembleRelease` OK; `check_apk_natives.py` passes the release APK |
| Component lock | `tools/components.py check --upstream shooter=../void.game --upstream voidsys=../void.sys`: OK |
| New tests on the old code | The verifier and crypto tests target classes that did not exist, and the old `verify()` returned `false` after its `TODO` for every input. The F19/F20 tests assert files and manifest entries absent at `4ae9b33`. The Shooter sound tests need the new synthesizer |
| Release APK manifest (void.os) | names `AxiomApplication`, `allowBackup=true`, both backup rule files present |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 |
| Pushes | fast-forward to `main`; these repositories have no branch rules |

**Not verified:** nothing ran on a physical device. That includes safe mode, a backup and restore, sound
playback, and real certificate digests from a signed install. Signing and a pinned issuer key don't exist yet.

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F1 | void.os | PARTIAL (D-11) | signature v1 done; Play licensing and Integrity still `TODO` |
| F2 | void.game | RESOLVED_VERIFIED | verifier done; keys and issuer under D-04/D-11 |
| F17 | void.sys | RESOLVED_VERIFIED | verifier done (gate not yet called by the app) |
| F19 | void.os | PARTIAL (D-03) | guard done; device verification pending |
| F20 | void.os | PARTIAL (D-03) | layout-only backup configured; device restore pending |
| F21 | void.os | EXTERNAL_BLOCKED (D-04) | no signing custody |
| F29 | void.game | PARTIAL (D-03) | synthesized SFX; not heard on a device |
| F30 | void.game | RESOLVED_VERIFIED | owner decision: runs are not resumed |

## Stage output

```yaml
stage_id: OV-58
implementation:
  changes: [product signature v1 in three apps with reference issuer, crash-loop guard, layout-only backup,
            synthesized Shooter SFX re-vendored into AXIOM]
  excluded: [signing (D-04), device matrix (D-03), Play licensing and Integrity (D-11), icon visual review,
             Stage 27 (blocked)]
validation:
  unit: [void.os 93, void.sys 8, void.game core 24 + android 8]
  builds: [release APKs for all three (unsigned), 16 KB native checks pass]
  combination: [component lock re-synced and checked against both upstreams]
disposition: {state: PARTIAL, blockers: [D-03, D-04, D-11], next_actions: [owner decisions D-04 and D-11; device run; OV-59 needs authorization]}
```
