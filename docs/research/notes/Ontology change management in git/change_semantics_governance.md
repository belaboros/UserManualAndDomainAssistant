# Change Semantics and Governance for Ontologies, Taxonomies, Glossaries, SHACL Rules and Knowledge Graphs

Scope: how to classify, approve, version, communicate and propagate changes to git-managed semantic artifacts (SKOS glossary/taxonomy, OWL ontology, SHACL shapes, KG instance data) under federated PR-based governance with an AI Reviewer. Researched 2026-11-13.

Source-quality note: items marked "(spec)" cite W3C/DCMI normative documents that are well established. I did not re-fetch every one of them in this session; their URLs are canonical. Items fetched and checked in this session are cited without that mark. Several search hits came from geosurge.ai "corpus" pages. They look like machine-generated SEO content, so I deliberately left them out.

## 1. Change taxonomies and change representation

### Takeaway
Classify changes along two axes. The first is the operation: atomic (add/remove/modify one axiom, label or triple) versus composite (rename, move, merge, split, obsolete-and-replace). The second is the semantic effect: none/editorial, additive, or meaning-altering/breaking. To record changes, use a layered vocabulary stack. KGCL describes the change operations, OWL/SKOS/dcterms annotations go on the entities themselves, PROV-O records who, when and why, and an OWL ontology header or DCAT/dcterms metadata describes each release. Historic dedicated change ontologies (CHAO, the OWL Change Ontology, OMV) are mostly of academic interest today.

### Cited Findings
- **Change operations: atomic vs composite.** Protégé's Change and Annotation Ontology (ChAO) models change types as classes and actual edits as instances of those classes. It distinguishes atomic from composite changes, and each record carries the author, the affected concepts and a timestamp. Threaded discussions and notes on concepts live in the same ontology. — [Walk et al., arXiv 1403.1070](https://arxiv.org/pdf/1403.1070); [Protégé wiki ChAO API](https://protegewiki.stanford.edu/wiki/ChAO_API)
- ChAO instances can be generated from live editing activity or from a structural diff between two versions. — [Springer, ISWC 2006 paper](https://link.springer.com/content/pdf/10.1007/11926078_39.pdf)
- Noy & Klein (2004, *Knowledge and Information Systems* 6(4):428–440) argue that ontology evolution differs from database schema evolution. Ontologies have different usage paradigms and explicit semantics, the classic versioning/evolution distinction does not carry over, and much of the extra complexity comes from managing composite operations. — [VU Research Portal](https://research.vu.nl/en/publications/ontology-evolution-not-the-same-as-schema-evolution/)
- Zablith et al., "Ontology evolution: a process-centric survey" (*Knowledge Engineering Review* 30(1):45–75, 2015; online 2013; DOI 10.1017/S0269888913000349). It builds a unified evolution process model from earlier models: roughly, detecting the need for change → suggesting changes → validating → assessing impact → managing/applying changes. It then surveys approaches for each stage. — [Cambridge Core](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/abs/ontology-evolution-a-processcentric-survey/CE4387A954917B7CA3282CE25FAC09FA); [Huddersfield repository](https://pure.hud.ac.uk/en/publications/ontology-evolution-a-process-centric-survey/)
- **KGCL (Knowledge Graph Change Language)**, by Hegde, Vendetti, Goutte-Gattat, Caufield, Graybeal, Harris, Karam, Kindermann, Matentzoglu, Overton, Musen and Mungall (arXiv 2024; *Database (Oxford)* Jan 2025). It is a standard data model plus a controlled natural language for changes to ontologies and KGs, with examples such as `add synonym 'arm' to 'forelimb'` and `move 'Parkinson disease' under 'neurodegenerative disease'`. It is used both to *request* changes ("apply patch") and to *describe* changes that already happened ("diff"). A GitHub agent watches ontology repos and applies requested changes, and BioPortal has a change-request front end. — [arXiv 2409.13906](https://arxiv.org/abs/2409.13906)
- **SKOS documentation properties for change** (all sub-properties of skos:note):
  - `skos:changeNote` "documents fine-grained changes to a concept, for the purposes of administration and maintenance". Example: "Moved from under 'fruits' to under 'vegetables' by Horace Gray".
  - `skos:historyNote` "describes significant changes to the meaning or the form of a concept". Example: "estab. 1975; heading was: Cruelty to children [1952-1975]".
  - `skos:editorialNote` "supplies information that is an aid to administrative housekeeping".
  - `skos:scopeNote` gives partial information about intended meaning.
  - A note can be a structured node carrying `rdf:value`, `dct:creator` and `dct:date`.
  — [W3C SKOS Primer](https://www.w3.org/TR/skos-primer/)
- SKOS-XL (Appendix B of the SKOS Reference) turns labels into resources (`skosxl:Label` with `skosxl:literalForm`, linked via `skosxl:prefLabel`/`altLabel`/`hiddenLabel`). Labels can then carry their own metadata, such as dates and provenance. That makes a label change, for example a preferred label demoted to an alternative label, traceable as a first-class event. (spec) — [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)
- **OWL 2 versioning annotations**: `owl:versionIRI`, `owl:versionInfo`, `owl:priorVersion`, `owl:backwardCompatibleWith`, `owl:incompatibleWith` (ontology-level), and `owl:deprecated` (entity-level). The compatibility properties are annotations with no formal semantics. (spec) — [OWL 2 Structural Specification §3](https://www.w3.org/TR/owl2-syntax/); [OWL 2 Quick Reference](https://www.w3.org/TR/owl2-quick-reference/)
- **DCMI Terms** for succession and versioning: `dcterms:replaces`/`isReplacedBy`, `dcterms:hasVersion`/`isVersionOf`, `dcterms:modified`, `dcterms:issued`, `dcterms:valid`. (spec) — [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- **PROV-O** for audit and provenance: `prov:wasRevisionOf`, `prov:wasDerivedFrom`, `prov:wasGeneratedBy`, `prov:Activity`, `prov:wasAssociatedWith`, `prov:invalidatedAtTime`. For example, the release activity can be associated with a PR, its approvers and an AI reviewer agent. (spec) — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- **OMV** (Ontology Metadata Vocabulary, Hartmann/Palma et al., mid-2000s) and its change extensions were used to describe ontology releases. In this session I could not confirm any current maintenance or adoption. See Gaps.
- **Versioning ontology for production systems.** Semantic Arts publishes a "versioning ontology" for semantic versioning and dependency tracking (including imports) across a suite of semantic artifacts. I did not inspect its class definitions. — [GitHub semanticarts/versioning-ontology](https://github.com/semanticarts/versioning-ontology)
- **Release descriptions in practice.** EU Vocabularies (Publications Office) requires release notes in each publication package (HTML/PDF/TXT) stating the version ID, the formats and, where possible, the new elements. Versions are identified by publication date plus a release number within the year. — [EU Vocabularies](https://op.europa.eu/en/web/eu-vocabularies/advanced-learners)

### Inferences
- A practical stack for this system:
  1. Write KGCL (or a KGCL-like YAML) change records in the PR, generated from a diff of the Turtle files.
  2. Put entity-level annotations in the artifacts: `owl:deprecated`, `dcterms:isReplacedBy`/the OBO "term replaced by", `skos:changeNote` and `skos:historyNote`.
  3. Put an ontology/scheme header per release with `owl:versionIRI`, `owl:versionInfo`, `owl:priorVersion`, `dcterms:issued` and `owl:backwardCompatibleWith`/`incompatibleWith`.
  4. Record a PROV-O activity per release linking the PR, the approvers, the AI reviewer and the commit SHA.
- Composite operations (rename, merge, split, move) should be first-class in the change record. If a rename is recorded only as atomic triples (delete label, add label), its intent is lost, and the end-user assistant can no longer say "renamed".
- Use `skos:historyNote` for meaning- or form-level changes that end users should see. Use `skos:changeNote` for fine-grained maintenance and `skos:editorialNote` for internal notes. The assistant would surface only historyNote (plus deprecation and replacement links) to end users.

### Gaps
- I could not confirm the current status or URL of the OWL Change Ontology (Palma et al.) or of the OMV change extension. Both appear to be dormant academic artifacts from about 2006–2009.
- I found no widely adopted W3C-standard "release notes" vocabulary. Release notes are typically Markdown or HTML, linked through `dcterms`/DCAT metadata.

## 2. Semantic versioning: what counts as breaking, and published policies

### Takeaway
No single standard exists. Mature communities either use dates (OBO prefers ISO dates) or a SemVer-like scheme whose "major" bump means one of two things: consumers' queries, validations or inferences may break, or the meaning or identity of a term changes. A good test (Health-RI) is to ask whether the change alters logical consequences or constraints, or makes previously valid instances invalid (or the reverse). FIBO and schema.org add a maturity or staging layer (Provisional/Release, pending/core/attic), so new terms can change without breaking stable consumers.

### Cited Findings
- **OBO Foundry principle 4 (versioning).**
  - Each release has a unique `owl:versionIRI` that resolves to that artifact, and a matching `owl:versionInfo` (`data-version` in OBO format).
  - ISO 8601 dates (YYYY-MM-DD) are *preferred*. SemVer-like numbering is allowed.
  - The PURL pattern is `http://purl.obolibrary.org/obo/idspace/YYYY-MM-DD/idspace.owl`, optionally with a `/releases/` segment.
  - Released files must never be altered. Fixes go into a new release.
  - Version IRI resolution is checked automatically.
  — [OBO Foundry FP-004](https://obofoundry.org/principles/fp-004-versioning.html)
- **OBO principle 19 (stability of term meaning).** A definition must keep denoting the same referents. Clarity or grammar edits are allowed. If the referents change, create a new term with a new IRI and consider deprecating the old one. — [OBO Foundry FP-019](https://obofoundry.org/principles/fp-019-term-stability.html)
- **Health-RI Ontology versioning policy** (the project has been discontinued and the policy is kept as a reference).
  - Version format is X.Y.Z. X increments when a domain package is added or removed. Y increments for any semantic change or stage transition. Z increments for non-semantic fixes (labels, typos, layout, URI fixes, export settings).
  - Only one component increments per update, chosen by highest priority.
  - A change is semantic if any of these is true: it alters logical consequences, constraints or permitted structures (subsumption, typing, multiplicities, keys, disjointness); it makes previously valid instances invalid or the reverse; or it changes IRIs or definitions so that identity or meaning changes.
  - A label-only rename with the same IRI and definition is Z. Renaming an IRI or narrowing/broadening a definition is Y. Changing a multiplicity from 0..* to 1..* is Y.
  - One version identifier covers all co-released artifacts: OWL `.ttl`, `.shacl`, docs and the JSON export.
  - A GitHub Release is required only when a package enters or is updated in an externally reviewed or published stage.
  — [Health-RI ontology versioning](https://health-ri.github.io/semantic-interoperability/method/ontology-versioning)
- **FIBO maturity levels.**
  - Release: unit- and integration-tested, and passed the most rigorous completeness, consistency and correctness tests.
  - Provisional: early-stage, wide range of maturity.
  - Informative: sources conflict. One says these were considered and explicitly rejected; another says they are deprecated but kept because provisional content depends on them.
  - The level is set per ontology module through `fibo-fnd-utl-av:hasMaturityLevel`.
  - The Production build includes only Release modules. The Development build includes all levels.
  — [FIBO Development Process](https://spec.edmcouncil.org/fibo/page/development-process); [FIBO CONTRIBUTING.md](https://www.github.com/edmcouncil/fibo/blob/master/CONTRIBUTING.md)
- **schema.org.**
  - Releases are numbered; the latest is **30.1 (2026-09-16)**, which promoted terms from Pending to general availability.
  - New terms usually start in the "Pending" section and graduate based on adoption. Retired vocabulary goes to the "Attic".
  - Patch releases fix regressions: 29.1 and 29.2 fixed problems from 29.0, including terms mislabeled as pending.
  - Deprecations come with supersession in release notes. In 29.0, DeliveryTimeSettings was superseded by ShippingConditions and GraphicNovel by SequentialArt, and shippingSettingsLink and related properties were moved to the Attic.
  - Terms are not removed casually.
  — [schema.org releases](https://schema.org/docs/releases.html)
  - The machine-readable supersession property is `schema:supersededBy`. (spec, not re-fetched) — [schema.org/supersededBy](https://schema.org/supersededBy)
- **DCAT-AP change and release management policy** (SEMIC, 2017; now marked archived).
  - Three change types by interoperability impact: bug fixes, minor semantic changes, and major semantic changes.
  - Change requests go through GitHub. Requests received after a cut-off roll over to the next release.
  - DCAT-AP 2.0 (Nov 2019) was a major release, and the 3.x line followed.
  — [Interoperable Europe: DCAT-AP change & release policy](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/dcat-application-profile-data-portals-europe/document/change-and-release-management-policy-dcat-ap)
- **FHIR terminology.**
  - `CodeSystem.version`/`ValueSet.version` is the *business version* used for referencing and ordering. It is independent of `meta.lastUpdated`.
  - A ValueSet expansion can change under the same business version when an underlying CodeSystem version changes. Pinning code system versions in `compose`, or using `lockedDate`, makes expansions reproducible, and each expansion has its own `expansion.identifier`.
  - Most of this nuance comes from HL7 Zulip implementer discussions, so treat it as practice rather than normative text.
  — [FHIR ValueSet](https://www.hl7.org/fhir/ValueSet.html); [FHIR chat: definition vs expansion](https://chat-archive.fhir.org/stream/179166-implementers/topic/Value.20set.20definition.20vs.20expansion.html)
- **SNOMED CT.**
  - Components are never deleted, only inactivated.
  - Inactivation reasons go in inactivation-indicator refsets (concept: 900000000000489007; description: 900000000000490003).
  - Successors are linked through historical association refsets: SAME AS, REPLACED BY (900000000000526001), WAS A, PARTIALLY EQUIVALENT TO and POSSIBLY EQUIVALENT TO (for ambiguous concepts). The editor first assigns the reason, then the association.
  - The RF2 "history supplement" lets queries follow history.
  — [SNOMED Terminology Services Guide 4.11](https://docs.snomed.org/snomed-ct-practical-guides/snomed-ct-terminology-services-guide/4-terminology-service-types/4.11-get-history-data); [SNOMED ECL history supplements](https://docs.snomed.org/snomed-ct-specifications/snomed-ct-expression-constraint-language/examples/6.11-history-supplements)
- `owl:backwardCompatibleWith` and `owl:incompatibleWith` let a release declare its compatibility with an earlier version IRI. They are annotations only, so a reasoner does not enforce them. (spec) — [OWL 2 Structural Specification](https://www.w3.org/TR/owl2-syntax/)

### Inferences
Proposed breaking-change matrix for this system. The Health-RI test (do previously valid instances or queries change?) applied per artifact type:

| Artifact | PATCH (no semantic effect) | MINOR (additive, backward-compatible) | MAJOR (breaking) |
|---|---|---|---|
| Glossary/SKOS | typo, formatting, added example, changeNote | new concept, new altLabel/hiddenLabel, new broader-leaf, clarifying definition with same referents | prefLabel change that consumers key on, concept merge/split, moving concept to a different broader (changes transitive closure queries), definition change that alters referents (OBO says: new IRI instead), removal (never; deprecate) |
| OWL ontology | annotation fixes | new class/property, new subclass, deprecation with replacement | removing/renaming IRI, changing domain/range, adding disjointness, changing superclass (changes inferences), changing property characteristics (functional, transitive) |
| SHACL | message/severity text | new optional property shape, *loosening* a constraint (minCount 1→0, wider sh:in), new shape targeting new class only | *tightening* (minCount 0→1, maxCount ↓, narrower sh:datatype/sh:pattern/sh:in, sh:closed true, severity Warning→Violation), new shape targeting existing class; existing KG data may fail validation |
| KG instances | provenance fixes | new nodes/edges | deleting/re-identifying nodes, changing a fact that is cited by assistant answers |

- SHACL behaves in the reverse direction from the ontology. In SHACL, adding constraints is the breaking change for *data producers*, while removing constraints breaks *consumers* who relied on the guarantee. Classify a SHACL change by running the new shapes against the current KG: any new violations means MAJOR, or at least needs a migration.
- A maturity flag such as FIBO Provisional/Release or schema.org pending lets platform teams iterate on new services' terms without bumping MAJOR. Changes to `provisional` terms do not count against the compatibility promise.
- Date-based release IDs (OBO style) suit a frequent PR-driven cadence. SemVer communicates compatibility. A hybrid works too: SemVer in `owl:versionInfo`, and a dated or tagged versionIRI in git (for example, `/releases/2026-11-13/` or `/v3.2.0/`).

### Gaps
- I could not extract the full text of the DCAT-AP policy PDF (it is a binary stream). The exact definitions of minor and major semantic change are not confirmed.
- I found no authoritative published SemVer policy specifically for SHACL shapes. The SHACL matrix above is my own inference.
- I did not find an official, current EU Vocabularies deprecation-timing policy.

## 3. Deprecation and obsoletion policies

### Takeaway
There is a strong cross-community consensus. Never delete or reuse an identifier. Mark the term deprecated (`owl:deprecated true`, SNOMED inactive, schema.org attic). Keep its definition. Point to an exact successor (replaced_by / isReplacedBy / supersededBy / SNOMED REPLACED BY) or to inexact candidates (consider / POSSIBLY EQUIVALENT TO). Record a reason. Pre-announce the change. Keep old IRIs resolvable.

### Cited Findings
- **OBO obsoletion rules.**
  - Set `owl:deprecated true` (`is_obsolete: true` in OBO format).
  - Prefix the label with exactly "obsolete " in lowercase.
  - Remove all logical axioms from the term, and remove or replace its uses elsewhere.
  - *Keep* the textual definition.
  - Use "term replaced by" (IAO:0100001/OMO) for an exact replacement and `oboInOwl:consider` for inexact ones. Optionally record the reason.
  - Pre-announce obsoletions (principle 13).
  - The OBO Dashboard flags as errors: an obsolete term without the label prefix, an obsolete term with logical axioms, and other terms referencing an obsolete term.
  — [OBO FP-019](https://obofoundry.org/principles/fp-019-term-stability.html)
- Mondo uses `consider` rather than `term replaced by` when the successor lives in another ontology or is not equivalent. — [Mondo editors guide](https://mondo.readthedocs.io/en/latest/editors-guide/merging-and-obsoleting/)
- OAK (Ontology Access Kit) treats `owl:deprecated` as the canonical obsolescence marker. The "obsolete" label prefix is only a convention. — [OAK obsoletion guide](https://incatools.github.io/ontology-access-kit/guide/obsoletion.html)
- OBO requires released versions to remain resolvable at persistent versioned PURLs. — [OBO FP-004](https://obofoundry.org/principles/fp-004-versioning.html)
- schema.org deprecates first, then moves terms to the Attic and records successors in release notes. Superseded terms may be kept but flagged rather than removed. — [schema.org releases](https://schema.org/docs/releases.html)
- SNOMED never deletes. It uses a reason refset plus association refsets (see §2). — [SNOMED glossary: historical reference set](https://docs.snomed.org/snomed-international-documents/snomed-ct-glossary/h/historical-reference-set)
- EU Vocabularies: historical concepts carry start and end validity dates and are deprecated by default. — [EU Vocabularies](https://op.europa.eu/en/web/eu-vocabularies/advanced-learners)

### Inferences
- Recommended policy for internal platform-service vocabularies:
  1. Never delete or reuse an IRI.
  2. For a deprecated term, set `owl:deprecated true`, add `dcterms:isReplacedBy` (exact) or `rdfs:seeAlso`/oboInOwl `consider` (inexact), and add `skos:historyNote` with the reason, the release and the date. Keep `skos:definition`. Move the old prefLabel to `skos:hiddenLabel` on the successor, so search and lint still match the old name.
  3. Grace period: announce in release N, deprecate in N, and allow removal from *active* views, SHACL targets and lint allow-lists no earlier than N+1 MAJOR or after a fixed window, such as 90 days.
  4. Old IRIs keep resolving (via the git-tagged release and a redirect or 410-style "obsolete" page) to a page showing the successor.
- For a retired platform service (a real-world thing that ended), treat it as historic. Keep the entity, add `dcterms:valid` or an end date, and avoid "replaced_by" unless a successor service exists.

### Gaps
- I found no quantitative grace-period standard across communities. OBO says "pre-announce" without fixing a duration.

## 4. Change impact analysis and propagation

### Takeaway
Impact analysis means computing a dependency closure from the changed IRIs to every artifact that references them, then classifying each hit. The research literature (Stojanovic, Zablith et al., and bottom-up atomic/composite impact methods) frames this as the "change propagation" and "impact assessment" stages. In a git setup it reduces to:
1. A semantic diff (KGCL/ROBOT diff) of changed IRIs and axioms.
2. A reverse-reference search across the repo and the deployed KG.
3. Re-running SHACL validation and reasoner checks against current data.
4. Generating migration SPARQL Updates for renames and merges.

### Cited Findings
- Zablith et al. identify impact assessment and change propagation (to dependent ontologies, instances and applications) as distinct stages of the evolution process. — [Cambridge Core](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/abs/ontology-evolution-a-processcentric-survey/CE4387A954917B7CA3282CE25FAC09FA)
- A pre-LLM bottom-up method analyzes the structural and semantic impacts of atomic and composite ontology changes *before* applying them. — [CORE record](https://core.ac.uk/works/4767265)
- ChAO and KGCL change records can be derived from a structural diff between versions, which allows automated change lists. — [Springer ISWC 2006](https://link.springer.com/content/pdf/10.1007/11926078_39.pdf); [KGCL arXiv](https://arxiv.org/abs/2409.13906)
- Health-RI treats "previously valid instances become invalid" as a defining semantic-change test. In practice this means re-validating instance data against the new shapes. — [Health-RI](https://health-ri.github.io/semantic-interoperability/method/ontology-versioning)
- The OBO Dashboard automatically flags axioms that still reference obsolete terms, an example of an automated dangling-reference impact check. — [OBO FP-019](https://obofoundry.org/principles/fp-019-term-stability.html)
- The Semantic Arts versioning ontology models dependency tracking (including imports) across semantic artifacts in production, which can serve as a model for the dependency graph. — [semanticarts/versioning-ontology](https://github.com/semanticarts/versioning-ontology)
- **Recent LLM work (2025) is early-stage.**
  - Evo-DKD uses dual decoding to propose ontology edits plus justifications.
  - TRACE-OU-Bench benchmarks LLM-generated ontology update proposals against the ontology state at proposal time.
  - A CEUR ELMKE paper treats deciding whether a transformation can proceed as an LLM classification task; it is a preliminary, qualitative study.
  - None of these combine LLM change classification with downstream impact analysis.
  — [ELMKE 2025 (CEUR Vol-4246)](https://ceur-ws.org/Vol-4246/elmke-6.pdf); [TRACE-OU-Bench (CEUR Vol-4316)](https://ceur-ws.org/Vol-4316/pd-short-8.pdf); [Evo-DKD](https://aitopics.org/doc/arxivorg:8E726119)

### Inferences
Impact checklist the CI or AI Reviewer should produce for each PR (the changed IRI set comes from the diff):

| Dependent | Detection | Propagation |
|---|---|---|
| SHACL shapes | grep/SPARQL for IRI in `sh:targetClass`, `sh:path`, `sh:class`, `sh:in` | update shapes; re-run validation on full KG; report new violations |
| KG instances | `SELECT (COUNT(*)) WHERE { ?s ?p ?o FILTER(?o = <old> \|\| ?p = <old> \|\| ?s = <old>) }` | SPARQL Update migration: `DELETE {?s a <old>} INSERT {?s a <new>} WHERE {?s a <old>}`; checked into `migrations/vX.Y.Z/` |
| Mappings (skos:exactMatch, SSSOM) | reverse lookup | flag for mapping owner |
| Vale/lint vocabularies | regenerate accept/reject lists from prefLabel/altLabel/hiddenLabel + deprecated labels → "use X instead" rules | regenerate on release |
| Assistant prompts, routes, tool descriptions | text search for labels and IRIs | owner notification; prompt regression tests |
| Docs pages | text/IRI search | docs PR or warning banner |
| Cached answers / vector index | answers tagged with vocabulary version + IRIs used | invalidate entries citing changed IRIs; re-embed changed definitions |
| Downstream imports | `owl:imports` / dependency manifest | notify subscribers |

- Make migrations *idempotent* SPARQL Updates, versioned alongside the release and tested in CI against a snapshot of the KG.

### Gaps
- I did not retrieve Stojanovic's dissertation (2004, "Methods and Tools for Ontology Evolution", Karlsruhe) or the details of its change-propagation strategies, such as the dependent-ontology consistency and "evolution strategies" for orphan subclasses. They are cited here from general knowledge only and should be verified.
- I found no published tooling that computes impact across non-RDF dependents (prompts, docs, caches). This has to be custom.

## 5. Governance workflow (proposal → review → approval → release)

### Takeaway
Published communities converge on a common pattern:
- Change requests are GitHub issues or PRs using templates.
- Stewards or editors review, and the required approvals scale with the impact class.
- Releases are cut on a cadence, with a cut-off date for requests.
- Release notes link to issues and PRs.
- Maturity staging insulates stable consumers from in-progress work.

An AI Reviewer fits naturally as a classifier and drafter. It produces the change class, the impact report and the release-note draft, and humans keep approval authority for MINOR and above.

### Cited Findings
- DCAT-AP: change requests via GitHub, three change classes by interoperability impact, and late requests roll over to the next release. — [Interoperable Europe DCAT-AP policy](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/dcat-application-profile-data-portals-europe/document/change-and-release-management-policy-dcat-ap)
- schema.org: proposals and discussion on GitHub, drafts staged on staging.schema.org, numbered releases with itemized changes linked to issues and PRs, and patch releases for regressions. — [schema.org releases](https://schema.org/docs/releases.html)
- FIBO: a documented development process with member-firm review, Jira/Confluence/GitHub, and maturity levels that gate inclusion in the Production build. — [FIBO Development Process](https://spec.edmcouncil.org/fibo/page/development-process)
- Health-RI: stage gates (internal → internal review → external review → published), where any semantic change reverts a package to internal, and releases are mandatory only for externally visible stages. — [Health-RI](https://health-ri.github.io/semantic-interoperability/method/ontology-versioning)
- OBO: documented versioning procedures are required, released files are immutable, and obsoletions are pre-announced. — [OBO FP-004](https://obofoundry.org/principles/fp-004-versioning.html); [FP-019](https://obofoundry.org/principles/fp-019-term-stability.html)
- KGCL supports controlled-natural-language change requests that an automated GitHub agent can apply. This is a precedent for machine-assisted application of approved changes. — [KGCL arXiv](https://arxiv.org/abs/2409.13906)
- EU Vocabularies: release notes are mandatory in each publication package. — [EU Vocabularies](https://op.europa.eu/en/web/eu-vocabularies/advanced-learners)

### Inferences
Proposed workflow for the platform-service domain assistant.

**1. Proposal.** A PR template with these fields:
- change type (KGCL verb)
- affected IRIs
- rationale or evidence (ticket, ADR)
- the proposer's self-declared impact class
- replacement for deprecations
- migration needed (y/n)
- the owning team/steward

**2. Automated checks (CI).** Syntax and RDF parse, reasoner consistency, SHACL validation of the shapes themselves and of the KG against the new shapes, OBO-style obsoletion lint, label uniqueness, and a semantic diff (ROBOT diff or KGCL) attached to the PR.

**3. AI Reviewer.**
- Classifies each change as PATCH, MINOR or MAJOR using the matrix in §2, and flags meaning changes to definitions (OBO FP-019 test: same referents?).
- Runs the impact query set from §4 and posts the report.
- Drafts `skos:changeNote`/`historyNote` text and the release-note entry.
- Checks the deprecation hygiene: replaced_by present, label kept, no dangling references.
- Its verdict is advisory, and humans approve.

**4. Approval thresholds.**

| Class | Approvals |
|---|---|
| PATCH | 1 domain steward |
| MINOR | owning-team steward + 1 cross-team reviewer |
| MAJOR, or a SHACL tightening that produces violations | governance council or quorum (e.g., 2 stewards + council chair), migration plan, announcement period |

Use CODEOWNERS per namespace or module to enforce federated ownership.

**5. Emergency changes** (for example, a wrong definition causing harmful answers). Fast-track with one steward plus a post-hoc council review, but never as a destructive edit. Ship as a PATCH release or an assistant-side suppression.

**6. Release.**
- Cadence: for example, a monthly MINOR train with a cut-off date, and MAJOR at most quarterly.
- Git tag `vX.Y.Z` plus an immutable versionIRI.
- Ontology header: `owl:priorVersion`, `owl:backwardCompatibleWith`/`incompatibleWith`, `dcterms:issued`.
- A PROV-O release activity.
- `CHANGELOG.md` generated from the change records.

**7. Communication.**
- Release notes grouped by Breaking / Deprecated / Added / Changed / Fixed.
- Subscriber notifications (Teams/Slack/email or a GitHub release watch) targeted to the teams whose dependents were hit in the impact report.
- A deprecation calendar.

**8. Audit trail.** Git history + PR reviews + PROV-O + change records give a who/what/why/when record for every triple.

### Gaps
- I found no published approval-threshold numbers from OBO, FIBO or schema.org. The thresholds above are a design proposal.
- I found no published case study of an AI reviewer in ontology PR governance beyond the KGCL agent and the early LLM benchmarks.

## 6. How the end-user assistant handles versions

### Takeaway
Treat each release as an addressable, immutable named graph or snapshot keyed by versionIRI or tag. Answer against "current" by default, support "as of vX or date", cite the release in every answer, and use the deprecation and replacement links plus historyNotes to explain changes ("X was renamed to Y in v3.0"). Precedents include SNOMED history supplements in queries, FHIR's pinned versions for reproducible expansions, and OBO's resolvable versioned PURLs.

### Cited Findings
- SNOMED's ECL history supplements let a query include inactive or historical components linked through association refsets. This is a precedent for "include what this used to be called" queries. — [SNOMED ECL history supplements](https://docs.snomed.org/snomed-ct-specifications/snomed-ct-expression-constraint-language/examples/6.11-history-supplements)
- FHIR separates the business version from the expansion. Answers are reproducible only if the underlying code system versions are pinned. — [FHIR ValueSet](https://www.hl7.org/fhir/ValueSet.html)
- OBO's versioned PURLs resolve every past release permanently, which enables "as of" retrieval. — [OBO FP-004](https://obofoundry.org/principles/fp-004-versioning.html)
- SKOS historyNote examples ("heading was: Cruelty to children [1952-1975]") are exactly the kind of human-readable rename history an assistant can quote. — [SKOS Primer](https://www.w3.org/TR/skos-primer/)

### Inferences
- Load each release into its own named graph (for example, `<.../releases/v3.2.0>`), plus a `current` alias. Retrieval filters by graph, and the answer footer cites "Platform Glossary v3.2.0 (2026-11-01)".
- When a user's term matches a deprecated or hidden label, the assistant answers with the successor and explains: "'Foo Gateway' was renamed to 'Edge API Gateway' in v3.0 (2026-06); old name deprecated". This is driven by `owl:deprecated`, `dcterms:isReplacedBy` and `skos:historyNote`.
- For "what changed?", the assistant answers from the release-notes/change-record graph (KGCL records with PROV activities) rather than diffing on the fly.
- Cached answers store the vocabulary version and the IRIs they used. After a release, invalidate only the entries whose IRIs are in the change set.

### Gaps
- I found no published system or paper that describes an LLM assistant answering "as of version" over versioned vocabularies. The design above is inference from the terminology-service precedents.
