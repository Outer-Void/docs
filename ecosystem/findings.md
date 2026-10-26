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
| F3 | void.os ↔ void.game | No single source of truth for Shooter: 14 shared files differ. The launcher copy has newer lifecycle, control and progression fixes (2026-10-21); `void.game` gameplay dates from 2026-05-12. | High | The READMEs called the copies "mirrored" | Stage 24 / 26 (versioned shared core with a drift check) | Yes: product |
| F4 | void.game | Two versions: root Gradle `version = "0.1.0"` and Android `versionName = "2.0.0-dev"` | Low | Version-consistency audit | Stage 26 | No |
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
