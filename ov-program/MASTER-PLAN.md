# Outer Void master execution plan: OV-46 → OV-70 (locked baseline)

**Status: APPROVED WITH AMENDMENTS (owner, 2026-11-04).** This file is the execution baseline. The amendments are
already folded into the stage contracts below.

**Authorized:** OV-46 → OV-49 (complete, 2026-11-05), then OV-55 and OV-56 (owner, 2026-11-05). Each other stage
needs its own authorization.

**How to change this plan.** Change it only for an evidenced cross-stage architecture, safety or dependency-order
defect, or an explicit owner product decision. Record any change in the amendment log at the end.

Sources:
- the owner's review candidate "Deep repository sweep & master execution plan" (prepared 2026-11-04);
- the owner's "Master execution authorization" (2026-11-04);
- the workspace corrections from the plan review.

The history it builds on is not changed by this plan:
- the [Stage 45 freeze](../POST_STAGED_REBUILD_REASSESSMENT_INPUT.md) and its [exports](../reassessment/);
- the [2026-11-03 system report](../OV-System-Report.md);
- the [forward execution report](../OV-scaffold/forward-plan.md);
- the [recommendations](../POST_REBUILD_RECOMMENDATIONS.md);
- the [Definition of Done](../ecosystem/definition-of-done.md).

## 0. Goal

Deliver a repeatable evidence-to-release pipeline:
- qualify the most ready products;
- keep the deterministic engines independently operable;
- establish a sustainable release and maintenance cadence.

Do not rediscover the architecture, merge repositories, build a second BLUX runtime or take MVP shortcuts.

## 1. Repository scope

There are 32 GitHub repositories: 31 active and 1 archived (`blhermes-agent`). The workspace has 31 checkouts. The
32nd repository, `er`, lives under `secret-project/`.

**ER is inventoried from GitHub metadata only:**
- What may be recorded: visibility, default branch, latest remote commit SHA, status and metadata.
- Its checkout and contents are never opened, read, indexed, summarized or modified.
- Content inspection is marked `EXCLUDED_BY_OWNER_POLICY`, not a failed audit.
- ER stays separately governed and outside the software execution path.

SECRIPTS (`Justadudeinspace/jadis.secripts`) and Outer-Void Recovery (OVR) are not Outer-Void repositories:
- They follow their own frozen plan, and OV-46–70 does not wait for them.
- A future integration would be versioned. The flow would be: a SECRIPTS artifact, manifest and closure/hash; then
  an independent VoidForge compatibility check; local authorization; the physical device operation; an OVR runtime
  report; and finally evidence import.
- In that flow:
  - SECRIPTS owns Android image and recovery engineering;
  - VoidForge owns device transport and write authority;
  - OVR owns its runtime evidence;
  - `ax` and BLUX may route or advise, but never flash or assert hardware qualification.

## 2. Constitution for this program

1. **Standalone products remain standalone.** BLUX stays optional or excluded per repository, with no hidden
   mandatory network or model dependency.
2. **One owner per authority.**
   - BLUX routes.
   - CogA reasons.
   - cA constructs.
   - DAT judges.
   - LRC creates and migrates repositories.
   - GOD discovers.
   - BLUX System records.
   - VoidForge controls devices.
   - Product backends own their business data.
3. **Deterministic first.** AI output is a proposal, never proof, privilege or a promotion of evidence state.
4. **No self-certification.** cA never certifies cA, and DAT verdicts must be independently testable.
5. **Evidence states are not marketing.** `COMPILED` is not `QUALIFIED`, `MOCK_TESTED` is not `LIVE_VERIFIED`, and
   `PRIVATE` is not `SECRET_HISTORY_REMEDIATED`.
6. **Fail closed on high-risk actions.** This covers firmware writes, entitlement, signing, secrets, payments, care
   escalations and destructive file operations.
7. **Protect sources and users.** Visibility is explicit, secrets are redacted, rights are reviewed, and privilege is
   least by default.
8. **No silent contract rewrites.** Version interfaces, keep compatibility windows, and migrate explicitly.
9. **Git workflow** (owner decision, 2026-11-04). After each authorized stage:
   1. Review the scope of the working-tree changes.
   2. Run every applicable gate, with commits gated on exit codes.
   3. Update docs, evidence, credits and status.
   4. `git add` the intended changes.
   5. Commit with a stage-specific message.
   6. Push directly to `main`.
   7. Verify HEAD equals `origin/main` and the tree is clean.

   Further rules:
   - Use normal fast-forward pushes, with no feature branches or pull requests.
   - Never force-push by default. `--force-with-lease` is allowed only when genuinely necessary, after verifying
     that no unrelated remote work is overwritten.
   - Respect protected branches and the owner-bypass mechanism; never weaken or disable protections.
10. **At most two concurrent background processes.**
11. **Reuse verified work.** Compare current commits, dependencies, interfaces and affected files with their
    verified baselines. Reuse valid evidence with its original date and commit, and rerun only affected suites and
    mandatory current-HEAD gates. Never present a historical result as fresh execution.
12. **No release claim** without immutable source, build, test, security, deployment and operating evidence.
13. **Owner shell configuration is not modified automatically** (D-12).
14. **Product decisions (owner, 2026-11-04).**
    - VoidForge stays free, private and members-only.
    - AXIOM Launcher, VOID.SYS and AXIOM Shooter are a coordinated release family. The bundled Shooter stays a
      hidden home-screen Easter egg, never a Settings feature.

## 3. Stage dependencies

```
OV-46 BASELINE + INVENTORY
   ├─ OV-47 FINDINGS / DOCUMENTATION RECONCILIATION
   ├─ OV-48 CI / BUILD / REPRODUCIBILITY
   └─ OV-49 SECURITY / LICENSING / PRIVACY / CONTRACTS
         ├─ PLATFORM: OV-50 BLUX → 51 ENGINES → 52 EVIDENCE → 53 MODEL PROGRAM; 54 TOOLING/UI
         ├─ WEB: OV-55 ROUGHIN | 56 VIGYL | 57 RESOLVER
         ├─ ANDROID: OV-58 LAUNCHER/ICONS/SHOOTER | 59 VOIDFORGE/TERMUX
         └─ SUPPORT: OV-60 INSTITUTIONAL/UTILITIES
                 └─ OV-61 CONTRACTS · OV-62 FAULT INJECTION · OV-63 RELEASE PIPELINE / DAT PILOT
                       ├─ OV-64 SERVICES · OV-65 DEVICES · OV-66 PRODUCT RCs · OV-67 DISTRIBUTION
                       └─ OV-68 OPERATIONS · OV-69 MAINTENANCE · OV-70 FINAL RECONCILIATION
```

Tracks can run in parallel once their OV-46/48/49 gates are recorded. Three things are not on the critical path:
- OV-53 (native models) for deterministic releases;
- OV-65 (Android hardware) for Roughin and Vigyl;
- ER institutional review for software releases.

## 4. Stage contracts

### OV-46: baseline, inventory, owner map (authorized)
**Reuse:**
- The frozen `reassessment/inventory.json` and `dependency-graph.json`.
- The recovered Stage 45 export script, moved to `tools/export_reassessment.py` with `--check`. It reads its inputs
  at the frozen commits, so the frozen exports can be reproduced.

**Do not** rebuild inventory machinery that already exists.

**Record current state separately** under `inventory/` with `tools/build_inventory.py` (`--refresh`, `--check`):
- `baseline-commits.json`;
- `visibility-attestation.json`, from the authenticated GitHub API;
- `inventory-current.json`, covering manifests, lock files, workflows, toolchains, tags, licence, owner map and
  movement since the freeze.

**Exit:**
- 32/32 accounted for. A repository that cannot be reached is marked `INACCESSIBLE`, and ER is marked
  `EXCLUDED_BY_OWNER_POLICY`.
- The historical snapshots are unchanged.

### OV-47: current findings and documentation (authorized)
**Frozen records stay unchanged:** `ecosystem/findings.md` and `reassessment/open-findings.json` are not edited.

**`ecosystem/findings-current.json`** is a separate current projection:
- Every frozen open finding gets a disposition, with evidence, owner, priority and next action.
- Dispositions: `OPEN`, `RESOLVED_VERIFIED`, `PARTIAL`, `EXTERNAL_BLOCKED`, `BLOCKED_LOCAL_ENVIRONMENT`,
  `SUPERSEDED`, `DEFERRED`, `UNKNOWN`.
- Severity and source are kept as frozen.
- A finding is never resolved without verification.

**Documentation fixes:**
- Correct the confirmed Vigyl, Roughin and VOID.SYS documentation drift after verifying current source and
  manifests.
- Do not touch historical test counts or documentation that is already accurate.

**Credits:**
- UNR-021 and UNR-022 (tool attribution) and UNR-020 (font) are resolved only with evidence; otherwise they stay
  unresolved.

### OV-48: CI, builds, reproducibility (authorized)
**Hosted CI:**
- The billing lock (F49) is a verified external blocker as of 2026-11-03.
- Recheck its status from existing run annotations. Do not repeatedly trigger jobs that cannot start.

**PostgreSQL:**
- PostgreSQL cannot reliably run in this Android/PRoot environment.
- Every PostgreSQL-dependent check is `BLOCKED_LOCAL_ENVIRONMENT`. Acceptance is deferred to hosted CI or a
  suitable external machine.
- SQLite or mocked PostgreSQL is never evidence of PostgreSQL qualification.

**Workflow audit:** permissions, action pinning, secret boundaries and triggers. Changes that only hosted CI could
validate are recorded and wait until CI runs.

**Fresh runs:**
- Fresh local runs of the suites affected since their verified baselines, plus the current-HEAD gates.
- Record the environment, versions, commands and pass/fail/skip results.
- Continue all independent engineering.

**Exit:** the evidence says where CI actually runs. If it does not run, that is recorded as BLOCKED, never as
green.

### OV-49: security, licensing, privacy, contracts (authorized)
**Privacy:**
- Current authenticated visibility is accepted.
- Current privacy and historical exposure are kept separate.

**Credential history:**
- Review the git history and the existing evidence for actual credential exposure.
- Record verified findings without credential values.
- Never assume compromise just because a repository was public.

**Reuse and re-check:**
- Reuse the Stage 44 DAT evidence where it is still valid. Investigate only changed or unresolved areas.
- Contract v1, SDK 0.2.0, Model API v1 and Hook System v1: run the compatibility check and the mutation tests at
  current HEAD.
- Run the dependency advisory and licence checks for changed dependency sets.

**F76:** DAT target policies, narrowly scoped to triaged fixtures, never global suppressions.

**Exit:**
- No unreviewed critical risk.
- Contract mutations are detected.
- Every known High finding has a release disposition.

### OV-50 → OV-70 (OV-55 and OV-56 authorized 2026-11-05, OV-50 to OV-54 on 2026-11-07; the rest not yet authorized)
These stages are unchanged from the approved plan. Each starts with the delta review from rule 11 instead of
repeating work verified in Stages 42–44.

| Stage | Work | Exit |
|---|---|---|
| OV-50 | BLUX runtime and model routing: tool approvals, path confinement, timeouts, structured output, fallback, offline and no-model use, hooks | Deterministic and mock suites pass. Provider claims stay BLOCKED until OV-64 |
| OV-51 | Engine reliability: replay, rollback, interrupted transactions, LRC atomicity, GOD on malformed input. CogA → cA → DAT with a forced rejection | Engines work standalone and with BLUX |
| OV-52 | BLUX System as the evidence authority: hash chain, graph, partial failure, retention, migrations | Tampering and corruption are detected, and required receipts fail closed |
| OV-53 | Native BLUX research: eligible corpus, provenance, PII screening, independent holdout, compute, evaluation against Gen 0 | Promote only on reproducible, independent wins; otherwise EXPERIMENTAL |
| OV-54 | `ax`, blux10k, JADIS Toolbox, BLUX App, bluxai.app (owner deployment decision D-08) | Clean install, exit 69, tenant isolation; no second runtime |
| OV-55 | Roughin production: PostgreSQL, Stripe sandbox, R2, PWA on poor networks, mobile, staging | Real-service evidence. A financial release is gated separately |
| OV-56 | Vigyl production: delivered notifications, PostgreSQL, accessibility, privacy | Two-account flow; delivered, failed and unknown are distinguished |
| OV-57 | Resolver and website: bot authorization, subscriptions, Cloudflare 530/1033 root cause | Healthy domain, verified bot, recovery rehearsed |
| OV-58 | Launcher family: F1, F2 and F17 first, then signing (F21) and the crash-loop guard, then the icon and Shooter work. Stage 27 stays closed until its gate passes | Each repository qualifies, the combination qualifies, signed artifacts, device matrix |
| OV-59 | VoidForge: local confirmation UI, read-only device qualification, graduated write classes. Termux Background on a device | Per-class device evidence; never a blanket unlock |
| OV-60 | Institutional and support repositories: ER governance (separately), ivrp, operationrestore, profiles, credits | Explicit state and safe next action |
| OV-61 | Versioned cross-repository integration, building on the Stage 42 contract checks | Integration matrix at pinned commits; BLUX off still works |
| OV-62 | Adversarial and fault-injection drills | No unauthorized change, false success or hidden data loss |
| OV-63 | DAT pilot release and the shared release machinery | A signed, installable DAT with release receipts |
| OV-64 | Real services and providers (D-02, D-05, D-06, D-07) | Dated evidence tied to a deployed version |
| OV-65 | Physical Android qualification (D-03) | Exact device, firmware, build and log evidence |
| OV-66 | Independent product RCs | Explicit `RELEASE_CANDIDATE` with an immutable manifest |
| OV-67 | Controlled distribution; VoidForge to authorized members only | Deployed artifacts verified against the RC |
| OV-68 | Operational resilience | Tested recovery for each released service |
| OV-69 | Lifecycle and continuous qualification | A recurring schedule |
| OV-70 | Final reconciliation and freeze | States RELEASED, QUALIFIED, BLOCKED, DEFERRED, EXPERIMENTAL |

## 5. Product release gates (unchanged)

| Product | Minimum gate | Non-negotiable |
|---|---|---|
| DAT | Real CI, F76 policy, package, tag and signature, independent install | No self-certification |
| BLUX deterministic | Contract and SDK, offline/no-model use, receipts, installer | No model credits required |
| BLUX real-provider | Budgeted call, timeout, error and usage handling, privacy | No fabricated provider success |
| Roughin | PostgreSQL with restore, Stripe sandbox, R2, mobile, staging | No financial claim from mocks |
| Vigyl | Multi-account UI, external notifications, PostgreSQL, accessibility | Never claim an undelivered alert was received |
| Resolver | Bot authorization and subscriptions, domain and tunnel, live smoke test | Website status kept separate from bot health |
| AXIOM Launcher | Entitlement, integrity and signing, crash safety, icon and game polish, devices | Bundled Shooter stays hidden |
| VOID.SYS | Signature, icon quality and coverage, third-party launchers | Source and generated assets match |
| Shooter | Signature, licensed assets, playthrough, GL, frame time, battery | Bundled and standalone versions tested independently |
| VoidForge | Local confirmation, physical device evidence, write unlock per class | Free and members-only |
| Termux Background | Device test with Monet and Termux, reset and uninstall, signing | File writes don't prove rendering |
| bluxai.app | Owner deployment decision, tenancy, remote-run authorization | No second runtime |
| ER / IVRP / Restore | Independent institutional governance and review | Not treated as software qualification |

## 6. Decision register

| ID | Owner decision or external input | Blocks | Safe parallel work |
|---|---|---|---|
| D-01 | GitHub Actions billing and runner access | Hosted CI and release gates | Source, tests, docs |
| D-02 | Real-model provider access and a spend ceiling | Real BLUX provider qualification | Deterministic runtime, evaluation design |
| D-03 | Physical Android reference devices | Device qualification | JVM, build, UI and safety tests |
| D-04 | Signing key custody and distribution channels | Paid Android releases | Entitlement implementation, negative tests |
| D-05 | Stripe, R2 and PostgreSQL staging accounts | Roughin live-service gates | Local functional tests |
| D-06 | Notification provider, privacy and delivery policy | Vigyl delivered-alert claims | In-app flows, accessibility |
| D-07 | Cloudflare and Telegram access for Resolver diagnostics | Resolver production gate | Configuration, local tests |
| D-08 | bluxai.app hosted UI and deployment priority | Hosted workspace release | Core BLUX unaffected |
| D-09 | Font and asset rights; AI contribution attribution (UNR-020, UNR-021, UNR-022) | Some distribution and legal gates | Code and tests |
| D-10 | Independent approval of institutional clinical, legal and financial claims | ER and IVRP operations | Confidential planning |
| D-11 | Pricing or entitlement trust model not yet pinned | Paid distribution | Engineering without invented policy |
| D-12 | Owner correction of shell configuration: the stale `blux()` in `~/.zshrc.local` (F65) and the outdated `ANDROID_HOME` in `~/.zshrc` | Running `blux` and Android builds by name on the owner's machine | Diagnosis and recommended fix (OV-48); never edited automatically |
| D-14 | Transactional email provider and sender domain for account recovery and verification (Roughin and Vigyl) | Password reset and email verification (F38, F46) | Lockout, password change, session hardening (done in OV-55/OV-56) |
| D-13 | Disposition of termux-background's historical artifacts: the four unsupported 2025 GitHub releases (F77) and the compromised keystore in public history (F81; a purge needs an authorized history rewrite) | Truthful distribution state; user safety | Done in OV-49: signer check, README correction |
| D-15 | Independent evaluation custodian for native-model work, and a compute budget (hardware or a paid service) | Native-model training, protected evaluation and any promotion (OV-53) | Data controls, gates, Gen 0 re-runs, EXPERIMENTAL history |

No external blocker is ever reclassified as PASS. A missing decision becomes a targeted question at the stage that
needs it.

## 7. Stage output schema

Every stage report ends with this schema. Its sections:
- baseline: repositories, commits, contracts;
- implementation: changes, exclusions, decisions;
- validation: static, unit, contract, integration, security, build, external, hardware;
- evidence: logs, artifact hashes, receipts, findings;
- disposition: state, blockers, next actions;
- git: commits, remote verified, clean.

A stage is complete only when every required acceptance condition has evidence and the source, contracts,
generated docs, ledger, credits and tests agree. An environment-blocked stage is BLOCKED: not failed, not passed.

## Amendment log

| Date | Change | Authority |
|---|---|---|
| 2026-11-04 | Baseline locked. Amendments: OV-46 reuse and the recovered script; OV-47 separate current findings; OV-48 PostgreSQL `BLOCKED_LOCAL_ENVIRONMENT`; OV-49 history review and reuse of DAT evidence; reuse rule for Stage 42/43 evidence; D-12; git workflow; ER metadata-only | Owner authorization, 2026-11-04 |
| 2026-11-04 | D-13 added: an owner question raised by OV-46 evidence (F77) | Plan section 6 (missing decisions become targeted owner questions) |
| 2026-11-05 | D-13 widened to cover F81 (found in OV-49) | Plan section 6 |
| 2026-11-05 | OV-55 and OV-56 authorized | Owner authorization, 2026-11-05 |
| 2026-11-05 | D-14 added: account recovery needs an email provider, which no stage may pick | Plan section 6 |
| 2026-11-07 | OV-50 authorized | Owner authorization, 2026-11-07 |
| 2026-11-07 | OV-51 authorized | Owner authorization, 2026-11-07 |
| 2026-11-07 | OV-52 authorized | Owner authorization, 2026-11-07 |
| 2026-11-07 | OV-53 authorized | Owner authorization, 2026-11-07 |
| 2026-11-07 | D-15 added: OV-53 needs an independent evaluation custodian and a compute budget, which no stage may choose | Plan section 6 |
| 2026-11-07 | OV-54 authorized; owner decisions F58 (master_log private by default) and F59 (newproject proprietary by default) | Owner authorization and answers, 2026-11-07 |
