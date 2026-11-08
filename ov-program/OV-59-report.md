# OV-59: VoidForge and Termux Background (2026-11-08)

**State: PARTIAL.** The exit asks for device evidence per write class and never a blanket unlock. The "never a
blanket unlock" half is now enforced in code: the write barrier opens one class at a time and only with a
recorded device qualification. No class has one, because no physical device is available (D-03). No device was
attached (`adb devices` empty), and Termux Background has not run on a device either.

| Repository | Before | After |
|---|---|---|
| voidforge | `80aec1a` | `671349e` |
| termux-background | `9fc05d5` | `49164f6` |

## Owner decision (2026-11-08)

F87: VoidForge accepts the **F-Droid** Termux by default. The **GitHub** Termux build is accepted only while a
local switch in VoidForge is on; it is off at every launch. Termux publishes that build's signing key and
password in its repository, so its signature proves nothing about who built the app.

## Delta review (rule 11)

| Plan item | Result |
|---|---|
| Local confirmation UI (F5) | None existed: the app declined every request. Now a confirmation screen exists (below), but it is not reached while every write class is locked |
| Read-only device qualification | `tools/device_acceptance.py` (read-only) is unchanged. No device was attached, so the qualification is BLOCKED (D-03, F6 in OV-65) |
| Graduated write classes | One barrier covered every write class. Now it opens per class (SAFE_WRITE, PRIVILEGED, DESTRUCTIVE), and only through a reviewed `WriteQualification` entry citing a `voidforge-write-qualification v1` record. None exists |
| Integration trust (F87) | Any app named `com.termux` was trusted. Now its current signers must match a pin |
| Docs (F86) | README and DISTRIBUTION.md said "public"; the repository is private |
| Termux Background on a device | Not possible (D-03). F57 (a failed `set` left a new image with old properties) fixed; F79 triaged |

## Changes

- **VoidForge.**
  - **Confirmation broker:** `ConfirmationBroker` (core) waits on the engine thread while the device shows the
    request. The dialog shows the operation, class, risk, target, identity and source hash, and for PRIVILEGED
    or DESTRUCTIVE operations the phrase to type. Approve stays disabled until the phrase matches.
  - **Broker rules:** one request at a time; a 90-second timeout; never on the UI thread; only an answer for the
    shown request counts.
  - **Per-class barrier:** `SafetyPolicy` is per class, and its blocker names the locked class. Core tests can
    still open every class through the existing internal constructor.
  - **Termux pinning:** `TermuxTrust` requires every current signer (`apkContentsSigners`) to be the F-Droid
    signer, or the GitHub signer while the switch is on. The digests were measured from the official 0.118.3
    APKs with the new `tools/apk_signer_digest.py` and checked against Google's `apksigner`. The installed
    Termux is byte-identical to the GitHub release.
  - **Docs:** ADR-011; the write-qualification record format in `docs/testing/hardware-acceptance.md`;
    README and DISTRIBUTION.md now describe the private repository.
- **Termux Background.**
  - `set` keeps the previous image. If anything fails before the properties are committed, the exit trap
    restores it, or removes the new image and any newly created Monet marker.
  - `docs/ISSUE_TRIAGE.md` assesses issues #4, #6, #7 and #8 against 1.1.0. No reply was posted: that is the
    owner's call, after a device run.

## Evidence (executed 2026-11-08)

| Check | Result |
|---|---|
| VoidForge tests | core 96, integration 13 passed. New: `ConfirmationBrokerTest` 5, `WriteQualificationTest` 5, `TermuxTrustTest` 4. The new tests target classes absent at `80aec1a`; there, every request was declined |
| VoidForge CI task list | `assembleDebug`, `assembleRelease` (unsigned), `lintDebug`, `verifySourcePolicy` (app, core), `detekt`, `spotlessCheck`, `python3 -m unittest discover -s tools`, `distribution_policy.py`: all pass |
| Architecture rule | the existing "core knows nothing about the integration" test caught a BLUX mention in a new core comment; reworded |
| Termux Background | `tests/cli_test.sh` passes; the new rollback case fails on `9fc05d5`; `tests/package_test.sh` passes against a `.deb` rebuilt from the fixed source (the local `.deb` had been stale); `shellcheck -S warning` clean |
| Signer digests | `apksigner verify --print-certs` and `apk_signer_digest.py` agree on the installed Termux and on a debug APK. F-Droid `com.termux_1002.apk`: `228FB2CF…1C42` (CN=FDroid). GitHub `v0.118.3` arm64: `B6DA0148…E5E1` (CN=APK Signer) |
| Device | `adb devices` empty; the adb server started for the check was stopped |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 (both repositories) |
| Pushes | fast-forward to `main`; no branch rules |

The exposed termux-background keystore (F81) was never used.

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F5 | voidforge | PARTIAL (D-03) | confirmation screen and per-class barrier done; every class locked |
| F87 | voidforge | RESOLVED_VERIFIED | Termux signer pinning (owner decision) |
| F86 | voidforge | RESOLVED_VERIFIED | private-state docs; two old artifacts remain an owner follow-up |
| F57 | termux-background | RESOLVED_VERIFIED | image rollback on a failed `set` |
| F79 | termux-background | OPEN | triaged; owner reply after a device run |
| F56 | termux-background | DEFERRED | targetSdk 36 needs a device re-test |
| F6, F14 | both | EXTERNAL_BLOCKED (D-03, OV-65) | no device evidence |
| F77, F81 | termux-background | OPEN (D-13) | historical releases; exposed key never used |

## Stage output

```yaml
stage_id: OV-59
implementation:
  changes: [local confirmation screen, graduated write classes (none qualified), Termux signer pinning,
            private-state docs, set image rollback, issue triage]
  excluded: [device qualification per class (D-03), Termux Background device run (D-03), targetSdk 36 (F56),
             historical release and key decisions (D-13), GitHub issue replies (owner)]
validation:
  unit: [voidforge core 96, integration 13; termux-background cli and package tests]
  builds: [voidforge debug and release, lint, detekt, spotless, source policy]
  security: [signer digests measured from official APKs and cross-checked with apksigner; DAT gate exit 0]
disposition: {state: PARTIAL, blockers: [D-03], next_actions: [device run per write class; owner replies to #4-#8; OV-60 needs authorization]}
```
