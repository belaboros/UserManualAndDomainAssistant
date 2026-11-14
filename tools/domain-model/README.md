# domain-model

Turns a hand-authored **domain folder** (YAML sources) into every standard format, Mermaid diagrams and three cumulative level views, and checks that the model is consistent and the rules work ([spec 0002](../../docs/specs/0002-domain-model-generator/spec.md), [ADR-0016](../../docs/architecture/adr/0016-generate-domain-model-formats-from-yaml-sources.md)). Offline; no LLM calls.

Worked example used by the tests: [example/](example/) (library lending, prefix `lib`). Its [generated/](example/generated/) folder shows real output.

## Commands

Run from the repo root:

```
uv run domain-model build    <folder>        # writes <folder>/generated/ (refuses when the model has problems)
uv run domain-model check    <folder>|--all  # model + freshness of generated/ + sample coverage + validate
uv run domain-model validate <folder>        # the generated SHACL on the samples only
```

Exit code 0 = clean, 1 = problems (one line each: `<file>:<item id>: <message>`, file relative to the folder; with `--all` prefixed by the folder), 2 = usage error. `check --all` runs on every folder that holds both `ontology.yaml` and `statements.yaml` (hidden, `tests/` and `generated/` folders are skipped); pre-commit and CI run it.

Workflow: edit the sources, run `build`, then `check`; commit sources and `generated/` together. Never edit `generated/` by hand: `check` fails on any difference.

## Domain folder

| File | Kind | Holds |
|------|------|-------|
| `statements.yaml` | source | The expert's statements, verbatim |
| `ontology.yaml` | source | Namespace, prefix, levels; concepts, individuals, relations, properties, rules |
| `taxonomy.yaml` | source, optional | Extra trees beyond is-a (e.g. part-of), for diagrams and level views |
| `ontology.axioms.ttl` | source, optional | Hand-written OWL axioms the YAML cannot express (unions, defined classes); merged into the ontology. It may only use domain-namespace names that `ontology.yaml` defines |
| `samples/` | source | Instance data that proves every rule (see [Samples](#samples)) |
| `generated/` | generated | `statements.md`, `glossary.md`, `glossary.tbx`, `taxonomy.skos.ttl`, `ontology.owl.ttl`, `ontology.owl.rdf`, `ontology.jsonld`, `rules.md`, `rules.shacl.ttl`, `diagrams.md`, `level-1.md`, `level-2.md`, `level-3.md` |

Output is deterministic (sorted, canonical blank nodes, no timestamps). Turtle, RDF/XML, TBX and Markdown carry a "generated, do not edit" comment; JSON-LD cannot.

## `statements.yaml`

```yaml
statements:
  - id: S1            # unique
    date: 2026-11-14
    level: 1          # the working level when the statement was given
    text: "…"         # verbatim
```

Fields: `id`, `date`, `level`, `text` (all required).

## `ontology.yaml`

Top level:

| Field | Required | Meaning |
|-------|----------|---------|
| `namespace` | yes | Namespace IRI, ending in `#` or `/` |
| `prefix` | yes | Prefix for the namespace in every format |
| `label` | yes | Domain name, used in titles |
| `language` | no (`en`) | Language tag of labels, synonyms and definitions |
| `working_level` | no (`1`) | The level new items get while modelling |
| `levels` | no | `{1: {name, audience}, …}`; defaults: core / main / detailed |
| `concepts`, `individuals`, `relations`, `properties`, `rules` | no | Lists of items (below) |

Ids start with a letter and use `[A-Za-z0-9_]` (convention: PascalCase for concepts and individuals, camelCase for relations and properties). Ids are unique across all items and rules; `level` and `status` are reserved.

**Every item** (concept, individual, relation, property) has:

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | Local name in the namespace |
| `label` | yes | Preferred term |
| `level` | yes | 1 core, 2 main, 3 detailed (cumulative). An item's level is never lower than the level of an item it uses |
| `status` | yes | `confirmed` (the expert's words) or `draft` (proposed, marked _(draft)_ in Markdown) |
| `source` | yes | Statement ids, at least one |
| `definition` | no | One-sentence definition |
| `synonyms` | no | Alternative terms |

Per kind, additionally:

| Kind | Field | Meaning |
|------|-------|---------|
| concept | `parent` | The is-a parent (concept id), or omitted for a top concept |
| concept | `also_parents` | Further is-a parents (a concept with several parents) |
| concept | `disjoint_with` | Concepts that share no instances with this one |
| individual | `types` | Concepts it is an instance of |
| individual | `facts` | `{relation: [individual, …]}` |
| individual | `values` | `{property: literal}` |
| relation | `domain`, `range` | Concepts |
| relation | `inverse` | The inverse relation |
| relation | `parent` | Super-relation (`rdfs:subPropertyOf`) |
| relation | `cardinality` | See below |
| relation | `characteristics` | Any of `functional`, `inverse_functional`, `transitive`, `symmetric`, `asymmetric`, `reflexive`, `irreflexive` |
| property | `domain` | Concept |
| property | `datatype` | `string` (default), `integer`, `decimal`, `boolean`, `date`, `dateTime`, `anyURI` |
| property | `cardinality` | See below |

**Cardinality** is read from the domain side ("each _domain_ has … _range_"): `"1"`, `"0..1"`, `"1..*"`, `"2..4"`, `"*"`. It becomes OWL qualified cardinality restrictions on the domain class (`owl:qualifiedCardinality` when min = max, else `owl:minQualifiedCardinality` / `owl:maxQualifiedCardinality`; `owl:onClass` = range, `owl:onDataRange` for properties). OWL is open-world, so this documents the model but rejects nothing; to reject instance data, add a `cardinality` **rule**.

**Every concept must be reachable** from a top concept through `parent` / `also_parents`; cycles are errors. The is-a taxonomy (SKOS, Mermaid, level views) comes only from these fields.

## Rules

```yaml
rules:
  - id: R1
    level: 1
    status: confirmed
    source: [S2]
    statement: "A loan has between 1 and 5 items."   # plain English; also the SHACL message
    cardinality: {focus: Loan, path: hasItem, min: 1, max: 5}   # exactly one pattern key
```

Fields: `id`, `level`, `status`, `source`, `statement` and exactly one pattern key. Every pattern has `focus`: the concept whose instances the rule applies to. A rule becomes the node shape `<prefix>:<RuleId>_shape` (`sh:targetClass` = focus) with `rdfs:label`, `sh:message`, level, status and sources.

| Key | Kind | Fields | SHACL produced |
|-----|------|--------|----------------|
| `cardinality` | constraint | `focus`, `path`, `min` and/or `max`, optional `class` | property shape with `sh:minCount` / `sh:maxCount` (`sh:qualifiedValueShape` + `sh:qualifiedMinCount` / `sh:qualifiedMaxCount` when `class` is given) |
| `values` | constraint | `focus`, `path`, one of `in: [individuals]` / `class` / `datatype` | property shape with `sh:in` / `sh:class` / `sh:datatype` |
| `implies` | constraint | `focus`, `if: <condition>`, `then: <condition>` | `sh:or ( [ sh:not <if> ] <then> )` |
| `equal` | constraint | `focus`, `left: <path>`, `right: <path>` | `sh:equals` when both are single relations, else a generated `sh:sparql` constraint (a value on one side only is a violation) |
| `derive` | derivation | `focus`, optional `if: <condition>`, `add: {predicate, object}` | SHACL-AF `sh:TripleRule` (`sh:subject sh:this`, `sh:condition` for `if`) |
| `sparql` | constraint or derivation | `focus`, `select` (must select `$this`) **or** `construct` | `sh:SPARQLConstraint` (each result is a violation) / `sh:SPARQLRule`, with `sh:prefixes` |

- A **condition** is `{path, <test>}` with exactly one test: `has_value` (a string names an individual; numbers, booleans and dates are literals), `in` (a list of individuals) or `class` (a concept): at least one value is in the list / of the class, or `min` (at least that many values).
- **derive** `add.predicate` is a relation or property id, or `a` for rdf:type. `add.object` is a concept or individual id (a constant), or a path whose values become the objects (`hasItem/locatedIn`).
- **sparql** queries may use the domain prefix and `rdf`, `rdfs`, `xsd`, `owl` without declaring them. Domain names in the query must be defined; they count as "used" for the level check.
- A rule's kind follows from its pattern; there is no `kind` field.

**Paths** (in `path`, `left`, `right`, conditions and `add.object`), with SPARQL 1.1 precedence:

| Syntax | Meaning |
|--------|---------|
| `rel` | One relation or property (`a` = rdf:type) |
| `a/b` | Sequence |
| `^rel` | Inverse |
| `rel*`, `rel+`, `rel?` | Zero or more, one or more, zero or one |
| `a\|b` | Alternative |
| `( … )` | Grouping |

## `taxonomy.yaml` (optional)

```yaml
trees:
  - id: LibraryPartOf
    label: Library composition (part-of)
    relation: part of            # edge label in diagrams
    top:
      - id: Library
        children: [{id: Branch, children: [{id: Shelf}]}]
```

Fields: `trees` with `id`, `label`, `relation`, `top`; nodes have `id` (a concept) and `children`. Extra trees appear in `diagrams.md` and the level views, not in SKOS.

## Samples

| File | Meaning |
|------|---------|
| `samples/valid.ttl` | Must conform to every shape (required; may be empty) |
| `samples/<RuleId>.violates[-<n>].ttl` | Must produce at least one violation from that rule's shape (every constraint rule needs one) |
| `samples/<RuleId>.derives[-<n>].ttl` + `<RuleId>.expected[-<n>].ttl` | After the SHACL-AF rules ran, every triple of the expected file must be in the data (every derivation rule needs one pair) |

Each sample is validated by pyshacl with the generated ontology (`inference="rdfs"`) and SHACL-AF rules (`advanced=True`). Results are mapped back to rules by shape IRI. A sample for an unknown rule, of the wrong kind, without its partner file, or with a name outside this convention is a `check` problem.

## RDF vocabulary

| What | Triples |
|------|---------|
| Label, synonyms, definition | `rdfs:label` (`skos:prefLabel` in SKOS), `skos:altLabel`, `skos:definition`, all with the language tag |
| Level, status | `<prefix>:level 1` (`xsd:integer`), `<prefix>:status "draft"`; both `owl:AnnotationProperty`, on every class, property, individual, SKOS concept and SHACL node shape |
| Sources | `dct:source "S3"` |
| Is-a | `rdfs:subClassOf` (OWL); `skos:broader` / `skos:narrower`, `skos:inScheme`, `skos:topConceptOf` (SKOS, same IRIs as the classes) |

TBX (`glossary.tbx`): TBX-Basic, DCA style; one `conceptEntry` per item with `note`s for kind, level, status and sources, the label as preferred term and synonyms as admitted terms. The tests validate it against a minimal RELAX NG schema of the TBX core structure ([tests/resources/tbx-core-minimal.rng](tests/resources/tbx-core-minimal.rng)), written for this tool because the licence of the official TBXcoreStructV03 schema for redistribution was not confirmed.

## Code

`src/domain_model/`: `model.py` (schema) → `load.py` → `paths.py` → `consistency.py` → `rdf/` (OWL, SKOS, SHACL, serialisation) and `text/` (Markdown, Mermaid, TBX) → `build.py`, `freshness.py`, `validate.py`, `discover.py` → `cli.py`. Tests: `tests/` (one module per acceptance criterion, see the [plan](../../docs/specs/0002-domain-model-generator/plan.md#verification-map)).
