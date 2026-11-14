# Spec 0002 · Domain-model generator (formats, diagrams, level views)

- **Status:** implemented
- **Scope:** system
- **Idea:** [0002-domain-model-generator](../../ideas/0002-domain-model-generator.md)
- **Last updated:** 2026-11-14

## Problem
The domain expert defines a domain (first: AcmeDataPlatform, idea 0001) statement by statement in an interactive session. Claude records the result as hand-authored YAML. The expert wants to see the same model in **every standard format** (to learn which one suits which purpose), as **diagrams**, and as **three cumulative learnability levels** (core, main, detailed). Producing and cross-checking all of this by hand after every statement is slow and error-prone, and v0.1 did it with an untested helper written outside the quality gate (idea 0001, notes N1–N2). Modelling of level 1 is paused until a tested generator exists (idea 0001, Q43).

## Goals
- One command turns a hand-authored domain folder into all derived files, deterministically.
- One command proves the model is consistent and the derived files are up to date; it runs in pre-commit and CI.
- One command proves every rule works, by running the generated SHACL on sample data.
- Works for any domain folder, not only AcmeDataPlatform.

## Non-goals
- Harvesting terms from user manuals, question answering, the reviewer app (other ideas).
- A shared dataset contract for domain folders (ADR-0013); added when an app first reads a domain model.
- Diagram formats other than Mermaid (no SVG/PNG, GraphML, DOT).
- Per-level standard-format files (only the Markdown level views are per level).
- A reading-time check for level 1 (idea 0002, Q15).
- An editor or UI; the sources are edited as text (by Claude, with the expert).

## Users and scenarios
1. As the **domain expert**, after each modelling step I want to open the level views, glossary and diagrams, so that I can see and correct what was understood.
2. As **Claude in a modelling session**, I want to edit only the YAML sources and run one command, so that every format and diagram is regenerated and checked without hand edits.
3. As **Claude or the expert**, I want the check to tell me exactly which item is inconsistent (wrong level, unknown statement, missing sample), so that I can fix it before committing.
4. As a **reviewer of the repo**, I want CI to fail when someone edits a generated file or forgets to regenerate, so that the committed formats always match the sources.
5. As a **future domain author**, I want to point the generator at a new folder, so that a second domain needs no code change.

## Domain folder (inputs and outputs)

**Sources** (hand-authored, at the top of the domain folder):

| File | Holds |
|------|-------|
| `statements.yaml` | The expert's statements, verbatim, each with id, date and level |
| `ontology.yaml` | Namespace, prefix, working level; concepts (with `parent` / `also_parents`), individuals, relations, data properties, rules. Every item has `level` (1–3), `status` (`confirmed` / `draft`) and `source` (statement ids) |
| `taxonomy.yaml` | Optional extra trees beyond is-a (e.g. part-of) |
| `ontology.axioms.ttl` | Optional hand-written OWL axioms the YAML cannot express (e.g. unions, defined classes), merged into the generated ontology |
| `samples/` | Instance data for rule validation: one valid sample, and per rule at least one sample that violates it (constraint) or the triples it must infer (derivation) |

**Generated** (under `generated/`, each with a "generated, do not edit" header where the format allows):

| Artefact | Files |
|----------|-------|
| Statements | `statements.md` |
| Glossary | `glossary.md`, `glossary.tbx` (TBX, ISO 30042) |
| Taxonomy | `taxonomy.skos.ttl` (SKOS, Turtle) |
| Ontology | `ontology.owl.ttl` (OWL 2, Turtle), `ontology.owl.rdf` (RDF/XML), `ontology.jsonld` (JSON-LD) |
| Rules | `rules.md`, `rules.shacl.ttl` (SHACL, including SHACL-AF rules for derivations) |
| Diagrams | `diagrams.md` (Mermaid: taxonomy trees, ontology graph) |
| Level views | `level-1.md`, `level-2.md`, `level-3.md` |

## Functional requirements
| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-1  | A `build` command takes a domain folder path and writes every file in the "Generated" table under `<folder>/generated/`; namespace and prefix come from `ontology.yaml`. Nothing is written outside `generated/`. | must |
| FR-2  | Output is deterministic: building the same sources twice gives byte-identical files (stable ordering, no timestamps). | must |
| FR-3  | The is-a taxonomy (SKOS and Mermaid) is derived from `parent` / `also_parents` in `ontology.yaml`; `taxonomy.yaml` contributes only additional trees. | must |
| FR-4  | The OWL ontology is generated from `ontology.yaml`: classes, subclass hierarchy, individuals and their types, object and data properties with domain, range, inverse and super-property, cardinality restrictions, disjointness, labels, synonyms, definitions, sources, level and status. `ontology.axioms.ttl`, if present, is merged in. | must |
| FR-5  | RDF/XML and JSON-LD are produced from the same graph as the Turtle and are isomorphic to it. | must |
| FR-6  | `rules.shacl.ttl` is generated entirely from the rules in `ontology.yaml`. A rule is written either as one of a documented set of structured patterns (at least: cardinality, allowed values / class, implication along property paths, equality of two paths, derivation of a triple) or, if it fits no pattern, with its own SPARQL. Every rule keeps a plain-English `statement`. | must |
| FR-7  | The glossary (Markdown and TBX) lists every concept, individual, relation and property with preferred label, synonyms, definition, level, status and sources. | must |
| FR-8  | `level-N.md` (N = 1, 2, 3) contains a short intro, glossary, taxonomy tree, relations, properties, rules and the Mermaid taxonomy and ontology graph, filtered to items with level ≤ N. `level-3.md` contains the whole domain. | must |
| FR-9  | Every class, property, individual, SKOS concept, TBX entry and SHACL shape carries its level (`<prefix>:level` in RDF, a note in TBX). | must |
| FR-10 | Items with status `draft` appear in every output, visibly marked as draft in Markdown and annotated with their status in RDF and TBX. | must |
| FR-11 | `statements.md` is generated from `statements.yaml`. | must |
| FR-12 | A `check` command fails (non-zero exit, one line per problem naming file and item id) when: a source file is malformed or misses a required field; an id is duplicated or referenced but undefined; a `source` cites an unknown statement; a level is outside 1–3; a relation, property, rule, individual or child concept has a lower level than an item it uses; a concept is not reachable in the is-a taxonomy; `ontology.axioms.ttl` references a class or property in the domain namespace that `ontology.yaml` does not define; a SPARQL rule does not parse; a rule has no sample proving it; any file under `generated/` differs from what `build` would write, or is missing, or is extra. | must |
| FR-13 | A `validate` command runs the generated SHACL (with RDFS inference and SHACL-AF rules) on the samples: the valid sample conforms; each violating sample produces a violation from the rule it targets; each derivation sample yields its expected triples. It fails, naming the rule, otherwise. | must |
| FR-14 | `check` (including `validate`) runs in pre-commit and in CI for every domain folder in the repo. | must |
| FR-15 | The existing AcmeDataPlatform folder is migrated to this layout: S1–S10 move into `statements.yaml`, the hand-written `ontology.owl.ttl` and `rules.shacl.ttl` are replaced by the generated ones, and the folder README describes sources vs generated files. | must |
| FR-16 | The YAML source format (fields, rule patterns) is documented next to the tool, with an example domain used by the tests. | must |

## Apps and shared data affected
- **Apps:** none.
- **Repo tooling:** new tool `tools/domain-model/` (uv workspace member, under the Python quality gate, ADR-0014); new pre-commit hook and CI step.
- **Data:** `data/AcmeDataPlatform/` is reorganized (FR-15). It is hand-authored, versioned source (idea 0001, Q1), not a shared runtime dataset; no contract is added (non-goal). The root ADR that records the exception to ADR-0013 ("`data/` is runtime data") is still owed from idea 0001 Q1 and is written in `/plan`.
- **Shared code, base env variables:** none.

## Non-functional requirements
- **Quality gate:** the tool passes ruff, mypy strict, pytest and the complexity limits (ADR-0005, ADR-0014); new dependencies are pinned in `uv.lock` and pass `pip-audit`.
- **Speed:** `check` on a domain of ~200 items finishes in under 10 seconds locally, so it can run in pre-commit.
- **Offline:** no network or LLM calls.
- **Readability:** generated Markdown and Mermaid render on GitHub.

## Acceptance criteria
- [ ] AC-1 (FR-1): Given the example domain, when `build` runs, then every file in the "Generated" table exists under `generated/` and no file outside `generated/` changed.
- [ ] AC-2 (FR-1, FR-4): Given two example domains with different namespaces and prefixes, when each is built, then each output uses only its own namespace and prefix.
- [ ] AC-3 (FR-2): Given the example domain, when `build` runs twice, then all outputs are byte-identical.
- [ ] AC-4 (FR-3): Given concepts with `parent` and `also_parents`, when built, then `taxonomy.skos.ttl` has exactly the matching `skos:broader` links and the Mermaid tree shows the same edges; a part-of tree from `taxonomy.yaml` appears in `diagrams.md`.
- [ ] AC-5 (FR-4): Given an example domain covering every YAML field, when built, then the OWL graph contains the expected triples for each (subclass, domain/range, inverse, super-property, min/max/exact cardinality, disjointness, labels, synonyms, definitions, sources, level, status), and a triple from `ontology.axioms.ttl` is present.
- [ ] AC-6 (FR-5): When built, then `ontology.owl.rdf` and `ontology.jsonld` parse to graphs isomorphic to `ontology.owl.ttl`.
- [ ] AC-7 (FR-6): Given one rule per documented pattern plus one SPARQL rule, when built, then `rules.shacl.ttl` contains a shape for each rule with the rule's level, and the documentation lists every pattern.
- [ ] AC-8 (FR-7): When built, then `glossary.md` and `glossary.tbx` contain one entry per concept, individual, relation and property with label, synonyms, definition, level, status and sources, and the TBX validates against the TBX core structure.
- [ ] AC-9 (FR-8): Given items at levels 1, 2 and 3, when built, then `level-1.md` contains only level-1 items, `level-2.md` levels 1–2, `level-3.md` all, each with the listed sections and both Mermaid diagrams.
- [ ] AC-10 (FR-9): When built, then every class, property, individual, SKOS concept and SHACL shape has exactly one level annotation equal to its YAML level, and every TBX entry has a level note.
- [ ] AC-11 (FR-10): Given a draft item, when built, then it appears marked as draft in the Markdown files and carries a status annotation in RDF and TBX.
- [ ] AC-12 (FR-11): Given `statements.yaml`, when built, then `statements.md` lists every statement verbatim with id, date and level.
- [ ] AC-13 (FR-12): For each problem listed in FR-12, a test fixture containing exactly that problem makes `check` exit non-zero with a message naming the file and item id; the clean example domain passes.
- [ ] AC-14 (FR-12): Given a hand edit to a generated file, a missing generated file, or an extra file in `generated/`, when `check` runs, then it fails naming the file.
- [ ] AC-15 (FR-13): Given the example samples, `validate` passes; given a violating sample that the shapes do not flag, or a valid sample that is flagged, or a derivation whose expected triple is not inferred, `validate` fails naming the rule.
- [ ] AC-16 (FR-14): `.pre-commit-config.yaml` and the CI workflow run `check` on every domain folder; a commit with a stale generated file is rejected by the hook.
- [ ] AC-17 (FR-15): `check` passes on `data/AcmeDataPlatform/`; its `statements.yaml` contains S1–S10 verbatim; no hand-written `.ttl` other than `ontology.axioms.ttl` remains at the top level.
- [ ] AC-18 (FR-16): The format documentation exists and the example domain it references is the one the tests build.
- [ ] AC-19 (NFR): `uv run ruff check .`, `uv run mypy`, `uv run pytest`, `uv run qg-boundaries` and `uv run pip-audit --skip-editable` pass.
- [ ] AC-20 (NFR): A test builds and checks a generated domain of 200 items in under 10 seconds.

## Edge cases and failure modes
- **Empty domain** (no items yet, as AcmeDataPlatform today): `build` writes valid, mostly empty files; `check` passes.
- **Concept with several parents:** shown under each parent in the Markdown tree; one node with several edges in Mermaid.
- **Cycle in `parent` links:** `check` fails naming the cycle.
- **Hand axiom referencing an undefined class/property:** `check` fails.
- **Mermaid-unsafe labels** (quotes, slashes, e.g. "AI/analytical application"): escaped so the diagram still renders.
- **RDF/XML writer quirks** (v0.1: duplicated shared lists): caught by the isomorphism check (AC-6).
- **SPARQL rule that does not parse:** `check` fails naming the rule.
- **Domain folder without `generated/`:** `build` creates it; `check` reports every file as missing.

## Open questions
- None blocking. The exact rule-pattern list beyond the minimum in FR-6 and the YAML field names are design decisions for `/plan`.
