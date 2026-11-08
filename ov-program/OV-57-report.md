# OV-57: Resolver and website (2026-11-08)

**State: PARTIAL.** The exit needs a healthy domain, a verified bot and a rehearsed recovery. All three have
live parts that need the owner's Cloudflare and Telegram access (D-07), which this program does not have. What
could be done without it:
- the 530/1033 root cause was established from outside;
- a payment defect that lost paid charges was fixed (F125);
- database backup, restore and a recovery runbook were added and rehearsed locally (F126);
- the release gate and the website were re-verified.

No provider or paid service was called. Live checks were anonymous HTTP and DNS reads.

| Repository | Before | After |
|---|---|---|
| resolver | `aae88c2` | `63cce8b` |
| ov-webpages/theresolver | `49dbeff` | `49dbeff` (no change needed) |

## Delta review (rule 11)

| Exit item | Result |
|---|---|
| Healthy domain | **Not met (D-07).** `theresolverbot.net` and `www` answer HTTP 530, `error code: 1033`: Cloudflare routes them to a tunnel with no healthy connector. `theresolver.pages.dev` serves the current site; its visible text is identical to a local build of `49dbeff`. The apex should be a Pages custom domain. Also, `admin.` and `hq.`, the bot's Mini App hosts, have no DNS at all (NXDOMAIN, F127) |
| Verified bot | **Not met (D-07, F128).** Code review: Mini App `initData` is verified per Telegram's spec (HMAC with the `WebAppData` key, constant-time compare, 24 h freshness, live `get_chat_member` admin check). Admin endpoints take the group from the session. Owner routes answer 404 to non-owners. The owner portal header is constant-time and off unless configured. The release gate passes locally, but nothing has run against Telegram |
| Subscriptions | Pre-checkout and payment checks were thorough (signed payloads, payer, plan, amount and currency, TTL, processing lock, charge-id idempotency). **Gap (F125):** after the user was charged, any rejection dropped the charge without a record |
| Recovery rehearsed | **Local only.** There was no backup, restore or runbook (F126). They now exist and are rehearsed in tests. The live rehearsal (restore on the bot host, tunnel, domain) is an owner step |

## Changes (resolver)

- **F125:** `successful_payment` records every charge it can't apply in `stars_ledger` as `needs_review`, writes
  an audit entry `stars_payment_unapplied`, and gives the user a refund reference. Entitlement still fails
  closed. `needs_review` rows are not counted as revenue, and refunds stay an owner action. This covers:
  - an unknown invoice;
  - an amount, payer, plan or subject mismatch;
  - an expired invoice;
  - a second, different charge for an invoice already paid;
  - an error while applying the payment.
- **F126:** new `scripts/db_backup.py`:
  - `backup` uses SQLite's online backup and writes an integrity check and a checksum (owner-only files);
  - `verify`;
  - `restore` refuses a damaged backup and keeps the replaced database.

  New `docs/RECOVERY.md` covers the 530/1033 diagnosis and fix, Mini App DNS, token rotation, database
  recovery, held payments and website redeploys. `DEPLOY.md` and `RELEASE_READINESS.md` link to it.

## Evidence (executed 2026-11-07 and 2026-11-08)

| Check | Result |
|---|---|
| Release gate | `compileall` ok; 184 unit tests (173 + 11 new) OK; `scripts/smoke_check.py` OK; `run_resolver.sh` from a clean copy with a freshly installed `.venv`: proof mode passes (placeholder secrets refused, smoke probe passes) |
| New tests on the old code | `tests/test_payment_post_charge.py`: 6 of 8 fail on `aae88c2`. The other 2 are preservation checks (a valid payment activates; held charges are not revenue). `tests/test_recovery_rehearsal.py` needs the new script |
| Website | `npm ci`, lint, build and 9 tests pass; pricing matches the bot (5 plans); `npm audit --omit=dev` exit 0; 8 moderate dev-only advisories remain (F88), and npm's only fix is a major downgrade, which policy rules out |
| Live (anonymous reads) | apex and `www`: 530 / 1033 via Cloudflare; `theresolver.pages.dev`: 200; `admin.` and `hq.`: NXDOMAIN; nameservers are Cloudflare's |
| DAT gate | before commit only `release.dirty-worktree` (plus a low-confidence test fixture); after commit exit 0 |
| Push | fast-forward to `main`; resolver has no branch rules |

No secrets were read. The checkout has no `.env` and no tunnel credentials, and both are git-ignored.

## Findings

| ID | Repository | Severity | State | Note |
|---|---|---|---|---|
| F125 | resolver | High | RESOLVED_VERIFIED | charged payments dropped on rejection |
| F126 | resolver | Medium | RESOLVED_VERIFIED | no backup, restore or recovery runbook (live rehearsal is an owner step) |
| F127 | resolver | High | EXTERNAL_BLOCKED (D-07) | Mini App hostnames have no DNS |
| F128 | resolver | Medium | EXTERNAL_BLOCKED (D-07) | bot not verified live |
| F54 | theresolver | High | EXTERNAL_BLOCKED (D-07) | 530/1033: root cause recorded, owner fix in `docs/RECOVERY.md` |
| F88 | theresolver | Low | DEFERRED | dev-only lint advisories; no non-downgrade fix |

## Owner steps (D-07), in order

1. **Cloudflare:** route `theresolverbot.net` and `www` to the Pages project `theresolver` as custom domains,
   removing any tunnel route for them.
2. **Cloudflare:** create tunnel DNS routes for `admin.` and `hq.`. Then run the bot and `./tunnel_start.sh` on
   the bot host.
3. **Telegram:** with the real `.env`, run `docs/LAUNCH_CHECKLIST.md`, including a Stars test purchase and
   `ga:restore`.
4. **Bot host:** take a backup, then rehearse a restore with `scripts/db_backup.py`.

## Stage output

```yaml
stage_id: OV-57
implementation:
  changes: [charged payments held for review, database backup/restore, recovery runbook with the 530/1033 fix]
  excluded: [Cloudflare and Telegram changes (D-07), live bot run, live restore]
validation:
  unit_and_smoke: [184 tests, smoke check, run_resolver.sh proof mode from a clean copy]
  regression: [6 of 8 payment tests fail on aae88c2]
  website: [lint, build, 9 tests, pricing match, production audit clean, Pages serves the build]
  live: [domain 530/1033 and Mini App NXDOMAIN observed; not fixable without D-07]
disposition: {state: PARTIAL, blockers: [D-07], next_actions: [owner steps 1-4; OV-58 needs authorization]}
```
