# Outer Void post-execution deep audit (2026-11-06)

**Scope.** This is a read-only engineering audit against the locked [OV-46 → OV-70 master plan](MASTER-PLAN.md). It
changes no plan, product source, security policy, deployment setting, release asset or external account. It wrote
only this report, the findings register and the status matrix it regenerates, and the credits record.

**Evidence labels:**
- **VERIFIED**: executed or inspected in this audit, with the command and result in the [appendix](#19-evidence-appendix).
- **REPRODUCED_FAILURE**: a defect reproduced here against the current HEAD.
- **IMPLEMENTED_UNVERIFIED**: the code exists, but nothing here proves its behaviour.
- **HISTORICAL_EVIDENCE**: an earlier result, cited with its original date and commit, still applicable because
  nothing it covers has changed.
- **EXTERNAL_BLOCKED**, **BLOCKED_LOCAL_ENVIRONMENT**, **OWNER_DECISION_REQUIRED**, **NOT_INSPECTED**: as named.

## 1. Executive engineering verdict

**Nothing in Outer Void is releasable today, and nothing has been released.** That verdict is not from lack of
code. The deterministic platform and the two web products are substantially implemented, and their local
evidence is current. What holds every release back is concentrated in a few places:

1. **Hosted CI cannot start.** It is still locked by billing on 2026-11-06 (F49, D-01), so no release gate that
   needs CI can pass.
2. **Paid Android products have no working purchase verification.** Launcher and Shooter fail closed. VOID.SYS is
   worse than the record said: its verifier is never called, so the icon pack is **not gated at all** (F17,
   sharpened here).
3. **No real-service evidence exists.** That covers PostgreSQL, Stripe, R2, notification delivery, Telegram and
   Cloudflare, plus every Android device test. Each waits on an owner decision or on hardware.
4. **The audit found three new defects in BLUX's receipt path**, two of them reproduced:
   - a receipt is dropped when BLUX System is down and the operation carried an artifact, which every model call
     does (F83);
   - a concurrent spool is lost during `flush()` (F84);
   - nothing ever retries the outbox (F85).

   They break the constitution's "no hidden data loss" rule for the evidence authority, and they belong to OV-52.

**What does work.** These were verified today at current HEADs:
- the six BLUX ↔ engine hard gates (CogA, cA, DAT, LRC, GOD, BLUX System) with skipping disabled: 45 passed;
- `ax` routing and its exit codes;
- the contract compatibility check;
- DAT's release gate in 30 of 31 repositories;
- Roughin's full backend at its final commit (100 passed);
- every tracked Python and shell file parses.

Vigyl's accessibility work at `5637f3d` stands as recorded today. F43 stays **PARTIAL** until a real screen reader
and a real phone have been used.

**Next stage:** OV-50, as the head of the platform track. F83–F85 are to be fixed in OV-52. See
[section 18](#18-exact-next-executable-assignment). No stage was started by this audit.

## 2. Audit scope and limitations

| Area | Depth | Notes |
|---|---|---|
| All 31 accessible repositories | VERIFIED: HEAD, branch, worktree, remotes, fetched `origin`, changes since the OV-46 baseline, DAT gate, syntax parse | Sweep in [§19](#19-evidence-appendix) |
| `er` | GitHub metadata only | `EXCLUDED_BY_OWNER_POLICY`. `secret-project/` was not opened, read or indexed |
| Source review | Targeted, not line-by-line | Covered: Android entitlement and signing paths; VoidForge authorization and endpoint; BLUX subprocess provider, receipt sink and executor; `ax` router; Roughin money and tenancy paths; Resolver tunnel and site configuration; Termux Background bridge |
| Android builds (Gradle) | **Not re-run**: HISTORICAL_EVIDENCE | No Kotlin, Java or Gradle file changed since Stage 26 and 44 (2026-10-26/27). Only `.dat/policy.json` and README commits since |
| BLUX unit suite (594) and engine suites | **Not re-run**: HISTORICAL_EVIDENCE | No source change since Stage 44 (2026-10-27). The cross-repository hard gates *were* re-run |
| Physical devices | **Not run**: EXTERNAL_BLOCKED (D-03) | Nothing here is device evidence |
| PostgreSQL | **Not run**: BLOCKED_LOCAL_ENVIRONMENT | Not attempted under PRoot. No SQLite result is offered in its place |
| Real providers | **Not run** (D-02, D-05, D-06, D-07) | No paid or authenticated external calls. Only plain HTTP GETs to the public Resolver domain and public GitHub release assets |
| Not inspected in depth | NOT_INSPECTED | blux-gpt, blux-app, bluxai.app, datasets, jadis.toolbox, blux10k, operationrestore, ivrp, `.github`, `.github-private`: sweep, DAT and syntax only. OV-50 scope items (tool approvals, path confinement, hooks) rely on Stage 44 evidence. Roughin's UI has had no browser accessibility pass |
| blhermes-agent | Archived upstream fork | Swept; its DAT gate fails (1144 blocking, as an unmaintained fork). Not a release target |

## 3. Repository inventory

32 repositories on GitHub (13 private), matching the OV-46 constitution. All 31 local checkouts are on `main`,
clean, with one remote, and level with the fetched `origin/main` (2026-11-06).

| Repository | GitHub | Local HEAD | origin/main | Clean | Commits since OV-46 baseline | DAT gate today |
|---|---|---|---|---|---|---|
| `blux` | public | `56c9b76` | `56c9b76` | yes | 1 (1 file) | pass |
| `blux-system` | public | `f7f8ede` | `f7f8ede` | yes | 1 (1 file) | pass |
| `blux-gpt` | public | `0175196` | `0175196` | yes | 1 (1 file) | pass |
| `blux-coga` | public | `3dc86fa` | `3dc86fa` | yes | 0 | pass |
| `blux-ca` | public | `7cb953a` | `7cb953a` | yes | 0 | pass |
| `dat` | public | `487e1d4` | `487e1d4` | yes | 0 | pass |
| `lrc` | public | `443e532` | `443e532` | yes | 0 | pass |
| `god` | public | `ad6f0c4` | `ad6f0c4` | yes | 0 | pass |
| `blux-app` | public | `dca88bf` | `dca88bf` | yes | 1 (1 file) | pass |
| `blux-ca-dataset` | public | `9893d58` | `9893d58` | yes | 1 (1 file) | pass |
| `blux-coga-dataset` | public | `e8216be` | `e8216be` | yes | 1 (1 file) | pass |
| `axiom` | public | `ed079e8` | `ed079e8` | yes | 0 | pass |
| `blux10k` | public | `e2e9f58` | `e2e9f58` | yes | 0 | pass |
| `jadis.toolbox` | public | `253c386` | `253c386` | yes | 0 | pass |
| `voidforge` | private | `80aec1a` | `80aec1a` | yes | 1 (1 file) | pass |
| `void.os` | private | `4ae9b33` | `4ae9b33` | yes | 1 (1 file) | pass |
| `void.sys` | private | `3f2b7aa` | `3f2b7aa` | yes | 1 (1 file) | pass |
| `void.game` | private | `b56c1ae` | `b56c1ae` | yes | 0 | pass |
| `roughin` | private | `61c4b47` | `61c4b47` | yes | 5 (36 files) | pass |
| `vigyl` | private | `5637f3d` | `5637f3d` | yes | 8 (46 files) | pass |
| `resolver` | private | `aae88c2` | `aae88c2` | yes | 0 | pass |
| `ov-webpages/theresolver` | private | `49dbeff` | `49dbeff` | yes | 0 | pass |
| `termux-background` | public | `9fc05d5` | `9fc05d5` | yes | 2 (1 file) | pass |
| `ov-webpages/bluxai.app` | private | `e894ac6` | `e894ac6` | yes | 1 (1 file) | pass |
| `ov-webpages/operationrestore` | private | `126453f` | `126453f` | yes | 0 | pass |
| `ov-webpages/ivrp` | private | `68dbad7` | `68dbad7` | yes | 0 | pass |
| `credits` | public | `c51d767` | `c51d767` | yes | 9 (13 files) | pass |
| `docs` | public | `863d6f0` | `863d6f0` | yes | 9 (22 files) | pass |
| `.github` | public | `be5221d` | `be5221d` | yes | 0 | pass |
| `.github-private` | private | `5ea59da` | `5ea59da` | yes | 0 | pass |
| `secret-project/er` | private | EXCLUDED_BY_OWNER_POLICY | `ac4b89a` (API, unchanged since 2026-10-27) | — | — | not run (policy) |
| `blhermes-agent` | public, archived | `dc8abc1` | `dc8abc1` | yes | 0 | fail (unmaintained fork) |

The `docs` and `credits` rows show their state before this report's own commits.

## 4. Current HEAD versus last verified commit

Rule 11: reuse evidence whose inputs are unchanged, rerun what changed, and never present old results as new.

| Repository | Last verified (matrix) | Changed since | Evidence status |
|---|---|---|---|
| blux | `8d989de` (2026-11-04) | `.dat/policy.json` only | Unit suite: HISTORICAL_EVIDENCE (594 passed at `ba160c3`, Stage 34-36; Stage 44 at `51134af`, 2026-10-27). **Hard gates re-run today at `56c9b76`: 45 passed** |
| blux-system, blux-gpt, blux-app, datasets, bluxai.app, voidforge, void.os | Stage 44 / OV-49 | `.dat/policy.json` only | HISTORICAL_EVIDENCE still applies. Tree-walking suites were re-run with the policy present in OV-49 (2026-11-05) |
| blux-coga, blux-ca, dat, lrc, god, jadis.toolbox, void.game, resolver, theresolver, blux10k, axiom, `.github*`, operationrestore, ivrp | Stage 44 or later | none | HISTORICAL_EVIDENCE applies. `axiom` re-run today: 13 passed |
| void.sys | `09cf56f` | README version line | HISTORICAL_EVIDENCE (Stage 25 build and tools). Source re-read today |
| termux-background | `75cfb97` | README only | HISTORICAL_EVIDENCE (Stage 32, 2026-10-27) |
| roughin | `61c4b47` | none since OV-55 | Was: suite 100 at `0a794ac`, auth 23 at `61c4b47`. **Full backend re-run today at `61c4b47`: 100 passed** (SQLite) |
| vigyl | `5637f3d` (2026-11-06) | none | VERIFIED today, same session (backend 108 at `875b006`, unchanged; frontend 40; browser pass) |
| docs, credits | — | this program's records | Generators and validators re-run before this commit |

## 5. Architecture and authority

```
                        owner decisions (D-01 … D-14)
                                    │
   ┌──────────────── BLUX (routes; optional everywhere) ────────────────┐
   │  runtime/blux_runtime/executor.py ── policy ── approvals ── hooks  │
   │        │ subprocess JSON protocol (subprocess_provider.py)         │
   │        ├──► CogA (reasons) ──► cA (constructs) ──► DAT (judges)    │
   │        ├──► LRC (creates and migrates repos)  ◄── GOD (discovers)  │
   │        └──► receipts ──► BluxSystemSink ──► blux-system CLI        │
   │                          (outbox on failure)   (records)           │
   └─────────────────────────────────────────────────────────────────────┘
   ax (axiom/cockpit/ax/router.py): os.execv to the engine; exit 69 if missing
   Products (no BLUX code path):  Roughin · Vigyl · Resolver + site · Termux Background
   Android family:  AXIOM Launcher (void.os) ⊃ bundled Shooter (hidden) · VOID.SYS · standalone Shooter
   VoidForge: devices; local typed-phrase authorization; BLUX/ax endpoint off at every launch
```

**Verified authority properties:**
- **One authority per role.** No circular dependency. BLUX imports no engine code: the boundary is subprocess
  JSON (`subprocess_provider.py:1-12`) and the `blux-system` CLI (`system_sink.py:1-11`).
- **Exit codes propagate.** `ax` replaces itself with the engine (`router.py:161`), so the engine's exit code is
  `ax`'s, and a missing engine exits 69 (`router.py:37`).
- **Products don't depend on BLUX.** No BLUX code reference in Roughin, Vigyl, Resolver, the Resolver site, void.os,
  void.sys, void.game or Termux Background.
- **VoidForge's BLUX link is optional and bounded.** The endpoint is off at launch and accepts only its own UID and
  Termux's (`IntegrationEndpoint.kt:13-60`). Requests can only ask; write authority stays with `LocalAuthorizer`.
- **Shooter stays hidden.** It can be reached only from Home (`ShooterAccessPolicy.kt:5`) and is absent from
  `SettingsScreen.kt`. The bundled game activity is `exported="false"`.

## 6. Cross-repository dependency and compatibility

| Boundary | Result | Evidence |
|---|---|---|
| BLUX → CogA, cA, DAT, LRC, GOD, BLUX System | **VERIFIED**: 45 passed, 2 skipped (real-provider paths only) with every `BLUX_REQUIRE_*=1` | Runs the engines from their workspace checkouts at current HEAD (editable installs) |
| CogA → cA → DAT, forced rejection and bounded repair | **VERIFIED** (Stage 07 hard gate within the 45) | `tests/integration/test_ca.py` |
| GOD → LRC → DAT → BLUX System | **VERIFIED** (Stage 05 hard gate) | `tests/integration/test_god.py` |
| Contract and SDK compatibility | **VERIFIED**: 0 breaking, 0 invariant failures, 5 informational commit moves (all policy-only) | `tools/check_contracts.py --workspace ~/ov` |
| `ax` routing and exit codes | **VERIFIED**: 13 passed | `axiom/tests` |
| Receipt persistence when BLUX System is down | **REPRODUCED_FAILURE** (F83, F84). F85 verified by source | §7 |
| Credits and provenance | **VERIFIED** before commit | `credits/tools/validate.py --org-root ~/ov` |
| Hidden mandatory BLUX dependency | None found | §5 |
| Stale generated artifacts | None. BLUX `build/` and `*.egg-info` exist locally but are git-ignored and untracked. Every docs generator passes `--check` | §19 |

**DAT non-self-certification (reminder for OV-63).** DAT's own repository passes DAT's own gate today. That is
self-judgement and cannot count as an independent verdict. The OV-63 pilot must use independent checks: tests,
package install and a second scanner.

## 7. Source-level findings

### 7.1 New in this audit

| ID | Severity | Status | Evidence | Summary |
|---|---|---|---|---|
| F83 | Medium | OPEN, OV-52 | **REPRODUCED_FAILURE** | `executor.py:445-450` calls `emit_artifact()` and then `emit(receipt)` inside one `try`. If BLUX System is unavailable, `emit_artifact` raises `SINK_UNAVAILABLE` and the receipt is **neither stored nor spooled**. That contradicts `system_sink.py:107`, which says the receipt is still spooled. Every `model.generate` call attaches an artifact (`models/capability.py:135-147`), so model and provider-failure receipts are the ones lost. The control case without an artifact spools correctly |
| F84 | Medium | OPEN, OV-52 | **REPRODUCED_FAILURE** (simulated interleaving) | `system_sink.py:127-147` `flush()` reads the outbox, re-sends, then `os.replace`s it with no lock. A receipt spooled meanwhile by another process (`_spool`, lines 97-102) is deleted |
| F85 | Low | OPEN, OV-52 | VERIFIED (source search) | `flush()` is called only by tests. No CLI or entry point retries the outbox, so spooled receipts never reach BLUX System. The CLI does report "not recorded" (`cli/blux_cli/direct.py:441`). Also, `_retryable` (lines 94-95) retries every `SINK_*` code, including `SINK_REFUSED`, forever |
| F86 | Low | OPEN, OV-59 | VERIFIED | `voidforge/README.md` and `docs/DISTRIBUTION.md` say the repository is **public**; GitHub says **private**. The two old 983-byte workflow artifacts that DISTRIBUTION.md says to delete still exist (now private) |
| F87 | Low | OPEN, OV-59 | IMPLEMENTED_UNVERIFIED (source) | `IntegrationEndpoint.kt:56-58` trusts the UID of whatever app is installed as `com.termux`, by package name only. If the real Termux is absent, another app under that name could run READ_ONLY operations (properties, packages, logcat) while the endpoint is on. Writes remain locally authorized |
| F88 | Low | DEFERRED, OV-57 | VERIFIED | Resolver site lint toolchain: 8 moderate advisories (typescript-eslint and eslint-config-next, minimatch). Development only: `npm audit --omit=dev` exits 0 |

**Recommended fixes:**
- **F83:** attempt `emit(receipt)` unconditionally, in its own `try` after the artifact loop, and record which
  artifact ids failed.
- **F84:** take an exclusive file lock (`fcntl.flock`) on a sidecar lock file in both `_spool` and `flush`, or
  spool one file per receipt.
- **F85:** add `blux receipts flush`, or flush after the next successful emit, and remove `SINK_REFUSED` from the
  retryable codes.
- **Tests:** add a two-process regression test for each.

**Re-checked and not recorded as defects:**
- **Roughin invoice numbering** uses `count + 1` (`invoices.py:66-67`). That would be unsafe if invoices could be
  deleted, but deleting a job that has invoices is refused (`jobs.py:68-69`), and invoices go only with the whole
  account (`users.py:91-92`).
- **axiom ShellCheck "errors" at `py_venv.sh:11`** are valid ksh syntax inside a ksh-only branch.
- **BLUX subprocess output** is buffered before the 16 MiB check (`subprocess_provider.py:84-108`). That is a
  theoretical memory concern with trusted local providers only, so it isn't raised.

### 7.2 Reassessed high-priority findings

| ID | Status | Evidence today | Source facts |
|---|---|---|---|
| F1 AXIOM entitlement and integrity | **OPEN**, fail-closed | VERIFIED (source) | `SignatureVerifier.kt:38-39` and `IntegrityGate.kt:9-11` return false in release, and `EntitlementManager.kt:31-35` yields IntegrityFailed or Unlicensed. **The whole launcher shows `LockedScreen` in release** (`MainActivity.kt:216-221`). Debug builds bypass. Blocked on D-11 |
| F2 Shooter verification | **OPEN**, fail-closed | VERIFIED (source) | `voidgame/security/SignatureVerifier.kt:31-32` returns false. `StandaloneEntitlementGate` is wired (`AndroidLauncher.kt:27`) |
| F17 VOID.SYS verification | **OPEN**, and **not** fail-closed | VERIFIED (source) | The verifier returns false (`SignatureVerifier.kt:30-31`), but `SignatureGate` and `SignatureVerifier` are referenced nowhere outside their package. `IconPackActivity` and the icon resources are served ungated. The README's "fails closed" is inaccurate for the product |
| F5 VoidForge local authorization UI | **OPEN**, fail-closed | VERIFIED (source) | `Workstation.kt:40-44` always declines. The engine is sound: grants are single-use, scope-bound and expiring (`Authorization.kt:89-123`) |
| F6 Physical device qualification | EXTERNAL_BLOCKED (D-03) | — | No device evidence exists for any Android product |
| F21 Protected signing | EXTERNAL_BLOCKED (D-04) | VERIFIED (config) | Release signing comes only from environment variables (`void.os/app/build.gradle.kts:50-62`). No key exists in any repository |
| F49 Actions billing | EXTERNAL_BLOCKED (D-01) | VERIFIED 2026-11-06 | Annotation: "The job was not started because your account is locked due to a billing issue." |
| F70 Hosted contract CI | EXTERNAL_BLOCKED | — | Local check passes (§6) |
| F80 Workflow hardening | OPEN (apply with the first CI run) | VERIFIED: `audit_workflows.py --check` passes | Unchanged since OV-48 |
| F77 Termux Background 2025 releases | OPEN (D-13) | **Corrected** | Only **1** release is public (`version-1.0.0`). v1.0.0, v1.0.1 and v1.0.3 are **drafts** (the unauthenticated API lists only `version-1.0.0`). Both public APKs are signed by `7bd3603d…ab4a`, not by the compromised `070cd54d…f68e` |
| F79 Termux Background user issues | OPEN | **Corrected** | Issues #4, #6, #7 and #8 each have an owner reply (2026-10-21) saying "New debug-test version released", but no release newer than 2025-07-31 exists. The 1.1.0 source handles a missing service, permission and dispatch failures (`TermuxBridge.java:95-162`). Not reproducible without a device |
| F81 Exposed signing key | OPEN (D-13) | Unchanged | Permanently untrusted. No key material or password was read, printed or exported in this audit |

## 8. Test and build results (this audit)

| Check | Command (abbreviated) | Result |
|---|---|---|
| BLUX cross-repository hard gates | `BLUX_REQUIRE_{DAT,COGA,CA,GOD,LRC,SYSTEM}=1 pytest tests/integration` at blux `56c9b76` | **45 passed, 2 skipped** (`BLUX_REAL_MODELS` unset), 400 s, exit 0 |
| Roughin backend (full) | `pytest -q` at `61c4b47` | **100 passed**, 200 s, exit 0 (SQLite, not PostgreSQL evidence) |
| `ax` router | `pytest -q tests` at axiom `ed079e8` | **13 passed**, exit 0 |
| Receipt sink reproductions | scratch script against blux `56c9b76` | F83 and F84 reproduced |
| Syntax: Python | `ast.parse` over every tracked `.py` in 31 repos | 0 failures (10,700+ files incl. blhermes) |
| Syntax: shell | `bash -n` over every tracked `.sh` | 0 failures |
| ShellCheck 0.10.0 (`-S error`) | per repo | 0 real errors. axiom's 2 are ksh false positives; warnings are style-level |
| DAT release gate | `dat audit . --gate --fail-on high --min-confidence medium` | **30/31 pass**. blhermes-agent (archived fork) fails |
| Contracts | `tools/check_contracts.py --workspace ~/ov` | ok, 0 breaking |
| Vigyl | same session, `5637f3d` | backend 108 (at `875b006`, backend unchanged), frontend 40 twice, browser pass 12 states / 0 violations, `npm audit` 0 |
| Android Gradle | not run | HISTORICAL_EVIDENCE: void.os testDebugUnitTest 78 (Stage 26); void.game core 21; voidforge core 86 + integration 9 + tools 24; void.sys tools 8 and both builds (Stage 25/44, 2026-10-26/27) |

## 9. Security and licensing

| Topic | Result |
|---|---|
| DAT secrets and code gate | 30/31 pass at current HEAD (OV-49 suppressions are still exact-fingerprint pinned) |
| Dependabot (open) | roughin: 1 low (deepmerge, development scope, F78). vigyl, resolver, blux, dat, voidforge, theresolver: 0 |
| `npm audit` | Roughin: 6 build-time advisories, all already recorded in F78 (deepmerge, glob, minimatch); `--omit=dev` 0. Vigyl: 0. Resolver site: 8 moderate, development only (F88) |
| Licences | No dependency manifest changed since OV-49, so its licence evidence stands (shipped frontend licences all MIT). Third-party licence texts untouched |
| Historical key (F81) | Not touched. Public APK signers re-checked by certificate digest only |
| Resolver tunnel credentials | `cloudflared/credentials.json` is git-ignored and untracked. The tunnel id is not reproduced here |
| Secrets in this audit | None printed or stored. The Vigyl browser fixture uses a random password from the environment |

## 10. Android release blockers

| Product | Blockers (in order) | Unblocked engineering available now |
|---|---|---|
| AXIOM Launcher | D-11 trust model → F1 → F21 signing (D-04) → F19 crash-loop guard → device matrix (D-03) | F19 guard logic and JVM tests |
| VOID.SYS | **F17: wire a fail-closed gate first** (today the icon pack is ungated) → signature → icon review → launchers on device (F25) | Wiring `SignatureGate` fail-closed, with tests |
| Shooter (bundled and standalone) | F2 → F29 licensed audio → F31 device runs | F29 asset replacement |
| VoidForge | F5 confirmation UI → device qualification per class (F6) → signing (D-04) | **F5 UI** (JVM and UI tests); F86 docs; F87 Termux pin |
| Termux Background | D-13 (F77, F81) → F79 triage on a device | Answer #4, #6, #7 and #8 accurately (no newer release exists) |

**Paid distribution must not be approved** for Launcher, VOID.SYS or Shooter: entitlement and cryptographic
verification are incomplete in all three.

## 11. BLUX platform assessment

As a **deterministic developer platform**, independent of native-model training:
- **Ready:** the contracts, the subprocess boundary, the engine chain and `ax` (VERIFIED today), plus
  offline/no-model use (HISTORICAL, Stage 44).
- **Not ready:** receipt durability, in three ways.
  1. Receipts are lost during a BLUX System outage when the operation carries an artifact (F83).
  2. A spooled receipt can be lost to a concurrent flush (F84).
  3. Nothing ever re-sends the outbox (F85).

  The BLUX deterministic release gate requires receipts, so these block it.
- **Also open:**
  - installer and packaging release (OV-54 and OV-63, which need D-01 for CI);
  - real-provider qualification (F10 and F60, D-02);
  - native models: F61 DEFERRED, F63 EXTERNAL_BLOCKED. They stay off the deterministic critical path.

## 12. Roughin and Vigyl readiness

| | Roughin (`61c4b47`) | Vigyl (`5637f3d`) |
|---|---|---|
| Implemented and locally verified | Contractor workflow, tenancy (`_owned` checks, `test_isolation.py`), Decimal money (`Numeric(10,2)`), refresh cookie, lockout, password change; backend 100 today | Care circles, tasks, recurrence, reminders, escalation, receipts, live updates; backend 108, frontend 40, browser accessibility pass |
| Accessibility | F37 PARTIAL. **No browser accessibility pass yet** (NOT_INSPECTED) | F43 PARTIAL. Automated pass done. Screen reader and phone outstanding. Open question: live regions sit inside `aria-busy` `<main>` |
| Database | F34 BLOCKED_LOCAL_ENVIRONMENT (PostgreSQL migrations, backup and restore) | F45 BLOCKED_LOCAL_ENVIRONMENT |
| External services | F35: Stripe sandbox, R2, staging (D-05) | F44: notification delivery (D-06) |
| Account recovery | F38: D-14 | F46: D-14; 2FA and legal review are owner decisions |
| Verdict | **Not releasable.** No financial claim | **Not releasable.** Alerts are in-app only and never claimed as delivered |

## 13. Resolver deployment readiness

The bot and the website are separate products, assessed separately:
- **Bot runtime.** HISTORICAL_EVIDENCE: 173 unit tests and the offline smoke check at `bf7f26a` (2026-10-27).
  Live Telegram authorization and subscriptions: **not verified** (D-07).
  The tunnel config (`resolver/cloudflared/config.yml`) routes only `admin.` and `hq.theresolverbot.net`, and
  **neither hostname has a DNS record** (VERIFIED 2026-11-06).
- **Website and domain.** The apex and `www` return **HTTP 530 with Cloudflare error 1033** (a tunnel with no
  connector). The site is designed for Cloudflare Pages, and its earlier `pages.dev` deployment was healthy
  (2026-11-04). So the apex DNS points at a tunnel, not at Pages.
- **Fix:** in Cloudflare, attach the custom domain to the Pages project, and add DNS for the bot's tunnel
  hostnames when the bot is deployed (F54, D-07, OV-57).

## 14. CI and release pipeline

- **Hosted CI:** EXTERNAL_BLOCKED (F49). Every recent run is `startup_failure` or a 0-step failure, including on
  2026-11-06.
- **Workflow hardening (F80):** still unapplied by design: 0/26 actions pinned to a SHA.
- **Releases:** the release ledger records only historical tags. No `RELEASE_CANDIDATE` exists anywhere.

## 15. Findings by state

Register: [findings-current.json](../ecosystem/findings-current.json), regenerated with this audit.
- **Total:** 57 frozen + 12 new.
- **By state:** RESOLVED_VERIFIED 10, PARTIAL 6, OPEN 22, DEFERRED 13, EXTERNAL_BLOCKED 16,
  BLOCKED_LOCAL_ENVIRONMENT 2.
- **Unresolved by severity:** 3 Critical, 14 High, 23 Medium, 17 Low, 2 Info.

| State | Findings |
|---|---|
| Resolved (unchanged) | F7, F16, F48, F53, F55, F68, F72, F73, F76, F82 |
| Partial | F36, F37, F38, F39, F43, F46 |
| Open: engineering, unblocked | F17 (wiring), F5, F19 (logic), F29, F32, F57, F64, F79 (triage and replies), F83, F84, F85, F86, F87 |
| Open: owner decision or CI | F1 (D-11), F2 (D-11/D-04), F77 and F81 (D-13), F80 (with the first CI run, D-01), F50, F58, F59, F62 |
| External or environment | F6, F9, F10, F14, F21, F22, F25, F31, F34, F35, F44, F45, F49, F54, F60, F63, F65, F70 |
| Deferred | F8, F20, F30, F40, F41, F42, F47, F56, F61, F66, F69, F78, F88 |

**Can any finding be closed today?** No. No open finding has new evidence that satisfies its exit, and the
corrections to F77 and F79 do not change their state.

## 16. Owner decisions needed

1. **D-01:** clear the GitHub billing lock. This unblocks F49, F70, F80, the PostgreSQL jobs (F34, F45) and OV-63.
2. **D-11:** the entitlement trust model (F1, F2, F17).
3. **D-04:** signing key custody.
4. **D-03:** a reference Android device.
5. **D-13:** unpublish or deprecate the **one** public 2025 release (and delete the three drafts), and whether to
   rewrite history for F81.
6. **D-07:** Cloudflare access to point the apex at Pages (F54).
7. **D-05, D-06, D-14:** staging and payments, the notification provider, and the email provider.
8. **Termux Background replies:** correct the 2026-10-21 "new version released" replies on #4, #6, #7 and #8
   (F79). This is an owner action on a public surface; this audit did not post anything.
9. **VoidForge artifacts:** whether to delete the two stale workflow artifacts (F86).

## 17. Prioritized remaining work, by stage

| Priority | Work | Stage | Blocked by |
|---|---|---|---|
| 1 | Receipt durability: F83, F84, F85 | OV-52 (after OV-50 and 51 per the plan's order) | nothing |
| 2 | BLUX runtime hardening and offline/no-model behaviour | OV-50 | nothing (providers stay BLOCKED until OV-64) |
| 3 | Fail-closed VOID.SYS gate (F17 wiring); crash-loop guard logic (F19) | OV-58 | the full F17 fix needs D-11 |
| 4 | VoidForge confirmation UI (F5); F86 docs; F87 Termux pin | OV-59 | device classes need D-03 |
| 5 | Roughin browser accessibility pass (F37), using the Vigyl method | OV-55 (needs authorization) | nothing |
| 6 | Resolver domain and bot hostnames (F54) | OV-57 | D-07 |
| 7 | Workflow hardening (F80), DAT pilot | OV-48 / OV-63 | D-01 |

## 18. Exact next executable assignment

**Authorize OV-50 (BLUX runtime and model routing)**, then run OV-51 and OV-52 in order. F83, F84 and F85 are
assigned to OV-52's exit criterion: "required receipts fail closed".

**Why this stage:**
- It is the head of the only track that has defects reproduced today.
- It needs no owner decision, account or device: deterministic and mock suites are enough.
- It feeds OV-63, the DAT pilot release, as soon as D-01 is cleared.

**Running a track in parallel.** The plan allows parallel tracks once OV-46/48/49 are recorded, which they are.
OV-58's F17 wiring and OV-59's F5 UI are the unblocked Android candidates if the owner wants one alongside OV-50.

**Not started.** No stage was started by this audit. Each needs explicit owner authorization.

## 19. Evidence appendix

All commands ran on 2026-11-06 in the owner's PRoot Debian 13 (aarch64) workspace, with bounded timeouts. There
were never more than two background processes, and none was left running.

| # | What | Command | Exit / result |
|---|---|---|---|
| 1 | Repository sweep | `git fetch`; `rev-parse HEAD` and `origin/main`; `status --porcelain`; `rev-list --count <OV-46 baseline>..HEAD` over 31 checkouts | 31 level, 31 clean |
| 2 | GitHub inventory | `gh api orgs/Outer-Void/repos?type=all` | 32 repos, 13 private. `er` main `ac4b89a` (metadata only) |
| 3 | CI state | `gh api repos/Outer-Void/<repo>/actions/runs`; check-run annotations | billing-lock annotation on the docs run at `863d6f0` |
| 4 | BLUX hard gates | see §8 | 45 passed, 2 skipped, exit 0 |
| 5 | Roughin backend | `pytest -q -p no:cacheprovider` in roughin/backend | 100 passed, exit 0 |
| 6 | axiom | `pytest -q tests` | 13 passed, exit 0 |
| 7 | Sink reproductions | real `Runtime` and `BluxSystemSink` from blux `56c9b76` (import paths confirmed) | F83: `spooled: false`, no outbox; control spooled. F84: concurrent receipt gone |
| 8 | Syntax | `ast.parse` and `bash -n` over tracked files | 0 failures |
| 9 | ShellCheck | `shellcheck -S error` and `-S warning` | 0 real errors |
| 10 | DAT | gate over 31 repos | 30 pass, blhermes-agent fails |
| 11 | npm audit | roughin/frontend, vigyl/frontend, theresolver; with and without `--omit=dev` | 6 / 0 / 8; `--omit=dev` 0, 0, 0 |
| 12 | Dependabot | `gh api …/dependabot/alerts?state=open` | roughin 1 low; others 0 |
| 13 | Termux releases | authenticated and unauthenticated `…/releases`; `apksigner verify --print-certs` on the two public APKs (downloaded to scratch, then deleted) | 1 public, 3 drafts; signer `7bd3603d…ab4a` |
| 14 | Resolver | `curl` HEAD and GET to the apex and `www`; `getent ahosts` for `admin.` and `hq.` | 530, error 1033; no DNS records |
| 15 | Contracts | `tools/check_contracts.py --workspace ~/ov` | ok, 0 breaking |
| 16 | Docs gates | `build_findings_current.py --check`, `build_status_matrix.py --check`, `build_inventory.py --check`, `audit_workflows.py --check`, `export_reassessment.py --check` (9/9), `pytest tests` (13) | all pass before commit (see the closing message for the post-commit sweep) |
| 17 | Credits | `validate.py --org-root ~/ov`, `unittest discover` | pass before commit |

Not executed, and why: Gradle, the BLUX and engine unit suites (unchanged inputs); PostgreSQL (environment);
providers, Stripe, R2, Telegram and notifications (no authorization or accounts); devices (none); `er` (policy).
