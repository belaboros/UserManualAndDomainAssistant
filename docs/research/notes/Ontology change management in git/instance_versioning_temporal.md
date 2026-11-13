# Versioning and Temporal Modeling for Fast-Changing KG Instance Data (ABox) vs Git-Curated Schema (TBox)

Research date: 2026-11-13. Scope: how harvested, daily-changing instance data (services, teams, resource kinds, instances from Backstage/Port, CRDs, Crossplane, Terraform, OpenAPI) should be versioned alongside a git/PR-governed ontology, glossary and SHACL layer.

## Q1. Should harvested instance data live in git at all? (split architectures, snapshots, named graphs, patch logs, CDC)

### Takeaway
The established pattern is a split. Curated TBox, glossary and SHACL go in git with PR review. Harvested ABox goes to a store that keeps a change log or snapshots: named graphs per source and per harvest run, with PROV-O run metadata, plus either a patch log (RDF Patch) or periodic immutable snapshots with dated version IDs (Databus-style). Git-backed RDF stores exist (Quit Store) but are research-grade with weak maintenance signals, and the main patch-log tool (rdf-delta) is flagged for archiving. So "everything through git PRs" is not well supported by tools for daily, high-volume ABox churn.

### Cited Findings
- **Git-native RDF store.** Quit Store runs a SPARQL 1.1 query/update endpoint and versions each named graph in Git. Effective changes are applied to the Git blob of the ancestor commit and committed. It supports branch, merge and push/pull of distributed RDF datasets. — [Arndt et al., arXiv 1805.03721](https://arxiv.org/abs/1805.03721v3)
- Quit Store maintenance looks weak. An ecosyste.ms index reported "last pushed over 1 year ago", 54 open issues and 113 stars (snapshot date uncertain). — [ecosyste.ms AKSW/QuitStore](https://awesome.ecosyste.ms/projects/github.com%2FAKSW%2FQuitStore)
- **RDF Patch / RDF Delta.** RDF Patch records changes to a dataset. A patch log is a linear journal: each new patch must name the current latest patch as its `previous`, so there is no branching. The Delta Patch Server serves logs for many datasets. Fuseki can be configured (`delta:changes`, `delta:patchlog`) to log every change to the patch server, which is also the basis of the HA Fuseki setup. — [RDF Delta docs](https://afs.github.io/rdf-delta/ha-fuseki.html); [rdf-patch-logs](https://afs.github.io/rdf-delta/rdf-patch-logs); [system setup](https://afs.github.io/rdf-delta/system-setup.html)
- The rdf-delta site now shows the banner **"This project is going to be archived."** No replacement is named. A GitHub release listing showed v1.1.2 as the latest visible version. — [afs.github.io/rdf-delta](https://afs.github.io/rdf-delta); [ecosyste.ms rdf-delta](https://awesome.ecosyste.ms/projects/github.com%2Fafs%2Frdf-delta)
- **Snapshot-per-release with dated version IDs (DBpedia Databus).** An artifact is the version-independent dataset. A version is a specific release whose ID is appended to the artifact URI, e.g. `.../janfo/animals/cats/2023-03-30`. ISO-8601-like IDs (`YYYY.MM.DD-hhmmss`) are recommended because lexical order equals chronological order, which helps SPARQL. The version defaults to the current time. Re-submissions should change the version, and WIP versions can carry `-snapshot` or `-dev`. — [Databus versioning docs](https://dbpedia.gitbook.io/databus/model/versioning); [Databus version metadata](https://dbpedia.gitbook.io/databus/model/metadata/version)
- **Named graph per source, with provenance on the graph IRI.** This lets you query or drop a whole source at once. The trade-off is per-graph rather than per-triple granularity. — [kindatechnical guide (practitioner, low authority)](https://kindatechnical.com/knowledge-graphs/knowledge-graph-versioning-and-provenance.html)
- **Separate provenance graph.** A 2026 manufacturing KG paper keeps PROV-O provenance in its own named graph, separate from the ontology, instance and runtime graphs. Entities link to the ingestion activity via `prov:wasDerivedFrom`, and pipeline-created entities use `prov:wasGeneratedBy`. Each activity links to its source agent via `prov:wasAssociatedWith`. — [arXiv 2608.21418](https://arxiv.org/pdf/2608.21418)
- **Older proposal (2014).** A provenance graph records each update, and auxiliary named graphs hold each version's state plus the inserted and deleted triples. — [WWW2014 companion](https://archives.iw3c2.org/www2014/proceedings/companion/p287.pdf)
- **Bosch (FOIS 2024).** Extends PROV-O with RDF-star to record changes for full traceability, with provenance kept in a separate graph. It also surveys built-in options such as GraphDB's history plugin. — [Dibowski, FOIS 2024](https://utwente.nl/en/eemcs/fois2024/resources/papers/dibowski-full-traceability-and-provenance-for-knowledge-graphs.pdf); [IOS Press FAIA241309](https://ebooks.iospress.nl/pdf/doi/10.3233/FAIA241309)
- **Data-lake analogue (lakeFS).** Branching is a zero-copy metadata operation. lakeFS recommends committing whenever data changes and recording the commit ID with every run (ML) for reproducibility. These are vendor claims. — [lakeFS docs](https://docs.lakefs.io/); [lakeFS reproducibility blog](https://lakefs.io/blog/scalable-ml-data-version-control-and-reproducibility/)

### Inferences
- **Recommended layering for this system:**
  1. Git holds TBox, glossary, SHACL, harvest mappings and change-detection rules. Releases get semver tags and `owl:versionIRI`.
  2. Each harvest run writes one named graph per (source, run), e.g. `urn:harvest:backstage:2026-11-13T02:00Z`. A PROV-O `prov:Activity` records start/end time, the source agent, the mapping commit SHA and the ontology version used.
  3. A "current" graph per source is rebuilt or swapped atomically.
  4. Diffs between consecutive runs are stored as RDF Patch-style add/delete sets, or as an event table if the store is not RDF-native.
  5. A "release snapshot" is an immutable, Databus-like dated ID that pins (ontology tag, set of run graph IDs).
- Use git only for ABox data that is curated: hand-authored overrides, mappings, team ownership corrections, accepted ontology proposals. Routine harvested deltas should not become PRs. The PR gate belongs on schema-impacting changes (see Q5).
- Avoid depending on rdf-delta for new work given the archive banner. The RDF Patch format is simple enough to emit yourself (A/D lines plus header ids) and keep in object storage or a database table.
- If the store is not RDF-native (e.g. Neo4j or Postgres), the same split applies. Use CDC/outbox events as the change log and periodic snapshots as the archive.

### Gaps
- I did not verify Quit Store's latest commit date directly on GitHub.
- No authoritative enterprise case study was found that explicitly reports "ABox through git PRs did not scale". This is inferred from tooling design (Quit Store targets collaborative editing, not bulk ETL).
- CDC tooling specific to triplestores (e.g. Neptune Streams, Stardog/GraphDB change feeds) was not researched in depth.

## Q2. Temporal / bitemporal modeling in RDF and temporal KGs

### Takeaway
Use bitemporal semantics: valid time (when a fact holds in the platform) and transaction time (when the harvester observed or recorded it). In RDF there are three options: graph-level timestamps (named graph per run with PROV-O / `prov:generatedAtTime`), statement-level annotations (RDF 1.2 triple terms / reifiers, Wikidata-style qualifiers), or explicit state/version nodes (Neo4j identity/state pattern). Graphiti/Zep shows the LLM-memory flavour: four timestamps per edge, with invalidation instead of deletion. RDF 1.2 was still at Candidate Recommendation in spring 2026, so statement-level annotation is standardising but tool support varies.

### Cited Findings
- **RDF 1.2 Concepts** was a Candidate Recommendation Snapshot dated 7 April 2026, not expected to become a Recommendation before 5 May 2026. Exit requires RDF 1.2 Semantics and at least one concrete syntax to meet their exit criteria. RDF 1.2 TriG was still a Working Draft on 19 April 2026. — [RDF 1.2 Concepts (TR)](https://www.w3.org/TR/rdf12-concepts/); [CR 2026-04-03](https://www.w3.org/TR/2026/WD-rdf12-concepts-20260403/); [RDF 1.2 TriG WD 2026-04-19](https://www.w3.org/TR/2026/WD-rdf12-trig-20260419/)
- **Triple terms** are a new kind of RDF term alongside IRIs, literals and blank nodes. They may appear in the object position of a triple, which is how statement-level metadata such as validity intervals or provenance is attached in RDF 1.2. — [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/)
- **Graphiti (Zep's engine).** `EntityEdge` carries `valid_at` and `invalid_at` (real-world validity) plus `created_at` and `expired_at` (ingestion / supersession). On contradiction, the old edge's `invalid_at` is set to the new fact's `valid_at` and `expired_at` is stamped with processing time. The old edge is kept as history. A point-in-time filter is `valid_at <= t AND (invalid_at > t OR invalid_at IS NULL)`. Range indexes exist on these fields. — [Graphiti temporal model docs (Mintlify mirror)](https://mintlify.com/getzep/graphiti/concepts/temporal-model); [Graphiti nodes & edges](https://mintlify.com/getzep/graphiti/concepts/nodes-and-edges). These are secondary doc mirrors, so verify field names against the `graphiti_core` source.
- **Zep paper** (arXiv 2501.13956, Jan 2025): a bi-temporal model where timeline T orders events and timeline T′ orders ingestion. The graph has episodic, semantic and community subgraphs. The authors report 94.8% on Deep Memory Retrieval vs 93.4% for MemGPT, and gains on LongMemEval (vendor-authored). — [arXiv 2501.13956](https://arxiv.org/html/2501.13956v1)
- **Wikidata.** P580 (start time) and P582 (end time) are qualifiers on statement nodes. Ranks are preferred, normal and deprecated. Guidance: date outdated values with P580/P582 rather than only re-ranking. WDQS "truthy" `wdt:` triples return only preferred values when any exist, else normal, never deprecated. Full statements are reached via `p:`/`ps:`/`pq:`. — [Help:Qualifiers](https://www.wikidata.org/wiki/Help:Qualifiers); [Help:Ranking (2022 archive)](https://webcf.waybackmachine.org/web/20220322134249/https://www.wikidata.org/wiki/Special:MyLanguage/Help:Ranking); [Wikibase RDF lecture notes](https://courses.cs.umbc.edu/graduate/691/fall19/07/notes/24_wikidata/wikibase.pdf)
- **Neo4j patterns.** Official modeling docs describe linking an entity to versions held in State nodes (identity/state separation). Validity windows are from/to on relationships. Practitioners use a far-future sentinel instead of null for open intervals, and a `current: true` flag for fast current-state queries. Lazarevic's 2019 post covers bitemporal versioning for retroactive corrections. A linked-list (`NEXT`) variant is also shown. — [Neo4j versioning docs](https://neo4j.com/docs/getting-started/data-modeling/versioning/); [Lazarevic, Medium/Neo4j](https://medium.com/neo4j/keeping-track-of-graph-changes-using-temporal-versioning-3b0f854536fa)
- **Stardog** deprecated its built-in VCS in 7.0 and later removed it, because per-commit absolute diffs were incompatible with the new lock-free snapshot-isolation backend. Staff said bitemporal support was planned instead (forum evidence, not release notes). — [Stardog community: Versioning in Stardog 7](https://community.stardog.com/t/versioning-in-stardog-7/1700); [Querying over timelines](https://community.stardog.com/t/querying-a-database-over-different-timelines/2307)
- **Starvers** uses timestamp-based RDF-star annotations and SPARQL-star templates to evolve datasets and query time-specific snapshots, evaluated on BEAR. Query performance "differs vastly" between RDF-star stores. — [Semantic Web Journal swj3506](https://semantic-web-journal.net/system/files/swj3506.pdf); [starvers_eval repo](https://github.com/GreenfishK/starvers_eval)
- **Cuevas & Hogan (2020)** compared representing versioned RDF with standard SPARQL on off-the-shelf engines (named graphs, reification, n-ary, RDF*) on an 8-version Wikidata archive, measuring index size, indexing time and query cost. — [Cuevas & Hogan, "Versioned queries over RDF archives: all you need is SPARQL?"](https://www.aidanhogan.com/docs/sparql-version.pdf)

### Inferences
- For a platform-catalog KG, transaction time is cheap and reliable: it is the harvest run timestamp from the named graph or PROV activity. Valid time is often unknown or approximate (CRD `creationTimestamp`, Terraform state serial, Backstage entity `metadata` annotations). Model valid time only where the source provides it, and default to "observed-at" intervals: first seen run to last seen run.
- **Practical encoding options, ranked by maturity:**
  - (a) Named graph per run plus `prov:generatedAtTime`. Supported everywhere and SPARQL 1.1-only.
  - (b) Interval rows in a side table or as n-ary "observation" nodes, e.g. `:obs a :Observation; :subject; :validFrom; :validTo`. Portable.
  - (c) RDF 1.2 triple-term annotations. The most elegant, but the spec was at CR in 2026 and store support is uneven.
- The Graphiti 4-timestamp edge is a good template even outside LLM memory. Never delete; set `invalid_at`/`expired_at`. "As of t" then becomes a simple filter, and that filter needs range indexes.

### Gaps
- I could not confirm whether RDF 1.2 reached full W3C Recommendation between May and November 2026. Check https://www.w3.org/TR/rdf12-concepts/.
- Current RDF 1.2 / triple-term support levels in GraphDB, Stardog, Neptune and Jena as of late 2026 were not verified.
- W3C Time Ontology (OWL-Time) usage specifics were not researched beyond general knowledge, so no citation is given.

## Q3. Archive storage strategies and tool maturity (IC / CB / TB, BEAR, OSTRICH, ConVer-G, TerminusDB, Dolt-like)

### Takeaway
The literature classifies RDF archives as independent copies (IC), change-based (CB) and timestamp-based (TB), plus hybrids. The research systems (OSTRICH, ConVer-G, Starvers) show good results on BEAR, but most are academic and thinly maintained. ConVer-G (Postgres plus per-version bitmasks, SPARQL→SQL) is the most recently active (JOSS paper; 2026 QuaQue paper). TerminusDB is the most "Dolt-like" (git semantics for graphs) and is now maintained by DFRNT/Gettier, a single small vendor. For enterprise use, the pragmatic choice is still IC snapshots or named-graph-per-run plus CB diffs on a mainstream store.

### Cited Findings
- **Strategy taxonomy.**
  - IC stores full versions: simplest, but space-hungry.
  - CB stores deltas between versions.
  - TB annotates each triple with its validity period.
  - Some authors add fragment-based, and modern systems combine strategies.
  - A recent survey found existing solutions struggle with large archives that have many versions.
  — [Fernández et al., "Evaluating Query and Storage Strategies for RDF Archives" (SWJ)](https://www.semantic-web-journal.net/node/1814); [SWJ 3625](https://www.semantic-web-journal.net/system/files/swj3625.pdf); [MEPDaW 2023](https://vbn.aau.dk/ws/files/742318256/MEPDaW2023-paper1.pdf)
- **BEAR benchmark.** Three real-world datasets (BEAR-A, B, C) with varying size and change dynamics. It defines query types including version materialisation (query Q at version Vi), delta materialisation and version queries. — [BEAR site](https://aic.ai.wu.ac.at/qadlod/bear.html); [SEMANTiCS 2016 paper](https://aic.ai.wu.ac.at/qadlod/docs/semantics16.pdf)
- **OSTRICH** is a C++ hybrid IC/CB/TB versioned triple store with Node.js bindings. It efficiently answers VM, DM and VQ triple-pattern queries with count estimates for join ordering. A later bidirectional delta-chain paper (SWJ 2021) optimises storage. The repo was "last pushed over 2 years ago" per ecosyste.ms, and I found no 2024–2025 activity. — [Taelman et al., JWS 2019](https://ruben.verborgh.org/publications/taelman_jws_2019/); [Bidirectional delta chains (SWJ)](https://content.iospress.com:443/articles/semantic-web/sw210449); [ecosyste.ms rdfostrich/ostrich](https://awesome.ecosyste.ms/projects/github.com%2Frdfostrich%2Fostrich)
- **Full-SPARQL RDF archive querying.** Work by Pelgrin, Hose et al. (GLENDA, ESWC 2023) claims the first openly available full-SPARQL querying over RDF archives. — [SWJ node 3940](https://www.semantic-web-journal.net/node/3940)
- **ConVer-G.**
  - Architecture: QuaDer loader, QuaQue query engine, PostgreSQL storage. Each quad is stored once, with a bitmask marking which snapshots/versions contain it. SPARQL is translated to SQL, with bitwise version filtering.
  - Published in JOSS (10.21105/joss.10828). The 2026 QuaQue paper reports outperforming Apache Jena on multi-version queries (authors' own benchmark).
  - Supported operators include quad pattern, join, filter, union, optional and aggregation.
  - Code: github.com/VCityTeam/ConVer-G.
  — [ConVer-G arXiv 2409.04499](https://arxiv.org/pdf/2409.04499); [JOSS paper](https://joss.theoj.org/papers/10.21105/joss.10828.pdf); [QuaQue arXiv 2603.18654](https://arxiv.org/abs/2603.18654); [Condensed representation arXiv 2506.21203](https://arxiv.org/pdf/2506.21203)
- **TerminusDB** (git-like branch/merge/time-travel graph database). Maintenance passed to Gettier (formerly DFRNT) from 2025. The evidence is Wikipedia, not an official announcement. A third-party review flags single-vendor lock-in risk. — [Wikipedia: TerminusDB](https://en.wikipedia.org/wiki/TerminusDB); [dev.co review (low authority)](https://dev.co/cms/open-source/terminusdb)
- **GraphDB.** Ontotext's "data history and versioning" plugin gives access to earlier database states. 9.2 (2020) improved comparing the current state with a previous period. It cannot hold changes for approval before they apply. — [PR Newswire GraphDB 9.2](https://www.prnewswire.co.uk/news-releases/ontotext-s-graphdb-9-2-supports-rdf-to-match-the-expressivity-of-property-graphs-810974555); [StackOverflow thread (archive)](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/61097427/how-to-set-up-version-control-on-top-of-a-triple-store)
- **Stardog** has had no built-in VCS since 7.x (see Q2). — [Stardog community](https://community.stardog.com/t/versioning-in-stardog-7/1700)

### Inferences
- **Maturity ranking for an enterprise in late 2026:**
  1. Mainstream store with named-graph-per-run plus external diff/snapshot management (IC + CB, DIY). Most robust.
  2. GraphDB history plugin. Vendor-supported, but check that it is still in current docs.
  3. TerminusDB. Real git semantics, small vendor.
  4. ConVer-G. Active research with a Postgres base, which makes it attractive for prototyping.
  5. OSTRICH and Quit Store. Research, stale.
- The ConVer-G bitmask idea suits daily harvests with low churn: most quads persist across runs, so one row plus N bits beats N copies. It can be reproduced in plain Postgres or in a triplestore with an `observedInRuns` bitmap or interval table.
- Retention can be tiered: keep every daily run diff (small) indefinitely, full IC snapshots only for release-pinned versions, and compact old dailies to weekly.

### Gaps
- No independent benchmark comparing ConVer-G, TerminusDB and GraphDB history on the same workload was found.
- The current (2026) GraphDB documentation for the history plugin was not retrieved, so its present status is unverified.
- Amazon Neptune versioning patterns were not found in this pass. To my knowledge Neptune has no built-in time travel, but this is unverified, so no claim is made.
- Dolt itself (SQL) was not researched. Its applicability to graphs is by analogy only.

## Q4. Reproducibility: tying answers and quality reports to (schema version, data snapshot); retention; audit

### Takeaway
Borrow the lakeFS/DataHub pattern: every derived artifact records immutable identifiers. Here that means the ontology git tag/SHA plus a data snapshot ID (harvest run IDs or a release snapshot ID). The catalog tools version per entity or aspect with semantic change categories. These can be mirrored so that each harvested entity has a version history and each answer cites "ontology v1.4.2 @ sha / snapshot 2026.11.13-020000".

### Cited Findings
- lakeFS recommends committing whenever data changes and recording the commit ID with each run. Branching from a past commit lets you investigate issues in isolation. — [lakeFS blog](https://lakefs.io/blog/scalable-ml-data-version-control-and-reproducibility/); [lakeFS docs](https://docs.lakefs.io/)
- **DataHub.**
  - Each aspect version is immutable, and any update creates a new version (current = latest).
  - The Timeline API (server ≥0.8.28) returns chronological change transactions, each tagged with a semantic-versioning category MAJOR/MINOR/PATCH. It covers schema, documentation, tags and glossary terms, though docs say only Datasets and Glossary Terms are supported.
  - DataHub 2.0 (Cloud) notes Timeline support for versioned entities (Glossary Term).
  — [DataHub aspect versioning](https://docs.datahub.com/docs/advanced/aspect-versioning); [DataHub Timeline API](https://docs.datahub.com/docs/dev-guides/timeline); [DataHub Cloud v2.0 notes](https://docs.datahub.com/docs/managed-datahub/release-notes/v_2_0_0.md)
- **OpenMetadata** keeps version history for all entities as Major.Minor (starting 0.1), with a UI timeline of changes. The Python SDK has `get_entity_version` and `get_list_entity_versions`. — [OpenMetadata 0.6.0 release](https://newreleases.io/project/github/open-metadata/OpenMetadata/release/0.6.0); [OM SDK version mixin](https://docs.open-metadata.org/v2.0.x/sdk/python/api-reference/version-mixin.md)
- Databus dated version IDs give stable, sortable snapshot identifiers that work in SPARQL. — [Databus versioning](https://dbpedia.gitbook.io/databus/model/versioning)
- PROV-O `wasGeneratedBy` / `wasDerivedFrom` / `wasAssociatedWith` link generated entities to ingestion activities and agents. — [arXiv 2608.21418](https://arxiv.org/pdf/2608.21418)

### Inferences
- **Define a "context tuple"** `{ontology_version (semver + git SHA), shapes_version, mapping_version (SHA), snapshot_id, retrieval_time}`. Stamp it on:
  - every assistant answer, as a citation footer or log record;
  - every SHACL validation report (`sh:ValidationReport` with `prov:used` pointing at the shapes graph version and data graph ID);
  - every quality issue ticket.

  Re-running a validation for an old report then means loading that snapshot's graphs and that tag's shapes.
- **Use DataHub-style MAJOR/MINOR/PATCH classification for instance diffs as well:**
  - MAJOR: entity removed, type or kind changed, ownership changed.
  - MINOR: new entity or new relation.
  - PATCH: description or label change.

  This drives both the notification policy and the review policy in Q5.
- **Retention suggestion** (an inference, not a sourced standard):
  - Release-pinned snapshots and anything cited by an answer or issue: retain for the audit period, e.g. per internal policy, often several years.
  - Daily run diffs: retain long-term, since they are cheap.
  - Full daily snapshots: compact after N days.

### Gaps
- No source was found on specific regulatory retention requirements for internal platform-catalog KGs. These depend on the organisation (SOX, ISO 27001 change-management evidence, etc.).
- No published system was found that stamps LLM assistant answers with KG snapshot IDs. This appears to be an emerging practice without canonical references.

## Q5. Detecting and reviewing meaningful instance changes vs auto-accepting routine ones

### Takeaway
No standard exists. The best-supported building blocks are:
- semantic change classification (DataHub MAJOR/MINOR/PATCH; OpenMetadata Major.Minor);
- per-source diffs between harvest runs (RDF Patch add/delete sets);
- SHACL validation against the git-curated shapes, which flags instance data that the current ontology cannot express;
- Graphiti-style invalidation, so nothing is lost when changes are auto-accepted.

Changes that hit the TBox boundary should open an ontology PR. Everything else auto-commits to the ABox log.

### Cited Findings
- DataHub tags each change transaction with a semantic version category (MAJOR/MINOR/PATCH). — [DataHub Timeline API](https://docs.datahub.com/docs/dev-guides/timeline)
- GraphDB's history plugin cannot stage changes for approval. The suggested workaround is access control, which implies approval gating must be built outside the store. — [StackOverflow archive](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/61097427/how-to-set-up-version-control-on-top-of-a-triple-store)
- Graphiti resolves contradictions by invalidating rather than deleting edges, so auto-accepted updates remain auditable. — [Graphiti temporal model](https://mintlify.com/getzep/graphiti/concepts/temporal-model)
- Quit Store and TerminusDB support branch/merge, which allows "staging branch then merge" review workflows for data. — [Quit Store paper](https://arxiv.org/abs/1805.03721v3); [Wikipedia: TerminusDB](https://en.wikipedia.org/wiki/TerminusDB)

### Inferences (design proposal, not sourced practice)
- **Auto-accept (log only):**
  - instance add/remove/update where the class or kind already exists in the ontology and the change passes SHACL;
  - attribute churn such as versions, replicas or labels;
  - ownership changes that match an existing team.
- **Flag for human review (no ontology change):**
  - SHACL violations;
  - mass deletions above a threshold, e.g. more than X% of a source's entities disappearing in one run. This usually means a harvester or credential failure, so quarantine the run graph and do not promote it to "current";
  - orphaned references, such as an unknown team.
- **Auto-open ontology PR (TBox impact):**
  - a new CRD kind/group/version, a new Crossplane XRD/Composition, a new Terraform resource type or a new Backstage entity `kind`/`spec.type` with no mapping to an ontology class;
  - a new OpenAPI schema shape used by many instances;
  - a CRD version deprecation.

  The PR contains a proposed class or SKOS concept stub, sample instances, source evidence (run ID + diff) and an LLM-drafted definition.
- Use the harvest-run named graph as a staging area. Promote to "current" only after the run's gate passes (volume-delta check + SHACL). This gives PR-like governance at run granularity rather than per change.

### Gaps
- No published thresholds or benchmarks for "meaningful change" detection in platform-catalog KGs were found. The thresholds above are illustrative.
- No academic sources were retrieved on ontology-evolution triggers from instance drift (e.g. schema-induction literature). This is worth a targeted follow-up.

## Q6. Real-world examples (Wikidata, DBpedia Databus, Stardog, GraphDB, Neptune, Neo4j, DataHub/OpenMetadata, lakeFS)

### Takeaway
Each production system picks a different point on the spectrum:
- **Wikidata:** statement-level temporal qualifiers plus ranks, with revision history at page level.
- **DBpedia Databus:** immutable dated release snapshots.
- **Data catalogs:** per-aspect or per-entity immutable versions with semantic change categories.
- **Neo4j:** modeling patterns (identity/state, bitemporal) rather than engine features.
- **Stardog:** dropped built-in VCS.
- **GraphDB:** a history plugin.
- **lakeFS:** git semantics over object-storage data.

### Cited Findings
- Wikidata: P580/P582 qualifiers, ranks, and truthy-vs-full RDF behaviour. — [Help:Qualifiers](https://www.wikidata.org/wiki/Help:Qualifiers); [Wikibase RDF notes](https://courses.cs.umbc.edu/graduate/691/fall19/07/notes/24_wikidata/wikibase.pdf)
- Databus: artifact/version split with ISO-date version IDs. — [Databus docs](https://dbpedia.gitbook.io/databus/model/versioning)
- Stardog: VCS deprecated in 7.0 and removed, with bitemporal support planned. — [Stardog community](https://community.stardog.com/t/versioning-in-stardog-7/1700)
- GraphDB: data history and versioning plugin. — [PR Newswire 2020](https://www.prnewswire.co.uk/news-releases/ontotext-s-graphdb-9-2-supports-rdf-to-match-the-expressivity-of-property-graphs-810974555)
- Neo4j: identity/state and bitemporal modeling patterns. — [Neo4j docs](https://neo4j.com/docs/getting-started/data-modeling/versioning/)
- DataHub and OpenMetadata version models. — [DataHub](https://docs.datahub.com/docs/advanced/aspect-versioning); [OpenMetadata](https://newreleases.io/project/github/open-metadata/OpenMetadata/release/0.6.0)
- lakeFS zero-copy branches and commit-ID-per-run. — [lakeFS docs](https://docs.lakefs.io/)
- Graphiti/Zep bitemporal agent memory. — [arXiv 2501.13956](https://arxiv.org/html/2501.13956v1)

### Inferences
- The Backstage/Port → KG pipeline is closest to the DataHub/OpenMetadata model: entity-level versions from automated ingestion. Combining that with a Databus-style release snapshot gives both fine-grained history and citable, reproducible states.

### Gaps
- Amazon Neptune temporal/versioning guidance was not retrieved.
- Wikidata's own dump/revision-based versioning (page revisions, weekly dumps) was not verified in this pass.
- Port's and Backstage's own entity-history capabilities were not researched.
