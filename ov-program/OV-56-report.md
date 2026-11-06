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

## Follow-up: repeating tasks and the remaining screens (`68a56a0`, owner request 2026-11-05)

- **Repeating tasks.** A task can repeat every 1–30 days, which needs a due time. The sweep creates each next
  occurrence 24 hours before it is due, copying the latest occurrence.
- **Why the schedule drives it.** Occurrences follow the schedule, not completions. If they followed completions,
  someone who stopped responding would be escalated once and then never again. Now each missed occurrence
  escalates on its own (tested: four missed days give levels 1, 2, 3, 3).
- **Safety rules:**
  - **Sweep outage.** Occurrences already past grace are not created, because nobody was shown them. The gap is
    recorded once (`task.series_gap`), so there is no burst of escalations when the sweep restarts.
  - **Assignee leaves or is deleted.** The series stops and caregivers are told. It is never reassigned
    automatically.
  - **Duplicates.** A unique constraint on series and due time, plus a row lock, stop concurrent sweeps creating
    the same occurrence twice.
  - **Cancel and stop.** Cancel affects one occurrence. "Stop repeating" ends the series.
  - **Migration 0003.** It only adds, and it is checked on SQLite only.
- **Screens:**
  - repeat option, schedule label and stop repeating;
  - edit task (with discard) and reassign;
  - invitation list and revoke (only pending invitations can be revoked);
  - leave circle, and remove member (confirmed, never yourself);
  - load older timeline activity.
- **Evidence:** backend **97 passed** (11 new in `tests/test_recurrence.py`); frontend **25 passed** (11 new in
  `src/Manage.test.jsx`); build ok; `npm audit` 0; DAT gate pass.
- **Not done:** reminders before a task is due, live updates, and browser and mobile accessibility testing.

## Follow-up: reminders (`728be24`, owner request 2026-11-06)

- **What it does.** A task with a due time can carry an in-app reminder for its assignee, from 5 minutes to a
  week before (the app offers 15 minutes, 1 hour and 1 day). The sweep sends it once, when the window opens.
- **Rules:**
  - **Never late.** If the sweep missed the window and the task is already due, nothing is sent; missed-task
    escalation takes over.
  - **Re-armed.** Moving the due time or changing the reminder re-arms it; other edits do not.
  - **Repeating tasks** copy the setting to each occurrence.
  - **Scope.** Only the assignee and only open tasks. In-app only, like every Vigyl notification.
  - **Migration 0004.** It only adds, and it is checked on SQLite only.
- **UI.** Choose a reminder at creation or in the editor. The task shows the reminder and whether it was sent in
  the app.
- **Defect fixed (existing).** The add-task form was not cleared after a task was added, so the next task
  silently reused the previous title, repeat and reminder. It is now reset, with a test.
- **Evidence:** backend **105 passed** (8 new in `tests/test_reminders.py`); frontend **27 passed** (2 new); build
  ok; `npm audit` 0; DAT gate pass.

## Follow-up: live updates (`875b006`, owner request 2026-11-06)

- **Why polling.** Vigyl keeps the access token in memory and sends it as a header. A browser `EventSource`
  stream cannot send headers, so the token would end up in URLs and server logs. Polling keeps it in the header.
- **Pulse endpoint.** `GET /care-groups/{id}/pulse` is for members only. It returns the latest timeline event id,
  the latest message id, and the caller's unread-notification count. Every change to tasks, members and
  invitations is a timeline event, so any movement means something changed.
- **App behaviour.**
  - Polls every 30 seconds, only while a circle is open, the tab is visible and the browser is online. Coming back
    to the tab or reconnecting checks at once.
  - Reloads the circle in place, and only when a value moved.
  - With an editor open or an action running, it shows "New activity in this circle / Show updates" and applies
    the update when the editor closes. Typed text is never lost.
  - Background failures show a "Live updates paused" note, not an error banner.
  - Being removed from the circle clears it and says so.
  - Screen readers hear "Circle updated" only when a reload actually happened.
- **Not covered:** profile name changes are not detected until the next reload.
- **Evidence:** backend **108 passed** (3 new, `tests/test_pulse.py`); frontend **35 passed** (8 new,
  `src/Live.test.jsx`, stable over two consecutive runs); build ok; `npm audit` 0; DAT gate pass.

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
| F43 | PARTIAL | PARTIAL | Browser and mobile accessibility testing; staging |
| F44 | EXTERNAL_BLOCKED | EXTERNAL_BLOCKED | A real channel (D-06). In-app receipts are now honest |
| F46 | OPEN | PARTIAL | Password reset and email verification (D-14); 2FA; subscriptions and location; legal review |
| F45 | BLOCKED_LOCAL_ENVIRONMENT | unchanged | CI `postgres` job (D-01) |

## Stage output

```yaml
stage_id: OV-56
implementation:
  changes: [alert receipts API + UI, DB-backed lockout, password change, migration 0002, messages UI,
            account export/delete UI, privacy-policy draft disclosure]
  follow_up: [repeating tasks + migration 0003, edit/reassign, invitation revoke, leave/remove member, timeline paging]
  follow_up_2: [in-app reminders + migration 0004, add-task form reset fix]
  follow_up_3: [live updates: pulse endpoint + polling that never disturbs an open editor]
  excluded: [external notification channel (D-06), password reset (D-14), legal review]
validation:
  unit: [backend 86, 97, 105, 108 (SQLite); frontend 14, 25, 27, 35]
  security: [DAT gate pass; npm audit 0]
  external: [PostgreSQL BLOCKED_LOCAL_ENVIRONMENT, CI EXTERNAL_BLOCKED, delivery EXTERNAL_BLOCKED]
disposition: {state: PARTIAL, blockers: [D-01, D-03, D-06, D-14], next_actions: [browser accessibility pass, staging]}
```
