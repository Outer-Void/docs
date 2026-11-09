# OV-64: real services and providers (2026-11-09)

**State: BLOCKED.** The exit asks for dated evidence tied to a deployed version. None of the four external paths
could produce it:
- **D-02, model providers:** you authorized paid calls with a US$1 ceiling. The configured OpenAI, Anthropic and
  DeepSeek keys are valid, but every account has no balance, so no model answered. Actual spend: US$0.
- **D-05 (Roughin live services), D-06 (Vigyl notifications), D-07 (Resolver domain and bot):** kept blocked by
  your decision.

The stage still fixed two local defects in BluxGPT (F118, F141). It also showed that every failure path tells
the truth: no unfunded or refused call was reported as a success.

| Repository | Before | After |
|---|---|---|
| blux-gpt | `0175196` | `bc2aba4` (F118), `11b83a4` (F141); owner bypass: protected `main` |
| docs | `ab13142` | this commit |

## Owner decisions (2026-11-09)

| Decision | Choice |
|---|---|
| D-02 | Paid calls authorized, ceiling US$1 total |
| D-05 | Keep blocked |
| D-06 | Keep blocked |
| D-07 | Keep blocked |

## Delta review (rule 11)

| Item | Result |
|---|---|
| Real-provider tests | Reused: BluxGPT `test_real_providers.py` (one tiny prompt per route; an unfunded account is a skip with its reason) and BLUX's two `BLUX_REAL_MODELS` tests |
| Credentials | `~/.config/bluxgpt/.env` holds OpenAI, Anthropic and DeepSeek keys (only lengths were read; values never printed). The old request logs redact them. The file is mode 644, because `install.sh` created it with the default umask (**F141**) |
| F118 | In scope (OV-53 deferred it here) |
| Domain (D-07) | Re-checked from outside, read-only |

## Changes (blux-gpt)

- **F118 (`bc2aba4`).** A reasoning model served through an OpenAI-compatible server without a reasoning parser
  returns its chain of thought as a leading `<think>…</think>` block, which reached answers and BLUX sessions.
  - A leading `<think>` or `<thinking>` block is now dropped.
  - In streams, the start of the answer is held back until it is clear whether a block opens.
  - An unclosed block leaves no answer text; a tag later in the answer is kept.
- **F141 (`11b83a4`).**
  - `scripts/setup_config.sh` creates the key file as 0600 in a 0700 directory.
  - An existing file that others can read gets a warning with the `chmod 600` command and is not changed.
  - Your file was not changed: running the step on this machine printed the warning.

## Real-provider run

Every call went through a metered harness (`ov-program/evidence/OV-64-real-providers.json`):
- Before each call it checked that the call's worst case kept the running total under the ceiling. The bound uses
  US$5 per million input and US$25 per million output tokens, above every route's list price.
- A provider stopped at its first auth or billing error.
- The run failed if any key value appeared in its results.

| Case | OpenAI `gpt-5-mini` | Anthropic `claude-haiku-4-5` | DeepSeek `deepseek-chat` | DeepSeek `deepseek-reasoner` |
|---|---|---|---|---|
| Text | `PROVIDER_QUOTA_EXCEEDED` ("no credits remaining") | `PROVIDER_QUOTA_EXCEEDED` ("credit balance is too low") | `PROVIDER_QUOTA_EXCEEDED` ("Insufficient Balance") | not run (provider stopped) |
| Streaming, structured output, tool call | not run | not run | not run | not run |
| Wrong key (free) | `PROVIDER_AUTH_FAILED` (401), as expected | same | same | - |
| 1 ms deadline (free) | `PROVIDER_TIMEOUT`, as expected | - | - | - |

**Spend:**
- Actual spend is US$0: every paid request was refused for billing before generating anything.
- The harness's upper bound, US$0.039, counts the worst case for the three refused calls.
- The official suites added 6 more refused requests (BluxGPT 4, BLUX 2), also unbilled. Their worst case would
  still be well under the ceiling.

**The official suites under the same accounts:**

| Suite | Result | Verdict |
|---|---|---|
| BluxGPT `test_real_providers.py` | 4 skipped, each naming `PROVIDER_QUOTA_EXCEEDED` | Correct: never a pass |
| BLUX `test_model_api.py::test_real_provider_through_default_routes` | Failed: `EXECUTION_FAILED`, "Every route for blux-main failed" | Correct: fails closed |
| BLUX `test_cli_direct.py::test_real_provider_through_default_routes` | Failed: `blux` exit 1, `ALL_ROUTES_FAILED`, each route with its billing message | Correct: fails closed |

These two BLUX tests stay failing until an account is funded. They are not counted as passes.

## D-07 re-check (2026-11-09T21:33Z)

The domain is unchanged since OV-57:
- `theresolverbot.net` and `www.` return HTTP 530 (error 1033, a tunnel with no connector);
- `theresolver.pages.dev` returns 200;
- `admin.` and `hq.` do not resolve.

## Evidence (executed 2026-11-09)

| Check | Result |
|---|---|
| Old-code check | F118: 7 reasoning cases fail on `0175196`, 3 control cases pass on both. F141: 3 tests fail on `bc2aba4` |
| blux-gpt | 62 passed, 1 skipped (real providers); ruff, format, mypy, shellcheck clean |
| BLUX boundary | `test_model_api.py` and `test_cli_direct.py` with `BLUX_REQUIRE_BLUXGPT=1` (mock): 18 passed. The 2 skips are the real-provider tests. blux's integration pin stays `0175196` until the next matrix rerun |
| DAT gate | before each commit only `release.dirty-worktree`; after each commit exit 0 |

**Not covered:** F118 against a real local reasoning server (none is installed here); every live service (D-05,
D-06, D-07).

## Findings

| ID | Repository | State | Note |
|---|---|---|---|
| F118 | blux-gpt | RESOLVED_VERIFIED | inline reasoning dropped (fake-provider evidence) |
| F141 | blux-gpt | RESOLVED_VERIFIED | key file created private; your existing file needs `chmod 600 ~/.config/bluxgpt/.env` |
| F10, F60 | - | EXTERNAL_BLOCKED (D-02) | keys valid, accounts unfunded; rerun the same US$1 run after funding one |
| F35 | - | EXTERNAL_BLOCKED (D-05) | kept blocked |
| F44 | - | EXTERNAL_BLOCKED (D-06) | kept blocked |
| F54, F127, F128 | resolver | EXTERNAL_BLOCKED (D-07) | re-checked, unchanged |

## Stage output

```yaml
stage_id: OV-64
implementation:
  changes: [F118 inline reasoning filter (responses and streams), F141 private key file, metered real-provider run]
  excluded: [Roughin live services (D-05), Vigyl notifications (D-06), Resolver domain and bot (D-07)]
validation:
  real_providers: [keys valid; OpenAI, Anthropic, DeepSeek accounts unfunded; spend US$0; failures reported honestly]
  regression: [new tests fail on the previous commits]
disposition: {state: BLOCKED, blockers: [D-02 funding, D-05, D-06, D-07],
              next_actions: [fund one provider account and repeat the run; OV-65 needs authorization]}
```
