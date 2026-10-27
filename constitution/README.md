# The Outer Void constitution

The authoritative description of how the Outer Void ecosystem is organized: who owns what, how components
integrate, and the policies every repository follows. Written 2026-10-27 (Stage 40) and cross-checked
against source and tests on that date.

## Precedence

1. **Source and tests are the truth.** Where this constitution and a repository disagree about behaviour, the
   repository's code and tests describe what happens. The constitution is then wrong, and gets a findings entry.
2. **Specifications live with their owners.** Contract, Model API and Hook System schemas, ADRs and protocol
   documents stay in the repositories that implement them. This constitution links to them and never copies them.
3. **Roles and policies live here.** Ownership, boundaries, naming and cross-repository policy are decided here
   and referenced from repositories.
4. **Status lives in the matrix.** [`ecosystem/status-matrix.md`](../ecosystem/status-matrix.md) records evidence
   (generated from `tools/build_status_matrix.py`); nothing here claims a status.
5. **Gaps live in findings.** [`ecosystem/findings.md`](../ecosystem/findings.md).

Nothing aspirational is described as shipped. "Not built" and "blocked" are stated as such.

## Contents

| Document | Covers |
|---|---|
| [repositories.md](repositories.md) | Repository ownership map: every active repository's role, authority, interface and integration boundary (generated, checked by `tools/build_constitution.py --check`) |
| [architecture.md](architecture.md) | Layers, product vs platform boundaries, naming, Resolver bot vs website, AXIOM Launcher vs `ax` |
| [contracts.md](contracts.md) | BLUX Contract, SDK policy, capability policy, Hook System, Model API, receipt and provenance spec, integration standard, compatibility matrix |
| [policies.md](policies.md) | AI and model policy, training and data policy, privacy, credentials, device operations, VoidForge restricted distribution, licensing and provenance |
| [lifecycle.md](lifecycle.md) | Release policy, deprecation, incident and recovery |

## Principles

- **Standalone first.** A product or tool that can stand alone must keep working without BLUX
  ([ADR-0002](https://github.com/Outer-Void/blux/blob/main/docs/adr/0002-standalone-vs-integrated-boundary.md)).
- **One authority per concern.** Every concern has exactly one owning component (repositories.md). Others
  route to it, ask it or read from it; they never reimplement it.
- **Evidence over intent.** Statuses need evidence; claims need sources.
- **Proprietary by default, attribution beyond the minimum.** See policies.md and
  [Outer-Void/credits](https://github.com/Outer-Void/credits).
