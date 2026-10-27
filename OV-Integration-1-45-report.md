# Outer Void integration report: Stages 00–45 (2026-10-24 → 2026-10-27)

The closing report of the staged rebuild of the Outer Void ecosystem.

**Status.** The staged execution plan is complete: every stage was executed with evidence or resolved with a
recorded reason. Stage 27 is BLOCKED by its precondition, not done. **Nothing is shipped.** No component can meet
the release rule while Outer-Void CI cannot start (billing lock, F49), and real-provider and device evidence is
missing.

**Where to look:**
- **Current state:** [ecosystem/status-matrix.md](ecosystem/status-matrix.md) (the final matrix) and
  [ecosystem/findings.md](ecosystem/findings.md).
- **Architecture rules:** [constitution/](constitution/README.md).
- **Freeze:** [POST_STAGED_REBUILD_REASSESSMENT_INPUT.md](POST_STAGED_REBUILD_REASSESSMENT_INPUT.md) with
  [reassessment/](reassessment/).
- **Forward plan:** [POST_REBUILD_RECOMMENDATIONS.md](POST_REBUILD_RECOMMENDATIONS.md).

## 1. What was built

The rebuild turned a collection of loosely related repositories into a contract-driven ecosystem. Standalone
products stay usable without BLUX; integrated engines meet through one contract.

- **BLUX Contract v1 and blux-sdk.** One schema set, one validator, typed errors and prefixed ULIDs. Capabilities
  are declared in `.blux/` (7 repositories) and discovered by GOD.
- **BLUX runtime.**
  - Capability registry, policy, subprocess providers and the Hook System v1 (37 events).
  - Model API v1 with four logical models and explicit, degraded fallback.
  - The direct `blux` CLI and the agent loop.
  - The training pipeline and a Generation 0 evaluation baseline.
- **Engines, each standalone and integrated by subprocess:**
  - CogA: structured reasoning.
  - cA: construction and repair; it never certifies its own work.
  - DAT: independent verdicts.
  - LRC: deterministic repository creation.
  - GOD: discovery.
  - BLUX System: receipts, operation graphs and a hash-chained store.
  - BluxGPT: provider gateway.
- **`ax`.** The thin control plane: it routes to the real engine, or exits 69.
- **VoidForge.** The device authority. Every write is confirmed by the person at the device; BLUX and `ax` can only
  ask.
- **Products.** AXIOM Launcher, VOID.SYS, AXIOM Shooter, Roughin, Vigyl, Resolver and its website, Termux
  Background, JADIS Toolbox, BLUX App, bluxai.app, blux10k and the datasets, each with its own release track.
- **Governance.**
  - Proprietary licensing, with third-party notices and verbatim licence texts.
  - The credits ledger, with evidence-based attribution and AI-assistance records.
  - The docs constitution, status matrix, findings register, cross-repository contract checks and release ledger.
- **BLHermes.** Inventoried, characterized, partly migrated into BLUX, proven unnecessary for BLUX, and archived.

## 2. Stage by stage

`repo@sha` is the stage's main commit. Credits and documentation-sync commits for each stage are in
`Outer-Void/credits` and `Outer-Void/docs`.

| Stage | Subject | Main commits | Outcome |
|---|---|---|---|
| 00 | Organization-wide baseline | blux@adad020 | Baseline of 30 repositories recorded (historical since Stage 44) |
| 01 | BLUX Contract v1, Python SDK, reference runtime, CLI | blux@0b09a46 | Done; tag `blux-sdk-v0.1.0` |
| 01A | Credits, licensing policy, per-repo decisions | blux@8bd9e26, credits@68aec9c | Done; proprietary by default, notices and licence texts |
| 02 | BLUX System as the execution truth layer | blux-system@ebdf84c, blux@73a018c | Hard gate passed |
| 03 | Subprocess providers; DAT 4.0 | dat@ba58386, blux@64bd72b | Hard gate passed |
| 04 | LRC 2.0; LRC → DAT chain | lrc@e64c138, blux@19a9c5a | Hard gate passed |
| 05 | GOD 2.0; discovery chain | god@26fa415, blux@609d6a2 | Hard gate passed |
| 06 | CogA 2.0 | blux-coga@64375dc, blux@97de739 | Hard gate passed |
| 07 | cA 2.0; CogA → cA → DAT → bounded repair | blux-ca@930e902, blux@9b76007 | Hard gate passed |
| 08 | Datasets rebuilt (2.0.0) | blux-ca-dataset@db29214, blux-coga-dataset@2c88726 | Done; reproducible, locked splits |
| 09 | Model API v1, BluxGPT 2.0 | blux@8733593 | Done with the mock provider; real providers BLOCKED (F10) |
| 10 | Direct `blux` CLI | blux@d804edc | Hard gate passed (mocked); real path BLOCKED (F10) |
| 11 | BLHermes inventory, parity matrix, characterization | blux@542e344 | Done (44 features tracked) |
| 12 | Hook System v1 | blux@a223749 | Done |
| 13 | BLHermes runtime core migrated | blux@e6443e0 | Done (clean-room) |
| 14 | BLHermes extensions migrated | blux@b3a5168 | Done |
| 15 | BLUX Termux package | blux@76eeb51 | Package built and audited; on-device APT install not run |
| 16 | BLUX independent of BLHermes | blux@1ebc230 | Proven; decoupling enforced in tests |
| 17 | Owner review of BLHermes | (owner decision) | Archived read-only at `dc8abc1db0` |
| 18 | `ax` control plane, `blux agent`, blux10k 3.0 | axiom@022de2f, blux@463e7b0, blux10k@fcb127d | Done |
| 19 | VoidForge workstation core, operation classes, local authorization | voidforge@0d660ff | Done (mock-tested; writes locked in production) |
| 20 | VoidForge Magisk and root workflows | voidforge@5f07ec9 | Done, fail-closed (mock-tested) |
| 21 | VoidForge members-only distribution | voidforge@114278d | Policy and workflow defined; repository still public (F7) |
| 22 | VoidForge device capabilities for BLUX and `ax devices` | blux@f491524, axiom@a276744, voidforge@91fba7e | End to end at protocol level |
| 23 | VoidForge real-device acceptance | voidforge@463b921 | BLOCKED: no hardware |
| 24 | AXIOM Shooter source of truth; launcher release foundations | void.game@ad7e0ab, void.os@097f50d | Gate not passed (F1, devices, keystore, legal, public repo) |
| 25 | VOID.SYS release track; bundle through the component lock | void.sys@09cf56f, void.os@4964895 | Gate not passed (F17, devices) |
| 26 | AXIOM Shooter release track; bundled host contract | void.game@6f6c85b, void.os@24b07cd | Gate not passed (F2, devices) |
| — | Interjected checkpoint: JADIS Toolbox overhaul | jadis.toolbox | Done (not a numbered stage) |
| 27 | AXIOM Launcher optional BLUX layer | docs@faccc83 | **BLOCKED**: precondition (Stage 24 gate) not met; circled back after Stage 45 |
| 28 | Roughin release readiness | roughin@9e5cf12 (+6a63057, f3599d3, 97921fc) | Partly passed; PostgreSQL, backup and deployment evidence missing (F34, F35) |
| 29 | Vigyl core release readiness | vigyl@a01497d, a0816a4 | Passed locally; no UI (F43, F44) |
| 30 | Wave checkpoint and full reconciliation | docs@4af1e5f | Done; CI billing lock found (F49) |
| 31 | Resolver website | ov-webpages/theresolver@49dbeff | Passed on `pages.dev`; custom domain down (F54) |
| 32 | Termux Background | termux-background@75cfb97 | Local checks pass; no device qualification |
| 33 | JADIS Toolbox scripts | jadis.toolbox@253c386 | Hard gate passed; plaintext-push guard |
| 34 | BLUX training pipeline | blux@7bdd076 | Hard gate passed |
| 35 | Generation 0 evaluation baseline | blux@8ef10d5 | Reproducible; model suites BLOCKED (F60) |
| 36 | Native specialist register; adb wipe rule fix | blux@ba160c3 | Passed by evidence-backed rejections; none integrated |
| 37 | Generation 2 readiness | blux@b634dd3 | No model trained (no data, baseline or compute); isolation guard |
| 38 | BLUX App 2.0 mission control | blux-app@6c8e8dd (+dbdd2a4) | Hard gate passed |
| 39 | BLUX web | ov-webpages/bluxai.app@9fdb0a2 | `blux-web` confirmed absent; bluxai.app 0.1.0 API |
| 40 | Docs as constitution | docs@465f966 | Hard gate passed |
| 41 | Organization metadata | .github@be5221d, .github-private@5ea59da; classifiers dat@487e1d4, god@ad6f0c4, lrc@443e532 | Done; false repository claims removed |
| 42 | Cross-repository contract verification | docs@b888d62 | Passed locally (13 mutation tests); CI BLOCKED (F70) |
| 43 | Ecosystem release candidate | blux@83ded6f, docs@ef7d357 | Validated locally; 1 blocker found and fixed (F71); not releasable |
| 44 | Final repository-by-repository release pass | bluxai.app@9e5706a, blux-app@0de2d9a, blux@51134af, docs@9cb9798 | Done; final matrix; F74 and F75 fixed |
| 45 | Freeze for reassessment | docs@43d9a6c | Done: reassessment input and exports |

## 3. Final state (from the freeze)

| Class | Components |
|---|---|
| SHIPPED | none |
| RELEASE_CANDIDATE | none |
| INTEGRATED | BLUX runtime and CLI, BLUX System, CogA, cA, DAT, LRC, GOD, `ax`, BLUX App, JADIS Toolbox |
| FUNCTIONALLY_COMPLETE | blux10k, both datasets 2.0.0, the Roughin API, the Vigyl API, the governance repositories |
| BLOCKED | BluxGPT (F10), Resolver bot (F48, F53), Resolver website (F54), Termux Background (device), VoidForge (hardware, F7), AXIOM Launcher (F1), VOID.SYS (F17), AXIOM Shooter (F2), Stage 27 |
| EXPERIMENTAL | Roughin frontend (F36, F37), bluxai.app, native models (none integrated) |
| DEFERRED | Vigyl UI, Operation: Restore website, IVRP |
| ARCHIVED | BLHermes |

The release-candidate invariants (Stage 43), with full evidence in
[ecosystem/release-candidate.md](ecosystem/release-candidate.md):
- **PASS:** the BLUX-off suites; capability discovery through contracts; authority staying with its owners;
  operation ids and receipts; provider fallback; BLUX with BLHermes removed; offline operation; VoidForge refusing
  destructive requests; cA unable to certify itself; `ax` routing.
- **BLOCKED:** real devices, real providers, CI.

## 4. Defects found at the end of the run, all fixed with regression tests

| # | Where | Defect | Fix |
|---|---|---|---|
| F71 | blux | `blux agent` ignored `system_store`, so `ax agent` left no receipts | blux@83ded6f: sink added, tool calls linked to their model call, fail closed (exit 5) |
| F74 | bluxai.app | Without `blux-system`, creating an organization returned 500 after committing it | bluxai.app@9e5706a: store created on first use; BLUX absent answers 503 |
| F75 | blux-app | 17 lint issues; CI never ran ruff | blux-app@0de2d9a: fixed; ruff in CI |

Earlier fixes are listed by stage in [ecosystem/findings.md](ecosystem/findings.md). Examples:
- Roughin: billing idempotency, tenant isolation, and the PyJWT swap.
- JADIS Toolbox: the plaintext-push guard.
- The adb wipe rule.
- The Resolver website's privacy page correction.

## 5. What blocks release

The full open list is [reassessment/open-findings.json](reassessment/open-findings.json): 57 rows.

| Blocker | Owner action |
|---|---|
| CI cannot start: GitHub billing lock (F49, F70) | Clear the lock |
| No funded model provider (F10; F60 suites BLOCKED) | Fund a provider |
| No Android hardware for acceptance (VoidForge, launcher family, Termux Background) | Provide a device |
| Proprietary and members-only source in public repositories (F7) | Make them private |
| Resolver domain (F54), tunnel config (F53), version (F48) | Fix Cloudflare; align the version |
| Stale `blux()` in `~/.zshrc.local` (F65); stale `ANDROID_HOME` in `~/.zshrc` | Edit the shell config |
| Unfinished signature and entitlement verification (F1, F2, F17) | Engineering work |
| DAT raw gate fails on triaged fixtures (F76) | Engineering work: DAT target policies |

## 6. Process record

- **Git.** Every stage was committed and pushed to `main` with gated checks: `check && … && commit && push`, never
  `;` or `| tail`.
  - No history was rewritten, and no force push was needed or used. Appendix C allows force pushing only for
    intentional rewrites.
  - Protected `main` branches (blux-ca, blux-coga, blux-ca-dataset, dat, lrc, blux-gpt, .github,
    termux-background and blux) were pushed with the owner's bypass.
  - Concurrent work by another session (Router 0.x in `blux/training/`) was rebased over, never overwritten (F62).
- **Attribution.** Every stage updated `Outer-Void/credits`:
  - AI-assistance commit counts are taken from `Co-Authored-By` trailers;
  - undeclared tooling is recorded as unresolved (for example UNR-021);
  - lineage is recorded for BLHermes and Hermes Agent (Nous Research, MIT).
- **Privacy and safety.**
  - `secret-project` and the owner's real `~/.hermes` were never read; tests ran with an isolated HOME.
  - Provider hidden reasoning is never stored, and no private data enters datasets.
  - Every documentation pass scanned added lines for secrets and personal paths.
- **Evidence rules.**
  - Statuses come only from evidence.
  - Environment-blocked checks are marked BLOCKED with next commands (Appendix B), never PASS.
  - Docs follow the code; code is never changed to make docs true.

## 7. Final repository SHAs

Recorded at finalization. Every repository was clean and level with `origin/main`. The docs row is the commit
before this report; this report and its credits record add one commit each to docs and credits.

FINAL_SHA_TABLE

## 8. Next

1. The Outer Void reassessment, using
   [POST_STAGED_REBUILD_REASSESSMENT_INPUT.md](POST_STAGED_REBUILD_REASSESSMENT_INPUT.md).
2. The phased plan in [POST_REBUILD_RECOMMENDATIONS.md](POST_REBUILD_RECOMMENDATIONS.md):
   1. owner unblockers;
   2. a pilot release;
   3. standalone apps to release-ready (VOID.SYS icons, Shooter graphics, launcher UI, Vigyl UI, Roughin UI);
   4. VoidForge fully operational for developer support;
   5. the intelligence flywheel.

**STAGED EXECUTION PLAN COMPLETE — READY FOR OUTER VOID REASSESSMENT**
