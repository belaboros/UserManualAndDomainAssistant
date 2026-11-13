# Modeling an Enterprise Internal Platform Landscape as Glossary / Taxonomy / Ontology / KG: Standards, Patterns, Toolchain, Process

Research date: 2026-11-13. Source notes: 19 search/fetch calls. Facts marked "(spec, not re-fetched)" are long-stable W3C/OASIS spec facts cited to the canonical spec URL, but this session did not re-open those pages. Treat them as high-confidence but unverified here.

## 1. Reusable vocabularies/ontologies and their maturity

### Takeaway
No single standard ontology covers an "internal developer platform" (IDP) landscape. The practical approach is a thin enterprise core that reuses stable W3C vocabularies (SKOS, ORG, PROV-O, DCAT 3, Dublin Core, schema.org) plus an upper ontology for structure (gist 14.x is current and actively maintained). Domain structure comes from de facto models: the Backstage catalog model for systems, components, APIs, resources and ownership; TOSCA 2.0 for node/relationship/capability topology; Kubernetes, Crossplane and Terraform schemas for resource kinds. None of these de facto models has an official RDF serialization, so you write the mappings yourself.

### Cited Findings
**Backstage catalog model (de facto IDP schema, no official RDF)**
- Backstage describes its catalog as a graph: entity descriptors are nodes and relations are edges. Kinds group entities, and `spec.type` sub-categorizes within a kind — [Backstage: creating the catalog graph](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph)
- Well-known relations (forward/inverse) and the kinds they connect. The docs call this list non-exhaustive — [Backstage well-known relations](https://backstage.io/docs/features/software-catalog/well-known-relations):
  - `ownedBy`/`ownerOf`: any entity → User or Group
  - `providesApi`/`apiProvidedBy` and `consumesApi`/`apiConsumedBy`: Component (or System) → API
  - `dependsOn`/`dependencyOf`: Component or Resource → any entity
  - `partOf`/`hasPart`: Component, API, Resource, System or Domain → System, Domain or Component
  - `memberOf`/`hasMember`: User → Group
  - `parentOf`/`childOf`: Group → Group
- The Backstage docs say the catalog should not be treated as the ultimate source of truth. They describe it as more of a caching mechanism — [Backstage catalog graph docs (via search summary)](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph)
- I found no official or widely adopted Backstage-to-RDF/OWL mapping. Third-party tools such as Knowledge Tree push discovered resources *into* Backstage and map relationships onto `dependsOn`, but they do not use RDF — [Knowledge Tree Backstage integration](https://knowledge-tree-web-docs.pages.dev/integrations/backstage/)

**TOSCA (OASIS)**
- TOSCA v2.0 was approved as an OASIS Standard, announced 9 September 2025. Cisco, HPE, Huawei, IBM, Red Hat, SAP and NIST were among its backers — [OASIS press release](https://www.oasis-open.org/?p=13225); [CIO Influence](https://cioinfluence.com/cloud/oasis-approves-tosca-v2-0-standard-for-cloud-orchestration/)
- 2.0 drops the "Simple Profile" (computing-only) framing so users can define domain-specific profiles. It adds user-defined functions, a formal graph traversal syntax for relationships and a Day-2 operational model. It supersedes TOSCA Simple Profile in YAML v1.3 and keeps nodes and relationships as first-class entities — [TOSCA v2.0 spec](https://docs.oasis-open.org/tosca/TOSCA/v2.0/TOSCA-v2.0.html); [OASIS TOSCA tag](https://www.oasis-open.org/tag/tosca)
- Sources disagree on the exact stage: some OASIS pages still show a Committee Specification Draft — [TOSCA TC discussion](https://groups.oasis-open.org/discussion/request-a-special-majority-vote-to-approve-a-candidate-for-oasis-standard-for-tosca-version-20-from-topology-and-orchestration-specification-for-cloud-applications)
- Relevance: TOSCA's concepts are a good conceptual template for a platform service model: node types, relationship types (DependsOn, HostedOn, ConnectsTo), capabilities and requirements, and substitution mappings, which let a node be realized by a whole sub-topology. TOSCA is YAML, not RDF. I found no maintained official TOSCA OWL ontology (see Gaps).

**OSLC (OASIS)**
- OSLC Core 3.0 became an OASIS Standard on 26 Aug 2021. Part 6 (Resource Shape) defines constraints, published as Turtle. OSLC Configuration Management 1.0 is a separate OASIS Standard defining an RDF vocabulary plus REST APIs for versions and configurations of linked-data resources. Tracked Resource Set 3.0 was published 23 July 2023 — [OASIS announcement](https://www.oasis-open.org/?p=10180); [OSLC Core 3.0 changes](https://oslc-op.github.io/oslc-specs/notes/core-3.0-changes/core-3.0-changes.html); [Resource Shape spec](https://docs.oasis-open.org/oslc-core/oslc-core/v3.0/csprd03/part6-resource-shape/oslc-core-v3.0-csprd03-part6-resource-shape.html)
- Relevance: OSLC is RDF-native and the most mature linked-data standard for versioned configurations and baselines of engineering artifacts. It suits ALM-style traceability. Its resource shapes predate SHACL, so SHACL is the more common choice today.

**ITIL/CMDB ontologies**
- ITSMO is an OWL/RDF vocabulary for ITIL-style IT service management. It treats services as configuration items linked to providers and customers. It is small (43 classes, 11 individuals) and described as still being populated — [ITSMO user guide](https://itsmo-efe4e5.gitlab.io/userguide/overview); [IndustryPortal ITSMO](https://industryportal.enit.fr/ontologies/ITSMO)
- The rest of the work is academic: an OWL formalization of ITIL processes with SWRL/SQWRL (Health, Jones and Valiente 2012) — [paper](https://www.dhi.ac.uk/san/waysofbeing/data/health-jones-valiente-2012.pdf); a foundational-ontology-based configuration-management conceptual model (Baiôco et al.) — [core.ac.uk](https://core.ac.uk/download/322416295.pdf); a CIM-based semantic CMDB (University of Zurich BA thesis) — [thesis](https://files.ifi.uzh.ch/CSG/staff/machado/extern/studenttheses/Daniel_Meier_BA_Thesis.pdf)
- Vendor patents describe CI dependency types and transforming a CMDB into a knowledge base. They show common practice but are not standards — [US 12481681](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12481681); [US 11755931](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11755931)

**ArchiMate**
- There is no official Open Group RDF/OWL serialization. The official Model Exchange File Format is XML/XSD, an intermediate representation meant for ArchiMate-aware tools — [Open Group exchange format guide](https://pubs.opengroup.org/architecture/archimate31-exchange-file-format-guide); [XSD](https://www.opengroup.org/xsd/archimate/)
- Conversions are custom. Published mapping rules turn metamodel concepts into OWL classes and relationships into object properties — [Springer paper](https://rd.springer.com/content/pdf/10.1007/978-3-642-54734-8_7.pdf). The Archi plug-in "OWLExchange" is a work in progress — [GitHub](https://github.com/archimatetool/OWLExchange). Open Group forum participants argued OWL is a poor fit for diagram exchange — [forum](https://groups.google.com/g/open-archimate-forum/c/poUR2BRqve0)
- Relevance: ArchiMate's Application/Technology layers fit an IDP model well: Application Component, Application Service, Application Interface, Technology Service, Node, System Software, plus Serving, Realization, Composition, Aggregation and Assignment relations. Its Capability and Business Service split is useful for "capabilities vs services".

**gist (Semantic Arts upper ontology)**
- gist 14.0.0 was released 31 Oct 2025. It is a major, breaking release with a streamlined hierarchy, including "composites and components", and ships migration scripts. gist 14.1.0 (documentation dated April 2026) is backward-compatible with 14.0. License CC BY 4.0; IRI `https://w3id.org/semanticarts/ontology/gistCore` — [Semantic Arts gist page](https://www.semanticarts.com/gist/); [gist 14.0 docs](https://semanticarts.github.io/gist-doc/gist-14.0/widoco-documentation/index-en.html); [GitHub](https://github.com/semanticarts/gist)
- gistBFO (FOIS 2025) is a BFO-compatible version of gist, which bridges to BFO-based ontologies — [UB ResearchConnect](https://researchconnect.buffalo.edu/en/publications/gistbfo-an-open-source-bfo-compatible-version-of-gist/)
- Note: gist publishes its documentation with Widoco, showing that toolchain in a maintained project — [gist 14.0 Widoco docs](https://semanticarts.github.io/gist-doc/gist-14.0/widoco-documentation/index-en.html)

**Kubernetes / cloud ontologies**
- No standard Kubernetes OWL ontology exists. The closest projects are:
  - The FLUIDOS "kubernetes" ontology, generated automatically from the Kubernetes API, plus a mapping ontology for cloud-continuum concepts — [fluidos-ontology](https://github.imc.re/fluidos-project/fluidos-ontology)
  - CNOnt, an OWL model of cloud-native cluster state with a broker that syncs it with a live cluster in both directions (Springer IJSTT 2024) — [Springer](https://link.springer.com/article/10.1007/s10009-023-00705-2)
  - Dynatrace Binnacle, a TypeDB knowledge graph with inference rules — [GitHub](https://github.com/dynatrace-research/binnacle)
  - milo-os Knowledge Graph Service, which defines CRDs (RelationshipType, RelationshipPolicy, ResourceRelationship) for typed edges beyond ownerReferences, with CEL auto-discovery and ArangoDB storage — [GitHub](https://github.com/milo-os/knowledge)
- A CNCF TAG Network issue notes that the Kubernetes OpenAPI specs already provide a taxonomy that could be formalized — [cncf/tag-network#39](https://github.com/cncf/tag-network/issues/39)

**DCAT 3 (data services)**
- DCAT 3 has been a W3C Recommendation since August 2024. It adds dataset series, versioning and inverse properties, and stays backward-compatible with DCAT 2. `dcat:DataService`, introduced in DCAT 2, models a service giving access to datasets or data processing. `dcat:servesDataset` links the service to its datasets, and `dcat:endpointDescription` points to a (possibly machine-readable) API description — [DCAT 2 rationale paper, arXiv 2303.08883](https://arxiv.org/pdf/2303.08883); [Dublin Core MSI DCAT entry](https://msi.dublincore.org/standards/dcat)
- DCAT-US 3.0 states that the endpoint description is typically an OpenAPI or WSDL URL. This is a profile rule, not a core W3C requirement — [DCAT-US 3 DataService](https://resources.data.gov/resources/dcat-us-3-data-service/)
- The semantics of `servesDataset` (does the service deliver the data itself, or metadata about it?) were debated in the DXWG in 2022 — [W3C list](https://lists.w3.org/Archives/Public/public-dxwg-wg/2022Jan/0001.html)
- Relevance: `dcat:DataService` plus `dcat:endpointURL`/`endpointDescription` is a standards-based way to describe platform APIs and data products in a catalog.

**Stable W3C/community vocabularies (spec, not re-fetched)**
- SKOS: W3C Rec 2009; SKOS-XL is its label-reification extension — [SKOS Reference](https://www.w3.org/TR/skos-reference/)
- W3C Organization Ontology (ORG, Rec 2014): `org:Organization`, `org:OrganizationalUnit`, `org:Membership`, `org:Role`, `org:memberOf`, `org:hasUnit`/`unitOf`. It fits platform teams and team topologies — [ORG](https://www.w3.org/TR/vocab-org/)
- PROV-O (Rec 2013) covers provenance of generated triples: which pipeline produced which assertion from which source — [PROV-O](https://www.w3.org/TR/prov-o/)
- Dublin Core Terms (DCMI) — [DCMI Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- schema.org `SoftwareApplication` / `WebAPI` / `SoftwareSourceCode` — [schema.org SoftwareApplication](https://schema.org/SoftwareApplication)
- DOAP (Description of a Project) is a community RDF vocabulary for software projects and repositories, with low maintenance activity — [DOAP GitHub](https://github.com/ewilderj/doap)
- FOAF (persons, groups) — [FOAF spec](http://xmlns.com/foaf/spec/)

### Inferences
- Recommended reuse stack:
  - SKOS/SKOS-XL for the glossary and synonyms
  - Your own OWL classes for resource kinds, aligned to gist or BFO if you want an upper ontology
  - ORG (+FOAF) for teams and ownership
  - DCAT 3 `DataService` + schema.org `WebAPI` for APIs
  - PROV-O for lineage of auto-generated facts
  - Dublin Core for metadata
  - Backstage relation names as the *operational* predicate vocabulary (`ownedBy`, `dependsOn`, `partOf`, `providesApi`, `consumesApi`), because product teams already understand them
  - TOSCA and ArchiMate as conceptual references, not import targets
- Expect to maintain your own Backstage→RDF mapping. JSON-LD contexts over Backstage entity JSON are the lowest-effort route (inference; no off-the-shelf project found).
- CIM (DMTF) and ITIL ontologies are either old or academic. Use them for inspiration only.

### Gaps
- No maintained, official TOSCA OWL ontology found; there are academic TOSCA-in-RDF efforts, but they were not verified.
- DMTF CIM's current status (and any CIM-OWL mapping) was not verified this session.
- No BFO-based IT/software ontology verified beyond gistBFO. The Software Ontology (SWO, OBO) and IAO exist, but this session did not check their maintenance status.
- No Backstage-to-RDF open-source project found.
- schema.org, DOAP and FOAF current maintenance activity was not re-verified.

## 2. Modeling patterns (taxonomy, partonomy, dependencies, versioning, ownership, capabilities, synonyms)

### Takeaway
- Keep two layers:
  - a SKOS concept scheme (glossary/thesaurus) for human terms, synonyms and deprecations
  - an OWL/SHACL schema for typed instances of resource kinds and their relations
- Bridge the layers with punning or explicit links.
- Model compound resources with a transitive `partOf`/`hasPart` pair; Crossplane compositions and TOSCA substitution are natural sources for it.
- Model dependencies, API provision and API consumption as distinct, non-transitive base properties, with a transitive super-property used for impact analysis.

### Cited Findings
- **SKOS vs OWL hierarchy:**
  - `skos:broader` is a non-transitive, loose "more general concept" link between concepts (individuals). `rdfs:subClassOf` is logical set inclusion with inheritance under reasoning (spec, not re-fetched) — [SKOS Reference](https://www.w3.org/TR/skos-reference/)
  - OWL 2 punning lets the same IRI be both a class and an individual, so a resource-kind IRI can be an `owl:Class` *and* a `skos:Concept` with `skos:broader` mirroring `rdfs:subClassOf` — [W3C public-esw-thes, Jan 2024](https://lists.w3.org/Archives/Public/public-esw-thes/2024Jan/0001.html)
  - Punning also allows a class to be the value of an object property in OWL 2 DL — [Hitzler ODP slides](https://www.cs.ksu.edu/~hitzler/resources/presentations/2013-08-ICCLSS-patterns.pdf)
  - No standard says which class a pun should be an instance of — [same thread](https://lists.w3.org/Archives/Public/public-esw-thes/2024Jan/0001.html)
- **Part-whole (partonomy):**
  - The W3C SWBP note defines `partOf` as an `owl:TransitiveProperty` with inverse `hasPart`. It recommends a non-transitive `directPartOf` sub-property to keep immediate structure queryable — [W3C SWBP Simple part-whole relations draft](https://lists.w3.org/Archives/Public/public-swbp-wg/2005Apr/att-0056/simplePartOfWithIndividuals.html)
  - Meronymy has subtypes (functional component, member-collection, portion and others) — [CTU ontology design patterns lecture](https://cw.fel.cvut.cz/old/_media/courses/osw/lecture-07designpatterns-h.pdf)
  - gist 14 restructured its "composites and components" classes, giving a maintained upper-level pattern for compound things — [gist page](https://www.semanticarts.com/gist/)
  - Backstage `partOf`/`hasPart` connects Component, API, Resource, System and Domain to its container — [Backstage relations](https://backstage.io/docs/features/software-catalog/well-known-relations)
- **Dependencies/uses:**
  - Backstage separates `dependsOn`/`dependencyOf` from `providesApi`/`consumesApi` — [Backstage relations](https://backstage.io/docs/features/software-catalog/well-known-relations)
  - TOSCA 2.0 keeps typed relationships as first-class entities and adds graph traversal syntax — [TOSCA v2.0](https://docs.oasis-open.org/tosca/TOSCA/v2.0/TOSCA-v2.0.html)
  - CMDB practice defines dependency as one CI relying on another to function — [US 12481681](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12481681)
- **Ownership:** Backstage `ownedBy` → User or Group — [Backstage relations](https://backstage.io/docs/features/software-catalog/well-known-relations). W3C ORG `org:Membership` + `org:Role` gives n-ary, time-bounded team membership (spec, not re-fetched) — [ORG](https://www.w3.org/TR/vocab-org/)
- **Versioning:**
  - DCAT 3 added versioning properties (e.g. `dcat:version`, `dcat:hasVersion`, `dcat:previousVersion`) and dataset series — [arXiv DCAT paper / DCAT 3 summary](https://arxiv.org/pdf/2303.08883)
  - OSLC Configuration Management 1.0 standardizes versions/configurations/baselines of linked-data resources — [OASIS](https://www.oasis-open.org/?p=10180)
- **Synonyms (SKOS-XL):**
  - `skosxl:prefLabel`/`altLabel`/`hiddenLabel` have range `skosxl:Label`, so labels become resources that can carry metadata such as status, source, deprecated or team — [W3C SKOS-XL design wiki](https://www.w3.org/2006/07/SWD/wiki/SkosDesign/SKOS-XL)
  - The SKOS integrity rules still apply: pref, alt and hidden labels are pairwise disjoint, and a concept has at most one prefLabel per language — [W3C SKOS-XL design wiki](https://www.w3.org/2006/07/SWD/wiki/SkosDesign/SKOS-XL)
  - TopBraid EDG converts SKOS-XL labels into plain SKOS labels for consumers — [TopQuadrant docs](https://www.topquadrant.com/doc/7.2/user_guide/guidance_specific_to_asset_collection_type/working_with_taxonomies/skos_xl_taxonomies.html)
  - The EU Publications Office uses SKOS-XL with the same semantics — [EU Vocabularies](https://webanalytics.op.europa.eu/en/web/eu-vocabularies/semantic-knowledge-base/-/knowledge_base/labels-and-data-models-why-and-how-to-use-them)
  - Skosmos honours `owl:deprecated` when displaying concepts — [Skosmos Concept.php](https://scrutinizer-ci.com/g/NatLibFi/Skosmos/issues/main/files/src/model/Concept.php)
  - OntoLex discussion distinguishes deprecated (outdated, non-preferred) terms from hidden labels (misspellings) — [public-ontolex 2013](https://lists.w3.org/Archives/Public/public-ontolex/2013Jul/0058.html)

### Inferences
- **Taxonomy:**
  - Put resource kinds (e.g. `:PostgresDatabase rdfs:subClassOf :ManagedDatabase rdfs:subClassOf :PlatformResource`) in OWL.
  - Pun each kind as a `skos:Concept` in a "Resource Kinds" concept scheme, with `skos:broader` generated from `subClassOf` by a SPARQL CONSTRUCT in CI.
  - Use SKOS-only, with no OWL class, for fuzzy, overlapping topic terms such as "observability" or "golden path".
- **Synonym reduction:**
  - Each concept has one `skos:prefLabel` (the canonical term).
  - Team-specific or legacy names go in `skos:altLabel`. Misspellings and Slack slang go in `hiddenLabel`, which is searchable but not displayed.
  - Upgrade to SKOS-XL only if you need per-label metadata: owning team, "deprecated since", source system.
  - Deprecate a concept with `owl:deprecated true` + `dct:isReplacedBy` (common practice; not verified in a source this session).
  - A SHACL rule enforces one prefLabel per language and no label collisions across concepts. Collision detection is the main anti-synonym control.
- **Compound resources:**
  - Define `:hasComponent` ⊑ `:hasPart` (transitive) with a non-transitive `:hasDirectComponent`.
  - A Crossplane XR / Composition, a Backstage System, or a TOSCA substitution-mapped node becomes the "whole". The composed managed resources become parts.
  - Class-level SHACL shapes state which component kinds a compound kind must contain, e.g. "a `:WebAppStack` has exactly one `:Ingress`, ≥1 `:Deployment`".
- **Dependencies:**
  - Base properties: `:dependsOn` (runtime), `:providesApi`/`:consumesApi`, `:hostedOn`/`:deployedOn`, `:realizes` (service realizes capability).
  - A transitive super-property `:transitivelyDependsOn`, or SPARQL property paths `dependsOn+`, supports blast-radius queries.
- **Capabilities vs services:**
  - A capability (what the platform *can do*: "provide relational storage") is an abstract SKOS/OWL concept.
  - A service (an offered, versioned, owned implementation) `:realizes` a capability. This follows ArchiMate's Realization and the TOSCA capability idea.
  - Overlapping services are then easy to find: multiple services realizing the same capability.
- **Versioning:**
  - Model the service as a stable IRI with `dcat:hasVersion` → version IRIs (or `schema:softwareVersion` literals).
  - Model the ontology itself with `owl:versionIRI` + `owl:priorVersion`.

### Gaps
- No authoritative source found that directly compares `skos:broader` with `rdfs:subClassOf` for this use case. The guidance above is synthesized.
- The ODP portal (ontologydesignpatterns.org) componency pattern was not fetched. Its current availability is unverified.
- `dct:isReplacedBy` / `owl:deprecated` conventions for SKOS were not confirmed by a source this session.

## 3. Generating schema automatically from machine-readable sources

### Takeaway
LinkML is the most practical "hub". Its schema-automator imports JSON Schema (and therefore OpenAPI component schemas and Kubernetes CRD `openAPIV3Schema`), OWL (functional syntax via ROBOT) and SHACL into LinkML YAML. LinkML generators then emit OWL, SHACL, JSON-LD contexts and JSON Schema. Crossplane XRDs plus Compositions, Terraform provider schemas and Backstage YAML are rich, structured inputs: XRDs give resource kinds, Compositions give partonomy, Terraform schemas give attributes. All of these need custom extractors. Importer output is heuristic and needs human curation.

### Cited Findings
- **LinkML generators and importers:**
  - LinkML generators produce OWL, SHACL, ShEx, JSON Schema, JSON-LD context and others from a single YAML schema — [LinkML generators](https://linkml.io/linkml/generators/); [SHACL gen](https://linkml.io/linkml/generators/shacl.html); [OWL gen](https://linkml.io/linkml/generators/owl)
  - schema-automator imports JSON Schema (`import-json-schema`) and SHACL (`import-shacl`). SHACL import maps node shapes to classes and `sh:property` to attributes, with auto-detection of two shape-to-class conventions — [schema-automator importers](https://linkml.io/schema-automator/packages/importers.html)
  - The OWL importer accepts only schema-style OWL in functional syntax, so convert with ROBOT first — [schema-automator importers](https://linkml.io/schema-automator/packages/importers.html)
  - The project FAQ says seeding is heuristic, not guaranteed correct, and that importing from less expressive languages loses information — [LinkML FAQ tools](https://linkml.io/linkml/faq/tools.html); [schema-automator intro](https://linkml.io/schema-automator/introduction.html)
  - An old PyPI page (1.0.0b0) still lists JSON-Schema and SHACL import as TODO, which conflicts with current docs. Trust the current docs — [PyPI 1.0.0b0](https://pypi.org/project/schema-automator/1.0.0b0)
- **LinkML release status:**
  - linkml-model 1.10.0 was published 26 Feb 2026 — [Zenodo](https://zenodo.org/records/18780354)
  - v1.11.0 (13 May 2026) added owlgen disjointness for child classes and covering axioms for abstract classes, and moved shaclgen to SchemaView — [Zenodo](https://zenodo.org/records/20169054)
  - The June 2026 newsletter reports metamodel and runtime at 1.11.1, with a stricter linkml-lint — [LinkML community group](https://groups.google.com/g/linkml-community/c/SPxSD8Muiiw)
  - The `linkml` package is at 1.12.1 on PyPI (Oct 2026) — [PyPI linkml](https://pypi.org/project/linkml/). The project is actively maintained.
- **Crossplane v2:**
  - XRDs carry a `scope` field that defaults to Namespaced, and Claims are no longer supported for new namespaced/cluster XRs — [Crossplane v2.0 what's new](https://docs.crossplane.io/v2.0/whats-new/)
  - Namespaced XRs can compose any Kubernetes resource, not only Crossplane managed resources. Upbound docs conflict and say they compose only namespaced resources — [Crossplane v2.0 what's new](https://docs.crossplane.io/v2.0/whats-new/); [Upbound](https://docs.upbound.io/manuals/cli/howtos/compositions/python/)
  - Compositions are pipelines of composition functions (`mode: Pipeline`), and native patch-and-transform was deprecated in v1.17 — [Crossplane compositions v2.1](https://docs.crossplane.io/v2.1/composition/compositions/); [upgrade guide](https://docs.crossplane.io/v2.1/guides/upgrade-to-crossplane-v2/)
  - Docs exist up to v2.3, and the CLI is at v2.4 — [docs v2.3](https://docs.crossplane.io/v2.3/get-started/get-started-with-composition/)
- **Terraform:**
  - `terraform providers schema -json` prints a JSON document with `format_version` and `provider_schemas` keyed by provider. Each entry holds provider, resource, data source and function schemas, made of blocks with attributes (type, description, required, optional, computed, sensitive) and nested blocks — [HashiCorp docs](https://developer.hashicorp.com/terraform/cli/commands/providers/schema)
  - Within 1.x the format is backward-compatible, so consumers should ignore unknown properties — [HashiCorp docs](https://developer.hashicorp.com/terraform/cli/commands/providers/schema)
- **Kubernetes:**
  - The FLUIDOS project auto-generates a Kubernetes ontology from the Kubernetes API, a precedent for generating OWL from Kubernetes OpenAPI — [fluidos-ontology](https://github.imc.re/fluidos-project/fluidos-ontology)
  - A CNCF TAG Network issue argues that Kubernetes OpenAPI specs already form a taxonomy — [cncf/tag-network#39](https://github.com/cncf/tag-network/issues/39)
- **Backstage:** entity YAML has kind, `spec.type`, owner and relations, which map directly to RDF predicates (see section 1) — [Backstage relations](https://backstage.io/docs/features/software-catalog/well-known-relations)
- **OpenAPI → catalog:** DCAT `endpointDescription` is typically an OpenAPI URL (DCAT-US 3 profile) — [DCAT-US 3](https://resources.data.gov/resources/dcat-us-3-data-service/)

### Inferences
Proposed generation pipeline (synthesized):
1. **Resource kinds:**
   - Inputs: CRDs (`kubectl get crd -o json`), XRDs, and `terraform providers schema -json`.
   - A script emits a LinkML class per Kind/resource type, with `is_a` assigned from a curated mapping table (e.g. `aws_db_instance`, `XPostgreSQLInstance` and `CloudSQLInstance` all `is_a ManagedRelationalDatabase`).
   - The curated table is where synonyms across clouds get resolved into one canonical concept, with the provider-specific names as `altLabel`.
2. **Compound resources:**
   - Parse each Composition's pipeline inputs (resources templated by function-patch-and-transform or KCL/Go functions) and emit `:XWebApp :hasDirectComponent :Deployment, :Service, :RDSInstance` at class level, as SHACL `sh:qualifiedValueShape` or OWL restrictions.
   - At instance level, harvest live XR → composed resource refs from the cluster (`spec.crossplane.resourceRefs` in v2; field name not verified this session).
3. **Instances (A-box):**
   - Map Backstage entity JSON to JSON-LD via a hand-written `@context`.
   - Load it alongside cluster and Terraform state harvests.
   - Stamp each triple batch with PROV-O (`prov:wasGeneratedBy` pipeline run, `prov:wasDerivedFrom` source).
4. **APIs:**
   - Convert OpenAPI component schemas with schema-automator `import-json-schema` for data shapes.
   - Describe each API as `dcat:DataService`/`schema:WebAPI` with `dcat:endpointDescription` → OpenAPI URL.
   - Do not convert every operation into the ontology.
5. LinkML is the single source → `gen-owl`, `gen-shacl`, `gen-jsonld-context`, `gen-json-schema` (also usable to validate Backstage YAML), and `gen-doc` for docs.

Treat generated schema as *proposals* that go through PR review, because importers are heuristic.

### Gaps
- No off-the-shelf CRD→OWL, XRD/Composition→OWL or Terraform-schema→OWL converter was verified. Expect to build these extractors (small scripts).
- OpenAPI→RDF tools (e.g. Hydra, openapi2rdf-style projects) were not researched this session.
- Whether LLM-assisted term extraction or mapping is built into LinkML tooling (e.g. schema-automator's LLM annotators, OntoGPT) was not verified.

## 4. Git-based toolchain and CI, ease of use for non-ontologists

### Takeaway
Mature pieces exist for every stage:
- **Authoring:** Turtle or LinkML YAML in git, edited directly or generated from spreadsheets (VocExcel/voc4cat for SKOS, ROBOT templates for OWL).
- **Validation:** pySHACL, ROBOT `report`/`reason`, and LinkML lint.
- **Diffs:** ROBOT diff posts markdown diffs as PR comments in ODK.
- **Publishing:** Widoco, pyLODE, Skosmos or Prez.
- **Querying:** Fuseki, Oxigraph or GraphDB.

ODK is the most complete "ontology repo in a box", built for OBO/biomedicine but reusable.

### Cited Findings
- **ODK and ROBOT:**
  - The ODK changelog lists a release-diff GitHub Action that posts diffs as PR comments, a markdown report comparing the latest release to the current build, and a `public_release` workflow that creates a GitHub release, tags it and uploads artefacts — [ODK CHANGELOG](https://github.stncp.dns-dynamic.net/INCATools/ontology-development-kit/blob/master/CHANGELOG.md); [ODK releases](https://www.github.com/INCATools/ontology-development-kit/releases)
  - Since the June 2022 release, `diff.yaml` must be configured explicitly — [ODK v1.3.1](https://github.com/INCATools/ontology-development-kit/releases/tag/v1.3.1)
  - `robot diff --labels true --left <release> --right <build> -f markdown` is the typical command — [C-Path ontology issue](https://gitlab.c-path.org/c-pathontology/critical-path-ontology/-/issues/84)
  - OBO Academy documents wiring ROBOT diff into `.github/workflows` — [OBO Academy GitHub Actions how-to](https://oboacademy.github.io/obook/howto/github-actions)
  - ODK editor and release workflows are documented in projects such as Mondo — [Mondo release guide](https://mondo.readthedocs.io/en/latest/developer-guide/release/); [ODK editors workflow](https://berkeleybop.org/artificial-intelligence-ontology/odk-workflows/EditorsWorkflow/)
  - ODK paper (Database journal / arXiv 2207.02056) — [arXiv](https://export.arxiv.org/abs/2207.02056)
- **Spreadsheet front-ends for SKOS:**
  - VocExcel converts template Excel workbooks to SKOS following the VocPub profile. Development moved to KurrawongAI, which hosts an online VocExcel — [Kurrawong VocExcel](https://github.com/Kurrawong/VocExcel); [PyPI vocexcel](https://pypi.org/project/vocexcel/)
  - The NFDI4Cat fork is archived. Its successor voc4cat converts Excel↔Turtle in both directions, validates against VocPub SHACL and supports GitHub workflows (contribution by PR) — [nfdi4cat/VocExcel](https://github.com/nfdi4cat/VocExcel); [voc4cat on PyPI](https://pypi.org/p/voc4cat)
  - The VocPub profile ships a SHACL validator (CC-BY-4.0) — [BARTOC vocabulary software list](https://gbv.github.io/bartoc-vocabulary-software)
- **Viewers and publishing:**
  - Skosmos is a PHP, MIT-licensed SKOS browser. VocPrez is a Python read-only SKOS delivery tool. Prez is a configurable Linked Data API framework (KurrawongAI) — [BARTOC software wiki](https://github.com/gbv/bartoc.org/wiki/Software-for-controlled-vocabularies)
  - The South Australian SARIG vocabularies show Prez in production — [SARIG about](https://vocabularies.sarig.sa.gov.au/about)
  - Widoco generates ontology documentation; gist uses it — [gist Widoco docs](https://semanticarts.github.io/gist-doc/gist-14.0/widoco-documentation/index-en.html)
- **LinkML tooling:**
  - LinkML YAML is the friendliest authoring format for developers, with `linkml-lint` and generators (see section 3) — [LinkML overview](https://linkml.io/linkml/intro/overview.html)
  - schema-automator also has spreadsheet-based schema authoring ("schemasheets" in the LinkML ecosystem) — [LinkML FAQ tools](https://linkml.io/linkml/faq/tools.html)
- **TopBraid EDG** (commercial, TopQuadrant) supports SKOS-XL taxonomies and SHACL-based governance — [TopQuadrant docs](https://www.topquadrant.com/doc/7.2/user_guide/guidance_specific_to_asset_collection_type/working_with_taxonomies/skos_xl_taxonomies.html)

### Inferences
Reference repo layout and CI (synthesized):
- **Layout:**
  - `core/` (LinkML YAML → generated OWL/SHACL; owned by architecture group)
  - `vocab/` (SKOS Turtle, or `.xlsx` via voc4cat; glossary)
  - `teams/<team>/` (team modules importing core)
  - `mappings/` (SSSOM or plain `skos:exactMatch` files for cross-team synonyms)
  - `data/` (generated A-box; usually not committed, rebuilt by harvest jobs)
- **CI on PR:**
  - `linkml-lint` → `gen-owl`/`gen-shacl`
  - `riot --validate` or rdflib parse
  - `robot reason` (ELK/HermiT; consistency, unsatisfiable classes) and `robot report` (missing labels/definitions)
  - `pyshacl` validation of vocab and sample data against shapes, including a VocPub-style SKOS profile and custom label-collision rules
  - `robot diff -f markdown` posted as a PR comment
  - CODEOWNERS approval
- **On merge/tag:**
  - Build a release with `owl:versionIRI`
  - Publish docs (Widoco or pyLODE for OWL; Skosmos/Prez for SKOS) to an internal site
  - Load into a triple store (Fuseki or Oxigraph for light use, GraphDB for reasoning/enterprise)
- Non-ontologists edit spreadsheets (voc4cat for terms, ROBOT templates or LinkML schemasheets for classes) or Backstage-style YAML. CI turns these into RDF. Domain teams never need to hand-write Turtle.
- pySHACL, rdflib, Oxigraph and Fuseki are well-known OSS. Their current versions were not checked this session.

### Gaps
- Current release status of pySHACL, pyLODE, Oxigraph, Fuseki, GraphDB and Skosmos (v3) was not verified this session.
- owl-diff (Bosch/ontology diff tools) and ROBOT's current version were not checked.
- SSSOM was not researched here (recommended to check for synonym/mapping governance).

## 5. Federated governance across many teams

### Takeaway
Use a hub-and-spoke model: a small, centrally governed core ontology and glossary (shared namespaces, upper classes, the relation vocabulary, SHACL profiles), with team-owned modules that import the core and extend it bottom-up. Changes flow through PRs with CODEOWNERS and automated validation. Practitioners warn that central governance becomes a bottleneck (Capital One) and that cross-domain agreement takes more effort than expected.

### Cited Findings
- Capital One (SEMANTiCS 2022) presented a federated contribution and governance framework for an enterprise ontology, reasoning that centralized governance becomes a bottleneck — [SEMANTiCS 2022 talk](https://2022-eu.semantics.cc/node/3655)
- In the hub-and-spoke pattern, a central ontology is a shared framework that domain-specific models plug into, built bottom-up and linked to the top-down core — [Towards Data Science, Data Mesh part 3](https://towardsdatascience.com/challenges-and-solutions-in-data-mesh-part-3-dacb917f3c91)
- A vendor (Promethium) argues for keeping semantics (ontology) central and implementation local, with central changes propagating via mappings. It warns that organizations underestimate the effort of building domain ontologies all stakeholders agree on. This is a vendor source — [Promethium guide](https://promethium.ai/guides/metadata-management-data-mesh-federated-ownership-patterns/)
- Domains own vocabularies while the platform enforces SKOS/OWL/SHACL standards — [Federated knowledge graph substack](https://dataintelligenceplatform.substack.com/p/federated-knowledge-graph)
- Knowledge graphs tend to be managed more centrally than data mesh, while Dehghani frames data products as an "emergent knowledge graph" — [Enterprise Knowledge](https://enterprise-knowledge.com/?p=18312)
- ODK's import/module mechanisms and the OBO practice (each ontology owns its namespace, imports others via extracted modules) are a working federated model at scale — [ODK paper](https://export.arxiv.org/abs/2207.02056)

### Inferences
Governance blueprint (synthesized):
1. **Namespaces:**
   - `https://kg.example.com/core/` for the core
   - `.../platform/<team>/` for team modules
   - `.../id/<kind>/<slug>` for instance IRIs derived from Backstage entity refs, so IRIs are stable and resolvable
2. **Ownership:**
   - CODEOWNERS per folder. The core needs approval from a small "semantic council" (architecture + 1–2 rotating platform-team reps). Team modules need only team approval plus green CI.
   - Map each module to its Backstage Group as `dct:creator` / `ownedBy`.
3. **Rules enforced by CI:**
   - Team modules may only add classes *under* core classes, and may not redefine core terms.
   - New labels must not collide with existing prefLabels or altLabels; if they do, link with `skos:exactMatch` or reuse the term.
   - Every term needs a definition and an owner.
4. **Lifecycle:**
   - Status for terms: proposed → approved → deprecated (`owl:deprecated`, replacement link). Never delete an IRI.
   - Semantic versioning of modules via `owl:versionIRI`, with a release-diff changelog.
5. **Semi-automation:** harvest jobs (CRD, XRD, Terraform, Backstage, OpenAPI) open *bot PRs* that propose new kinds and labels. Humans curate the mapping to canonical concepts. Synonym candidates can be found by label similarity or LLM suggestion, and are always approved by humans.
6. **Product teams:** the same template repo (cookiecutter of the platform core repo) lets product teams build their own domain glossaries/KGs that import the platform core. This lets a product KG cleanly reference platform resources.

### Gaps
- I found no published case study of an enterprise *platform-engineering* ontology governed this way. Evidence comes from data-mesh/KG governance and OBO practice by analogy.
- The details of Capital One's framework (tooling, approval SLAs) were not retrieved beyond the abstract.
- No metrics found on adoption or effort of federated ontology governance.
