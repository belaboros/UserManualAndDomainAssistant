# 0002 · Domain-model generator (formats, diagrams, level views)

- **Status:** done
- **Scope:** system (repo tooling: `tools/domain-model/`; reorganizes `data/AcmeDataPlatform/`)
- **Captured:** 2026-11-14
- **Spec:** [docs/specs/0002-domain-model-generator/spec.md](../specs/0002-domain-model-generator/spec.md)

## Original idea

The idea came over several messages in the idea-0001 session; each is quoted verbatim.

> 2026-11-13: "I define the terms, concepts, relations, properties, rules here.
> You build the glossary, ontology, taxonomy, rule description files in the dedicated /data/Acme/DataPlatform folder.
>
> Then you generates diagrams for me to see the outcome: taxonomy trees, ontology graph."

> 2026-11-13 (answer to Q2 of idea 0001): "I want to store the outcome in all possible standard formats inorder to understand which one I like when (includeing your YAML + Markdown files)."

> 2026-11-14: "Same set-up with an extra addition to support granular learnability.
>
> Each concept, relation, rule, ... has a level.
> Level-1: (core) for a quick overview for anyone to understand the domain in 5-10 minutes.
> Level-2: (main) for an adopter to be able to use the domain for the most simple use-case(s)
> Level-3: (detailed) all the concepts, relations, rules that exist in the domain.
>
> We need to generate one-one markdown file for each level."

> 2026-11-14 (answer to Q39 of idea 0001): "/add-language python, then spec it (Recommended)"

> 2026-11-14 (answer to Q43 of idea 0001): "Pause, build generator first"

### Notes for `/spec` (Claude, not part of the original idea)

What the v0.1 session helper did (archived in `data/archive-data-platform-concepts-v0.1.zip`, `tools/derive.py`, written outside the quality gate; see idea 0001 notes N1–N2), and what the restart added (idea 0001 Q36–Q38):
- **Inputs:** `ontology.yaml` (concepts, individuals, relations, data properties, rules, views; every item has `level` 1–3, a `source` statement and a `status`), `taxonomy.yaml` (is-a trees, optional part-of trees), the hand-written `ontology.owl.ttl` (axioms such as cardinality restrictions and unions) and `rules.shacl.ttl` (constraints and derivations).
- **Outputs:** `taxonomy.skos.ttl` (SKOS), `glossary.tbx` (TBX, ISO 30042), `glossary.md`, `rules.md`, `ontology.owl.rdf` (RDF/XML) and `ontology.jsonld` (JSON-LD) from the Turtle, `diagrams.md` (Mermaid taxonomy tree, ontology graph, hand-drawn views), and `level-1.md`, `level-2.md`, `level-3.md` (cumulative; glossary, taxonomy, relations, properties, rules and diagrams filtered to level ≤ N).
- **Checks:** YAML and OWL agree on classes, properties and levels (`adp:level`); every rule has a SHACL shape with the same level; a relation, rule or child concept is never at a lower level than the concepts it uses; RDF/XML and JSON-LD are isomorphic to the Turtle (rdflib's pretty RDF/XML writer sometimes duplicates shared lists); every concept appears in the taxonomy.
- **Validation of instance data:** run the SHACL rules (pyshacl, RDFS inference, SHACL-AF for SPARQL targets and rules) against sample data, as the v0.1 tests did.
- **Open for `/spec`:** where the tool lives (`tools/` or a shared component), whether the domain folder becomes a dataset with a contract (ADR-0013), how much of the OWL could be generated from the YAML instead of hand-written, and new dependencies (rdflib, pyshacl, pyyaml) under the quality gate (ADR-0014).

## Q&A log

<!--
Append one entry per question, oldest first. Never delete entries.
-->

### 2026-11-14 · spec · Q1
**Asked by:** Claude
**Q:** [spec · scope] Where should the generator live? It reads a hand-authored domain folder and writes the derived files; later the assistant/reviewer apps may read the same model.
**Options offered:** System: repo tool (Recommended); System: shared component; New app
**A:** System: repo tool (Recommended)
**Effect:** Scope `system`. The generator is a repo tool in `tools/domain-model/` (uv workspace member); spec in `docs/specs/0002-domain-model-generator/`. The domain folder stays hand-authored source; no dataset contract until an app reads it.

### 2026-11-14 · spec · Q2
**Asked by:** Claude
**Q:** [spec · clarifying question] How should the OWL ontology be produced? (v0.1 hand-wrote ontology.owl.ttl and checked it against the YAML.)
**Options offered:** Generate + hand axioms (Recommended); Fully generated; Hand-written, checked
**A:** Generate + hand axioms (Recommended)
**Effect:** OWL (classes, hierarchy, properties, domain/range, inverses, cardinalities, disjointness, labels, levels) is generated from the YAML; an optional hand-written axioms file is merged in for what the YAML can't express.

### 2026-11-14 · spec · Q3
**Asked by:** Claude
**Q:** [spec · clarifying question] And the SHACL rules (rules.shacl.ttl)?
**Options offered:** Hand-written, checked (Recommended); Generate simple ones; Fully generated
**A:** Fully generated
**Effect:** Every rule must be expressible in the YAML so that `rules.shacl.ttl` is generated; the YAML rule schema has to cover constraints and derivations (SPARQL-based where needed).

### 2026-11-14 · spec · Q4
**Asked by:** Claude
**Q:** [spec · clarifying question] Should the generator work only for AcmeDataPlatform or for any domain folder?
**Options offered:** Any domain folder (Recommended); AcmeDataPlatform only
**A:** Any domain folder (Recommended)
**Effect:** The generator takes a domain folder path; namespace and prefix come from the YAML. AcmeDataPlatform is the first user.

### 2026-11-14 · spec · Q5
**Asked by:** Claude
**Q:** [spec · clarifying question] Since SHACL is fully generated, how should a rule be written in the YAML?
**Options offered:** Patterns + SPARQL fallback (Recommended); SPARQL for every rule; Patterns only
**A:** Patterns + SPARQL fallback (Recommended)
**Effect:** Common rule kinds are structured YAML fields translated to SHACL; a rule that fits no pattern carries its own SPARQL. The plain-English statement is always kept for the Markdown.

### 2026-11-14 · spec · Q6
**Asked by:** Claude
**Q:** [spec · clarifying question] Should the derived files be committed, and kept in sync automatically?
**Options offered:** Commit + stale check (Recommended); Commit, no check; Don't commit
**A:** Commit + stale check (Recommended)
**Effect:** Derived files are committed; a `check` command runs in pre-commit and CI and fails if a derived file is out of date or the model is inconsistent.

### 2026-11-14 · spec · Q7
**Asked by:** Claude
**Q:** [spec · clarifying question] Should validating instance data against the generated SHACL (pyshacl, as the v0.1 tests did) be part of this generator?
**Options offered:** Yes, with sample data (Recommended); Validate command only; Not now
**A:** Yes, with sample data (Recommended)
**Effect:** A `validate` command runs the shapes on valid and invalid sample data kept in the domain folder, proving every rule fires.

### 2026-11-14 · spec · Q8
**Asked by:** Claude
**Q:** [spec · clarifying question] Which diagram outputs? (ADR-0004: diagrams are Mermaid in Markdown.)
**Options offered:** Mermaid only (Recommended); Mermaid + graph exports; Mermaid + rendered images
**A:** Mermaid only (Recommended)
**Effect:** Taxonomy trees and ontology graph as Mermaid in `diagrams.md` and the level files; no image or graph-file exports.

### 2026-11-14 · spec · Q9
**Asked by:** Claude
**Q:** [spec · clarifying question] Today ontology.yaml has a `parent` per concept and taxonomy.yaml repeats the is-a tree. Which should be the source of the is-a taxonomy?
**Options offered:** Derive from parents (Recommended); Keep both, check agreement
**A:** Derive from parents (Recommended)
**Effect:** The is-a tree is generated from `parent` / `also_parents` in ontology.yaml; taxonomy.yaml keeps only extra trees (e.g. part-of).

### 2026-11-14 · spec · Q10
**Asked by:** Claude
**Q:** [spec · clarifying question] Every item cites the expert statements it comes from (`source: [S3]`). How should statements be handled?
**Options offered:** statements.yaml → .md (Recommended); Keep statements.md, check refs; No statement checks
**A:** statements.yaml → .md (Recommended)
**Effect:** Statements move into `statements.yaml` (verbatim text, date, level); `statements.md` is generated; the check fails on a `source` that cites an unknown statement. The existing S1–S10 are migrated.

### 2026-11-14 · spec · Q11
**Asked by:** Claude
**Q:** [spec · clarifying question] Must every rule have sample data proving it fires?
**Options offered:** Required, check fails (Recommended); Warning only; Optional
**A:** Required, check fails (Recommended)
**Effect:** Each constraint needs at least one invalid sample that violates it, each derivation an expected inferred triple; the valid sample must pass. Claude writes the samples while modelling.

### 2026-11-14 · spec · Q12
**Asked by:** Claude
**Q:** [spec · clarifying question] Besides level-1/2/3.md, should the standard formats also be produced per level?
**Options offered:** Markdown only (Recommended); Also per-level RDF
**A:** Markdown only (Recommended)
**Effect:** Only the three Markdown level views are per level; standard formats hold the whole domain with `adp:level` annotations.

### 2026-11-14 · spec · Q13
**Asked by:** Claude
**Q:** [spec · clarifying question] Where should the generated files go inside a domain folder?
**Options offered:** Subfolder generated/ (Recommended); Same folder, flat
**A:** Subfolder generated/ (Recommended)
**Effect:** Sources (YAML, hand axioms, samples) stay at the top of the domain folder; every derived file goes under `generated/` with a "generated, do not edit" header.

### 2026-11-14 · spec · Q14
**Asked by:** Claude
**Q:** [spec · clarifying question] Items with status `draft` (wording proposed by Claude, not yet confirmed by you): how should the outputs treat them?
**Options offered:** Include, marked (Recommended); Markdown only; Exclude drafts
**A:** Include, marked (Recommended)
**Effect:** Drafts appear in every output, marked as draft in Markdown and with a status annotation in RDF/TBX.

### 2026-11-14 · spec · Q15
**Asked by:** Claude
**Q:** [spec · clarifying question] Level 1 should be readable in 5–10 minutes. Should the check guard that?
**Options offered:** Warn on reading time (Recommended); Fail above budget; No check
**A:** No check
**Effect:** No reading-time check; the domain expert judges the size of level 1.

### 2026-11-14 · spec · Q16
**Asked by:** Claude
**Q:** [spec · approve] Approve spec 0002 (system scope; build/check/validate tool in tools/domain-model/; 16 FRs, 20 ACs; no blocking open questions)?
**Options offered:** Approve; Changes needed
**A:** Approve
**Effect:** Spec 0002 approved; idea status `specified`. Next: `/plan 0002`.

### 2026-11-14 · plan · Q17
**Asked by:** Claude
**Q:** [plan · plan approval] Approve the plan for spec 0002 (tool `tools/domain-model/` with build/check/validate on rdflib, pyshacl, pydantic, PyYAML; one in-memory render used by build and check; 6 rule patterns; sample file-name convention; example library-lending domain; 23 tasks) and the proposed root ADR-0015 (curated domain models versioned in `data/<Domain>/`) and ADR-0016 (all formats generated from YAML, committed, checked in pre-commit and CI)?
**Options offered:** Approve; Changes needed
**A:** "Explain the way of working for me first. then let's return to this question."
**Effect:** No decision yet. Claude explains the way of working (modelling session with the generator, and how the plan is implemented), then asks again.

### 2026-11-14 · plan · Q18
**Asked by:** Claude
**Q:** [plan · plan approval] With that way of working in mind (generator built task by task test-first, then modelling loop: statement → questions → YAML + samples → build + check → expert reviews level views), approve the plan for spec 0002 (plan.md + tasks.md, 23 tasks) and the proposed root ADR-0015 and ADR-0016?
**Options offered:** Approve; Changes needed
**A:** Approve
**Effect:** Plan approved; ADR-0015 and ADR-0016 accepted; idea status `planned`. Next: `/implement 0002` in a fresh session.
