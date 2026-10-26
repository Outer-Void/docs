# Implementation findings from documentation synchronization

Documentation passes record real implementation gaps here. They do not silently fix them. Each entry
gives the repository, the issue, its severity, how the documentation exposed it, the recommended stage, and
whether it blocks a release. Entries leave this register only when the fix is merged, with the fixing commit
noted. History stays in git.

## Pass of 2026-10-26 (after Stage 23)

| # | Repo | Issue | Severity | How documentation exposed it | Recommended stage | Blocking |
|---|---|---|---|---|---|---|
| F1 | void.os | Paid-app entitlement, Play Integrity and product-signature verification are `TODO` stubs (`EntitlementManager`, `IntegrityGate`, `SignatureVerifier`). Release paths fail closed. | Critical | The README claimed a "signed AXIOM-to-VOID.GAME launch contract" | Stage 24 (needs the owner's Play/backend decisions) | Yes: paid release |
| F2 | void.game | `SignatureVerifier` and `LaunchGate` also leave cryptographic verification as `TODO`. Release fails closed; debug builds bypass. | Critical | `docs/security.md` said "protected by a launch contract and runtime module signature gate" | Stage 26 | Yes: paid release |
| F3 | void.os ↔ void.game | ~~No single source of truth for Shooter~~ **Resolved in Stage 24:** `void.game/core` is authoritative (void.game `ad7e0ab`); AXIOM vendors it byte-for-byte at a locked commit, and `tools/components.py check` fails CI on drift (void.os `097f50d`). | High | Status audit | Stage 24 | No longer |
| F4 | void.game | ~~Two versions (root 0.1.0 vs versionName 2.0.0-dev)~~ **Resolved in Stage 24:** one version, 2.1.0-dev (void.game `ad7e0ab`) | Low | Version-consistency audit | Stage 24 | No |
| F5 | voidforge | No local confirmation UI. The app's authorizer declines every write, and the production write barrier is locked. File pull/push, backup capture, install, sideload, flash and the root/module workflows exist only in `:core`. | High (by design until hardware qualification) | Four-state status audit (core / app / mock / hardware) | After real-device acceptance | Yes: write features |
| F6 | voidforge | No real-device evidence. The Stage 23 probe was BLOCKED: no USB in the build container, no attached target, app not installed. | High | Hardware column of the status matrix | Owner-run acceptance (`tools/device_acceptance.py`) | Yes: release |
| F7 | voidforge, void.os, void.sys, void.game, roughin, vigyl | Proprietary, paid or members-only product source sits in **public** repositories (unauthenticated GitHub API returns 200). VoidForge's members-only policy is therefore not met for source. | High (policy) | Distribution-status audit | Owner action (repository visibility) | Yes: VoidForge distribution policy |
| F8 | dat | README install command pinned tag `v4.0.0`, which does not exist (tags: `v1.0.0`, `v2.0.0-alpha.1`, `v2.0.0-Stable`). The README is now corrected. | Medium | Command verification | Owner: tag 4.0.0, or keep installing from `main` | No |
| F9 | blux | No release tag or published package. Termux APT on-device installation not run. | Medium | Package and release status | Owner steps in `packaging/termux/ACCEPTANCE.md` | Yes: BLUX release |
| F10 | blux, blux-gpt | No real-provider Model API evidence (provider accounts without balance). Hard-coded provider model IDs are not checked against current catalogs. | Medium | Evidence-model audit (mock vs real-provider) | When provider access exists | No |
| F11 | .github | `docs/ecosystem-diagram.md` described five repositories that do not exist (`blux-core`, `blux-orbit`, `blux-design-system`, `blux-experience-kit`, `blux-governance`). Now replaced by a pointer to this map. | Medium (docs) | Cross-reference audit | Fixed in this pass | No |
| F12 | theresolver | Stage 00 baseline: `next` 16.1.6 critical advisory, upgrade to >= 16.4.3. Not re-verified. | High (security, unverified) | Status matrix | Product maintenance | Yes: site release |
| F13 | roughin | Stage 00 baseline: missing `greenlet` dependency. Not re-verified. | Medium (unverified) | Status matrix | Stage 28 | Unknown |
| F14 | termux-background | README said "v1.0.0 Not Operational" while `VERSION` is 1.1.0; no device has passed its checklist. README corrected. | Low | Version-consistency audit | Owner device run | Yes: release |
| F15 | jadis.toolbox | The README was an operating checklist and did not describe the repository's scripts. An identity section was added. | Low (docs) | Identity audit | Fixed in this pass | No |
| F16 | blux10k | `dotfiles/.zshrc` exports `BLUX10K_VERSION="2.0.0"`, while `VERSION` and `bin/blux10k --version` report 3.0.0 | Low | Version-consistency audit | Next blux10k change | No |
| F17 | void.sys | `security/SignatureVerifier.kt` also leaves signature verification as `TODO`: the standalone icon-pack signature gate is scaffolding | High | TODO/FIXME source audit | Stage 25 | Yes: paid release |

## Stage 24 incremental sync (2026-10-26)

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F18 | void.os | CI uploaded the debug APK from a public repository. Debug builds bypass entitlement, so unlocked builds of a paid product were downloadable. **Contained in Stage 24:** upload limited to private repositories (`097f50d`). The unauthenticated API lists no current void.os artifacts (2026-10-26), so none remain to clean up. | High | CI workflow review | Distribution blocker | **Resolved** |
| F19 | void.os | No crash-loop guard: a startup crash repeats until the user changes the default Home app | Medium (P1) | Stage 24 release matrix | Future-stage work, needs device verification | Yes: paid release |
| F20 | void.os | Backup is disabled (`allowBackup="false"`); customization is lost on device transfer | Low (P2) | Release matrix | Product decision (open question) | No |
| F21 | void.os | No release keystore or protected signing job; environment-only signing exists | High (P0) | Release matrix | Release blocker (owner) | Yes |
| F22 | void.game | Standalone Android packaging is only build-verified (debug APK with 4 native libraries). The 16 KB alignment audit, release/R8 build and device runs are not done | Medium | Stage 24 build | Stage 26 | Yes: standalone release |

## Stage 25 incremental sync (2026-10-26)

| # | Repo | Issue | Severity | Evidence | Class | Blocking |
|---|---|---|---|---|---|---|
| F23 | void.os ↔ void.sys | VOID.SYS work had been authored only inside AXIOM: 7 vector glyphs, their mappings, and the generic-drawable classification, so the standalone pack lacked them. **Resolved:** promoted to void.sys (`09cf56f`); AXIOM vendors the versioned bundle through its component lock (`4964895`). | Medium | Byte comparison of both repositories | Stage 25 | No longer |
| F24 | void.sys | The VOID.SYS app icon was a plain vector, not an adaptive icon. **Resolved:** adaptive background/foreground/monochrome layers inside the safe zone (`09cf56f`). | Low | Adaptive-icon audit | Stage 25 | No longer |
| F25 | void.sys | The standalone pack has not been device-tested in third-party launchers (Nova, Lawnchair); appfilter resolution is verified only statically | Medium | Stage 25 tests are static | Hardware pending | Yes: standalone release |

## TODO / FIXME source audit (2026-10-26)

`git grep -E '\b(TODO|FIXME|XXX|HACK)\b'` over every repository except archived BLHermes, excluding Markdown,
JSON and vendored licences, found 17 hits:

| Classification | Hits | Where |
|---|---|---|
| Genuine unfinished implementation (release blocker) | 6 | Cryptographic verification in void.os (`EntitlementManager`, `IntegrityGate`, `SignatureVerifier`), void.game (`LaunchGate`, `SignatureVerifier`) and void.sys (`SignatureVerifier`): F1, F2, F17 |
| Tool rule definition or test fixture (intentional) | 10 | blux-ca `validator/validators.py` and test; dat `analyzers/quality.py` and three tests; blux-ca-dataset legacy fixture |
| Third-party template content | 1 | blux10k `dotfiles/.p10k.zsh` (powerlevel10k generated config comment) |

One broken relative link remains by design: `dat/snapshot.md` is a historical repository snapshot dated
2026-01-21 that links to `docs/ROADMAP.md`, which was removed in Stage 03.
