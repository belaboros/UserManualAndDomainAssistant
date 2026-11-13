# Reusable libraries and frameworks for ontologies, taxonomies, glossaries and knowledge graphs (status as of 13 Nov 2026)

Method note: release versions, dates, licences and activity were checked directly against the PyPI JSON API, the npm registry, Maven Central `maven-metadata.xml`, and the GitHub REST API (repo `pushed_at`, latest release, stars, SPDX licence) on 2026-11-13. "Pushed" means the date of the last push to the default branch or any branch. Where GitHub reports `NOASSERTION`, the licence comes from the package registry or the licence file. Source URLs follow the pattern `https://pypi.org/project/<name>/`, `https://www.npmjs.com/package/<name>`, `https://github.com/<owner>/<repo>`.

## Q1. Core RDF/OWL/SHACL libraries (Python, JVM, JS/TS, Rust): which to use, and are they maintained and licence-safe?

### Takeaway
Python is well covered and actively maintained, and every package below is permissively licensed except owlready2 and py-horned-owl, which are LGPL. The core is **rdflib 7.6 + pyoxigraph 0.5.13 + pySHACL 0.40.2 + LinkML 1.12 + OAK 0.7.4**, with owlready2 or py-horned-owl when OWL-level editing or reasoning is needed. For the TypeScript Reviewer the core is **N3.js + @zazuko/env/rdf-ext + shacl-engine + Comunica + jsonld.js** (all MIT/BSD, all released in 2025-2026), or **oxigraph (WASM npm)** as an in-browser store. On the JVM, **Jena 6.2 / RDF4J 6.0 / ROBOT 1.9.11** are active. The OWL reasoner layer (OWL API 5.5.1 from 2024, ELK 0.6.0 from 2024, HermiT from 2020, Openllet from 2019) is stable but rarely released, so treat it as a frozen dependency used through ROBOT, OAK or owlready2.

### Cited Findings
**Python**
- rdflib 7.6.0, released 2026-02-13, BSD-3-Clause. Repo pushed 2026-11-11, about 2.5k stars. Parsers and serializers for Turtle, TriG, N-Quads, JSON-LD and RDF/XML, a SPARQL 1.1 engine, and `Dataset`/`ConjunctiveGraph` for named graphs. — [PyPI](https://pypi.org/project/rdflib/); [GitHub](https://github.com/RDFLib/rdflib)
- pyoxigraph 0.5.13, released 2026-10-22, MIT OR Apache-2.0. Python bindings to the Rust Oxigraph store: an in-memory or RocksDB quad store with SPARQL 1.1. — [PyPI](https://pypi.org/project/pyoxigraph/); [GitHub](https://github.com/oxigraph/oxigraph)
- pySHACL 0.40.2, released 2026-10-28, Apache-2.0. It is the SHACL validator in the RDFLib ecosystem. — [PyPI](https://pypi.org/project/pyshacl/); [GitHub](https://github.com/RDFLib/pySHACL)
- owlready2 0.51, released 2026-06-22, **LGPL-3.0-or-later**. It provides OWL 2 object-oriented access, a SQLite quadstore, and bundled HermiT/Pellet reasoners (these need Java). — [PyPI](https://pypi.org/project/owlready2/)
- oaklib (Ontology Access Kit) 0.7.4, released 2026-08-03, Apache-2.0. Repo pushed 2026-11-06. It gives one API and CLI over local OWL/OBO files, SQLite semsql, OLS, BioPortal and Ubergraph, covering search, lexical matching, diffs, KGCL change application and validation. — [PyPI](https://pypi.org/project/oaklib/); [GitHub](https://github.com/INCATools/ontology-access-kit)
- LinkML 1.12.1, released 2026-10-13, Apache-2.0. linkml-runtime 1.12.1 is CC0-1.0. Generators target OWL, SHACL, ShEx, JSON Schema, Pydantic, SQL DDL, JSON-LD contexts and TypeScript. — [PyPI linkml](https://pypi.org/project/linkml/); [PyPI linkml-runtime](https://pypi.org/project/linkml-runtime/); [GitHub](https://github.com/linkml/linkml)
- funowl 0.2.3 was last released on **2023-08-08** (CC0). It is a functional-syntax OWL model and is effectively dormant. — [PyPI](https://pypi.org/project/funowl/)
- py-horned-owl 2.0.0, released 2026-09-23, **LGPL-3.0-or-later**. It provides fast OWL 2 parsing and serialization in Python on top of Rust horned-owl, which released v4.0.0 on 2026-09-17 (LGPL-3.0). — [PyPI](https://pypi.org/project/py-horned-owl/); [GitHub horned-owl](https://github.com/phillord/horned-owl)
- kglab 1.0.1, released 2026-01-23, MIT. Repo pushed 2026-01-25. It is a thin integration layer (rdflib, pySHACL, NetworkX, pandas) with low activity. — [PyPI](https://pypi.org/project/kglab/); [GitHub](https://github.com/DerwenAI/kglab)
- SPARQLWrapper 2.0.0 was last released 2022-03-13 under the W3C licence. It still works as an HTTP SPARQL client but is not actively released. — [PyPI](https://pypi.org/project/sparqlwrapper/)
- morph-kgc 2.10.0, released 2026-01-20, Apache-2.0. It is an RML/R2RML engine for mapping tables or JSON into RDF. — [PyPI](https://pypi.org/project/morph-kgc/)

**JVM**
- Apache Jena (including Fuseki) 6.2.0 is the Maven Central release with `lastUpdated` 2026-07-31; the version sequence is 5.5.0 → 5.6.0 → 6.0.0 → 6.1.0 → 6.2.0. Apache-2.0. Repo pushed 2026-11-12. — [Maven Central jena-core](https://repo1.maven.org/maven2/org/apache/jena/jena-core/maven-metadata.xml); [GitHub](https://github.com/apache/jena)
- Eclipse RDF4J 6.0.0 was released 2026-08-10, and 6.2.0-M2 was on Maven on 2026-11-02. The licence is BSD-3-Clause (EDL). Repo pushed 2026-11-13. — [GitHub](https://github.com/eclipse-rdf4j/rdf4j); [Maven Central](https://repo1.maven.org/maven2/org/eclipse/rdf4j/rdf4j-model/maven-metadata.xml)
- OWL API: the latest release is 5.5.1 (Maven `lastUpdated` 2024-09-07), but the repo is still pushed (2026-11-02). Licence is LGPL-3 or Apache-2.0 dual licensing (GitHub reports no SPDX ID). — [Maven Central](https://repo1.maven.org/maven2/net/sourceforge/owlapi/owlapi-distribution/maven-metadata.xml); [GitHub](https://github.com/owlcs/owlapi)
- ROBOT 1.9.11 was released 2026-10-01, BSD-3-Clause. Commands include merge, reason, report (QC), template (spreadsheet to OWL), diff, convert and verify (SPARQL checks). — [GitHub](https://github.com/ontodev/robot)
- ELK reasoner (OWL 2 EL): v0.6.0 was released 2024-05-25 as `io.github.liveontologies:elk-owlapi`, Apache-2.0, repo pushed 2026-06-13. HermiT's Maven artifact is `1.4.5.519` from 2020-02-18. Openllet's last release is 2.6.5 from 2019-09-27, with the repo pushed 2025-08-04 (GitHub reports NOASSERTION; the Pellet lineage is AGPL, so verify before use). — [GitHub ELK](https://github.com/liveontologies/elk-reasoner); [Maven HermiT](https://repo1.maven.org/maven2/net/sourceforge/owlapi/org.semanticweb.hermit/maven-metadata.xml); [GitHub Openllet](https://github.com/Galigator/openllet)

**JS/TS**
- N3.js 2.13.12, released 2026-10-10, MIT. Fast Turtle/TriG/N-Triples/N3 parser, writer and in-memory store, RDF/JS compliant. — [npm](https://www.npmjs.com/package/n3); [GitHub](https://github.com/rdfjs/N3.js)
- rdf-ext 2.6.0 was released 2025-08-31. @zazuko/env 3.0.6 was released 2026-11-09 and bundles an RDF/JS environment with clownface. sparql-http-client 3.1.0 was released 2025-11-11. All three are MIT. — [npm rdf-ext](https://www.npmjs.com/package/rdf-ext); [npm @zazuko/env](https://www.npmjs.com/package/@zazuko/env); [npm sparql-http-client](https://www.npmjs.com/package/sparql-http-client)
- shacl-engine 1.1.3 was released 2026-10-11 under MIT and is the newer, faster SHACL engine from rdf-ext. rdf-validate-shacl 0.6.5 was released 2025-05-30 under MIT, with the repo pushed 2026-04-02. — [npm shacl-engine](https://www.npmjs.com/package/shacl-engine); [npm rdf-validate-shacl](https://www.npmjs.com/package/rdf-validate-shacl)
- Comunica (`@comunica/query-sparql`) 5.4.1 was released 2026-09-14 under MIT. It is a modular SPARQL 1.1 engine with link traversal and federation over SPARQL endpoints, files and TPF. — [npm](https://www.npmjs.com/package/@comunica/query-sparql); [GitHub](https://github.com/comunica/comunica)
- jsonld.js 9.0.0 was released 2025-11-21 under BSD-3-Clause and implements JSON-LD 1.1 expand, compact, frame and toRDF. — [npm](https://www.npmjs.com/package/jsonld)
- rdflib.js 2.4.1 was released 2026-09-18 under MIT. It is from the SolidOS lineage and includes a store, fetcher and update manager. — [npm](https://www.npmjs.com/package/rdflib)
- LDkit 2.10.1 was released 2026-10-13 under MIT. It is a typed TypeScript Linked Data ORM over SPARQL (schema to TS types, Comunica underneath). Small project (83 stars). — [npm](https://www.npmjs.com/package/ldkit); [GitHub](https://github.com/karelklima/ldkit)
- oxigraph npm (WASM) 0.5.13 was released 2026-10-22 under MIT/Apache-2.0. — [npm](https://www.npmjs.com/package/oxigraph)

**Rust**
- Oxigraph v0.5.13 was released 2026-10-22 under Apache-2.0/MIT, with about 2k stars and the repo pushed 2026-11-12. Its README states it is "nearly fully conformant with the latest recommendations (1.1 for RDF, SPARQL and JSON-LD) with preliminary support for 1.2 RDF and SPARQL drafts", and that it implements the SPARQL 1.1 Protocol and Graph Store Protocol. — [GitHub](https://github.com/oxigraph/oxigraph)

### Inferences
- **Downloader (Python):** use rdflib for building and serializing (TTL/JSON-LD/TriG); pyoxigraph for a local quad store and fast SPARQL; pySHACL for quality-issue detection (SHACL shapes = machine-checkable quality rules); LinkML as the single schema source for the extraction target, generating Pydantic for LLM structured output plus SHACL/OWL/JSON-LD; and OAK for lexical matching and lookups against external ontologies.
- **Assistant (Python):** pyoxigraph or a remote SPARQL endpoint for KG retrieval; rdflib for small curated graphs. Use owlready2 only if OWL reasoning is needed at runtime, and remember it is LGPL and its reasoners need Java.
- **Reviewer (TS):** N3.js + @zazuko/env + shacl-engine gives client-side validation previews, jsonld.js handles the JSON-LD API payloads, and LDkit or sparql-http-client provides typed access. If the Python backend does validation, it should use pySHACL so the two sides do not diverge.
- **CI/QC:** run ROBOT (JVM) for OWL reasoning (ELK) and `robot report` against the git-curated ontology. This avoids embedding the JVM reasoner stack in the apps.
- Avoid building on funowl, kgcl-rdflib or SPARQLWrapper as long-term dependencies (2022-2023 releases).

### Gaps
- Jena 6.x minimum Java version and exact SPARQL 1.2 / RDF 1.2 (triple terms) feature coverage in Jena 6 and RDF4J 6 were not checked.
- The OWL API licence comes from the project's historical dual licensing; GitHub reports no SPDX ID.
- The owlready2 source repository moved to Bitbucket/its own site; commit activity there was not checked.

## Q2. Triple stores and graph DBs: named graphs, SPARQL 1.1/1.2, licence

### Takeaway
For an experimental monorepo with named graphs, **Oxigraph** (embedded, or as a server via the CLI) is the lightest fully open option. **Apache Jena Fuseki (TDB2)** is the most standards-complete OSS server, with SHACL, inference and text search. **QLever** (Apache-2.0) fits very large read-heavy graphs. Virtuoso OSS is GPLv2. GraphDB Free and Stardog Free are proprietary with use restrictions. RDF 1.2 / SPARQL 1.2 are **not yet Recommendations**: the SPARQL 1.2 Query document is still a Working Draft dated 12 Nov 2026, so do not depend on 1.2 features (triple terms/reification) beyond Oxigraph's and Jena's preliminary support.

### Cited Findings
- Oxigraph server/CLI implements the SPARQL 1.1 Protocol and Graph Store Protocol with named-graph quads, and has preliminary support for the RDF/SPARQL 1.2 drafts. v0.5.13 was released 2026-10-22. — [GitHub](https://github.com/oxigraph/oxigraph)
- Apache Jena Fuseki ships with Jena 6.2.0 (Maven `jena-fuseki-server` 6.2.0, 2026-07-31) under Apache-2.0. — [Maven Central](https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-server/maven-metadata.xml)
- QLever v0.6.0 was released 2026-08-13 under Apache-2.0, with the repo pushed 2026-11-13. It offers official packages for Debian/Ubuntu/macOS, and recent work covers a geo index, materialized views and a query cache. — [GitHub release](https://github.com/ad-freiburg/qlever/releases)
- Virtuoso Open-Source v7.2.17 was released 2026-05-07. It is licensed under **GNU GPL version 2 only**, per the LICENSE file. — [GitHub](https://github.com/openlink/virtuoso-opensource); [LICENSE](https://github.com/openlink/virtuoso-opensource/blob/develop/7/LICENSE)
- GraphDB (Graphwise, formerly Ontotext): 11.5.0 was released 19 Aug 2026, and the Free edition requires a licence file requested by email. One secondary source says Free is for non-commercial use, capped at 5 repositories, with enterprise authentication removed in 11.0; this was **not confirmed** from official docs. — [GraphDB 11.5.0 release notes](https://help.graphwise.ai/en/graphdb/graphdb-release-notes/graphdb-11-5-0-release-notes.html); [GraphDB licence setup](https://graphdb.ontotext.com/documentation/11.2/set-up-your-license.html); [Beri article (secondary)](https://www.beri.net/article/oakley-capital-graphwise-acquisition-graphdb-license-not-open-source)
- Stardog: Stardog Free is a renewable 1-year licence. Stardog Cloud Free is shared hosting with up to 1M edges, community support only. Community forum answers conflict on whether on-prem free licences are still issued. — [Stardog pricing](https://stardog.com/pricing); [Stardog download](https://www.stardog.com/download/); [Community thread](https://community.stardog.com/t/how-can-one-obtain-the-license-for-the-free-version/5373)
- Neo4j + neosemantics (n10s): the latest release is 2025.06.1 (published 2026-06-16, notes: "Bugfix release for Jackson CVE"), Apache-2.0, repo pushed 2026-11-06. It imports and exports RDF/OWL/SKOS into the property graph and supports SHACL-based validation; it is a Neo4j Labs project, so it has no official support. — [GitHub](https://github.com/neo4j-labs/neosemantics)
- Amazon Neptune Database supports RDF 1.1 and SPARQL 1.1 Query/Update/Protocol. Every triple lives in a named graph, and the default graph is the union of all named graphs. Neptune Analytics supports openCypher over RDF graphs (Aug 2024 announcement). — [Neptune SPARQL compliance](https://docs.aws.amazon.com/fr_fr/neptune/latest/userguide/feature-sparql-compliance.html); [Neptune named graphs](https://docs.aws.amazon.com/neptune/latest/userguide/best-practices-sparql-query.html); [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2024/08/amazon-neptune-analytics-opencypher-queries-graphs)
- W3C SPARQL 1.2 Query Language is a **Working Draft dated 12 November 2026**. RDF 1.2 Concepts reached Candidate Recommendation in 2026 and defines triple terms and `rdf:reifies`. — [SPARQL 1.2 Query](https://www.w3.org/TR/sparql12-query/); [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/)

### Inferences
- Recommended default: Oxigraph for development, tests and single-node use (pyoxigraph inside the Downloader; the CLI server shared over HTTP by the Assistant and Reviewer). Use Fuseki if server-side SHACL, GeoSPARQL, text indexing or a more mature admin UI are needed. Both keep the code at standard SPARQL 1.1 + GSP, so the store can be swapped.
- Named-graph pattern: one graph per source manual or run (provenance), with separate graphs for candidate, reviewed and curated data. All OSS options support this, and in Neptune the default-graph semantics differ (union of all graphs).
- Use Neo4j only if property-graph tooling (LLM Graph Builder, Graphiti, neo4j-graphrag) is chosen for the Assistant. Then n10s is the bridge to and from RDF/SKOS in git, and governance is weaker on the RDF side.
- Avoid GraphDB Free and Stardog Free for anything that could become commercial, because of their licence restrictions.

### Gaps
- Official GraphDB Free limits for 11.5 were not verified.
- Stardog on-prem free availability is inconsistent across sources.
- Per-store SPARQL 1.2 support (Jena, RDF4J, GraphDB, QLever) was not checked in detail.

## Q3. Ontology engineering toolchains (ODK, ROBOT, LinkML, KGCL/OAK, docs, SKOS publishing)

### Takeaway
A git-based curated-knowledge repo maps well onto **ODK (Docker, wraps ROBOT, make-based CI) or a lighter ROBOT+pySHACL GitHub Actions pipeline**. Documentation comes from **pyLODE** (OWL/SKOS to HTML, very active) or **Widoco**, browsing from **Skosmos 3.x** for SKOS taxonomies, and spreadsheet-based vocabulary curation from **voc4cat**. **KGCL** with OAK `apply` is a good machine-readable change-proposal format for the Reviewer, but kgcl-schema itself has not been released since Nov 2024.

### Cited Findings
- Ontology Development Kit v1.6.1 was released 2026-03-10 under BSD-3-Clause, repo pushed 2026-11-09. — [GitHub](https://github.com/INCATools/ontology-development-kit)
- ROBOT 1.9.11 was released 2026-10-01 (see Q1). — [GitHub](https://github.com/ontodev/robot)
- LinkML schema-automator 0.5.7 was released 2026-08-27 under BSD-3-Clause. It infers or bootstraps LinkML schemas from TSV/JSON/OWL and can annotate enums with ontology terms. — [PyPI](https://pypi.org/project/schema-automator/); [GitHub](https://github.com/linkml/schema-automator)
- KGCL: kgcl-schema 0.7.0 was released 2024-11-14 under MIT, with the repo pushed 2026-02-11. kgcl-rdflib 0.5.0 dates from 2023-05-11. OAK 0.7.4 (2026-08-03) is the actively maintained KGCL applier and diff producer. — [PyPI kgcl-schema](https://pypi.org/project/kgcl-schema/); [GitHub kgcl](https://github.com/INCATools/kgcl); [PyPI kgcl-rdflib](https://pypi.org/project/kgcl-rdflib/); [GitHub OAK](https://github.com/INCATools/ontology-access-kit)
- Widoco v1.4.26 was released 2026-10-23 under Apache-2.0 (Java). — [GitHub](https://github.com/dgarijo/Widoco)
- pyLODE 3.6.1 was released 2026-11-06 under BSD-3-Clause, repo pushed 2026-11-13. — [PyPI](https://pypi.org/project/pylode/); [GitHub](https://github.com/RDFLib/pyLODE)
- Skosmos v3.5 was released 2026-10-22 and the repo was pushed 2026-11-12. It is a PHP SKOS browser that reads from a SPARQL endpoint, usually Fuseki. GitHub shows NOASSERTION for the licence (the project states MIT; verify). — [GitHub](https://github.com/NatLibFi/Skosmos)
- voc4cat 1.2.0 was released 2026-09-22 under BSD-3-Clause. It converts Excel to SKOS and back, with GitHub-based vocabulary curation and checks. Small community (9 stars). — [PyPI](https://pypi.org/project/voc4cat/); [GitHub](https://github.com/nfdi4cat/voc4cat-tool)

### Inferences
- Curated repo layout: `ontology/*.ttl` (OWL), `vocab/*.ttl` (SKOS glossary/taxonomy), `shapes/*.ttl` (SHACL), `schema/*.yaml` (LinkML). CI runs ROBOT (merge, reason with ELK, report), pySHACL, and pyLODE for HTML docs on GitHub Pages. Add ODK if OBO-style imports and release management are needed.
- Reviewer: represent each proposed edit as a KGCL statement or SPARQL Update plus provenance, apply it with OAK/rdflib, and open a git PR. Skosmos gives reviewers a read-only taxonomy browser.

### Gaps
- Whether ODK 1.6.x supports non-OBO (generic OWL/SKOS) projects without friction was not evaluated.

## Q4. LLM-assisted extraction and construction frameworks

### Takeaway
Two families exist. **Schema- or ontology-grounded extraction**: OntoGPT/SPIRES (LinkML-driven, BSD-3), neo4j-graphrag `SimpleKGPipeline` with a schema, LlamaIndex `SchemaLLMPathExtractor`, and DSPy for optimizing the prompts. **Open or schema-light GraphRAG**: Microsoft GraphRAG, LightRAG, Cognee, Graphiti, KGGen. For this project the schema-grounded approach fits the Downloader best: **Docling to parse → LinkML schema → structured-output LLM extraction (OntoGPT/SPIRES-style or DSPy/Pydantic) → RDF candidates → SHACL checks**. LightRAG or GraphRAG fit the Assistant's retrieval side. Graphiti/Cognee fit agent memory more than curated ontologies.

### Cited Findings
- OntoGPT 1.2.0 was released 2026-09-09 under BSD-3, with about 1.1k stars and the repo pushed 2026-09-10. SPIRES extracts nested structures to a LinkML template and grounds terms to ontologies through OAK. — [PyPI](https://pypi.org/project/ontogpt/); [GitHub](https://github.com/monarch-initiative/ontogpt)
- neo4j-graphrag (Python) 1.24.0 was released 2026-11-10 under Apache-2.0 per PyPI (the repo LICENSE includes a NOTICE about mixed licences). It is Neo4j's official GraphRAG package with KG-construction pipelines and retrievers. — [PyPI](https://pypi.org/project/neo4j-graphrag/); [GitHub](https://github.com/neo4j/neo4j-graphrag-python)
- Neo4j LLM Graph Builder v0.8.7 was released 2026-07-23 under Apache-2.0, with about 5.3k stars. It is a full app (React + Python) that turns PDFs/web pages into a Neo4j KG. — [GitHub](https://github.com/neo4j-labs/llm-graph-builder)
- LlamaIndex (llama-index-core 0.14.25, 2026-09-21, MIT): `PropertyGraphIndex` handles graph construction and querying, and `SchemaLLMPathExtractor` follows "a strict schema of allowed entities, relationships". — [PyPI](https://pypi.org/project/llama-index-core/); [LlamaIndex docs](https://developers.llamaindex.ai/python/framework/module_guides/indexing/lpg_index_guide/)
- LangChain: `LLMGraphTransformer` is still imported from `langchain_experimental.graph_transformers` (langchain-experimental 0.4.2, 2026-05-22, MIT). langchain-neo4j 0.11.0 was released 2026-10-09 (MIT). No deprecation notice was found. — [PyPI langchain-experimental](https://pypi.org/project/langchain-experimental/); [PyPI langchain-neo4j](https://pypi.org/project/langchain-neo4j/); [Neo4j dev guide](https://neo4j.com/developer/genai-ecosystem/importing-graph-from-unstructured-data/)
- Microsoft GraphRAG 3.3.0 was released 2026-10-08 under MIT, with about 36.6k stars. — [PyPI](https://pypi.org/project/graphrag/); [GitHub](https://github.com/microsoft/graphrag)
- LightRAG (`lightrag-hku`) 1.5.7 was released 2026-09-02 under MIT, with about 40.7k stars and the repo pushed 2026-11-13. — [PyPI](https://pypi.org/project/lightrag-hku/); [GitHub](https://github.com/HKUDS/LightRAG)
- Cognee 1.6.8 was released 2026-11-12 under Apache-2.0, with about 33k stars. — [PyPI](https://pypi.org/project/cognee/); [GitHub](https://github.com/topoteretes/cognee)
- Graphiti (`graphiti-core`) 0.31.2 was released 2026-10-20 under Apache-2.0, with about 32.8k stars. It is a temporal KG for agent memory (Zep). — [PyPI](https://pypi.org/project/graphiti-core/); [GitHub](https://github.com/getzep/graphiti)
- KGGen (`kg-gen`) 0.4.0 was released 2025-09-30. PyPI says MIT, but the GitHub repo has no detected licence; the repo was last pushed 2026-03-24. — [PyPI](https://pypi.org/project/kg-gen/); [GitHub](https://github.com/stair-lab/kg-gen)
- EDC (Extract-Define-Canonicalize) is research code under MIT, last pushed **2024-08-13**, with no releases. Treat it as a reference implementation only. — [GitHub](https://github.com/clear-nus/edc)
- DSPy 3.5.0 was released 2026-11-10 under MIT, with about 39k stars. — [PyPI](https://pypi.org/project/dspy/); [GitHub](https://github.com/stanfordnlp/dspy)
- Docling 2.150.0 was released 2026-11-10 under MIT, with about 70.6k stars. Unstructured 0.27.37 was released 2026-11-06 under Apache-2.0. — [PyPI docling](https://pypi.org/project/docling/); [PyPI unstructured](https://pypi.org/project/unstructured/)
- Ontology matching: OntoAligner 1.9.4 was released 2026-09-01 under Apache-2.0 and is active. DeepOnto 0.9.3 dates from 2025-03-10 under Apache-2.0, with the repo pushed 2026-09-04 (it includes BERTMap and LLM-based OM). OntoChat's last release was v1.0.0 (2024-03-27, MIT), with the repo pushed 2026-04-22; it is research-grade. — [PyPI ontoaligner](https://pypi.org/project/ontoaligner/); [PyPI deeponto](https://pypi.org/project/deeponto/); [GitHub OntoChat](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat)

### Inferences
- **Downloader pipeline:** Docling (layout-aware, MIT) produces a structured document. LinkML defines Term/Concept/Relation/Definition/QualityIssue, and its generated Pydantic models serve as LLM structured-output targets, used directly or via OntoGPT SPIRES or DSPy signatures (DSPy allows eval-driven prompt optimization). The output is serialized to RDF/SKOS candidates in a per-run named graph, then pySHACL plus LLM-judge checks flag quality issues. OAK or OntoAligner suggest mappings to existing vocabularies.
- **Assistant:** hybrid RAG with LightRAG or a custom retriever (vector + SPARQL over curated graphs). GraphRAG is heavier (community summaries) and costlier to index. neo4j-graphrag or LlamaIndex make sense only if the property-graph store is Neo4j.
- Glossary or term extraction: no dominant maintained dedicated LLM tool was found. Implementing it as a LinkML/DSPy extraction task appears simplest (inference).
- Licence risk: none of the main frameworks is copyleft. KGGen's missing repo licence needs checking.

### Gaps
- No benchmarked comparison of these frameworks on user-manual corpora was gathered.
- No up-to-date, maintained LLM-specific glossary/term-extraction library was identified, and none was searched exhaustively.
- Whether GraphRAG 3.x and LightRAG 1.5 can export to RDF natively was not checked.

## Q5. MCP servers for ontologies, SPARQL and KGs

### Takeaway
Production-grade options are few. **EBI OLS4 now runs a public MCP endpoint** for ontology lookup, and **Neo4j has an official MCP server** (Go, GPL-3.0 under the community edition) alongside the MIT-licensed `neo4j-contrib/mcp-neo4j` set. For SPARQL, `sib-swiss/sparql-llm` (MIT) is the most credible maintained option. Many 2026 community "ontology MCP" projects exist but are young; vet them before use. A thin custom MCP server over Oxigraph/Fuseki (SPARQL query, describe, SHACL validate, propose KGCL change), built with the official MCP SDKs, is the low-risk route.

### Cited Findings
- EBI OLS4 README: OLS provides a website, a REST API and an MCP server, with the endpoint (stateless Streamable HTTP) at `https://www.ebi.ac.uk/ols4/api/mcp`. Licence Apache-2.0, release v4.0.5. — [GitHub EBISPOT/ols4](https://github.com/EBISPOT/ols4)
- The Neo4j official MCP Server (`neo4j/mcp`) v2.1.1 was released 2026-11-11 and is written in Go. Its NOTICE states the software is licensed under **GPL v3** to third parties, while with Aura or commercial Neo4j it is client software under those agreements. — [GitHub neo4j/mcp](https://github.com/neo4j/mcp)
- neo4j-contrib/mcp-neo4j is MIT-licensed, with about 1k stars; the latest release is mcp-neo4j-cypher v0.6.0 (2026-04-10). — [GitHub](https://github.com/neo4j-contrib/mcp-neo4j); [PyPI](https://pypi.org/project/mcp-neo4j-cypher/)
- sib-swiss/sparql-llm describes itself as a "Chat system, MCP server, and reusable components to improve LLMs capabilities when generating SPARQL queries". It is MIT-licensed, pushed 2026-11-05, with release v0.1.4. — [GitHub](https://github.com/sib-swiss/sparql-llm)
- Other community MCP servers, from a GitHub search on 2026-11-13: mcp-rdf-explorer (MIT, 56 stars, pushed 2026-10-30); robsyc/ld-mcp (MIT); dbcls/togomcp (MIT, life-science KGs); keonchennl/mcp-server-graphdb (GPL-3.0, read-only GraphDB); ExtensityAI/ontoloom (BSD-3, OWL 2 building, pushed 2026-06-01); seandavi/ols-mcp-server (no licence, last pushed 2025-07-16); jsilvanus/skosmos-mcp (MIT, 1 star); fabio-rovai/open-ontologies (MIT, Rust, about 2.9k stars, created 2026-03-09, "plan, apply and roll back changes to a production ontology"); trustgraph-ai/trustgraph (Apache-2.0, about 2.9k stars, "open-source ontology runtime for AI agents"). — [mcp-rdf-explorer](https://github.com/emekaokoye/mcp-rdf-explorer); [ld-mcp](https://github.com/robsyc/ld-mcp); [togomcp](https://github.com/dbcls/togomcp); [mcp-server-graphdb](https://github.com/keonchennl/mcp-server-graphdb); [ontoloom](https://github.com/ExtensityAI/ontoloom); [ols-mcp-server](https://github.com/seandavi/ols-mcp-server); [skosmos-mcp](https://github.com/jsilvanus/skosmos-mcp); [open-ontologies](https://github.com/fabio-rovai/open-ontologies); [trustgraph](https://github.com/trustgraph-ai/trustgraph)
- The official TypeScript MCP SDK `@modelcontextprotocol/sdk` 1.32.2 was released 2026-10-23 under MIT. — [npm](https://www.npmjs.com/package/@modelcontextprotocol/sdk)

### Inferences
- Assistant and Reviewer agents can use OLS MCP for external term grounding and a custom SPARQL/SHACL MCP over the project's own store. open-ontologies (plan, apply, rollback with blast radius) aligns conceptually with the Reviewer's governance goal and is worth a spike, but it is less than a year old.
- If a Neo4j path is chosen, prefer the MIT `mcp-neo4j` servers to avoid GPL questions, or confirm that the GPL terms are acceptable for internal use.

### Gaps
- Feature depth, security model and maturity of the community MCP servers were not tested; star counts are only a weak signal.
- No official MCP server from Oxigraph, Jena, GraphDB or Stardog was found; the GraphDB one above is community-made. Searches were limited to GitHub.

### Recommended concrete stack (synthesis)
- **Shared formats/CI:** Turtle/TriG in git; LinkML as the schema source; ROBOT (with ELK) + pySHACL + pyLODE in GitHub Actions; KGCL for change records.
- **Store:** Oxigraph (pyoxigraph embedded plus the server for shared access), with named graphs per source/run/status; Fuseki as a fallback if more server features are needed.
- **Downloader:** Docling → LinkML/Pydantic structured extraction (OntoGPT SPIRES or DSPy) → rdflib → pySHACL; OAK/OntoAligner for mapping.
- **Assistant:** LightRAG or a custom hybrid retriever (vector + SPARQL), with citations kept as provenance in named graphs; OLS MCP plus a custom SPARQL MCP for agent tools.
- **Reviewer:** TypeScript with N3.js, @zazuko/env, shacl-engine, jsonld.js and LDkit/Comunica; a Python backend with rdflib/OAK to apply KGCL changes and open git PRs; Skosmos for read-only browsing.
- **Licence watch:** owlready2 and py-horned-owl/horned-owl are LGPL; Virtuoso is GPLv2; the official Neo4j MCP is GPLv3; GraphDB/Stardog Free are proprietary; Openllet is likely AGPL.
