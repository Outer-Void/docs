# OV-60: institutional and support repositories (2026-11-08)

**State: PASSED.** The exit asks for an explicit state and a safe next action for each repository; both are
recorded below. "Passed" does not mean institutional approval: ER, IVRP and Operation: Restore are not software
qualification (plan section 5), and their claims still need independent review (D-10).

| Repository | Before | After |
|---|---|---|
| void.game | `0839bcd` | `c5ce555` |
| void.os | `d4c3dc9` | `d009469` |
| .github | `be5221d` | `6e8083f` |
| .github-private | `5ea59da` | `dbe0b6f` |
| credits | `25e8b1b` | `c0d4565` (data), then the OV-60 record |
| ov-webpages/operationrestore | `126453f` | unchanged (owner decision: record only) |
| ov-webpages/ivrp | `68dbad7` | unchanged |
| er | `ac4b89a` (GitHub metadata) | unchanged; content EXCLUDED_BY_OWNER_POLICY |

## Owner decisions (2026-11-08)

- **F50:** the public profile banner now reads "Currently in the OV-46–70 qualification program. No product is
  released yet."
- **operationrestore.net:** record only. No site change, because a push may redeploy the site and the
  Cloudflare setup is not visible to this program.

## State and safe next action

| Repository | State | Safe next action |
|---|---|---|
| `er` | Private; `main` at `ac4b89a`, last push 2026-10-27; no releases or tags; 0 open issues; no branch protection. GitHub metadata only: content EXCLUDED_BY_OWNER_POLICY | Owner arranges the independent institutional review (D-10). Nothing for this program |
| `ivrp` | Private; a reserved repository holding only a README and the licence. Its policies (`docs/legal/ivrp/`, April 2026) are plain-language drafts, not legal advice | None until the owner starts the site; clinical or legal claims need D-10 |
| `operationrestore` | Private; live at operationrestore.net, matching `126453f` file for file (index.html differs only by Cloudflare's email obfuscation). Security headers present (`X-Frame-Options`, `nosniff`, `Referrer-Policy`) | Owner: serve only the site files (F130), refresh the impact section and decide on a privacy notice for the forms (F131, D-10) |
| `.github` / `.github-private` | Profiles corrected against the live GitHub API (F50, F132) | Recheck whenever a repository changes visibility |
| `credits` | lsans-15 licence established (UNR-020 resolved); UNR-014 narrowed to the six proprietary repositories still public | Owner: the UNR-014 visibility decision; the open UNR items stay listed |

## Changes

- **lsans-15 font (F32, credits UNR-020).**
  - AXIOM Shooter draws all text with libGDX's default bitmap font, and both release APKs ship it inside the
    gdx jar, which carries no licence for it.
  - libGDX PR #6727 (commit `50bc5e2c89`, merged 2021-12-14) states that LSans is Liberation Sans, renamed
    because "Liberation" is a Reserved Font Name under the OFL. The Liberation Fonts LICENSE gives the copyright
    lines: Google 2010 and Red Hat 2012.
  - The bundled `.fnt` and `.png` have the same git blob ids as libGDX tag 1.14.2.
  - void.game and void.os now carry the OFL-1.1 notice. void.game gains `licenses/OFL-1.1.txt`, identical to
    the credits copy.
- **Notice check.** The new `tools/check_notices.py` (in both product repositories, and in CI) fails if:
  - a shipped bitmap font, or a font under `res/font`, is missing from `THIRD_PARTY_NOTICES.md`;
  - the APK holds more TrueType/OpenType fonts than the source;
  - the notices state a libGDX version other than the build's;
  - a referenced licence file is missing.
  It failed on both old notice files.
- **void.game notices (F129):** they listed libGDX 1.12.1 and tracked natives. They now state 1.14.2 with the
  natives from Maven; the shipped arm64 `libgdx.so` equals `gdx-platform-1.14.2`.
- **Profiles (F50, F132):**
  - New banner.
  - VoidForge is private, and every write class stays locked until it has device evidence.
  - Vigyl has a development-preview UI.
  - The six private products are no longer linked as if public.
  - The members' private-repository list is complete (checked against the API on 2026-11-08).
- **Credits:**
  - New asset record: `asset:font/lsans-15`.
  - `asset:libgdx-natives` updated to 1.14.2 from Maven.
  - The void-os record gains the libGDX Android backend and natives it ships.
  - UNR-014 narrowed: roughin, vigyl, void.os, void.game and void.sys are now private.

## Evidence (executed 2026-11-08)

| Check | Result |
|---|---|
| Release builds | `:android:assembleRelease` (void.game) and `:app:assembleRelease` (void.os) rebuilt from HEAD, exit 0 |
| Notice check | `check_notices.py` fails on the old notices (lsans-15 missing; void.game also says 1.12.1), passes on the new; ruff clean |
| Natives | `check_apk_natives.py` passes on the void.game release APK; `components.py check` OK in void.os |
| Font provenance | git blob ids of `lsans-15.fnt`/`.png` in gdx-1.14.2.jar equal libGDX tag 1.14.2 (`6adbdfdf`, `62658ff8`) |
| Live site | 13 operationrestore.net files compared with the repository: all assets and PDFs byte-identical; `/README.md` and `/.gitignore` return 200 (F130) |
| Visibility | `gh api orgs/Outer-Void/repos?type=all`: 32 repositories, 13 private; `constitution/repositories.md` agrees |
| ER | repository, branch, commit-date, release and tag metadata only; no content, tree or commit message read |
| Credits | `validate.py`, `render_acknowledgments.py --check`, `render_unresolved.py --check`, pytest 39 passed |
| DAT gate | before commit only `release.dirty-worktree`; after commit exit 0 (every changed repository) |
| Pushes | fast-forward to `main`. `.github` `main` is protected: the push used the owner bypass (unsigned commit, no pull request) |

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F32 | void.game, void.os | RESOLVED_VERIFIED | lsans-15 is OFL-1.1 Liberation Sans; notices and check added |
| F50 | .github | RESOLVED_VERIFIED | banner (owner decision) |
| F129 | void.game | RESOLVED_VERIFIED | notices matched libGDX 1.12.1 |
| F132 | .github, .github-private | RESOLVED_VERIFIED | stale profile facts |
| F130 | operationrestore | OPEN | the site serves README.md and .gitignore; unknown paths return 200 |
| F131 | operationrestore | OPEN (D-10) | stale impact text; no privacy notice for the forms |

## Stage output

```yaml
stage_id: OV-60
implementation:
  changes: [lsans-15 OFL notice in both products, notice check in CI, void.game notices at libGDX 1.14.2,
            profile banner and facts, credits UNR-020 resolved and UNR-014 narrowed]
  excluded: [ER content (EXCLUDED_BY_OWNER_POLICY), operationrestore site changes (owner decision),
             institutional claims (D-10), visibility of the six public proprietary repositories (owner, UNR-014)]
validation:
  builds: [void.game and void.os release APKs from HEAD]
  checks: [check_notices.py fails before and passes after, check_apk_natives.py, components.py, credits validate]
  live: [operationrestore.net file comparison, GitHub visibility via the authenticated API]
disposition: {state: PASSED, blockers: [], next_actions: [owner F130/F131, D-10 review for ER/IVRP/Restore, OV-61 needs authorization]}
```
