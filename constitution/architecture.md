# Architecture

## Layers

```text
  Products (own their truth)         AXIOM Launcher · VOID.SYS · AXIOM Shooter · VoidForge · Roughin · Vigyl
                                     · Resolver bot · Resolver website · Termux Background
  Developer tools                    ax (AXIOM control plane) · blux10k · jadis
  ─────────────────────────────────────────────────────────────────────────────────────────────────────
  Platform: BLUX                     blux runtime + CLI (Contract v1, capability registry, policy,
                                     Model API v1 router, Hook System v1) · blux-sdk
                                     BLUX System (execution truth) · BluxGPT (provider transport)
                                     BLUX App (local mission control) · bluxai.app (private workspace)
  Engines (standalone, callable)     CogA (reasoning) · cA (construction/repair) · DAT (audit) · LRC (repository
                                     creation) · GOD (discovery)
  Data                               blux-coga-dataset · blux-ca-dataset · blux_training (pipeline in blux)
  Governance                         docs · credits · .github · .github-private
```

Arrows only point down or sideways through published interfaces: CLIs that print one JSON document
([ADR-0008](https://github.com/Outer-Void/blux/blob/main/docs/adr/0008-no-arbitrary-stdout-protocol.md)),
subprocess providers ([ADR-0009](https://github.com/Outer-Void/blux/blob/main/docs/adr/0009-subprocess-provider.md)),
`.blux/` declarations, and the Model API. No component imports another component's internals across a
repository boundary, apart from the shared `blux-sdk`.

## Product vs platform

| | Products | Platform (BLUX) |
|---|---|---|
| Truth | Each owns its business, care, financial, device or moderation truth | Owns execution records (BLUX System) and capability/policy definitions |
| BLUX | Optional or excluded; must work without it | Is BLUX |
| Integration | Calls BLUX (or is called) only through Contract v1 / Model API / `.blux/` | Never reaches into a product's state |
| Examples of the rule | Roughin's invoices, Vigyl's care responsibility, VoidForge's device writes never move into BLUX | BLUX may draft, summarize or suggest for a product only where that product integrates it |

## Naming

| Name | Is | Is not |
|---|---|---|
| BLUX | The intelligence platform (`Outer-Void/blux`) and its `blux` CLI | The organization (Outer Void) |
| `blux` | BLUX's direct CLI | A shell function: BluxGPT 1.0's `blux()` overlay was retired (BluxGPT installs `bluxgpt`) |
| BluxGPT | The provider transport behind the Model API (`blux-gpt`, command `bluxgpt`) | An agent or a router |
| AXIOM / `ax` | The developer control plane (`Outer-Void/axiom`) | The launcher |
| AXIOM Launcher | The Android launcher (`Outer-Void/void.os`) | `ax`; the repository is named void.os for history |
| VOID.SYS | The icon system (`void.sys`) | A system service |
| AXIOM Shooter | The game (`void.game`), also a hidden launcher Easter egg | Part of `ax` |
| Resolver / TheResolverBot | The Telegram bot runtime (`Outer-Void/resolver`, private) | The website |
| Resolver website | The marketing site (`ov-webpages/theresolver`, private) | A source of bot state or pricing truth |
| BLUX System | Execution truth store (`blux-system`) | BLUX itself |
| BLUX App | Local mission control (`blux-app`) | bluxai.app |
| bluxai.app | The private web workspace (`ov-webpages/bluxai.app`) | `blux-web` (it does not exist) |
| jadis | JADIS Toolbox's workstation CLI (`jadis.toolbox`) | blux10k |
| BLHermes | Archived Hermes fork, replaced by BLUX | Active |

## Resolver bot vs Resolver website

- The **bot** (`resolver`) owns moderation, entitlements, the Telegram Stars price catalogue
  (`app/pricing.py`) and payments. It is the only source of runtime state.
- The **website** (`theresolver`) owns marketing, acquisition, support and legal pages. It shows no live status.
  Its prices are a description checked against the bot (`npm run check:pricing -- <bot checkout>`). It links into
  Telegram through a reviewed set of deep links.
- They release independently: separate repositories, versions and deployment (the bot runs on Outer Void's
  server; the site on Cloudflare Pages).

## AXIOM Launcher vs `ax`

- **AXIOM Launcher** (`void.os`) is an Android app. It bundles VOID.SYS and AXIOM Shooter, vendored from their
  authoritative repositories at locked commits with drift checks. It does not require BLUX; its optional BLUX
  layer (Stage 27) has not been built.
- **`ax`** (`axiom`) is a command-line control plane on a developer's machine. It routes commands (`ax env`,
  `reason`, `build`, `create`, `audit`, `projects`, `inspect`, `capabilities`, `devices`, `ask`, `agent`) to the
  engine that owns each concern, and exits 69 when that engine is missing. `ax routes` prints the table.
- They share the AXIOM name and nothing else: no code, no runtime dependency.
