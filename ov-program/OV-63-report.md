# OV-63: DAT pilot release and shared release machinery (2026-11-09)

**State: PARTIAL.** The exit asks for a signed, installable DAT with release receipts. That build exists:
- `4.0.0-pilot.1`, built from DAT `eff11ee` in two fresh clones, byte-identical;
- checked by tests and scanners other than DAT, installed into empty environments;
- signed with a new release key, its receipt anchored in BLUX System;
- verified again from a third clone.

It is not a release:
- CI still cannot start (D-01, run 42672703427 at `eff11ee`: "account is locked due to a billing issue");
- the release policy needs green CI on the release commit;
- by owner decision, no tag and no GitHub release were made;
- the DAT tag workflow is rewritten but cannot run.

| Repository | Before | After |
|---|---|---|
| dat | `24a7290` | `eff11ee` (owner bypass: protected `main`) |
| docs | `28a0006` | this commit |

## Owner decisions (2026-11-09)

- **Signing (D-04, for DAT).** A dedicated Ed25519 release key generated on the owner's machine:
  - format and namespace: SSH signature format (`ssh-keygen -Y sign`), namespace `outer-void-release`;
  - private key: outside every repository (`~/.config/outer-void/release-keys/`, mode 600, no passphrase);
  - public key: `releases/allowed_signers`, fingerprint `SHA256:Puur0bR6kbQK+12BgzoUQ7gnoa1z972W966bRqumEyc`;
  - the exposed termux-background key is not used;
  - Android signing custody is still open.
- **Publication.** Local pilot. No tag, no GitHub release, `release_status` stays `NOT_RELEASED`.
- **F113.** Store heads are anchored in signed release receipts. Signing every store head on write is out of scope.

## Delta review (rule 11)

| Item | Result |
|---|---|
| F76 target policies | Reused (OV-49). DAT's gate passes at `eff11ee` |
| DAT's own CI and wheel check | Reused as design (`scripts/verify_wheel.sh`); replaced for the pilot by the fresh-clone pipeline |
| DAT tag workflow | **F140**: it published a GitHub release after DAT's own audit only, no tests; it signed only `if: env.GPG_PRIVATE_KEY != ''`, and DAT has no secrets. A version tag would have published unsigned, self-certified artifacts |
| Non-self-certification (deep audit §6) | The pilot counts only independent checks; DAT's verdict on itself is recorded with `counted: false` |
| Reproducibility | The wheel was reproducible; the setuptools sdist was not (checkout mtimes and the local user in the tar). The tool normalizes sdists |
| Independent scanners | bandit flagged XML parsing in the Android analyzer. A hostile-manifest drill found **F139** |
| F113 | Decided (above) and implemented in the tool |

## Changes

**DAT `eff11ee`:**
- **F139.** `android.manifest-unparseable` is now security/high. It was quality/medium, which `dat security`
  drops, so a `<!DOCTYPE …>` line in front of a debuggable manifest made `dat security --gate` pass with no
  finding. DTDs are still refused.
- **F140.** `release.yml` now only verifies: read-only permissions, the tests, then
  `release_pipeline.py verify --rebuild` against the signed record in docs. It never signs or publishes.
- The README "Releases" section, CHANGELOG and `docs/FINDINGS.md`.

**docs: shared release machinery (`tools/release_pipeline.py`):**
- **`pilot`:**
  - builds from two fresh clones at the spec's full commit, with a pinned toolchain and `SOURCE_DATE_EPOCH` =
    the commit time; sdists are normalized, and the two builds must be identical;
  - runs counted checks: test suite and lint in a fresh environment; wheel and sdist installed into empty
    environments with smoke commands; bandit, detect-secrets (git-tracked files) and pip-audit, whose accepted
    results are listed in the spec with reasons;
  - writes `SHA256SUMS` and `receipt.json`;
  - stores the artifacts and an operation receipt in a BLUX System store and writes its head into the receipt;
  - signs both files.
- **`verify`:**
  - checks signatures against `releases/allowed_signers`, sums against the receipt, and that the receipt says PASS;
  - optionally checks the artifact bytes, the store anchor (`blux-system verify --expect-head`) and a rebuild
    from a checkout.
- **Records:**
  - `releases/README.md` (layout, key, rotation, verification);
  - `releases/dat/4.0.0-pilot.1/` (spec, sums, receipt, signatures).

## The pilot

| Check | Result |
|---|---|
| Reproducible build | Two fresh GitHub clones at `eff11ee`, byte-identical; all three runs gave the same hashes |
| Tests | 98 passed, 0 skipped (`DAT_REQUIRE_BLUX_SDK=1`) |
| Lint | `ruff check`, `ruff format --check`, `mypy` pass |
| Wheel install | `--no-index --no-deps` into an empty environment; 6 smoke checks pass (version, schemas, planted token fails the gate, clean tree passes, F139 manifest fails, missing target exits 3) |
| sdist install | Same 6 smoke checks pass |
| bandit 1.8.6 | 0 blocking; 1 accepted (B314, Android manifest parsing, see F139); 8 low |
| detect-secrets 1.5.0 | 12 hits, all accepted after review: `snapshot.md` (historical example values) and test fixtures. Values never recorded |
| pip-audit 2.9.0 | No vulnerabilities; DAT has no dependencies (`outervoid-dat` itself is not on PyPI) |
| DAT on itself | Gate exit 0; recorded, not counted |
| Evidence | 2 artifacts and receipt `rcpt_01M70TWPTCN37DSYTZMCAAS1ZX` in the evidence store (9 records, every run kept); head `5538fdc8…3370` in the signed receipt |

| Artifact | Size | SHA-256 |
|---|---|---|
| `outervoid_dat-4.0.0-py3-none-any.whl` | 61,855 | `c3869b5f4f5d49cc861f2075a857e4c3ad6913152cdd176e509b4b1e44f3bc2f` |
| `outervoid_dat-4.0.0.tar.gz` | 65,598 | `6387b305eef56d4fce4cb919bef2a511d25d7229228d8ae3eeaf4f5b31b07cde` |

**Pilot run 1 failed.** detect-secrets scanned the cache folders that mypy and ruff had just written into the
clone, and flagged their tags. The tool refused the build (FAIL), recorded a failed receipt in the evidence
store and signed it. Now only git-tracked files are scanned, with a test. Run 2 passed. Run 3 is the recorded one:
it repeated run 2 after the spec's accepted detect-secrets entries were renamed (`hashed_secret` → `value_sha1`,
because DAT's gate on docs read that key as a credential), so the recorded spec is exactly the one that ran.

**Independent verification:**
- **The tool's own check:** `verify` from a third fresh clone passes on both signatures, the sums, the artifact
  bytes, the store anchor and the rebuild.
- **Plain consumer path:** `ssh-keygen -Y verify` and `sha256sum -c` pass. The wheel installs with `--no-index`
  into a new environment and gates LRC.

The artifacts are kept at `~/.local/share/outer-void/releases/dat/4.0.0-pilot.1/`. Anyone can reproduce them
with `verify --rebuild`.

## Evidence (executed 2026-11-09)

| Check | Result |
|---|---|
| Old-code check | `test_ov63_a_manifest_dat_cannot_parse_fails_the_security_gate` (3 cases) and `test_release_workflow.py` (3) fail on `24a7290`; the control case passes on both |
| DAT suite | 98 passed; ruff, format, mypy clean; the five Android repositories still pass `dat security` with F139 |
| Release tool tests | 11 passed: sdist normalization, spec pinning, scanner verdicts, signature/tamper/wrong-key/FAIL-receipt, the F113 store-rewrite drill, tracked files only, and the recorded release verifies against the published key |
| BLUX boundary | blux `tests/integration/test_dat.py` 5 passed against `eff11ee` (`BLUX_REQUIRE_DAT=1`). The integration pin stays `24a7290` until the next matrix rerun |
| Contracts | `check_contracts.py`: ok, 0 breaking, 1 INFO (DAT commit move); lock not rewritten, to stay consistent with the OV-62 integration pins |
| Docs | findings, status matrix, constitution, export, integration matrix `--check` pass; docs tests 24 passed |
| DAT gate | DAT before commit only `release.dirty-worktree`, after commit exit 0 |

**Not covered:**
- Python 3.11 and 3.12: only 3.13 is installed here. CI's matrix would cover them, but CI is blocked (D-01).
- The tag workflow: it has never run (D-01).

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F113 | blux-system | RESOLVED_VERIFIED | release evidence heads anchored in signed receipts (owner decision) |
| F139 | dat | RESOLVED_VERIFIED | an unparsed manifest no longer passes the security gate |
| F140 | dat | RESOLVED_VERIFIED | the tag workflow cannot publish unsigned, self-certified releases; the workflow run waits on D-01 |

## Stage output

```yaml
stage_id: OV-63
implementation:
  changes: [shared release pipeline (pilot, verify), release key and allowed_signers, DAT pilot 4.0.0-pilot.1,
            F139 manifest rule, F140 verify-only tag workflow, F113 store-head anchor]
  excluded: [tag and GitHub release (owner decision), CI (D-01), Python 3.11/3.12 locally, Android signing (D-04)]
validation:
  reproducibility: [two fresh clones identical; second run identical; rebuild from a third clone identical]
  independent: [tests, lint, installs, bandit, detect-secrets, pip-audit; DAT self-check not counted]
  regression: [new DAT tests fail on 24a7290]
disposition: {state: PARTIAL, blockers: [D-01], next_actions: [tag and publish after D-01; OV-64 needs authorization]}
```
