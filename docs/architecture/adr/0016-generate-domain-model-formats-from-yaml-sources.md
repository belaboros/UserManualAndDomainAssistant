# ADR-0016: Generate every domain-model format from YAML sources with a repo tool

- **Status:** accepted
- **Scope:** system
- **Date:** 2026-11-14
- **Related:** [ADR-0004](0004-diagrams-as-mermaid.md), [ADR-0014](0014-introduce-python-and-its-quality-gate.md), [ADR-0015](0015-curated-domain-models-are-versioned-in-data.md); idea [0002](../../ideas/0002-domain-model-generator.md) Q1–Q14; spec [0002](../../specs/0002-domain-model-generator/spec.md), [plan](../../specs/0002-domain-model-generator/plan.md)

## Context
A domain model (ADR-0015) is built statement by statement with a domain expert, who wants to see it in every standard format (OWL in Turtle, RDF/XML and JSON-LD; SKOS; SHACL; TBX), as Mermaid diagrams, and as three cumulative learnability levels. In v0.1 these files were partly hand-written and partly derived by an untested helper outside the quality gate, and they drifted. Every domain folder in the repo needs the same treatment, and a reviewer must be able to trust that the committed formats match the model.

## Decision
We will treat a small set of hand-authored files as the only source of a domain model and generate everything else with a repo tool:

- **Sources** (top of the domain folder): `statements.yaml` (the expert's words, verbatim), `ontology.yaml` (concepts, individuals, relations, properties and rules, each with level, status and sources), optional `taxonomy.yaml` (extra trees) and `ontology.axioms.ttl` (OWL the YAML cannot express), and `samples/` (instance data proving every rule).
- **Rules** are written as structured patterns (cardinality, allowed values, implication, path equality, derivation) or, if none fits, as SPARQL; `rules.shacl.ttl` is generated entirely from them.
- **Tool:** `tools/domain-model/` (uv workspace member, package `domain_model`, command `domain-model build | check | validate`), under the Python quality gate of ADR-0014. Third-party libraries: rdflib (RDF graphs and serialisers), pyshacl (SHACL and SHACL-AF validation, with owlrl), pydantic (typed YAML schema), PyYAML (safe loading); lxml only in tests (TBX schema validation).
- **Generated files** go to `<domain>/generated/`, are deterministic (byte-identical on rebuild) and **are committed**, so they can be read on GitHub and diffed in review.
- **`domain-model check --all`** runs in pre-commit and CI on every domain folder it discovers (a folder with `ontology.yaml` and `statements.yaml`). It fails on an inconsistent model, on a generated file that differs from what `build` would write (hand edit, missing, extra), on a rule without a sample, and when the generated SHACL does not behave as the samples say.
- The tool makes no network or LLM calls.

## Alternatives considered
| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Hand-write OWL and SHACL, check them against the YAML (v0.1) | Full expressiveness | Two sources to keep in sync; slow for the expert to review | Idea 0002, Q2/Q3 |
| Generate but don't commit the outputs | No generated files in git | Nothing to read on GitHub; every reader must run the tool | Idea 0002, Q6 |
| Commit outputs without a freshness check | Simple | Outputs drift silently (the v0.1 problem) | Idea 0002, Q6 |
| A shared component (`shared/domain-model`) or an app | Reusable by apps later | No app needs it yet; a shared component implies a public API and a dataset contract | Idea 0002, Q1; revisit when an app reads domain models |
| Templates (Jinja2) for all outputs | Readable templates | Extra dependency; templated RDF can be silently invalid | RDF built as graphs, Markdown with small builders |

## Consequences
- **Positive:** one edit to the YAML regenerates every format consistently; reviewers and CI can trust the committed files; a second domain needs no code change; rules are proven by samples.
- **Negative / trade-offs:** generated files add diff noise to commits; the YAML schema and rule patterns are our own format to document and maintain; anything the patterns cannot express needs SPARQL or a hand axiom; pre-commit gets slower on domain changes (bounded by spec 0002's 10-second budget).
- **Follow-up:** root `pyproject.toml` (workspace member, mypy and pytest paths), `uv.lock`; `.pre-commit-config.yaml` hook and `.github/workflows/python.yml` step; `tools/domain-model/README.md` documents the format; root `CLAUDE.md` lists the commands; root `architecture.md` §7 row "Domain models".
