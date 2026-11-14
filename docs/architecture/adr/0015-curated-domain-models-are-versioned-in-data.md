# ADR-0015: Version curated, hand-authored domain models in `data/<Domain>/`

- **Status:** accepted
- **Scope:** system
- **Date:** 2026-11-14
- **Related:** [ADR-0013](0013-shared-data-through-owned-datasets-and-contracts.md); idea [0001](../../ideas/0001-acme-data-platform-domain-model.md) Q1; spec [0002](../../specs/0002-domain-model-generator/spec.md) (FR-15)

## Context
ADR-0013 treats `data/` as the default `SHARED_DATA_DIR`: runtime datasets, each written by one owning app, reproducible, and therefore git-ignored (only `data/README.md` is committed).

The AcmeDataPlatform domain model (idea 0001) does not fit that description. It is written by hand, statement by statement, together with the domain expert; it cannot be reproduced by running an app, and losing it means losing the expert's work. In idea 0001 (Q1) the user chose to keep it in `data/AcmeDataPlatform/` and to un-ignore that one folder. Spec 0002 makes the folder a structured source (YAML sources, samples, generated formats) for a repo tool, and more domains may follow. The exception was applied in `.gitignore` but never recorded as a decision.

## Decision
We will keep each **curated, hand-authored domain model** in `data/<Domain>/` (PascalCase domain name, e.g. `data/AcmeDataPlatform/`) and version it in git:

- `.gitignore` keeps `/data/*` ignored and adds one `!/data/<Domain>/` line per domain model, so runtime datasets stay ignored.
- A domain model folder is **source**, not a dataset: it has no owning app and no contract in `shared/contracts/` yet, and it is not listed in `components.json`. Its layout is the domain-folder format of spec 0002 (YAML sources, `ontology.axioms.ttl`, `samples/`, and a committed `generated/` folder kept in sync by ADR-0016).
- When an app first **reads** a domain model at runtime, the folder (or an export of it) becomes a dataset under ADR-0013 with a contract, and this ADR is revisited.
- Domain models must not contain personal data or secrets (the repository is public, ADR-0008).

## Alternatives considered
| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| `data/` for runtime data only; domain models elsewhere (e.g. `domains/<Domain>/`) | Keeps ADR-0013 without an exception | Moves an existing folder and its history; the user chose `data/` (idea 0001, Q1) | User decision |
| Keep the domain model git-ignored | No exception | Hand-authored work would be lost; no review, no CI checks | Unacceptable data loss risk |
| Treat it as a dataset now (owner + contract) | Fully within ADR-0013 | No app reads or writes it yet; a contract for an unused interface is speculative | Deferred until an app reads it (spec 0002 non-goal) |

## Consequences
- **Positive:** the expert's model is versioned, reviewable and checked in CI; runtime data stays out of git.
- **Negative / trade-offs:** `data/` now holds two kinds of content; contributors must read `data/README.md` to know which folders are committed.
- **Follow-up:** `data/README.md` describes the exception in general terms; `.gitignore` comment points to this ADR; root `architecture.md` §7 lists domain models as a cross-cutting concern.
