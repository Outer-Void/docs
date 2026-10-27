# After the staged rebuild: recommendations (2026-10-27)

A forward plan to go with the [reassessment input](POST_STAGED_REBUILD_REASSESSMENT_INPUT.md). Every item
starts from the frozen state recorded there; finding numbers point to
[ecosystem/findings.md](ecosystem/findings.md).

These are proposals for the owner to accept, reorder or reject. Nothing here has been started.

## Phase 0: owner unblockers

Without these, nothing can be called released.

| # | Action | Unblocks |
|---|---|---|
| 0.1 | Clear the GitHub billing lock (F49) | Every CI gate, release evidence, the automatic contract checks (F70) |
| 0.2 | Fund at least one model provider (F10) | Real Model API paths, BluxGPT, the BLOCKED Gen 0 suites (F60) |
| 0.3 | Make proprietary and members-only repositories private (F7): voidforge, void.os, void.sys, void.game, roughin, vigyl | VoidForge members-only distribution; product source protection |
| 0.4 | Fix the Cloudflare tunnel config typo (F53) and the custom domain (F54) | Resolver bot and website |
| 0.5 | Remove the stale `blux()` function from `~/.zshrc.local` (F65) and the stale `ANDROID_HOME` lines in `~/.zshrc` | Running `blux` and Android builds by name on the owner's machine |
| 0.6 | Make one Android phone available for testing (ideally two: a Pixel and a Samsung) | Every device checklist, VoidForge hardware acceptance, Termux Background RC |

## Phase 1: make releasing real (platform)

1. **Pilot one release end to end.** DAT is the best candidate: it is the most mature and has no device
   dependency. Do it with CI green, a signed tag, notices, a ledger entry and a matrix status change. That turns
   the lifecycle rules into a routine the other components can follow.
2. **DAT target policies (F76).** Commit justified suppressions for the triaged fixtures, so DAT's raw gate passes
   across the organization and stays meaningful.
3. **Contract hygiene.**
   - Move blux-system to blux-sdk 0.2.0 (F68).
   - Give `ax` a non-interactive executable alongside the sourced function (F72).
   - Retire or rename the misleading historical tags (F69).
4. **Decide BLHermes parity scope.** 15 features are not started and 10 are in progress. For each, choose migrate,
   drop or defer, so the parity matrix describes intent rather than a backlog.
5. **Python packaging.**
   - Publish the engines (blux-sdk, CogA, cA, DAT, LRC, GOD, BLUX System) to a private index.
   - Pin consumers by version instead of git SHA.

## Phase 2: standalone apps to release-ready

Each app keeps BLUX optional or excluded, as the constitution requires.

### VOID.SYS icons
Today there are 590 SVG icons in `icons/`, with a spec (`docs/icon-spec.md`, `docs/v2-icon-system.md`). The app
builds, but there are no automated tests and signature verification is a stub (F17).
1. **Icon linter in CI.** Check the grid and keyline, stroke weight, palette tokens and viewBox, and fail on drift
   from `icon-spec.md`.
2. **Coverage report.** Compare the most-installed Android packages with the icon-pack mapping, and close the
   largest gaps first.
3. **Android requirements.** Adaptive icons with monochrome layers (Android 13 themed icons), plus a raster export
   pipeline whose outputs are checked by checksum.
4. **Tests.** Add the first test suite: manifest and mapping integrity, plus a render smoke test of every icon.
5. **Signature gate.** Implement real signature verification (F17), then run `docs/device-testing.md` on a device
   and produce store screenshots.

### AXIOM Shooter graphics
Today the core has 21 tests and builds, but there are almost no graphic assets (five XML files), no audio, and
signature verification is a stub (F2).
1. **Art direction.** An art-direction section in `docs/v2-game-design.md` covering palette, silhouettes, motion
   language and the void aesthetic shared with the launcher.
2. **Assets.** A sprite and atlas pipeline (source → atlas → checksum lock), particle and VFX presets, and an
   audio set with a mixer.
3. **Frame budget.** Measure frame time on a mid-range device as a release gate.
4. **Release path.** Finish F2, keep the hidden Easter-egg entry in the launcher, and lock the vendored copy as
   today.

### AXIOM Launcher UI design (void.os)
Today there are 78 unit tests and the launcher builds. Assets come from VOID.SYS (a raster set per density).
`docs/visual-system.md` and `docs/design/` exist. The F1 verifications are stubs, and the Stage 24 gate fails.
1. **Design tokens.** Turn `visual-system.md` into tokens for colour, type, spacing and motion, shared with
   VOID.SYS and the Shooter.
2. **Accessibility pass.** TalkBack labels, font scale up to 200%, contrast, and reduced motion.
3. **Gate fixes.** Implement entitlement, Play Integrity and signature verification (F1), run the device matrix,
   provision the release keystore, and complete the legal review. That closes the Stage 24 gate.
4. **Stage 27 afterwards.** Only then reopen Stage 27, starting with the usefulness/complexity/reliability review.
   Natural-language app search is the likeliest feature to pass it.

### Vigyl UI and functionality
Today the backend API passes 78 tests: auth, groups and invitations, tasks, escalation, timeline, messages,
export and delete. `frontend/` is empty.
1. **Frontend stack.** A frontend on the same stack as Roughin (React PWA) to share components and the auth client.
2. **First flows.** Sign-in and invitation, a caregiver group dashboard, the task lifecycle, escalation alerts and
   the timeline.
3. **Accessibility and notifications.** Accessibility is required for caregivers; add push notifications for
   escalations.
4. **Tests and staging.** Frontend tests from the start, then a staging deployment with backups (scripts exist)
   and the release checklist in `docs/release-checklist.md`.

### Roughin UI and functionality
Today the backend passes 91 tests. The frontend has 33 source files, no tests (F37), dependency advisories that
need majors (F36), no staging run of Stripe or R2 (F35), and a metadata probe outside production (F73).
1. **Upgrades.** Move to vite 8 and react-router 7 (F36), then add component tests and Playwright flows (F37).
2. **Offline behaviour.** Offline and poor-network behaviour for field use: a queue for job notes and photos.
3. **Staging.** A staging deployment with Stripe test mode and a real R2 bucket (F35), and
   `AWS_EC2_METADATA_DISABLED` outside production (F73).

### Other standalone components
- **Termux Background.** Device RC checklist, target SDK 36 (F56), an offline signing key in CI.
- **Resolver.** Align the version with tag v4.0 (F48), then run the release gate with live secrets (after 0.4).
- **JADIS Toolbox.** Run it natively in Termux and Debian, and publish a package.
- **bluxai.app.** Decide whether to deploy it as the hosted workspace (it would need a UI) or keep it
  experimental.

## Phase 3: VoidForge fully operational for developer support

Today VoidForge has :core (86 tests) and :integration (9), and read-only diagnostics work. Writes are locked in
production. The integration authorizer declines every write because there is no local confirmation screen.
Hardware acceptance is BLOCKED, and the repository is public.

1. **Distribution (after 0.3).** Members-only distribution as `docs/DISTRIBUTION.md` describes: a private
   repository, an offline signing key, a reviewer-protected release workflow and a private update channel.
2. **Hardware acceptance lane.**
   - Run `tools/device_acceptance.py` on the reference devices for every read-only row: device list, inspect,
     logcat, shell diagnostics, packages and fastboot vars.
   - Publish the results in `docs/testing/acceptance/`.
3. **Local confirmation screen.** The missing piece for any write. It should show the person at the device the
   operation, the target and hashes, and for destructive classes require a typed phrase.
4. **Unlock writes one class at a time,** each behind its own acceptance rows:
   1. SAFE_WRITE: file push, APK install, reboot.
   2. Sideload.
   3. The backup-gated flash workflow.
   4. Root and Magisk last.
5. **Developer workflow.**
   - Wireless debugging pairing (deferred today).
   - A real PTY terminal.
   - Continuous logcat.
   - Rescue Point capture.
6. **Ecosystem link.** Ingest VoidForge receipts (`vf-…`) into BLUX System, so `ax inspect` shows device operations
   next to BLUX operations. `blux agent --tools device.*` then becomes a supported diagnose → evidence →
   authorized-fix loop, with VoidForge still the only authority.

## Phase 4: the bigger vision

- **Intelligence flywheel.**
  - Once providers are funded, measure the BLOCKED Gen 0 suites.
  - Feed `blux_training` from receipts and DAT verdicts that are eligible under the data policy; never private
    data.
  - Revisit the four Generation 1 specialists that were BLOCKED on data.
  - A native model is integrated only if it beats Gen 0 on the permanent holdout.
- **One design system across products.** Shared tokens and components for the launcher, VOID.SYS, the Shooter,
  Roughin, Vigyl, BLUX App and bluxai.app, kept in a repository of its own (unlike the fictional
  `blux-design-system`).
- **BLUX App as mission control.** Operations, receipts, devices (VoidForge) and release state in one local view.
- **A release train.** A quarterly cadence in which each component either releases or records why not, with the
  ledger and matrix updated automatically by docs CI.
- **Observability.** Opt-in, privacy-preserving health signals for the hosted products (Roughin, Vigyl,
  bluxai.app), with nothing sent from local tools.

## Suggested order

1. **Phase 0.** Owner actions, which can happen in parallel.
2. **Phase 1.** The DAT pilot release and F76.
3. **Fastest path to product revenue.** Roughin UI and staging, Vigyl UI.
4. **Launcher family.** The Stage 24 gate (F1, F2, F17 and devices), then VOID.SYS icons and Shooter graphics,
   then Stage 27.
5. **Phase 3.** VoidForge, in parallel once a device is available.
6. **Phase 4.** Continuous.
