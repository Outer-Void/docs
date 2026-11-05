# OV-55: Roughin production work (2026-11-05)

**State: PARTIAL.** The local work is done: session storage, account lockout, password change and timestamps.
What the stage exit needs is still blocked:
- PostgreSQL and a backup restore (F34, D-01);
- Stripe test mode, R2 and staging (F35, D-05);
- real-device mobile and poor-network testing (F37, D-03);
- account recovery, which needs an email provider (F38, new decision D-14).

No financial or production claim is made.

## Delta review (rule 11)

The review started from roughin `96d83d6` (OV-49).
- **Auth.** The code had not changed since the freeze, so F38 applied in full: tokens in `localStorage`, no
  lockout, no password change.
- **Timestamps.** `datetime.utcnow()` appeared in 23 places (F39; 938 deprecation warnings).
- **Reused.** OV-49's licence and advisory evidence still applies, because no dependency changed. F78 stays
  DEFERRED.

## Changes

| Commit | Change |
|---|---|
| `0a794ac` | **Session storage.** The refresh token is an `httpOnly`, `Secure`, `SameSite=Strict` cookie scoped to `/api/v1/auth`, and it never appears in a response body. The access token is kept in memory only. A reload restores the session from the cookie, and tokens that earlier versions left in `localStorage` are deleted. A non-secret flag keeps the app shell available on an offline reload |
| | **Lockout.** Per-account lockout is stored in the database, so it holds across instances. 5 consecutive failures lock the account for 15 minutes (429 with `Retry-After`, audited). Unknown emails never create a lock |
| | **Password change.** `POST /auth/password` and a Settings form. It needs the current password, ends every other session and rejects older access tokens |
| | **Migration 0004** adds three user columns. It only adds, and it is checked on SQLite only |
| | **Timestamps.** `app.timeutil.utcnow()` gives the same naive UTC values, and the schema is unchanged. Deprecation warnings drop to 0 |
| | **Configuration.** Production refuses `REFRESH_COOKIE_SECURE=false` |
| | **DAT.** 5 pinned suppressions for the new fictional test passwords |
| `61c4b47` | **Defect fix (in code added by this stage).** Presenting a token revoked by a password change set off reuse detection, which also ended the new session. The old tokens are now deleted, so they are simply unknown. A regression assertion was added |

## Evidence (executed 2026-11-05)

| Check | Result |
|---|---|
| Backend suite at `0a794ac` | 100 passed (93 before, 7 new), SQLite, 0 warnings |
| Auth suite at `61c4b47` | 23 passed |
| Frontend | 10 passed (4 before, 6 new); `vite build` ok; `npm audit --omit=dev` 0 |
| `ruff` | clean |
| DAT gate (`fail_on: high`, `min_confidence: medium`) | pass, 0 blocking, at both commits |
| PostgreSQL migration 0004, backup and restore | **not run**: BLOCKED_LOCAL_ENVIRONMENT (F34). No SQLite result is offered in its place |

## Findings

| ID | Before | After | Remaining |
|---|---|---|---|
| F38 | OPEN | PARTIAL | Password reset and email verification (D-14); the per-IP limiter is still per instance; 2FA is an owner decision |
| F39 | OPEN | PARTIAL | Partial-payment and refund semantics (owner); `timestamptz` needs PostgreSQL evidence |
| F37 | PARTIAL | PARTIAL | Real-device mobile and poor-network testing |
| F34, F35, F40, F41 | unchanged | unchanged | D-01, D-05, brand pipeline, after F34/F35 |

## Stage output

```yaml
stage_id: OV-55
implementation:
  changes: [httpOnly refresh cookie, in-memory access token, DB-backed lockout, password change, migration 0004,
            utcnow helper, production cookie guard, DAT suppressions x5]
  excluded: [password reset and email verification (D-14), Stripe/R2/staging (D-05), partial payments (owner)]
validation:
  unit: [backend 100 (SQLite), auth 23 after fix, frontend 10]
  security: [DAT gate pass; npm audit --omit=dev 0]
  external: [PostgreSQL BLOCKED_LOCAL_ENVIRONMENT, CI EXTERNAL_BLOCKED, Stripe/R2 EXTERNAL_BLOCKED]
disposition: {state: PARTIAL, blockers: [D-01, D-03, D-05, D-14], next_actions: [CI postgres job, staging accounts]}
```
