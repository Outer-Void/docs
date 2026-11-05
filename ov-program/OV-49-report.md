# OV-49: security, licensing, privacy, contracts (2026-11-04 → 05)

**State: COMPLETE locally.**
- **Hosted CI.** Still EXTERNAL_BLOCKED (D-01).
- **Credentials.** One real credential exposure was found in git history (F81). It was already declared compromised,
  and it was not used for any public release.
- **F76.** Resolved: DAT's raw release gate now passes in every repository.
- **Contracts.** Clean at current HEAD.
- **Licensing.** Drift from the post-freeze frontend work is corrected.

## 1. Privacy: current visibility versus historical exposure

**Current visibility (accepted).** The authenticated API reports 13 private repositories, matching the
constitution (OV-46).

**Historical exposure.** OV-49 reviewed the full `git log --all -p` history of all 30 inspected repositories. `er` was
excluded by owner policy, and the archived upstream fork is out of scope. Matched patterns:
- AWS, GitHub, OpenAI, Anthropic, Stripe, Telegram, Google, Slack and Cloudflare token shapes;
- PEM private-key blocks;
- credentials embedded in URLs;
- password and secret assignments;
- keystore, key and `.env` files ever added.

**Values were never stored or printed.** The scan recorded only the rule, the location, a SHA-256 prefix and the
shape.

| Result | Count | Disposition |
|---|---|---|
| Distinct credential-shaped values | 56 in 14 repositories | All inspected with values masked. They are test fakes proving redaction or rejection (blux, blux-system, blux-gpt, blux-app, voidforge, bluxai.app, the datasets), documentation and example placeholders (dat, lrc), CI-local PostgreSQL service credentials and `.env.example` (roughin, vigyl), a 2026-04 docker-compose development URL (`roughin:roughin@db`, removed), and the BLHermes redaction probe samples |
| Real Telegram, Stripe, cloud or provider tokens | **0** | Resolver's bot token was never committed |
| Key files ever added | 2, both termux-background | **F81**, below |

### F81: termux-background release keystore in public history (Medium)

- **What was committed.** `termux-release.keystore` and `app/termux-release.keystore` (PKCS12, alias
  `termuxbackground`), plus `keystore.properties` with non-placeholder 9-character store and key passwords. They were
  committed on 2025-07-30 (17f815b → 8c3857b).
- **Current state.** They were removed from HEAD on 2026-10-21 (f48d6c9), and the README already declares the key
  compromised. The files are still reachable in the public history.
- **How the fingerprint was read.** The certificate fingerprint was read with `keytool`. The historical password was
  passed through the environment and never printed. The temporary copies were deleted afterwards.
- **Fingerprint:** SHA-256 `070cd54d…f68e` (O=Justadudeinspace).
- **Next action.** Treat the key as permanently revoked. A history purge needs an authorized history rewrite and
  would not undo the exposure (owner decision D-13, widened).

### F77 re-assessed: the four public 2025 releases (High → Medium)

- **Signers.** `apksigner verify --print-certs` on all four `app-release.apk` files shows one signer, SHA-256
  `7bd3603d…ab4a` (O=Termux, OU=Dev). That is **not** the compromised key.
- **Where that key lives.** No trace of the signing key exists in the repository history.
- **README.** It now states this truthfully (termux-background b81c003 and 9fc05d5): the builds are historical and
  unsupported, there are open crash reports, and the signer has been checked.
- **Unpublishing.** Whether to unpublish the releases is still owner decision D-13.

## 2. DAT: reuse and F76

**Reused without re-running.** Stage 44 verdicts (2026-10-27) for the 13 unchanged repositories that passed then.

**Re-run** at current HEAD for every changed repository:
- axiom, blux10k, resolver, void.sys, docs and credits all pass;
- resolver's 2 high findings are low-confidence test fixtures in `tests/test_payment_payload.py`, below the gate, as
  at Stage 44.

**F76 resolved.** The 11 repositories whose raw gate failed now commit a `.dat/policy.json`. blux extended its
existing policy by one entry:
- **How they were triaged.** All 42 blocking findings were inspected line by line with values masked. The two
  `DEV_SECRET` defaults were confirmed refused by each production configuration check (equal to `DEV_SECRET` or
  shorter than 32 characters).
- **How narrow the suppressions are.** Each one pins `rule_id`, `path` and the exact `fingerprint`, and gives a
  reason. There are no globs and no global suppressions. A new finding, or a changed fake, stays blocking.
- **How they were validated.** `dat policy verify` passed for all 11. Repositories with tests that walk their own tree
  were re-run with the policy present:

  | Repository | Result |
  |---|---|
  | blux-ca-dataset | 36 passed, 2 skipped |
  | blux-coga-dataset | 38 passed |
  | blux-app | 11 passed, with BLUX on PATH |
  | blux-system | 74 passed |
  | voidforge tools | 24 passed |

| Repository | Policy commit | Suppressed | `dat audit` verdict at that commit (2026-11-05) |
|---|---|---|---|
| blux | 56c9b76 | 15 | pass, 0 blocking |
| blux-app | dca88bf | 3 | pass |
| blux-gpt | 0175196 | 2 | pass |
| blux-system | f7f8ede | 2 | pass |
| blux-ca-dataset | 9893d58 | 1 | pass |
| blux-coga-dataset | e8216be | 1 | pass |
| bluxai.app | e894ac6 | 1 | pass |
| roughin | b908af1 | 10 | pass |
| vigyl | 01a73bc | 7 | pass |
| void.os | 4ae9b33 | 5 | pass |
| voidforge | 80aec1a | 9 | pass |

Before the commits, each repository's only remaining blocker was `release.dirty-worktree`, caused by the
uncommitted policy itself. It cleared once the policies were committed.

## 3. Dependencies and licensing (changed sets only)

| Check | Result |
|---|---|
| Dependabot (authenticated, OV-47) | 0 open alerts except roughin #15 (low, development scope) |
| Roughin F78 | **DEFERRED, not suppressed.** Every package in the chain is at its latest version (vite-plugin-pwa 2.0.0 → workbox-build 7.4.1 → @rollup/plugin-node-resolve 16.0.3 → deepmerge 4.3.1), and deepmerge 4.3.1 is itself affected, so no fix exists. Build-time only, and not reachable as used: the inputs are Roughin's own config and globs |
| Shipped frontend licences (`npm ls --omit=dev`) | All MIT: vigyl 3 packages, roughin 36 |
| **F82**, licensing drift (resolved) | Vigyl bundled React 19 without notices. It now has `THIRD_PARTY_NOTICES.md` and verbatim licence texts (7234fb4). Roughin's notices now show react-router 7.18.4 and add scheduler (96d83d6). Credits gained 16 library entries and 4 corrected versions, and 6 project visibilities were set from the authenticated API |
| Python dependency sets | Unchanged since Stage 44 (roughin and vigyl requirements, resolver), so that evidence is reused |

## 4. Contracts at current HEAD

The contracts checked are Contract v1, SDK 0.2.0, Model API v1 and Hook System v1.

| Check | Result |
|---|---|
| `tools/check_contracts.py --workspace ~/ov` | ok: 0 breaking, 0 invariant failures, 5 informational commit moves |
| Contract mutation tests (`tests/`) | 13 passed (each docs gate run in OV-46 to OV-49) |
| blux-system SDK pin | blux 6ee4c80 = SDK 0.2.0, identical to HEAD (F68) |
| Hosted contract CI (F70) | EXTERNAL_BLOCKED (D-01) |

## Stage output

```yaml
stage_id: OV-49
implementation:
  changes: [.dat/policy.json x11, vigyl and roughin notices, termux-background README, credits catalog,
            findings F76/F77/F78/F81/F82, matrix blockers, D-13 scope]
  excluded: [er (policy), history rewrite (not authorized), F78 transitive overrides]
validation:
  security: [history scan 30 repos: 1 real exposure (F81); DAT pass 11/11 + 6 changed; apksigner on 4 APKs]
  contract: [check_contracts ok; 13 mutation tests]
  unit: [blux-ca-dataset 36, blux-coga-dataset 38, blux-app 11, blux-system 74, voidforge tools 24]
  external: [hosted CI EXTERNAL_BLOCKED]
disposition: {state: COMPLETE (local); hosted CI BLOCKED, blockers: [D-01, D-13], next_actions: [owner review before OV-50]}
```
