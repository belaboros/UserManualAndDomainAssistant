# End-user editors & platforms for ontologies, taxonomies, thesauri and glossaries: reuse evaluation (as of 2026-11-13)

Method note: GitHub activity figures (stars, last push, latest release tag/date, license SPDX) were pulled live from the GitHub REST API on 2026-11-13 (`api.github.com/repos/<owner>/<repo>` and `/releases`). Vendor product facts come from vendor pages/release notes found by web search in this session and are labeled "vendor claim" where not independently evidenced. Some feature descriptions of long-stable OSS tools come from their official repos/docs and prior knowledge of those docs. Those are cited to the repo/doc URL, but I did not re-read them page by page in this session, so treat them as "documented, not re-verified 2026".

## Q1. Which tools exist, what are they for, and are they maintained in 2026? (inventory + maintenance evidence)

### Takeaway
The open-source tools still actively released in 2026 are Protégé (6.0 alpha, Sep 2026), WebProtégé (new microservice line, released Oct 2026), VocBench/ShowVoc (15.1.2/6.1.2, Jul 2026), Skosmos 3 (v3.5, Oct 2026), iQvoc (4.15.1, Sep 2026), TermIt (5.2.0, Nov 2026), TemaTres (3.6.2, Oct 2026), voc4cat-tool (1.2.0, Sep 2026), OLS4, Prez and the data-catalog glossaries (DataHub, OpenMetadata, Atlas). SkoHub Editor is archived. VocExcel, SKOS Play (core) and OntoChat are effectively dormant. The commercial suites (TopBraid EDG, Graphwise PoolParty, Progress Semaphore, metaphactory, Stardog) are all shipping LLM-assisted modeling features in 2025-2026, but all of them are closed source and licensed per seat or per server.

### Cited Findings

**Live GitHub activity snapshot (queried 2026-11-13)**

| Repo | Stars | Last push | Latest release (date) | License (SPDX per GitHub) |
|---|---|---|---|---|
| protegeproject/protege (desktop) | 1646 | 2026-10-01 | 6.0.0-alpha-1 (2026-09-28) | NOASSERTION (BSD-2 historically) |
| protegeproject/webprotege (legacy monolith) | 813 | 2026-07-28 | v4.0.2 (2020-07-31) | NOASSERTION |
| protegeproject/webprotege-gwt-ui (new UI) | 22 | 2026-10-08 | 9.0.28 (2026-10-08) | NOASSERTION |
| protegeproject/webprotege-backend-service | 29 | 2026-07-27 | 5.0.17 (2026-07-27) | NOASSERTION |
| protegeproject/webprotege-deploy | 20 | 2026-10-08 | none (compose repo) | BSD-2-Clause |
| NatLibFi/Skosmos | 268 | 2026-11-12 | v3.5 (2026-10-22) | NOASSERTION (MIT per project) |
| innoq/iqvoc | 125 | 2026-11-13 | v.4.15.1 (2026-09-04) | NOASSERTION (Apache-2.0 per project) |
| skohub-io/skohub-vocabs | 45 | 2026-10-27 | none | Apache-2.0 |
| skohub-io/skohub-editor | 5 | 2025-10-30 | none | Apache-2.0, **archived=true** |
| nfdi4cat/voc4cat-tool | 9 | 2026-11-01 | v1.2.0 (2026-09-22) | BSD-3-Clause |
| nfdi4cat/voc4cat-template | 5 | 2026-11-01 | v26.10.1 (2026-10-21) | CC0-1.0 |
| RDFLib/VocExcel | 13 | 2024-01-04 | 0.9.0 (2023-11-06) | BSD-3-Clause (dormant) |
| sparna-git/skos-play | 84 | 2026-07-24 | 0.9.1 (2022-03-18) | LGPL-3.0 |
| sparna-git/shacl-play | 57 | 2026-11-13 | 0.12.7 (2026-11-13) | LGPL-3.0 |
| kbss-cvut/termit (+ termit-ui) | 12 / 5 | 2026-11-11 | v5.2.0 (2026-11-04) | GPL-3.0 |
| tematres/TemaTres-Vocabulary-Server | 142 | 2026-11-13 | v3.6.2 (2026-10-26) | n/a on GitHub (GPL per project) |
| RDFLib/prez | 40 | 2026-10-06 | v4.25.1 (2026-10-01) | BSD-3-Clause |
| EBISPOT/ols4 | 108 | 2026-11-12 | v4.0.5 (2026-11-10) | Apache-2.0 |
| ontoportal/ontoportal_web_ui | 6 | 2026-10-27 | v3.6.1 (2026-10-27) | NOASSERTION |
| ncbo/bioportal_web_ui | 24 | 2026-11-06 | v8.19.1 (2026-11-06) | NOASSERTION |
| geneontology/noctua | 45 | 2026-11-04 | none | BSD-3-Clause |
| datahub-project/datahub | 12981 | 2026-11-13 | v1.9.0rc5 (2026-11-12) | Apache-2.0 |
| open-metadata/OpenMetadata | 15769 | 2026-11-13 | 2.1.0-rc2 (2026-11-13) | Apache-2.0 |
| apache/atlas | 2164 | 2026-11-13 | (no GH releases; ASF dist) | Apache-2.0 |
| TopQuadrant/shacl (TopBraid SHACL API, OSS) | 248 | 2026-06-30 | v1.5.0 (2026-03-23) | Apache-2.0 |
| Ontotext-AD/graphdb-workbench | 60 | 2026-11-13 | (GH releases stale: v1.3.3-TR1 2021) | not stated |
| Ontotext-AD/graphdb.js | 40 | 2026-11-09 | v4.0.0 (2025-08-20) | Apache-2.0 |
| neo4j-labs/neosemantics (n10s) | 977 | 2026-11-06 | 2025.06.1 (2026-06-16) | Apache-2.0 |
| reactodia/reactodia-workspace (Ontodia successor) | 39 | 2026-11-12 | v0.35.2 (2026-08-08) | LGPL-2.1 |
| VisualDataWeb/WebVOWL | 1032 | 2026-06-04 | v1.1.7 (2026-06-04) | MIT |
| zazuko/blueprint | 33 | 2026-07-14 | v1.0.0 (2026-06-26) | Apache-2.0 |
| INCATools/ontology-development-kit (ODK) | 394 | 2026-11-09 | v1.6.1 (2026-03-10) | BSD-3-Clause |
| ontodev/robot | 333 | 2026-11-09 | v1.9.11 (2026-10-01) | BSD-3-Clause |
| INCATools/ontology-access-kit (OAK) | 209 | 2026-11-06 | v0.7.4 (2026-08-03) | Apache-2.0 |
| monarch-initiative/ontogpt | 1099 | 2026-09-10 | v1.2.0 (2026-09-09) | BSD-3-Clause |
| monarch-initiative/curategpt | 119 | 2025-10-20 | v0.2.4 (2025-06-25) | BSD-3-Clause |
| King-s-Knowledge-Graph-Lab/OntoChat | 38 | 2026-04-22 | v1.0.0 (2024-03-27) | MIT |
| wikimedia/mediawiki-extensions-Wikibase | 145 | 2026-11-13 | (Gerrit-managed) | GPL (NOASSERTION on GH) |

All rows above come from the GitHub API on 2026-11-13, e.g. [protege](https://github.com/protegeproject/protege), [webprotege-gwt-ui](https://github.com/protegeproject/webprotege-gwt-ui), [Skosmos](https://github.com/NatLibFi/Skosmos), [iqvoc](https://github.com/innoq/iqvoc), [skohub-editor](https://github.com/skohub-io/skohub-editor), [voc4cat-tool](https://github.com/nfdi4cat/voc4cat-tool), [termit](https://github.com/kbss-cvut/termit), [OpenMetadata](https://github.com/open-metadata/OpenMetadata), [datahub](https://github.com/datahub-project/datahub), [OntoChat](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat).

**Protégé desktop**
- The Protégé 6.0.0-alpha-1 release notes (2026-09-28) say it is "intended for testing purposes" and "not compatible with plugins produced for 5.x releases" because the OWL API was upgraded to 5.5.1 (breaking change). The release also removes JAXB/CORBA and the anonymous-defined-class infrastructure — [GitHub release](https://github.com/protegeproject/protege/releases/tag/6.0.0-alpha-1)
- The stable line is 5.6.x (5.6.4 updated the OWLAPI to 4.5.29) — [protege-distribution releases](https://github.com/protegeproject/protege-distribution/releases)
- Repos in the protegeproject org pushed after 2026-09-01: protege, protege-distribution, swrlapi, owlviz, swrltab-plugin, webprotege-gwt-ui, webprotege-deploy, autoupdate (GitHub search API, 2026-11-13) — [protegeproject org](https://github.com/protegeproject)

**WebProtégé**
- The legacy `webprotege` monolith's last GitHub release is v4.0.2 (2020). Active development has moved to a microservice stack: `webprotege-gwt-ui` 9.0.28 (Oct 2026) and `webprotege-backend-service` 5.0.17 (Jul 2026), with a Docker Compose repo `webprotege-deploy` (BSD-2) — GitHub API, 2026-11-13; [webprotege-deploy](https://github.com/protegeproject/webprotege-deploy)
- webprotege-deploy README: `cp .env.example .env && docker compose up -d`. You must map `webprotege-local.edu` in your hosts file because "WebProtege uses a custom hostname for cookie handling and Keycloak authentication flows". Self-hosters set SERVER_HOST to their public hostname — [webprotege-deploy README](https://github.com/protegeproject/webprotege-deploy)
- Third-party Docker Hub images (skyplabs, openkbs) are about 7 years stale — [search summary of hub.docker.com/r/skyplabs/webprotege](https://hub.docker.com/r/skyplabs/webprotege)
- A "WebProtégé Next Generation" wiki exists on a mirror of `protegeproject/webprotege-next-gen` — [mirror wiki](https://github.hscsec.cn/protegeproject/webprotege-next-gen/wiki/WebProt%C3%A9g%C3%A9-Next-Generation-Overview/a9a126fc64a3247a176720fe7631512c2fd578fd) (mirror, not primary; that repo did not resolve under the org via the API)

**VocBench 3 / ShowVoc (Univ. Rome Tor Vergata, ART group)**
- VocBench 15.1.2 and ShowVoc 6.1.2 were announced July 2026. The intermediate 15.1.1/6.1.1 release (May 2026) was mostly cybersecurity and dependency updates — [vocbench-user Google Group](https://groups.google.com/g/vocbench-user/c/pjIfpsgPC3E)
- The VB3 scope, funded by EU ISA²: native OWL, SKOS and SKOS-XL, user management, history tracking, a validation/publication workflow — [FAO AIMS webinar page](https://www.fao.org/agrovoc/node/26)
- The EU Interoperable Europe catalogue still lists 12.0 (2023) as latest, so it is out of date — [interoperable-europe.ec.europa.eu](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/vocbench/releases)
- VocBench is not on GitHub under VocBench/ or art-uniroma2/ (both 404 on the API). Source and downloads are distributed via the uniroma2 site.

**Skosmos 3, iQvoc, SkoHub, TemaTres, TermIt, Prez, OLS4** — see the activity table above. Skosmos v3.5 (2026-10-22) is the current 3.x line. Skosmos is a read-only browser/publisher over a SPARQL endpoint, not an editor — [Skosmos repo](https://github.com/NatLibFi/Skosmos). SkoHub Editor is archived. SkoHub Vocabs (static site from Turtle in git) is still active — [skohub-vocabs](https://github.com/skohub-io/skohub-vocabs).

**Commercial suites, 2025-2026 release evidence (vendor sources)**
- TopBraid EDG: 8.0 added a built-in vector DB for alignment and entity resolution. 8.3 (Feb 2025) added "AI-agent automation" for tagging content in AEM/SharePoint. 8.4 is described as adding medical terminologies, AI business-term mapping and Neo4j integration. EDG "Copilots" handle classification and linking — [TopQuadrant EDG 8.3 news](https://topquadrant.com/?p=18684), [EDG 8.0 release](https://topquadrant.com/?p=16532), [TopBraid EDG AI-ready page](https://www.topquadrant.com/?p=19931) (vendor claims; one TopQuadrant page mixes 8.0 and 8.2 labels, so version attribution is unreliable)
- Graphwise PoolParty: 10.1 (early 2026) added an LLM "Taxonomy Builder" that generates a hierarchy skeleton from a domain description, then drafts labels/definitions with human review. It also added custom user roles. External LLM providers are pluggable (cloud, self-hosted OSS, or hybrid) — [PP 10.1 docs](https://help.graphwise.ai/pp10.1/en/graphwise-documentation/poolparty-10-1---ai-powered-taxonomy-creation.html), [LLM config docs](https://help.graphwise.ai/en/graphwise-documentation/how-to-install---manage-graphwise-components/poolparty-configuration/configuring-external-llm-services.html). 10.2 (March 2026) brought 40+ languages and auto-rebuild of the extraction model — [Graphwise news](https://graphwise.ai/news/poolparty-10-2-advances-global-semantic-reach-with-a-unified-identity/). PoolParty and GraphDB are merging into the "Graphwise Platform" — [transition guide](https://help.graphwise.ai/pp10.1/en/graphwise-documentation/graphwise-sub-components-at-a-glance/poolparty-semantic-suite-to-graphwise-platform-transition-guide.html)
- Progress Semaphore 5.10.x (2026): 5.10.1 added mapping relationships to external resources, UI-defined constraints and alternative LLM providers in the "AI Model Builder". 5.10.2 (blog 2026-01-16) added skos:Collection. 5.10.4 standardized Docker images for all components and added backend paging in the Tree/Visualizer. 5.10.5 is an "innovation release" — [5.10.2 blog](https://www.progress.com/blogs/making-meaning-more-actionable-whats-new-in-progress-semaphore-5.10.2), [5.10.4 notes](https://docs.progress.com/bundle/semaphore-5-what-is-new/page/topics/release-notes-5/semaphore_5104.html), [5.10.5 notes](https://docs.progress.com/bundle/semaphore-5-what-is-new/page/topics/release-notes-5/semaphore_5105.html), [EAIW news on 5.10 "AI-assisted quality-oriented modeling"](https://www.enterpriseaiworld.com/Articles/News/News/Progress-Semaphore-5.10-Delivers-AI-Assisted-Quality-Oriented-Knowledge-Modeling-165603.aspx)
- metaphactory: 5.8 added an "AI modeling agent", a Vocabulary Mapping Editor and "improvements to the ontology review process". 6.0 (GA 2026-07-14) embeds the "metis" assistant in the real-time collaborative ontology editor. The agent is said to use OWL and SHACL with built-in validation — [metaphactory 5.8](https://metaphacts.com/metaphactory-5-8), [metaphactory 6.0](https://metaphacts.com/metaphactory-6-0), [AI modeling agent](https://metaphacts.com/ai-modeling-agent) (vendor claims; no independent evaluation found)
- Stardog: Voicebox release notes list 1.2.0 on 2026-10-22. Third-party Atlan reports Stardog Platform 12.1.4 on 2026-09-03 (not verified on stardog.com). The Free plan covers 1M edges and 3 databases on shared cloud. Voicebox needs a license that allows it, and free-tier users report not seeing Voicebox in Designer — [Voicebox release notes](https://docs.stardog.com/release-notes/stardog-voicebox), [Voicebox dev guide](https://docs.stardog.com/voicebox/voicebox-dev-guide/), [community thread](https://community.stardog.com/t/dont-see-voice-box-option-in-stardog-designer/4753), [Atlan article (third party, competitor)](https://atlan.com/know/ai-agent/knowledge-graph/what-is-stardog/)
- GraphDB (Graphwise): "From GraphDB 11 onwards, all editions (including GraphDB Free) require a license" (register on the website). The Workbench is included in Free with a single-core license. "Talk to Your Graph" is no-code RAG chat in the Workbench — [rdflib GraphDB docs](https://rdflib.readthedocs.io/en/latest/graphdb/), [Graphwise GraphDB page](https://graphwise.ai/?p=166320). The claims that Free is capped at 5 repos and bars for-profit service use come only from a secondary blog — [beri.net](https://www.beri.net/article/oakley-capital-graphwise-acquisition-graphdb-license-not-open-source) (unverified against the license text)

**Legacy/stagnant desktop editors**
- Fluent Editor (Cognitum, controlled-natural-language OWL editor): a May 2025 community post says it still has daily downloads and CogniPy commercial users, and the team is seeking funding for a new version, possibly open source — [fluenteditor Google Group](https://groups.google.com/g/fluenteditor/c/TDgfpgEfF5A). The last formal release announcement found was 2014-15 — [W3C list](https://lists.w3.org/Archives/Public/semantic-web/2015Mar/0155.html)
- OntoStudio (semafora, ex-Ontoprise): semafora pages refer to "legacy OntoStudio" and uninstall instructions. There is no explicit discontinuation notice — [semafora](https://semafora-systems.com/?p=113), [OntoBroker help](https://semafora-systems.com/ontobroker-help)

### Inferences
- "Maintained in 2026" for OSS: Protégé, WebProtégé (new stack), VocBench, Skosmos, iQvoc, TermIt, TemaTres, OLS4, Prez, voc4cat, SHACL Play, ODK/ROBOT/OAK, DataHub/OpenMetadata/Atlas. Dormant or dead: VocExcel (replaced by voc4cat), SkoHub Editor (archived), SKOS Play (no release since 2022, though there are commits in 2026), OntoChat (single 2024 release, research prototype), Fluent Editor, OntoStudio.
- Protégé 6 breaks 5.x plugins. If we built a Protégé plugin now, we would be targeting a moving API. Avoid desktop plugin investment for an experimental project.
- WebProtégé is mid-migration to microservices + Keycloak, so self-hosting is heavier (many containers) than the old single WAR + MongoDB.

### Gaps
- No official VocBench 3 source repo was located via GitHub. The exact date of 15.1.2 and its license (historically BSD-3) were not re-confirmed on the official site this session.
- No public 2026 pricing for TopBraid EDG, PoolParty, Semaphore, metaphactory, Collibra or Atlan. All are quote-based (no price lists found).
- WebProtégé public API documentation for the new microservice stack was not found (see Q2).

---

## Q2. Capabilities per tool: standards, collaboration/review workflow, versioning/git, visualization, API/extensibility, AI, licensing, deployment

### Takeaway
No single reusable tool covers the whole Reviewer use case: AI-proposed terms, concepts, relations and quality issues, triaged by a human with diagrams, round-tripped to git-stored OWL/SKOS/SHACL. VocBench 3 comes closest among the OSS options on governance: a SKOS/OWL/SKOS-XL editor with roles, history, and a validation/publication workflow where changes require approval. TermIt is the closest on "terms extracted from documents", and OpenMetadata is closest on a glossary approval workflow with a modern API. The commercial suites (EDG, PoolParty, metaphactory) have the richest review-plus-AI workflows but are closed and expensive.

### Cited Findings (compact matrix; detail bullets follow)

| Tool | Primary purpose | Standards I/O | Collab / review-approval | Versioning / git | Visualization | API / extensibility | AI | License / cost | Deploy |
|---|---|---|---|---|---|---|---|---|---|
| Protégé desktop 5.6 / 6.0α | OWL ontology | OWL/RDF all OWLAPI syntaxes | single user; no review flow | file-based; git via external tooling | OWLViz, OntoGraf plugins | Java OSGi plugins (5.x plugins break in 6.0) | none built in | BSD-2 (free) | desktop |
| WebProtégé (new stack) | collaborative OWL | OWL, RDF/XML, Turtle, OBO import/export | multi-user, comments/discussions, sharing perms, change history, forms | internal revision history; no native git | class hierarchy, limited graph | internal REST/GraphQL-ish services; no stable public API documented | none | BSD-2 (deploy repo); free | Docker Compose + Keycloak + MongoDB |
| VocBench 3 (15.x) + ShowVoc | SKOS/SKOS-XL thesauri + OWL + OntoLex | RDF all syntaxes, SKOS, SKOS-XL, OWL, OntoLex; SPARQL; SHACL validation | role-based users; history + **validation workflow** (changes pending until validator accepts); publication via ShowVoc | history in triple store; no native git | graph view, tree | Semantic Turkey REST services, extension points, custom forms | none core | BSD-3 (free) | Java (Karaf) + RDF4J/GraphDB backend |
| TopBraid EDG 8.x | enterprise ontologies, taxonomies, glossaries, data catalog | OWL, SKOS, SHACL-native, RDF; GraphQL | **workflows/working copies with review & approval**, roles, comments | asset collections w/ versions; Git integration documented | diagrams, graph views | SHACL-based extensibility, GraphQL/REST, TopBraid SHACL API OSS (Apache-2) | Copilots, vector DB, AI tagging (vendor) | commercial, quote | on-prem / cloud |
| Graphwise PoolParty 10.x | SKOS taxonomy/thesaurus + ontology + extraction | SKOS, SKOS-XL, OWL, RDF; SPARQL | roles, custom roles (10.1), approval workflows, history | versioning/snapshots | visual browser | full REST API, Extractor API | LLM Taxonomy Builder, extraction | commercial, quote | SaaS / on-prem |
| Progress Semaphore 5.10 | taxonomy/ontology + classification | SKOS, OWL, RDF | model management, task/review features | change history | Visualizer view | APIs; Docker images (5.10.4) | AI Model Builder w/ pluggable LLMs | commercial, quote | on-prem docker / cloud |
| metaphactory 5.8/6.0 | ontology/vocab modeling + KG apps | OWL, SHACL, SKOS, RDF | collaborative editor, ontology review process | ontology versions; Git-based ontology mgmt documented | visual ontology diagrams (Ontodia/Reactodia lineage) | low-code app templates, REST | metis AI modeling agent (6.0) | commercial | docker / cloud |
| Stardog Designer + Voicebox | KG modeling + virtualization + NL Q&A | OWL/RDFS models, SHACL, R2RML/SMS mappings | project sharing | DB versioning | Designer visual modeling | HTTP/SPARQL/GraphQL APIs | Voicebox NL modeling and Q&A | free tier (1M edges, 3 DBs); enterprise quote | cloud / self-host |
| GraphDB Workbench 11 | RDF store UI | all RDF; SHACL; SPARQL | users/roles; no editorial review | none (store) | Visual graph | RDF4J REST, graphdb.js | Talk to Your Graph (RAG chat) | Free requires license (v11) | docker |
| iQvoc 4.15 | SKOS thesaurus editor | SKOS(-XL), RDF export, import | **draft → published versioning** (edit copies, publish) | in-DB concept versions | tree, minimal | Rails engine (extensible), Linked Data endpoints | none | Apache-2.0 | Ruby/Rails + SQL |
| Skosmos 3.5 | SKOS **browser/publisher** (read-only) | SKOS via SPARQL | none (read-only) | none | hierarchy, (3.x) improved UI | REST API | none | MIT | PHP + Fuseki |
| SkoHub Vocabs / Editor | static SKOS publishing from git / JSON-schema form editor | SKOS Turtle | via git PRs | **git-native** (Turtle in repo, CI builds site) | tree | GitHub/GitLab webhook | none | Apache-2.0; Editor archived | static site / docker |
| voc4cat (+ template) | SKOS via Excel + git | SKOS Turtle ⇄ xlsx | **GitHub issues/PR review** | git-native, CI validation, releases | HTML via pyLODE/Prez-like docs | Python CLI | none | BSD-3 / CC0 | GitHub Actions |
| SKOS Play / SHACL Play | SKOS & SHACL visualization/docs generation | SKOS, SHACL, xlsx→RDF | none | none | trees, sunburst, alphabetical PDFs; SHACL docs/diagrams | web + CLI | none | LGPL-3.0 | Java webapp / docker |
| TermIt 5.2 | SKOS term vocabularies + **term extraction from documents** | SKOS, Turtle, Excel import/export | multi-user, comments, change history, term "states" (draft/confirmed) | change records in store | term relation graph | REST API (Spring), Keycloak | annotation/term occurrence suggestions via text analysis service | GPL-3.0 | docker (GraphDB backend) |
| TemaTres 3.6 | thesaurus server (ISO 25964) | SKOS-Core, Zthes, TBX, MARC, JSON | users, candidate/accepted/rejected term status | none | basic | REST-like web services | none | GPL | PHP/MySQL |
| OLS4 / OntoPortal | ontology lookup/repository (read-mostly) | OWL/OBO/SKOS | OntoPortal: notes, mapping proposals | none | tree, graph | REST APIs | OLS4 embeddings search (docs) | Apache-2 / BSD | docker |
| DataHub 1.9 | data catalog business glossary | own model; CSV/YAML ingestion | **glossary term proposals/approval** (proposal workflow; more in Acryl cloud) | GitOps via YAML glossary ingestion | lineage graph | GraphQL + REST + Python SDK | AI docs in cloud | Apache-2.0 / Acryl SaaS | docker/k8s |
| OpenMetadata 2.1 | data catalog business glossary | CSV import/export; JSON schema | **reviewers → draft → approve/reject tasks** | entity version history | relations graph | REST API + Python SDK | Collate AI (commercial) | Apache-2.0 / Collate SaaS | docker/k8s |
| Apache Atlas | Hadoop metadata catalog glossary | own typesystem | categories/terms; no rich review | none | lineage | REST API | none | Apache-2.0 | heavy (HBase/Solr/Kafka) |
| Collibra / Atlan | enterprise data-governance glossary | proprietary; CSV, some RDF/SKOS import connectors | configurable approval workflows (Collibra BPMN) | audit history | lineage/relations graphs | REST/GraphQL APIs | AI copilots (vendor) | commercial | SaaS |
| Neo4j + neosemantics (n10s) | LPG KG; RDF/SKOS import/export | RDF, OWL, SKOS import/export, SHACL validation | none (DB) | none | Bloom/Browser | Cypher, plugins | Neo4j LLM KG builder (separate) | Apache-2.0 (n10s); Neo4j CE GPLv3 | docker |
| OntoChat / OntoGPT / CurateGPT | LLM ontology engineering (CQs, extraction, curation) | OWL/LinkML outputs | OntoChat: chat-guided; CurateGPT: curate & suggest | n/a | none | Python | core purpose | MIT / BSD-3 | Python / HF Space |

**Detail and evidence notes**
- OpenMetadata glossary approval: when a glossary has reviewers, a new term starts as a **draft** and creates an approval task. Only the reviewers can approve or reject it. With no reviewers, terms are auto-approved. Owner and Reviewers are inherited by terms. From 2.0.6, approval by an authorized admin or owner updates the term. CSV bulk import offers a preview and supports parent (dot notation), synonyms, related terms, tags and references. Glossaries and terms are CRUD via the API, with FQN `glossary.parent.child` — [OM approval docs](https://docs.open-metadata.org/v2.1.x-SNAPSHOT/how-to-guides/data-governance/glossary/approval), [OM import docs](https://docs.open-metadata.org/latest/how-to-guides/data-governance/glossary/import), [OM glossary docs](https://docs.open-metadata.org/latest/how-to-guides/data-governance/glossary). Gap: the docs don't state whether CSV/API-created terms enter the approval workflow.
- PoolParty 10.1 Taxonomy Builder: "human review built in". An active LLM config is required for all Taxonomy Builder features — [PP 10.1 docs](https://help.graphwise.ai/en/graphwise-documentation/poolparty-10-1---ai-powered-taxonomy-creation.html), [Graphwise blog](https://graphwise.ai/blog/poolparty-10-1-ai-assisted-taxonomy-building-for-the-graphwise-era/)
- metaphactory AI modeling: "quality checks, suggestions for improvements", OWL+SHACL validation, persistent workspace — [AI-assisted modeling page](https://metaphacts.com/solutions/semantic-knowledge-modeling/ai-assisted-modeling) (vendor marketing)
- Stardog Voicebox: "helps our users in creating models and mappings", built around Designer models, but you can bring your own. Atlan notes Stardog's "hallucination-free" marketing versus its docs saying an agent's output "may contain Hallucinations" — [Stardog blog](https://www.stardog.com/blog/stardog-voicebox-makes-building-data-models-dead-simple/), [Atlan](https://atlan.com/know/ai-agent/knowledge-graph/what-is-stardog/) (Atlan is a competitor)
- VocBench validation/publication workflow, history and user management are part of the VB3 design — [FAO AIMS](https://www.fao.org/agrovoc/node/26)
- LLM-assisted ontology engineering, research state: OntoChat covers user stories, competency-question extraction and filtering, and ontology testing support (MIT; demo on HF Spaces) — [OntoChat arXiv 2403.05921](https://arxiv.org/abs/2403.05921v1), [repo](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat). OntoLearner (2026 preprint) is a modular Python library for benchmarking LLM ontology learning, not an editor — [arXiv 2607.01977](https://arxiv.org/pdf/2607.01977). A 2026 workshop paper describes an LLM → symbolic validators → corrective-prompt loop — [CEUR Vol-4246](https://ceur-ws.org/Vol-4246/llms4kgoe-6.pdf)
- WebVOWL (MIT, release Jun 2026) and Reactodia (LGPL-2.1, active, Ontodia successor) are embeddable OSS ontology/graph visualization components — GitHub API ([WebVOWL](https://github.com/VisualDataWeb/WebVOWL), [reactodia](https://github.com/reactodia/reactodia-workspace)). Zazuko Blueprint (Apache-2.0, v1.0.0 Jun 2026) is an OSS KG explorer UI — [blueprint](https://github.com/zazuko/blueprint)
- TopBraid's open-source piece is the TopBraid SHACL API (Apache-2.0, v1.5.0 Mar 2026). EDG itself is closed — [TopQuadrant/shacl](https://github.com/TopQuadrant/shacl)

### Inferences
- **Review/approval semantics map well onto three OSS designs:** (a) VocBench "validation" (each change is pending until a validator accepts it), the closest to change-level review of AI proposals; (b) OpenMetadata/TemaTres/TermIt term **status** (draft/candidate → approved/rejected), concept-level review; (c) voc4cat/SkoHub **git PR** review, file-level review that already matches our git-as-source-of-truth model.
- **None of the OSS editors understands "AI proposal + evidence span from a manual + confidence + quality issue" as first-class objects.** TermIt (term occurrences in documents) is the only OSS one with document-grounded terms.
- The data-catalog glossaries (DataHub/OpenMetadata/Atlas/Collibra/Atlan) are not SKOS/OWL-native. Round-tripping to SKOS would need a custom mapper, and their "relations" are limited (related, synonym, isA/hasA in Atlas), so they can't hold arbitrary OWL properties or SHACL. They are good glossary approval UIs but poor ontology stores.
- Commercial EDG/PoolParty/metaphactory functionally cover "Reviewer + AI proposals + diagrams", but they are not embeddable in a monorepo, need license negotiation, and the git integration is secondary. Overkill for an experiment, though worth mining for UX patterns.

### Gaps
- I did not verify in 2026 docs that TopBraid EDG has native Git integration, how its workflow states work, or metaphactory's Git-based ontology management. These come from prior knowledge of their docs, not this session's sources.
- DataHub glossary proposal workflow: OSS vs Acryl Cloud feature split not re-verified this session.
- No 2026 independent (non-vendor) comparison paper of these editors was found. The W3C "Ontology editors" wiki list is a dated index — [W3C wiki](https://www.w3.org/wiki/Ontology_editors).
- Collibra/Atlan: no 2026 primary-source review of SKOS import/export or of API access for glossary workflows was done.

---

## Q3. Fit for our apps: reuse vs build (Reviewer, Downloader, Assistant)

### Takeaway
Don't adopt a full platform as "the Reviewer". Build a thin custom Reviewer UI whose queue models AI proposals and quality issues as reviewable items, and reuse OSS parts: git/PR-based acceptance (voc4cat/SkoHub pattern), SHACL validation, Skosmos or SkoHub Vocabs for publishing/browsing, Reactodia or WebVOWL for diagrams, and optionally VocBench 3 or WebProtégé as a power-user editor next to it. If the project wants a turnkey glossary-approval UI, OpenMetadata is the most API-friendly OSS option, but it costs us OWL/SKOS fidelity.

### Cited Findings
- voc4cat-tool (BSD-3, v1.2.0 Sep 2026) and voc4cat-template (v26.10.1 Oct 2026) are actively maintained. They implement git-native SKOS with review via GitHub PRs — [voc4cat-tool](https://github.com/nfdi4cat/voc4cat-tool), [voc4cat-template](https://github.com/nfdi4cat/voc4cat-template)
- The WebProtégé self-host stack needs Docker Compose with Keycloak and a custom hostname — [webprotege-deploy](https://github.com/protegeproject/webprotege-deploy)
- TermIt (GPL-3.0) is actively released (5.2.0, 2026-11-04) — [termit](https://github.com/kbss-cvut/termit)
- OpenMetadata has a draft→approve reviewer workflow plus REST/CSV — [OM approval](https://docs.open-metadata.org/v2.1.x-SNAPSHOT/how-to-guides/data-governance/glossary/approval)
- Skosmos v3.5 (Oct 2026) is a read-only browser over SPARQL — [Skosmos](https://github.com/NatLibFi/Skosmos)
- GraphDB 11 Free now requires a registered license — [rdflib docs](https://rdflib.readthedocs.io/en/latest/graphdb/)

### Inferences (per-app fit, ranked)

**Reviewer (HITL governance of AI proposals, diagrams):**
1. **Build custom; borrow components.** The review unit is "proposal + evidence + issue", which no editor models. Reusable pieces: Reactodia (LGPL, React, RDF-aware diagram workspace; active) or WebVOWL (MIT) for diagrams; pySHACL/SHACL Play for validation and SHACL docs; a git PR as the final approval gate (voc4cat pattern).
2. **VocBench 3** is the best OSS candidate if a full collaborative editor with change-level validation is required. It is SKOS-XL/OWL-native and BSD-licensed, and its Semantic Turkey REST services could take AI proposals as pending changes. Downsides: a heavy Java stack, the triple store (not git) is the source of truth, it doesn't sit comfortably as a monorepo module, and it has no AI features. Possible use: export→git sync job.
3. **TermIt** is the best conceptual match for "terms from user manuals" (document annotation → term confirmation). GPL-3.0 matters if we embed or modify it, and it needs a GraphDB backend, which now requires a license since v11, though TermIt can likely use other RDF4J stores (unverified).
4. **WebProtégé** is good for OWL class editing with comments, but it has no approval workflow, no documented public API in the new stack and no git. As the Reviewer it is a weak fit, though it is OK as an expert side-editor.
5. **OpenMetadata/DataHub glossary**: a quick win if "glossary-only" review is acceptable (Apache-2, REST, draft/approve). It fits poorly for relations, higher-level concepts, OWL and SHACL.
6. **Commercial (EDG, PoolParty, metaphactory, Semaphore)**: functionally strongest, including LLM-assisted proposals with human review, but closed source, quote pricing and lock-in. Use them as UX benchmarks or for a vendor-trial comparison, not as a dependency of an experimental monorepo.

**Downloader (extraction of candidates):** editors don't help here. The relevant reuse is OntoGPT (BSD-3, v1.2.0 Sep 2026; LLM extraction to LinkML schemas), CurateGPT (slowing; last release Jun 2025), OAK (ontology access/lexical matching), and the PoolParty/Semaphore extractors if a commercial route were ever chosen. TermIt's text-analysis service is another document→term option.

**Assistant (Q&A over manuals + KG):** reuse a store and browse layer, not an editor. Options: Skosmos 3 or SkoHub Vocabs to publish curated vocabularies with stable URIs; OLS4 (Apache-2, active) for ontology lookup/search APIs; GraphDB "Talk to Your Graph" or Stardog Voicebox only as commercial references; QLever (Apache-2, active) or Fuseki as an OSS SPARQL backend; neosemantics if a Neo4j path is wanted (SKOS/OWL import, Apache-2).

**Avoid / not recommended:** VocExcel (dormant since 2023, superseded by voc4cat), SkoHub Editor (archived), OntoStudio (legacy), Fluent Editor (no release in about 10 years), OntoChat as a product (2024 research prototype; reuse its competency-question prompting ideas only), Apache Atlas (Hadoop-heavy, glossary-weak), Protégé desktop plugins (6.0 breaks the plugin API).

### Gaps
- No hands-on test of VocBench's REST API for programmatically injecting "pending validation" changes. Feasibility comes from its architecture description, not a verified example.
- TermIt with a non-GraphDB triple store, and whether the TermIt text-analysis service handles English manuals well: not verified.
- Whether WebProtégé's new microservices expose a stable, documented external API: not found.
