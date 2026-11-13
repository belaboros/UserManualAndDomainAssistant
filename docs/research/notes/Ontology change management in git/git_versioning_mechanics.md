# Git versioning mechanics for glossaries, taxonomies, ontologies, KGs and rules (OWL/RDF/Turtle/JSON-LD/SKOS/SHACL)

Research date: 2026-11-13. Maintenance status comes from GitHub API queries run on that date (`pushed_at`, latest release, archived flag). Each tool's repository URL is its source for those status figures.

## 1. Making RDF git-friendly: deterministic serialization, canonicalization, layout, hooks, diffs

### Takeaway
Plain git line diffs only work on RDF when every commit is re-serialized deterministically: sorted subjects, predicates and objects, stable blank node handling and fixed prefixes. The established tools for this are the EDM Council rdf-toolkit (FIBO's pre-commit serializer) and Cool RDF (formerly owl-cli/turtle-formatter). W3C RDFC-1.0 is a canonicalization standard for hashing and signing, not a readable diff format. Blank nodes are the main source of diff noise.

### Cited Findings
- **The problem:** RDF outgoing edges have no order, so one model can be serialized in many valid ways. The turtle-formatter README calls this "a problem when different versions of a model file are compared" (e.g. in git). — [atextor/turtle-formatter](https://github.com/atextor/turtle-formatter)
- **turtle-formatter is archived.** Its contents moved into **Cool RDF** (`cool-rdf-formatter`; CLI `cool`, formerly owl-cli and turtle-formatter). The `atextor/owl-cli` GitHub path redirects to `cool-rdf/cool-rdf`. — [turtle-formatter](https://github.com/atextor/turtle-formatter), [cool-rdf](https://github.com/cool-rdf/cool-rdf)
  - Status: latest release v2.0.1 (2026-07-15), not archived, 32 stars.
  - Cool RDF features: a `write` command that reads Turtle, RDF/XML, N-Triples or N3 and writes configurable, pretty-printed Turtle; an `infer` command (OWL DL reasoning); and a `diagram` command.
- **turtle-formatter ordering controls** (now in cool-rdf-formatter): — [turtle-formatter](https://github.com/atextor/turtle-formatter)
  - `subjectOrder` orders subjects by `rdf:type` (default list starts with rdfs:Class, owl:Ontology, owl:Class, ...).
  - `predicateOrder` defaults to rdf:type, rdfs:label, rdfs:comment, dcterms:description first.
  - `objectOrder` and `prefixOrder` work the same way; items not listed are sorted lexicographically.
  - Other options: `wrapListItems` and comma options.
  - Blank nodes are inlined as `[ ]` where possible. Named blank nodes reuse their existing label or get `gen`+i. Lists always use `( )`.
  - The changelog mentions fixes for "constant blank node ordering" and blank node cycles.
- **EDM Council rdf-toolkit:** — [edmcouncil/rdf-toolkit](https://github.com/edmcouncil/rdf-toolkit)
  - It is the reference serializer for FIBO. Its stated goal is to cut noisy git diffs so reviewers see only semantic changes. It is not FIBO-specific.
  - Sorting:
    - Ontology-subject triples (including imports) are written first.
    - Triples without blank nodes come next.
    - Within that, triples sort by subject, then predicate, then object, with IRIs before blank nodes and RDF collections before other blank nodes.
  - Blank nodes are named `blankXXX`.
  - `--inline-blank-nodes` fails on recursive blank node structures and on blank nodes that appear as subject but never as object.
  - Other options: `--infer-base-iri`, `--use-dtd-subset`, `--short-iri-priority`, `--suppress-named-individuals`, IRI rewriting (e.g. embedding git tags), and line ending/indent options.
  - Outputs Turtle (default), RDF/XML or JSON-LD. Requires Java 11+.
  - Ships a git `pre-commit` hook. You copy the hook and `rdf-toolkit.jar` into `.git/hooks/`; on each commit it re-serializes RDF files and re-stages them.
  - Status: last push 2026-01-22, last release v2.0 (2024-04-15). Maintained but releases are infrequent.
- **FIBO serialization rules:** — [FIBO ONTOLOGY_GUIDE](https://github.com/edmcouncil/fibo/blob/master/ONTOLOGY_GUIDE.md)
  - FIBO is checked in as RDF/XML produced by the standard serializer.
  - Files must keep DOCTYPE entity declarations and abbreviated IRIs, and have no default IRI.
  - Protégé can strip these, and the guide says they "must be rectified prior to checking in any ontology revisions". Editor tools that re-serialize files are therefore a recurring cause of diff noise.
- **Academic precedent (SerVCS, Halilaj et al., 2016):** Git reports false-positive conflicts when two files describe the same ontology but are serialized differently. SerVCS fixes this with a unique serialization on top of git, using Rapper for syntax validation and rdf-toolkit for canonical output. — [SciTePress paper](https://www.scitepress.org/Papers/2016/60546/)
- **W3C RDF Dataset Canonicalization (RDFC-1.0):** — [W3C TR rdf-canon](https://www.w3.org/TR/rdf-canon/), [implementation report](https://w3c.github.io/rdf-canon/reports)
  - W3C Recommendation, 2024-05-21. Produces a canonical N-Quads form of a dataset, including deterministic relabeling of blank nodes.
  - The spec says blank node identifiers are a feature of concrete syntax and are "not intended to be persistent or portable".
  - Pitfalls:
    - Language tag case handling can differ between implementations and give different canonical forms and hashes.
    - The internal hash algorithm must be stated for reproducibility.
  - Implementations include Titanium RDFC (Java), rdf-canonize (JS), rdfjs-c14n (TS), Sophia (Rust), Ruby RDF::Normalize, RDF.ex (Elixir) and zkp-ld/rdf-canon (Rust).
  - The `digitalbazaar/rdf-canonize` repo's last push was 2025-11-20. — [repo](https://github.com/digitalbazaar/rdf-canonize)
- **ROBOT diff vs. text diff:** `robot diff` compares two ontologies "ignoring differences in file structure". Two files with the same logical content but different serialization do not show as changes. Unix `diff` does show them. — [ROBOT diff docs](https://robot.obolibrary.org/diff)

### Inferences
- Recommended stack:
  - Pick one canonical serializer: rdf-toolkit, or cool-rdf for Turtle with a configurable predicate order. Run it in a pre-commit hook (e.g. the `pre-commit` framework, or rdf-toolkit's hook) and as a CI check that fails if re-serializing changes any file.
  - Use RDFC-1.0 N-Quads only for content hashing or "did the graph change" checks, not as the reviewed source. N-Quads are one triple per line, so they diff well but are unreadable for humans.
- **Blank node strategy:**
  - Avoid blank nodes in curated content wherever possible. Use IRIs for concepts, SHACL shapes (`sh:property` nodes can be IRIs) and reified statements.
  - OWL restrictions and RDF lists unavoidably use blank nodes. Keep them inline so their serialization is anchored to a named subject.
- **File layout:**
  - One file per module or team-owned namespace (FIBO style) fits federated ownership and CODEOWNERS.
  - One file per concept multiplies files and import or catalog overhead. This is not established practice for OWL; whether it is for SKOS is noted under Gaps.
  - Recommendation: modules per owning team, plus separate files for SHACL shapes, mappings and the release header.
- **Source format choice:**
  - LinkML YAML as the authoring source (already in the toolchain) sidesteps RDF serialization noise for schema-level artifacts. RDF and OWL are then generated build artifacts.
  - The ODK uses a single "edit file" as the source and generates releases. See section 4.
- Line diffs remain useful for review once serialization is canonical. Semantic diffs (ROBOT diff, KGCL via OAK) should be added as the human-facing PR summary.

### Gaps
- The exact sort algorithm and determinism guarantees of `robot convert` and OWLAPI's Turtle and Functional syntax writers were not verified. OBO practice relies on OWLAPI's Functional/OBO output being stable, but no source was fetched for that.
- I found no source on per-concept file layouts for SKOS in git. voc4cat uses a spreadsheet-centric workflow, which was not verified here.
- Whether cool-rdf's formatter is byte-stable across versions is not documented on the main README.

## 2. Semantic diff and merge

### Takeaway
Semantic diff is mature at the OWL axiom level (ROBOT diff with markdown/html output, OAK/KGCL), and RDF-level change logs exist (Jena RDF Patch). Semantic merge is not solved in mainstream git tooling. I found no maintained RDF git merge driver; the research prototypes (Quit Store) are dormant. The practical defense is canonical serialization plus small, team-scoped modules plus CI re-validation after merge.

### Cited Findings
- **ROBOT diff:** — [ROBOT diff](https://robot.obolibrary.org/diff), [ontodev/robot](https://github.com/ontodev/robot)
  - Formats: `plain` (OWL Functional syntax with IRIs; `--labels true` adds labels), `pretty` (labels and CURIEs), and `html` and `markdown` (Manchester-based).
  - `--left-iri` and `--right-iri` compare against a published release IRI. `--left-catalog` and `--right-catalog` handle differing imports.
  - The docs mention no direct git integration.
  - Status: ROBOT v1.9.11 released 2026-10-01; actively maintained.
- **Diff posted to PRs (OBO/ODK practice):**
  - The OBO Academy describes a `.github/workflows/diff.yml` that runs `robot diff` in markdown format and posts it as a PR comment when a PR to master is opened. FYPO's workflow is the model. — [OBO Academy GitHub Actions](https://oboacademy.github.io/obook/howto/github-actions)
  - Per search snippets, ODK 1.5 added a release-diff action that posts diffs as PR comments. — [ODK releases](https://github.com/INCATools/ontology-development-kit/releases) (snippet; not fully verified)
- **KGCL (Knowledge Graph Change Language):** a LinkML-based data model for ontology change operations. — [INCATools/kgcl](https://github.com/INCATools/kgcl)
  - Status: last push 2026-02-11.
  - OAK (Ontology Access Kit, v0.7.4, active as of 2026-11-06) is the companion Python library and CLI. — [ontology-access-kit](https://github.com/INCATools/ontology-access-kit)
  - `ontobot-change-agent` applies KGCL changes from GitHub issues to ontologies, but its last push was 2024-12-01, so it looks dormant. — [ontobot-change-agent](https://github.com/INCATools/ontobot-change-agent)
- **`balhoff/owl-diff`:** small (2 stars), last push 2026-10-06. — [repo](https://github.com/balhoff/owl-diff)
- **Ecco:** the OWL diff tool (rsgoncalves/ecco) has had no push since 2017-07-05, so treat it as unmaintained. — [repo](https://github.com/rsgoncalves/ecco)
- **Jena RDF Patch / RDF Delta:** — [RDF Patch spec](https://afs.github.io/rdf-delta/rdf-patch.html), [afs/rdf-delta](https://github.com/afs/rdf-delta)
  - Line-based change format:
    - `H` header rows.
    - `TX`/`TC`/`TA` begin, commit and abort a transaction.
    - `PA`/`PD` add and delete prefixes.
    - `A`/`D` add and delete triples or quads.
  - Patches chain into a patch log through `id` and `prev` UUID headers.
  - Status: last push 2026-09-01, but the last release is v1.1.2 from 2022-08-17. Low release cadence.
- **Quit Store merge strategies** (Arndt et al., Journal of Web Semantics 2018): — [arXiv 1805.03721](https://arxiv.org/abs/1805.03721v3), [MEPDaW abstract](https://svn.aksw.org/papers/2019/MEPDaW_DecentralizedCollaboration_Abstract/public.pdf)
  - Strategies: Union, All Ours / All Theirs, Three-Way-Merge on atomic graphs, and Context Merge.
  - A three-way merge can produce no textual conflicts and still introduce semantic contradictions. Context Merge flags a conflict whenever both sides change the same node.
  - In a follow-up evaluation, the three-way merge ran 1000 times with no failures. — [arXiv 1902.10703](https://arxiv.org/pdf/1902.10703)
- **No maintained git merge driver found:** a search found no ready-made RDF/Turtle git merge driver.
  - `oxirs merge` (Rust) does set-union merging of Turtle, N-Triples and RDF/XML and reports conflicts where the same subject and predicate have different objects. It is a standalone tool, not a git driver. — [oxirs merge_command](https://docs.rs/crate/oxirs/latest/source/src/commands/merge_command.rs)
  - SerVCS uses canonical serialization to avoid false conflicts. — [SerVCS](https://www.scitepress.org/Papers/2016/60546/)

### Inferences
- **Concurrent cross-team PRs:**
  1. Canonical serialization removes false-positive conflicts.
  2. Module or file ownership (CODEOWNERS per team module) reduces true conflicts.
  3. Rebase-and-revalidate: required status checks that re-run SHACL, reasoning and tests on the merge result, using GitHub merge queues so the post-merge state is validated.
  4. Use a custom `.gitattributes` merge driver only for N-Triples or N-Quads files, where union merge of sorted lines is semantically safe for additions but not for deletions or modifications.
- A Context-Merge-style rule ("both branches touched the same subject → human review") is easy to implement in CI. Run ROBOT diff or KGCL diff of base→A and base→B and intersect the changed subjects. It is a good fit for the Reviewer AI assistant to flag.
- KGCL is the most promising machine-readable change record. It is LinkML-based, which matches the proposed LinkML toolchain. It could serve as the changelog format and as the input format for AI-proposed changes.

### Gaps
- The maintenance status of Bubastis (EBI), OWLDiff (Protégé plugin) and the Protégé "compare ontologies" feature was not verified; no GitHub repo was located.
- No verified source on whether `oaklib diff` emits KGCL directly in its current release (it is widely reported to, but not fetched here).
- The ODK release-diff action details (YAML, Docker image) were not retrieved.

## 3. Versioned triplestores and querying history

### Takeaway
Use git as the system of record and load each release into a separate named graph or separate repository of an ordinary store for "as of version X" SPARQL queries. The dedicated archive and versioning stores are mostly dormant academic prototypes (Quit Store, R43ples, OSTRICH, BEAR). Stardog removed its built-in versioning. TerminusDB is active and git-like but is a JSON-document/WOQL system rather than a SPARQL/RDF store. GraphDB has a history plugin (syntax not verified).

### Cited Findings
- **Quit Store** (git-backed quad store with SPARQL 1.1 read/write; branches and merges map to git commits): last push 2024-06-27, last release 0.26.0 (2022-02-02). Effectively dormant. — [AKSW/QuitStore](https://github.com/AKSW/QuitStore), [arXiv 1805.03721](https://arxiv.org/abs/1805.03721v3)
- **R43ples:** last push 2020-11-17, so dormant. — [plt-tud/r43ples](https://github.com/plt-tud/r43ples)
- **OSTRICH:** last push 2025-08-21, only release 1.0.0 (2017). — [rdfostrich/ostrich](https://github.com/rdfostrich/ostrich)
- **BEAR benchmark** (RDF archives): repo last pushed 2021-06-30. — [rdfostrich/BEAR](https://github.com/rdfostrich/BEAR)
- **TerminusDB:** — [terminusdb/terminusdb](https://github.com/terminusdb/terminusdb), [TerminusDB time travel docs](https://terminusdb.com/docs/time-travel-to-previous-commits), [Wikipedia](https://en.wikipedia.org/wiki/TerminusDB)
  - Very active: last push 2026-11-13, v12.1.0-rc2 on 2026-11-03, about 3.5k stars.
  - Stores schema-enforced JSON documents as a graph. Every commit is an immutable delta layer.
  - Supports branching, and you can query any commit by pinning the commit ID. Query languages are WOQL (Datalog-based) and document queries.
  - None of the retrieved sources mention SPARQL or RDF import/export.
- **Stardog:** lightweight versioning (`vcs` commands) was deprecated around 7.0 and then removed. Community answers point to bitemporal modeling instead. — [Stardog community](https://community.stardog.com/t/versioning-in-stardog-7/1700), [migration guide](https://docs.stardog.com/additional-resources/migration-guide)
- **GraphDB:** has a documented "data history and versioning" plugin. A GraphDB 10.6.x changelog item adds distinguishing history plugin transactions and tracking the user who made a change. The official doc page returned 404 at the guessed URL, so the query syntax was not verified. — [StackOverflow mirror](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/64206790/get-the-timestamp-of-insert-sparql-query-in-graphdb), [GraphDB changelog](https://www.softpedia.com/progChangelog/GraphDB-Free-Changelog-252783.html)
- **Oxigraph:** very active (v0.5.13 released 2026-10-22). It is a plain SPARQL store; no versioning features were verified. — [oxigraph/oxigraph](https://github.com/oxigraph/oxigraph)
- **Other approaches:**
  - StarVers: versioning by timestamped RDF-star annotated triples, evaluated against GraphDB and Jena TDB2. — [SWJ StarVers](https://www.semantic-web-journal.net/content/starvers-versioning-and-timestamping-rdf-data-means-rdf-approach-based-annotated-triples)
  - OpenCitations time-agnostic-library: time-travel SPARQL over provenance-tracked change histories, supporting GraphDB among other stores. — [time-agnostic-library](https://opencitations.github.io/time-agnostic-library)
  - ConVer-G: concurrent versioning of KGs. — [arXiv 2409.04499](https://arxiv.org/pdf/2409.04499)

### Inferences
- **Pragmatic pattern:**
  - Load each release (git tag) into a named graph keyed by the versionIRI, e.g. `GRAPH <https://w3id.org/acme/svc/2026-11-01/>`, in Oxigraph, Fuseki or GraphDB.
  - "As of version X" then becomes `FROM <versionIRI>`, and cross-version diffs are SPARQL `MINUS` queries between graphs.
  - Keep "latest" as a separate graph or an alias.
  - This avoids depending on dormant versioned stores, and git stays the audit trail.
- For fine-grained "who changed what, when" between releases, store RDF Patch or KGCL change records per merged PR alongside the git history, rather than relying on a store's history plugin.

### Gaps
- GraphDB history plugin syntax and edition availability (it may be Enterprise-only) were not verified.
- The current Stardog bitemporal or versioning feature set was not verified against official docs.
- Whether TerminusDB supports RDF/Turtle import or SPARQL in v11/v12 was not verified.
- Oxigraph has no confirmed time-travel feature.

## 4. Release mechanics

### Takeaway
The OBO/ODK convention is the most codified release process:
- dated `owl:versionIRI` values (`.../releases/YYYY-MM-DD/...`)
- several release artifacts (base, full, simple, basic, non-classified) generated by ROBOT
- git tags and GitHub releases
- PURLs redirecting to versioned files

FIBO uses dated versionIRIs per module, mandatory change notes and maturity levels.

### Cited Findings
- **ODK release artifacts:** — [OBO Academy release artefacts](https://oboacademy.github.io/obook/reference/release-artefacts/)
  - **full** (required): all logical axioms plus inferred subsumptions. Pipeline: merge imports and components → reason (ELK) → relax → reduce → annotate IRIs.
  - **base** (required): the ontology's own axioms only. The page links to a separate spec and does not define it.
  - **non-classified:** the unmodified editor file with imports merged.
  - **simple:** subclass and existential restrictions only, foreign axioms removed.
  - **basic:** an OBO DAG keeping part_of by default.
  - **simple-non-classified:** transient.
  - Every artifact is annotated with ontology IRI `$(ONTBASE)/$@` and versionIRI `$(ONTBASE)/releases/$(TODAY)/$@`.
- **ODK status:** v1.6.1 (2026-03-10), last push 2026-11-09. Active. — [ODK](https://github.com/INCATools/ontology-development-kit)
- **FIBO:** — [FIBO ONTOLOGY_GUIDE](https://github.com/edmcouncil/fibo/blob/master/ONTOLOGY_GUIDE.md), [edmcouncil/fibo](https://github.com/edmcouncil/fibo)
  - Embedded versionIRI form: `https://spec.edmcouncil.org/fibo/ontology/<domain>/YYYYMMDD/<module>/.../<ontology>/`. Revised with every agreed change and accompanied by a change note.
  - Non-versioned resource IRIs stay stable.
  - Each ontology header declares a maturity level (release / provisional / informative).
  - Release-level content must be consistent under multiple OWL 2 reasoners.
  - Git `master` is the "gold source", and published IRIs can differ from source IRIs (rewritten at publish time).
  - Releases are tagged quarterly (latest: `master_2026Q3`, published 2026-10-20).
- **w3id.org:** the permanent-identifier redirect service is managed via the GitHub repo perma-id/w3id.org (per-namespace `.htaccess` PRs). Very active: last push 2026-11-13. — [perma-id/w3id.org](https://github.com/perma-id/w3id.org)
- **Documentation and publishing tools (all actively maintained):**
  - Widoco v1.4.26 (2026-10-23). — [dgarijo/Widoco](https://github.com/dgarijo/Widoco)
  - pyLODE 3.6.1 (2026-11-06). — [RDFLib/pyLODE](https://github.com/RDFLib/pyLODE)
  - Skosmos v3.5 (2026-10-22). — [NatLibFi/Skosmos](https://github.com/NatLibFi/Skosmos)
  - voc4cat-tool v1.2.0 (2026-09-22). — [nfdi4cat/voc4cat-tool](https://github.com/nfdi4cat/voc4cat-tool)
  - LinkML v1.12.1 (2026-10-13). — [linkml/linkml](https://github.com/linkml/linkml)
  - QUDT v3.5.3 (2026-10-20). — [qudt/qudt-public-repo](https://github.com/qudt/qudt-public-repo)
- **Other real-world repos:** schema.org (last push 2026-11-12) and Gene Ontology go-ontology (last push 2026-11-13) are active. — [schemaorg](https://github.com/schemaorg/schemaorg), [go-ontology](https://github.com/geneontology/go-ontology)
- **OWL 2 version properties:** OWL 2 defines an ontology IRI plus an optional version IRI. `owl:priorVersion`, `owl:backwardCompatibleWith` and `owl:incompatibleWith` are annotation properties for linking versions. — [OWL 2 Structural Spec §3.1](https://www.w3.org/TR/owl2-syntax/#Ontology_IRI_and_Version_IRI)

### Inferences
- **Recommended for the enterprise system:**
  1. Stable term IRIs (never versioned) and a stable ontology IRI. versionIRI = `.../releases/YYYY-MM-DD/<module>.ttl` (ODK style), or SemVer if consumers need compatibility signals.
  2. `owl:versionInfo` set to the tag. `owl:priorVersion` points to the previous versionIRI. Add `owl:incompatibleWith` on breaking changes.
  3. A git tag for each release, plus a GitHub release with artifacts: full (reasoned), base (module only), simple/SKOS export, SHACL shapes, the JSON-LD context, and generated docs (Widoco/pyLODE).
  4. Redirect rules (w3id or an internal PURL server) from the versionIRI to the tagged artifact, and from the ontology IRI to latest.
  5. A changelog generated from ROBOT diff or KGCL between the previous tag and the new one.
- **Deprecation:** use `owl:deprecated true` plus a replacement pointer (OBO convention `IAO:0100001` "term replaced by"; for SKOS, `dct:isReplacedBy`) rather than deleting terms. This is not verified in a fetched source here; take it from OBO principles and the voc4cat docs.
- **JSON-LD context versioning:** publish the context at a versioned URL alongside the release and keep the unversioned URL as a redirect to the latest version.

### Gaps
- Not fetched or verified:
  - schema.org's release process (versioned `data/releases/<ver>/` directories and its release notes practice)
  - the EU Publications Office / EU Vocabularies process (VocBench / ShowVoc)
  - QUDT's release process
  - the GO release pipeline
  - Skosmos support for multiple vocabulary versions
  - JSON-LD context versioning best practice
  - the internals of voc4cat's release and versioning workflow
- I found no verified source for a standard changelog generator beyond ROBOT diff and KGCL.

## 5. CI pipeline for change validation

### Takeaway
The standard OBO/ODK pattern runs `make test` in the ODK Docker image on every PR, and a separate workflow posts a ROBOT diff as a PR comment. FIBO runs SPARQL-based "hygiene tests" plus checks that multiple reasoners find the ontology consistent. All the core validator tools are actively maintained as of November 2026.

### Cited Findings
- **ODK-style QC** runs:
  - `robot report`, a set of SPARQL-based QC checks with ERROR, WARN and INFO levels that is customisable
  - reasoning (ELK or HermiT) for consistency and unsatisfiable classes
  - SPARQL `verify` queries, which fail CI if a query returns any rows

  A diff workflow posts `robot diff --format markdown` output as a PR comment. — [OBO Academy GitHub Actions](https://oboacademy.github.io/obook/howto/github-actions), [ROBOT diff](https://robot.obolibrary.org/diff)
- **Gist example:** a GitHub Gist by J. Balhoff runs `robot diff` with markdown output, escapes it as JSON and posts it to the GitHub API. — [gist](https://gist.github.com/balhoff/6c0d434b1601de4d4006bff76b858ac1)
- **FIBO hygiene tests:** run automatically on GitHub updates. 21 categories, including:
  - untyped references and domain/range crossing for subproperties
  - required labels, definitions and ontology metadata
  - non-circular imports and hierarchies
  - unique labels
  - no explicit `owl:Thing`
  - avoiding punning and "min 1" cardinality
  - no use of deprecated resources
  - detecting reasoning performance bottlenecks

  Release-maturity content must be consistent under multiple OWL 2 reasoners. — [FIBO ONTOLOGY_GUIDE](https://github.com/edmcouncil/fibo/blob/master/ONTOLOGY_GUIDE.md)
- **Validators (status):**
  - pySHACL v0.40.2 (2026-10-28; canonical repo is RDFLib/pySHACL; the older ashleysommer/pySHACL repo has been stale since 2019). — [RDFLib/pySHACL](https://github.com/RDFLib/pySHACL)
  - TopQuadrant SHACL API (Java/Jena), last push 2026-06-30. — [TopQuadrant/shacl](https://github.com/TopQuadrant/shacl)
  - zazuko rdf-validate-shacl (JS), 2026-04-02. — [zazuko/rdf-validate-shacl](https://github.com/zazuko/rdf-validate-shacl)
  - Sparna xls2rdf, Excel → SKOS/OWL/SHACL, active 2026-11-09. — [sparna-git/xls2rdf](https://github.com/sparna-git/xls2rdf)
- **OLIVAW (2025):** an arXiv paper on ACIMOV's GitHub robot for agile collaborative ontology development. Not fetched. — [arXiv 2510.17184 via fugumt](https://fugumt.com/fugumt/paper_check/2510.17184v1_enmode)

### Inferences
- **Suggested PR pipeline** (GitHub Actions with required checks):
  1. Syntax parse and canonical-serialization check: fail if re-serializing changes the files.
  2. LinkML schema validation and generation.
  3. pySHACL against shapes, including SKOS integrity shapes (e.g. a single prefLabel per language, no orphan concepts).
  4. `robot reason` for consistency.
  5. `robot report` with a custom profile.
  6. Competency questions as SPARQL `ASK`/`SELECT` tests (`robot verify` or a pytest harness) with expected results.
  7. Breaking-change detection: removed or renamed IRIs without deprecation (diff of the IRI set from the previous tag).
  8. `robot diff` markdown posted as a PR comment.
  9. The Reviewer AI assistant consumes the diff and KGCL output to write a natural-language review.
- Merge queues make sure checks run against the actual post-merge state, which matters for cross-team concurrent PRs.

### Gaps
- The exact ODK `make test` targets and the Docker image tag for v1.6.x were not retrieved.
- OLIVAW details were not verified.
- No benchmark data on CI runtime for reasoning over large modules.

## 6. Real-world examples: summary of verified status

### Takeaway
Every major reference project is actively maintained on GitHub as of November 2026. Only FIBO's and OBO/ODK's change-management mechanics were verified in detail here. The others are confirmed active, but their processes were not fetched.

### Cited Findings
- **OBO/ODK:** dated releases, multiple artifacts, ROBOT QC, PR diffs. — [release artefacts](https://oboacademy.github.io/obook/reference/release-artefacts/), [ODK](https://github.com/INCATools/ontology-development-kit)
- **FIBO:**
  - rdf-toolkit pre-commit serialization
  - dated per-module versionIRIs and change notes
  - maturity levels
  - hygiene tests
  - quarterly tags (`master_2026Q3`)

  — [FIBO guide](https://github.com/edmcouncil/fibo/blob/master/ONTOLOGY_GUIDE.md), [rdf-toolkit](https://github.com/edmcouncil/rdf-toolkit)
- **Other active repos:**
  - schema.org: about 6.3k stars, last push 2026-11-12.
  - QUDT: v3.5.3.
  - Gene Ontology: pushed 2026-11-13.
  - Finto-data (the Finnish national vocabularies feeding Skosmos): pushed 2026-11-13.

  — [schemaorg](https://github.com/schemaorg/schemaorg), [QUDT](https://github.com/qudt/qudt-public-repo), [GO](https://github.com/geneontology/go-ontology), [Finto-data](https://github.com/NatLibFi/Finto-data)
- **Blazegraph** is archived (2023). Do not choose it as a triplestore. — [blazegraph/database](https://github.com/blazegraph/database)

### Inferences
- FIBO is the closest analogue to an enterprise, multi-team, git-native OWL program. OBO/ODK is the most reusable automation (Docker, Makefile, GitHub Actions). Combining FIBO's per-module ownership and maturity levels with ODK's release automation fits the target system well.

### Gaps
- EU Vocabularies, schema.org, QUDT and GO release processes were not researched in depth (tool-call budget). The report writer should treat them as status-only.
