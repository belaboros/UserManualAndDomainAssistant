# AcmeDataPlatform domain model

Hand-authored with the domain expert in an interactive session (idea [0001](../../docs/ideas/0001-acme-data-platform-domain-model.md); restarted 2026-11-14, previous version archived as `data/archive-data-platform-concepts-v0.1.zip`, local only, git-ignored). Versioned in `data/` on purpose ([ADR-0015](../../docs/architecture/adr/0015-curated-domain-models-are-versioned-in-data.md)).

Namespace: `https://example.org/acme/data-platform#` (prefix `adp:`).

## Sources and generated files

Only the **sources** are edited (by Claude, with the expert). Everything under `generated/` is written by the domain-model tool ([format and commands](../../tools/domain-model/README.md), [ADR-0016](../../docs/architecture/adr/0016-generate-domain-model-formats-from-yaml-sources.md)) and must never be edited by hand; pre-commit and CI fail when it differs from the sources.

| Source | Holds |
|--------|-------|
| [statements.yaml](statements.yaml) | The expert's statements, verbatim |
| [ontology.yaml](ontology.yaml) | Concepts, individuals, relations, properties and rules, each with level, status and sources |
| [taxonomy.yaml](taxonomy.yaml) | Extra trees beyond is-a (e.g. part-of) |
| `ontology.axioms.ttl` | Optional hand-written OWL axioms the YAML cannot express (none yet) |
| [samples/](samples/) | Instance data that proves every rule (`valid.ttl`, `<Rule>.violates.ttl`, `<Rule>.derives.ttl` + `.expected.ttl`) |

| Artefact | Human-friendly | Standard formats |
|----------|----------------|------------------|
| Statements (provenance) | [statements.md](generated/statements.md) | — |
| Glossary | [glossary.md](generated/glossary.md) | [glossary.tbx](generated/glossary.tbx) (TBX, ISO 30042); SKOS labels and definitions in `taxonomy.skos.ttl` |
| Taxonomy | in the level views and diagrams | [taxonomy.skos.ttl](generated/taxonomy.skos.ttl) (SKOS) |
| Ontology | in the level views | [ontology.owl.ttl](generated/ontology.owl.ttl) (OWL 2, Turtle), [ontology.owl.rdf](generated/ontology.owl.rdf) (RDF/XML), [ontology.jsonld](generated/ontology.jsonld) (JSON-LD) |
| Rules | [rules.md](generated/rules.md) | [rules.shacl.ttl](generated/rules.shacl.ttl) (SHACL, SHACL-AF) |
| Diagrams | [diagrams.md](generated/diagrams.md) (whole domain, Mermaid) | — |
| Level views | [level-1.md](generated/level-1.md), [level-2.md](generated/level-2.md), [level-3.md](generated/level-3.md) | — |

## Levels (granular learnability)

Every concept, individual, relation, property and rule has a level. Levels are cumulative.

| Level | Name | For | View |
|-------|------|-----|------|
| 1 | core | anyone: understand the domain in 5–10 minutes | [level-1.md](generated/level-1.md) |
| 2 | main | an adopter: use the domain for the simplest use cases | [level-2.md](generated/level-2.md) |
| 3 | detailed | everything that exists in the domain | [level-3.md](generated/level-3.md) |

Current working level: **1** (new items get this level until the domain expert says the level is complete).

In the RDF formats the level is the annotation `adp:level` (1, 2 or 3) on every class, property, individual, SKOS concept and SHACL shape; in TBX it is a `note` on the concept entry.

## Commands

From the repo root:

```
uv run domain-model build data/AcmeDataPlatform   # after editing a source
uv run domain-model check data/AcmeDataPlatform   # model, freshness of generated/, samples
```
