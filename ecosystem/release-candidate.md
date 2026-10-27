# Ecosystem release-candidate validation (Stage 43, 2026-10-27)

Every invariant below was run on 2026-10-27 against the workspace at the commits current that day. Each one is
**PASS**, **FAIL** or **BLOCKED**:
- PASS means it was run and the evidence is recorded here.
- BLOCKED means the environment could not run it; the next commands are given.
- Nothing here was declared rather than run.

**This is not an ecosystem-wide release.** Two conditions rule that out today:
- No Outer-Void CI job starts (billing lock, findings F49), so the release rule in
  [lifecycle.md](../constitution/lifecycle.md) cannot be met by any component.
- Real-provider and real-device paths are BLOCKED (F10, no hardware).

The result is a local release-candidate verdict only.

## Method

- **Engines.** Each engine ran from its repository checkout: blux 0.4.0 (blux-sdk 0.2.0), blux-system 2.0.0,
  coga 2.0.0, ca 2.0.1, lrc 2.0.0, dat 4.0.0, god 2.0.0, blux10k 3.0.0 and the VoidForge client 1.0.0. `ax` is
  `axiom/cockpit/bin/ax-route`, and `ax doctor` resolved all 12 routes.
- **Models.** The `mock` provider of BluxGPT, behind the real subprocess backend protocol. Every mocked response is
  labelled `provider: mock`. Real providers are unfunded (F10).
- **Disable BLUX.** BLUX executables were removed from `PATH`. An import hook made `blux_runtime`, `blux_cli`,
  `bluxgpt`, `blux_app` and `blux_system` unimportable. Each component's own test suite then ran.
- **Remove BLHermes.** BLUX was cloned into an empty directory with no BLHermes checkout beside it. Its wheels were
  built and installed into a fresh virtual environment, with an import hook refusing any `*hermes*` module.
- **Disconnect network.** proot cannot drop the network (`unshare -n` still connected), so a `sitecustomize`
  refused every non-loopback connection and DNS lookup in each Python process. Android builds used Gradle
  `--offline`.

## End-to-end flows

| Flow | Result | Evidence |
|---|---|---|
| `ax create` → LRC | PASS | `ax create create -T python-cli … --git --blux rc-demo --audit` created 16 paths, `.blux/` and a reproducible initial commit. It handed off to DAT (`repo.audit`) |
| `ax agent` → BLUX Runtime | PASS (after fix) | `ax agent --routes <mock> --workspace rc-demo` answered in one turn with operation id `op_…`; the tool-calling variant ran `fs.read` through policy |
| BLUX → CogA / cA | PASS | BLUX integration hard gates with every engine required (`BLUX_REQUIRE_{COGA,CA,DAT,LRC,GOD,SYSTEM,BLUXGPT}=1`): 45 passed. The 2 skips are the real-provider paths (BLOCKED, F10) |
| DAT → independent verdict | PASS | DAT failed LRC's new repository (no licence: `release.missing-license`, high). In the cA chain, DAT failed cA's build and passed it only after the repair |
| BLUX System → receipts | **FAIL → fixed → PASS** | `blux agent` ignored the configured `system_store`, so agent runs left no receipts (F71). Fixed in blux; the agent's receipts now land and `verify` passes the hash chain |
| `ax inspect` → operation graph | PASS | `ax inspect graph --root <model op>` shows the model turn → `fs.read` edge; the aggregate status is `PARTIAL` (the tool failed) |
| `ax devices` → VoidForge → Android | BLOCKED (real device) · PASS (protocol) | No VoidForge running and no adb here: `ax devices` exits 69 with the reason. VoidForge `IntegrationTest.axDevicesReachesTheRealAdapterAndCannotSkipLocalAuthorization` drives `ax devices` → client → the real adapter on a fake device (0 skipped) |
| diagnose → BLUX/CogA + device evidence | BLOCKED | Needs a device and a funded provider |
| authorized operation → VoidForge → receipt → BLUX System | BLOCKED | Needs hardware; in production the write barrier is locked, so every write is `blocked` |

**Next commands for the BLOCKED rows:**
1. Fund a provider (F10), then run
   `BLUX_REAL_MODELS=1 pytest tests/integration/test_cli_direct.py tests/integration/test_model_api.py` in blux.
2. With a phone and VoidForge open (Settings → Local integrations on), run `ax devices`, then
   `blux agent --tools device.list,device.inspect "what device is connected?"`.
3. Record the device run with VoidForge `tools/device_acceptance.py` (Stage 23).

## Architecture invariants

### Disable BLUX

| Component | Result | Evidence |
|---|---|---|
| Roughin | PASS | backend: 91 passed |
| Vigyl | PASS | backend: 78 passed |
| AXIOM Launcher (void.os) | PASS (unit + build) · on-device BLOCKED | `:app:testDebugUnitTest` 78 passed, including `ProductBoundaryTest.launcherCoreDoesNotRequireBlux`; `:app:assembleDebug` built |
| AXIOM Shooter (void.game) | PASS (unit + build) · on-device BLOCKED | `:core:test` 21 passed; `:android:assembleDebug` built |
| VOID.SYS | BLOCKED (build only) | `:app:assembleDebug` built and there is no BLUX reference in the source. There are no automated tests and no device, so "works" is not shown |
| VoidForge | PASS | `:core:test` 86 and `:integration:test` 9 passed (forced rerun) |
| DAT | PASS | 88 passed |
| LRC | PASS | 133 passed; 1 skipped (DAT handoff with DAT absent; the handoff passed in the e2e flow) |
| GOD | PASS | 94 passed |

On-device next step: install each debug APK on a phone and follow each repo's `docs/device-testing.md`.

### Enable BLUX

| Invariant | Result | Evidence |
|---|---|---|
| Capabilities are discovered through contracts | PASS | `ax capabilities` (GOD) over blux, blux-coga, blux-ca, dat, lrc, god and jadis.toolbox found 38 capabilities from their `.blux/` declarations, none ambiguous. The contract check (`tools/check_contracts.py --workspace`) shows no breaking change and no invariant failure |
| Permissions remain with authoritative systems | PASS | VoidForge's local authorizer declines a flash request sent through `ax`. DAT alone decides a verdict. BLUX policy denies agents destructive device capabilities (`tests/cli/test_agent_cmd.py`) |
| Operations receive IDs | PASS | Every execution has an `op_` ULID, and receipts have `rcpt_` ULIDs |
| Receipts record what actually happened | PASS (after F71) | The failed `fs.read` and the all-routes-failed model calls are stored as `failed`; tool calls link to their model call. Observation: `error_code` is the Contract v1 code (`EXECUTION_FAILED`); the model-specific code is in the `blux.result` |
| AI assists without silently becoming authority | PASS | cA's `certified` is `const: false` in its schema. The model cannot approve anything: agents run with no approvals, so `rm -rf` was refused with `approval_required`. Fallback is marked `degraded` |

### Disable a provider

**PASS.**
- With the primary route failing (`PROVIDER_UNAVAILABLE`), BLUX served from the fallback, marked
  `degraded: true, fallback_used: true` with a note.
- With every route failing, `blux` exited 1 with `ALL_ROUTES_FAILED`, a per-route explanation, a hint and a
  receipt id, and no traceback.
- `--no-fallback` was honoured (exit 1).

### Remove BLHermes

**PASS.** BLUX ran from a clean clone with no BLHermes checkout beside it and any `*hermes*` import refused:
- **builds:** wheels `blux_sdk-0.2.0` and `outervoid_blux-0.4.0`;
- **installs:** into a fresh venv; **updates:** a forced reinstall over itself;
- **tests:** 568 passed; the 28 skips need sibling checkouts that are deliberately absent;
- **runs:** `blux version` and an `ask` both worked;
- **operates:** `blux migrate hermes` reports "no legacy home" and exits 0.

### Disconnect network

**PASS.** With every non-loopback connection and DNS lookup refused, each suite passed. Each figure below is from a
single run except where noted:

| Component | Result |
|---|---|
| blux (full suite, every engine required) | 597 passed, 15 skipped |
| blux-system | 74 passed |
| blux-coga | 343 passed (rerun) |
| blux-ca | 117 passed |
| lrc | 134 passed |
| god | 94 passed |
| blux-gpt | 49 passed, 1 skipped |
| roughin | 91 passed |
| vigyl | 78 passed |
| dat | 87 passed, 1 failed (see below) |

The CogA figure comes from a rerun: in the batch run its own `addopts = "-q"` hid the summary line (exit code 0).
The skip reasons were not captured in this run. The same suite online skipped only the two real-provider paths
among the integration gates.

- **The DAT failure is caused by the harness.** DAT's `test_dat_imports_no_blux_ai_or_network_modules` asserts
  that DAT never imports `socket`, and the blocker's `sitecustomize` imports `socket` into every interpreter.
  Without the blocker the test passes.
- **Two refused lookups, both from Roughin (F73).** They were for `169.254.169.254`, the cloud instance-metadata
  address. With the R2 settings empty, as in tests and development, `boto3` falls back to its default credential
  chain, and that chain probes instance metadata. Roughin's production configuration check already requires all
  four R2 settings, so production cannot fall back this way.
- **Android:** the three apps and VoidForge built and ran their unit tests with Gradle `--offline`.
- **Not run:** Node components (the Resolver website, the Roughin and Vigyl frontends) were not exercised offline
  here.

### Destructive device request

**PASS (protocol level) · real hardware BLOCKED.**
- Through `ax devices call device.flash …`, VoidForge prompted the person at the device once. The request was
  declined there and returned `authorization_declined` with exit 3; the flash never ran (`handled == [USB_LIST]`).
- Requests that carry authorization fields are refused with `ELEVATION_REFUSED`. In production the write barrier
  blocks every write.
- BLUX policy also denies agents `device.flash`.

### cA cannot certify itself

**PASS.** The hard gate ran CogA plan → cA build → DAT fail → cA repair → DAT pass. cA reported
`certified: false` at every step, and only DAT's second verdict passed the build. cA's construction schema fixes
`certified` to `const: false`.

### `ax` routes to real engines

**PASS.**
- `ax/router.py` imports only the standard library and execs the resolved engine with the user's arguments.
- A missing engine gives exit 69 with "AX does not do this work itself".
- The router tests pass (12), and the `ax-routes` invariant of the contract check verifies every route's
  executable and subcommand.

## Fixed in this stage

- **F71 (blux):** `blux agent` now records receipts in the configured BLUX System store and links each tool call
  to its model call. It fails closed with exit 5 when a receipt is not recorded. A regression test was added and
  mutation-checked (it fails without the fix).

## Verdict

**Release candidate: locally validated, not releasable.**
- The validation found one RC blocker, and it is fixed: F71.
- Everything that can run here passes.
- The remaining gaps are environmental and have exact next commands: CI (F49), funded providers (F10),
  hardware and device runs.
