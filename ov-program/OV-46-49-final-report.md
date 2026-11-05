# OV-46 → OV-49 final report (2026-11-05)

This is the report the owner's authorization requires at the end of OV-49 (section 6). The stage detail is in
[OV-46](OV-46-report.md), [OV-47](OV-47-report.md), [OV-48](OV-48-report.md) and [OV-49](OV-49-report.md). The
locked plan is [MASTER-PLAN.md](MASTER-PLAN.md).

**Work stops here for owner review. OV-50 is not started.**

## Verdict

OV-46, OV-47 and OV-49 are complete. OV-48 is BLOCKED for hosted CI and PostgreSQL, with every local check done.

Nothing is released, and no status was raised without evidence. Neither hosted CI nor PostgreSQL acceptance can run,
and both are recorded as blocked, not as green.

## 1. Repositories and commits examined

All **32** GitHub repositories are accounted for:
- **Inspected:** 31.
- **`er`:** metadata only, `EXCLUDED_BY_OWNER_POLICY`; remote `main` is `ac4b89a`.
- **Inaccessible:** none.

Baseline SHAs (2026-11-04, before any OV change) are in [inventory/baseline-commits.json](../inventory/baseline-commits.json).
The SHAs after this program are in section 9.

## 2. Evidence reused versus executed fresh

**Reused**, each with its original date and commit, because its repository has not changed since:
- **Stage 44 (2026-10-27):** the blux runtime (597 tests and 45 hard gates), blux-gpt, CogA, cA, DAT, LRC, GOD and
  JADIS Toolbox suites.
- **Stage 44/26:** the Gradle suites of VoidForge, void.os, void.game and void.sys.
- **2026-10-27:** the Vigyl backend (78 tests).
- **DAT verdicts:** the 13 unchanged repositories that passed.
- **Python dependency audits:** unchanged requirement sets.

**Executed fresh** (2026-11-04/05, current HEADs):

| Area | Runs |
|---|---|
| Affected suites | axiom 13, blux10k 10, blux dataset-program 3, blux-system 74 (twice), resolver 173, roughin backend 93 and frontend 4, vigyl frontend 8 |
| Tree-walking suites after the DAT policies | blux-ca-dataset 36, blux-coga-dataset 38, blux-app 11, voidforge tools 24 |
| Builds | roughin and vigyl frontends |
| Audits | `npm audit` for both frontends; Dependabot sweep of 31 repositories; DAT on 17 repositories; history credential scan of 30; `apksigner` on 4 public APKs |
| Governance | `check_contracts`, 13 mutation tests, the docs generators (`--check`) and credits validation, on every commit |
| Reproductions | The Stage 45 exports, rebuilt from the frozen commits: 9/9 byte for byte |

## 3. Changes implemented and committed

| Repository | Commits | Change |
|---|---|---|
| docs | de4f8ee (OV-46), 6ccecec (OV-47), 0f38675 (OV-48), plus the OV-49 commit | Locked plan; `tools/export_reassessment.py`, `build_inventory.py`, `build_findings_current.py`, `audit_workflows.py`; `inventory/`; `ecosystem/findings-current.json`; matrix OV-48 overlay; stage reports |
| credits | d7a6698, 0045778, 197b6d3, plus the OV-49 commit | Per-stage AI-assistance records; OV-49 library catalog and project visibility corrections |
| vigyl | ee34852, 01a73bc, 7234fb4 | README describes the development-preview UI; DAT policy; third-party notices |
| roughin | 19d8839, b908af1, 96d83d6 | README frontend row; DAT policy; notices |
| void.sys | 3f2b7aa | README version matches the manifest (2.1.0-dev) |
| termux-background | b81c003, 9fc05d5 | README states the 2025 releases truthfully |
| blux, blux-app, blux-gpt, blux-system, blux-ca-dataset, blux-coga-dataset, bluxai.app, void.os, voidforge | 56c9b76, dca88bf, 0175196, f7f8ede, 9893d58, e8216be, e894ac6, 4ae9b33, 80aec1a | DAT target policies (F76) |

What was not changed:
- the frozen findings, matrix exports and freeze;
- historical test counts;
- the owner's shell configuration (D-12);
- the workflow files (F80 waits for CI);
- any history rewrite or force push.

## 4. Current unresolved findings

This draws on [ecosystem/findings-current.json](../ecosystem/findings-current.json): 57 frozen findings plus 6 new
ones (F77–F82).

| Status | Count |
|---|---|
| RESOLVED_VERIFIED | 10: F7 (current visibility), F16, F48, F53, F55, F68, F72, F73, F76, F82 |
| PARTIAL | 3: F36, F37, F43 |
| OPEN | 20 |
| DEFERRED | 12 |
| EXTERNAL_BLOCKED | 16 |
| BLOCKED_LOCAL_ENVIRONMENT | 2 |

**Unresolved by severity:** 3 Critical, 14 High, 21 Medium, 13 Low, 2 Info.

| Critical / High | Status | Kind |
|---|---|---|
| F1 void.os entitlement, integrity and signature stubs (Critical) | OPEN | Software defect (trust model D-11) |
| F2 void.game signature verification stub (Critical) | OPEN | Software defect |
| F49 hosted CI cannot start (Critical) | EXTERNAL_BLOCKED | External (D-01) |
| F5 voidforge has no local confirmation UI | OPEN | Software defect |
| F17 void.sys signature verification stub | OPEN | Software defect |
| F43 Vigyl UI not release-qualified | PARTIAL | Software (qualification) |
| F6, F31 no device evidence | EXTERNAL_BLOCKED | External (D-03) |
| F21 no release keystore or signing job | EXTERNAL_BLOCKED | External (D-04) |
| F34, F45 PostgreSQL acceptance | BLOCKED_LOCAL_ENVIRONMENT | Environment (needs CI or a host) |
| F35 Roughin Stripe, R2 and staging | EXTERNAL_BLOCKED | External (D-05) |
| F44 Vigyl notification delivery | EXTERNAL_BLOCKED | External (D-06) |
| F54 theresolverbot.net returns 530 | EXTERNAL_BLOCKED | External (D-07) |
| F60 model suites; F63 native corpus | EXTERNAL_BLOCKED | External (D-02, D-09) |
| F70 contract CI | EXTERNAL_BLOCKED | External (D-01) |

## 5. External blockers versus software defects

- **Software defects that can be worked now:** F1, F2, F5, F17, F19, F29, F38, F39, F46, F57, F64, F79 (triage).
  These belong to OV-55 → OV-59.
- **External or owner-held:**
  - CI (D-01);
  - provider (D-02);
  - devices (D-03);
  - signing (D-04);
  - Stripe, R2 and PostgreSQL staging (D-05);
  - notifications (D-06);
  - Cloudflare and Telegram (D-07);
  - bluxai.app (D-08);
  - rights and attribution (D-09; UNR-020/021/022);
  - trust model (D-11);
  - shell configuration (D-12);
  - termux-background history (D-13).
- **Environment:** PostgreSQL under PRoot.

## 6. CI and PostgreSQL qualification

| Item | Status |
|---|---|
| Hosted CI | **EXTERNAL_BLOCKED**, rechecked 2026-11-04 from existing runs (none triggered). 18 repositories are annotated with the billing lock; 5 private repositories show `startup_failure` with 0 jobs, while their 26 workflow files all parse. No CI run passes at any current HEAD |
| PostgreSQL (Roughin, Vigyl) | **BLOCKED_LOCAL_ENVIRONMENT.** Not retried; no leftover processes. Accepted only from the CI `postgres` jobs or an external host. No SQLite or mock substitute is accepted |
| Workflow hardening | **F80** recorded: 0/26 SHA-pinned, 2 without `permissions`, 17 on `ubuntu-latest`. To be applied with the first CI run after D-01 |

## 7. Security and privacy findings

| Topic | Result |
|---|---|
| Current visibility | 13 private, all matching the constitution (authenticated) |
| Historical credential exposure | Full history of 30 repositories scanned. **One real exposure:** the termux-background release keystore and passwords from 2025 (F81, Medium). It was already declared compromised, is removed from HEAD, and signed none of the public releases. No other real credential was found, including in the six formerly public product repositories |
| Public 2025 termux-background releases | Signer verified as a different, uncompromised key (F77 lowered to Medium); README corrected |
| DAT | The raw release gate passes in all 11 previously failing repositories (F76) with 56 exact-fingerprint suppressions, plus the 6 other changed repositories |
| Dependencies | Shipped frontend licences are all MIT. Roughin build-time advisories (F78) are DEFERRED: no upstream fix exists, and they are not reachable as used. They are not suppressed |

## 8. Documentation and contract reconciliation

- **Documentation drift fixed:**
  - Vigyl's UI;
  - Roughin's frontend tests;
  - VOID.SYS's version;
  - termux-background's releases;
  - Vigyl and Roughin third-party notices;
  - the Resolver and Vigyl matrix versions;
  - 6 credits visibilities.
- **Contracts at current HEAD:** 0 breaking, 0 invariant failures, 13 mutation tests pass.
- **Reproducibility:** the frozen exports are reproducible (9/9). The new generators all have `--check` modes, and
  each passes.

## 9. Commit SHAs and remote synchronization

After the final OV-49 commits, every repository touched in OV-46 → OV-49 was fetched and verified level with
`origin/main` and clean. The SHAs are listed in section 3. The final docs and credits SHAs, and the full sweep, are
stated in the closing message of the session that committed this file. They are not written into this file, because
a commit cannot contain its own SHA.

**Protected branches.** Pushes to the protected `main` branches used the owner's bypass:
- blux, blux-gpt, blux-ca-dataset and termux-background;
- where configured, the others in the protected list.

## 10. Remaining owner decisions

D-01 through D-13 in [MASTER-PLAN.md](MASTER-PLAN.md#6-decision-register). The most consequential:
1. **D-01:** clear the GitHub billing lock.
2. **D-02:** provider access.
3. **D-03:** a reference Android device.
4. **D-13:** unpublish or deprecate the four 2025 termux-background releases, and whether to purge the compromised
   keystore from history (that needs an explicitly authorized rewrite).
5. **D-12:** the two shell configuration corrections (exact lines are in the OV-48 report).
6. **D-09:** confirm the tooling behind UNR-021 and UNR-022; the font licence (UNR-020).

## 11. Recommended next executable stage

**OV-55 (Roughin) and OV-56 (Vigyl)**, run together with OV-50 → OV-52 delta reviews. They are the most ready
products, and the parts of their work that are not blocked can proceed now:
- auth hardening (F38, F46);
- Vigyl's missing flows;
- the termux-background issue triage (F79), as part of OV-59.

PostgreSQL, Stripe, R2 and notification acceptance wait for D-01, D-05 and D-06.

If the owner clears **D-01** first, run the F80 workflow hardening with the first green CI run, then the OV-63 DAT
pilot release. DAT now has clean target policies across the organization.
