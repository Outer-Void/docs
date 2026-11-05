# OV-56: Vigyl production work (2026-11-05)

**State: PARTIAL.** For alerts, Vigyl now tells two states apart, "seen in the app" and "not seen", and it reports
external delivery as "not configured" instead of implying it. It also gained a lockout, password change and the
missing account and messaging UI flows. What the stage exit needs is still blocked:
- delivered notifications (F44, D-06);
- PostgreSQL (F45, D-01);
- browser and real-mobile accessibility testing (F43, D-03);
- account recovery (F46, D-14).

## Delta review (rule 11)

The review started from vigyl `7234fb4` (OV-49).
- **Already sound.** Tokens were in memory only and timestamps were timezone-correct (`app/core/time.py`).
- **Gaps.** There was no lockout and no password change. The UI had no messages, no account settings and no
  view of who an escalation reached.
- **Reused.** The backend suite at `a0816a4` (78 tests, 2026-10-27) served as the baseline; it was re-run in full
  here.

## Changes (`c7058b9`)

- **Alert receipts.** `GET /tasks/{id}/alerts`, for caregivers only (403 for others, 404 for non-members).
  - For each missed-task alert it shows the recipient, the level, and `in_app: seen` (with `seen_at`) or
    `not_seen`.
  - External delivery is `not_configured`. When a provider is added (D-06), a channel that cannot confirm
    delivery must report `unknown`, never `delivered`.
- **UI.** "Who has seen the alert?" on missed tasks, with the warning that no push, email or text message is sent.
  The other new flows:
  - circle messages;
  - password change;
  - data export;
  - account deletion (typing DELETE confirms it).
- **Lockout.** Stored in the database: 5 consecutive failures lock the account for 15 minutes (429 with
  `Retry-After`; timeline event `account.locked`).
- **Password change.** `POST /auth/password` deletes every refresh token, rejects older access tokens, and returns
  a fresh pair. The same reuse-cascade issue found in OV-55 was avoided here from the start.
- **Migration 0002.** It only adds columns, and it is checked on SQLite only.
- **Docs.** notifications, security-privacy, api-spec, release checklist and the READMEs. The privacy-policy draft
  now says that caregivers can see whether an alert was opened; it still needs legal review.

## Evidence (executed 2026-11-05)

| Check | Result |
|---|---|
| Backend suite | 86 passed (78 before, 8 new), SQLite |
| Two-account flow (exit criterion) | Covered through the API with three accounts in `tests/test_account_security.py::test_two_accounts_complete_and_verify_a_task`: assign, complete, notify, verify by a second caregiver. UI flows are tested with a scripted client. **Not done:** a real browser with two signed-in people, and staging |
| Seen / not seen / not configured | `test_alert_receipts_*`: one recipient opens an alert and only that row turns `seen`; external delivery is always `not_configured` |
| Frontend | 14 passed (8 before, 6 new); `vite build` ok; `npm audit --omit=optional` 0 |
| `ruff` | clean |
| DAT gate | pass, 0 blocking |
| Accessibility | New controls are labelled, status and errors use the existing `status` and `alert` regions, and focus styles cover `textarea`. **No** browser, screen-reader or mobile testing was done (F43) |
| PostgreSQL migration 0002 | **not run**: BLOCKED_LOCAL_ENVIRONMENT (F45) |

## Findings

| ID | Before | After | Remaining |
|---|---|---|---|
| F43 | PARTIAL | PARTIAL | Reassignment and editing, invitation revocation, live updates; browser and mobile accessibility testing; staging |
| F44 | EXTERNAL_BLOCKED | EXTERNAL_BLOCKED | A real channel (D-06). In-app receipts are now honest |
| F46 | OPEN | PARTIAL | Recurring tasks; password reset and email verification (D-14); 2FA; subscriptions and location; legal review |
| F45 | BLOCKED_LOCAL_ENVIRONMENT | unchanged | CI `postgres` job (D-01) |

## Stage output

```yaml
stage_id: OV-56
implementation:
  changes: [alert receipts API + UI, DB-backed lockout, password change, migration 0002, messages UI,
            account export/delete UI, privacy-policy draft disclosure]
  excluded: [external notification channel (D-06), password reset (D-14), recurring tasks, legal review]
validation:
  unit: [backend 86 (SQLite), frontend 14]
  security: [DAT gate pass; npm audit 0]
  external: [PostgreSQL BLOCKED_LOCAL_ENVIRONMENT, CI EXTERNAL_BLOCKED, delivery EXTERNAL_BLOCKED]
disposition: {state: PARTIAL, blockers: [D-01, D-03, D-06, D-14], next_actions: [recurring tasks, remaining UI flows, browser accessibility pass]}
```
