# Visualization of Taxonomies, Ontologies and Knowledge Graphs for Enterprise Platform Domain Assistants

Scope: tools, visual techniques, evidence on effectiveness, and automatic view generation for (a) platform teams governing glossary/taxonomy/ontology/KG quality (RDF/OWL/SKOS/SHACL) and (b) product teams who need quick concept explanations. Research done 2026-11-13 with a limited budget of about 16 tool calls. Evidence (peer-reviewed or primary docs) is marked separately from vendor or third-party claims. Some items come from search-result summaries rather than full-text reads, and they are flagged where that matters.

## 1. Tools that render RDF/OWL/SKOS visually and can be embedded or are open (maturity, licensing, scale)

### Takeaway
There is no de-facto standard for ontology visualization. The open, embeddable options split into two groups:
- **RDF-native explorers** such as VOWL/WebVOWL and Ontodia → Reactodia. These are good for schema-level OWL views and incremental exploration.
- **Generic graph renderers** such as Sigma.js, Cytoscape.js, G6 and NVL. You have to feed them a projected subgraph yourself, but they scale and style far better.

Commercial suites (PoolParty/Graphwise GraphViews, yFiles, GraphXR, Bloom) offer polish but have licensing constraints. For an assistant, the practical pattern is to query a focused subgraph with SPARQL and render it in a generic library or as diagrams-as-code. A whole-ontology viewer is the wrong fit.

### Cited Findings
**Ontology-specific tools and surveys**
- A Semantic Web Journal paper that surveys ontology visualization tools from a use-case perspective (with a prototype tool recommender) states that "no visualization method has been accepted by the majority of the semantic web community as de facto standard." — [SWJ swj3622](https://www.semantic-web-journal.net/system/files/swj3622.pdf). I saw this only via a search summary; the full PDF could not be parsed.
- A separate SWJ survey covers tools for visualizing ontology *changes*. — [SWJ swj755/swj672 (search result)](https://www.semantic-web-journal.net/system/files/swj755.pdf)
- **VOWL** (Visual Notation for OWL Ontologies), Lohmann et al., *Semantic Web* 7, 2016:
  - Its stated aim is a notation that casual users can understand with little training.
  - The paper reports three user studies and concludes VOWL gives "comparatively intuitive" visualizations.
  - Reviewers criticised the study design: the second study used expert users although VOWL targets lay users.
  - I found no published scalability or performance study for WebVOWL. The "benchmark ontology" in the paper tests coverage, not performance.
  - Sources: [SWJ VOWL page](https://www.semantic-web-journal.net/content/visualizing-ontologies-vowl), [SAGE](https://journals.sagepub.com/doi/full/10.3233/SW-150200)
- **ShapeVOWL** is a VOWL-based visual notation for SHACL/RDF constraints (shapes). — [ShapeVOWL spec](https://knowledgeonwebscale.github.io/shapevowl-spec/)
- **Ontodia and Reactodia**:
  - Ontodia is a JS library for interactive RDF graph exploration, distributed under LGPL-2.1. metaphacts sells a commercial edition with extra features and support. — [Ontodia README](https://cdn.jsdelivr.net/npm/ontodia@0.12.2/README.md), [metaphacts](https://metaphacts.com/ontodia)
  - One directory lists the metaphacts/ontodia repo as archived. — [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2Fmetaphacts%2Fontodia)
  - **Reactodia** (`@reactodia/workspace`) is the active open-source TypeScript fork. It supports exploring *and editing* graph data. — [Reactodia docs](https://reactodia.github.io/docs), [npm](https://www.npmjs.org/package/@reactodia/workspace)
  - "Graph Explorer" is another LGPL-2.1 fork for SPARQL endpoints. — [npm graph-explorer](https://npmjs.com/package/graph-explorer)
- **PoolParty (Graphwise) GraphViews** is an add-on with three views: an Overview, a Tree View of the taxonomy hierarchy, and a Detail View centred on one concept with its broader and narrower concepts. Licensing is not public in the sources I found. — [PoolParty docs](https://help.poolparty.biz/en/poolparty-graphviews/navigating-the-graphviews-user-interface.html), [product page](https://www.poolparty.biz/poolparty-graphviews)

**LinkML diagram generation**
- `gen-erdiagram` emits Mermaid ER diagrams. It can be restricted to one class plus the classes reachable from it (`-c`), and `--format mermaid` drops the markdown fences.
- The docgen framework renders Mermaid class diagrams by default, with PlantUML and ER as alternatives.
- `gen-yuml` depends on the external yuml.me service and carries a "consider deprecating" note.
- Sources: [LinkML ER](https://linkml.io/linkml/generators/erdiagram.html), [docgen](https://linkml.io/linkml/generators/docgen.html), [yuml](https://linkml.io/linkml/generators/yuml.html), [PlantUML gen](https://linkml.io/linkml/generators/plantumlgen.html)

**Backstage catalog-graph plugin**
- It visualizes relations between entities, such as ownership, grouping and API relations.
- It provides an entity card (`entity-card:catalog-graph/relations`, off by default) and a full page at `/catalog-graph`.
- Custom relation types can be added by overriding `DefaultCatalogGraphApi` / `ALL_RELATION_PAIRS`.
- The community plugin `@dweber019/backstage-plugin-relations` adds custom relation pairs through a catalog processor. It requires Backstage 1.27 or later.
- Sources: [Backstage API](https://backstage.io/api/stable/modules/_backstage_plugin-catalog-graph.html), [README](https://cdn.jsdelivr.net/npm/@backstage/plugin-catalog-graph@0.6.6/README.md), [dweber019 plugin](https://www.npmjs.com/package/%40dweber019%2Fbackstage-plugin-relations), [Backstage docs](https://backstage.io/docs/getting-started/viewing-entity-relationships)

**Generic graph renderers**
- **Neo4j NVL** was originally the engine behind Neo4j Bloom. It is now a standalone GPU-accelerated library and is "free to use with a Neo4j license". — [Neo4j blog](https://neo4j.com/blog/graph-database/neo4j-graph-visualization-library/), [NVL docs](https://neo4j.com/docs/nvl/current/)
  - Licensing conflict: npm points to a custom LICENSE.txt, and a third-party page says it is for use with Neo4j products only. This is unverified; check the LICENSE.txt before using NVL against an RDF store. — [npm @neo4j-nvl/base](https://npmjs.com/package/%40neo4j-nvl%2Fbase)
- **Sigma.js** renders with WebGL and claims "smooth performance with tens of thousands of nodes and edges" (project's own docs). Edge and label events are disabled by default for performance. The license is MIT per the listing, though one third-party page says Apache-2.0; verify on GitHub. — [Sigma v4 rendering docs](https://v4.sigmajs.org/concepts/rendering/), [performance](https://v4.sigmajs.org/how-to/technical/performance/)
- **Cytoscape.js**:
  - Its renderer switches to coarse level of detail when rendered nodes plus edges reach 4,000 or more (default threshold). — [Cytoscape.js init docs](https://github.com/cytoscape/cytoscape.js/blob/e6541de603f5714f572238573ea06ef17503282b/documentation/md/core/init.md)
  - A competitor (Linkurious Ogma) says it gets sluggish above about 10k elements. This is a vendor claim. — [Ogma comparison](https://doc.linkurious.com/ogma/latest/compare/cytoscape.html)
  - The Cytoscape *desktop* manual claims more than 10,000 nodes at interactive speed. That is the desktop app, not the JS library. — [Cytoscape manual](https://manual.cytoscape.org/en/3.9.0/Rendering_Engine.html)
- **yFiles** is a commercial SDK for Web, Java and .NET. yWorks publishes ontology-visualization use cases. — [yFiles ontology use case](https://www.yfiles.com/solutions/use-cases/visualizing-an-ontology), [KG guide](https://www.yfiles.com/knowledge-graph/guide)
- **Kineviz GraphXR** is proprietary and has a free personal tier and Docker trial images. AlternativeTo lists a subscription of $5,000–15,000/month (third-party, unverified). It can be deployed on-prem or air-gapped. — [AlternativeTo](https://alternativeto.net/software/graphxr/about), [Docker trial](https://hub.docker.com/r/kineviz/graphxr_trial)

### Inferences
- **Schema/ontology view for platform teams:** use Reactodia (LGPL, RDF-native, editable) or a WebVOWL-style view on a *module* of the ontology, never the whole thing.
- **Instance relations (platforms ↔ services ↔ teams ↔ resource kinds):**
  - Use Cytoscape.js (MIT, rich layouts such as compound nodes, which suit compound resources with components) for views up to a few thousand elements.
  - Use Sigma.js for large overviews.
  - Avoid NVL unless Neo4j is already licensed.
- **If the platform already runs Backstage**, the catalog-graph plugin is the cheapest route. Mapping RDF resource kinds and relations into Backstage entities and custom relation pairs gives the views "for free" inside the developer portal.
- **SKOS taxonomies:** a tree or indented list (PoolParty Tree View, Skosmos-style hierarchy) is likely better than a force graph for lookup tasks; see Q3 (Fu et al.).

### Gaps
- Not verified in this pass (only general knowledge, so no claims are made):
  - TopBraid EDG diagram features and licensing.
  - Skosmos hierarchy visualization.
  - Protégé OntoGraf maintenance status.
  - Gephi.
  - AntV G6 license and v5 WebGL capabilities.
  - Structurizr, D2.
- I found no head-to-head scale benchmarks across these libraries from a neutral source.

## 2. Diagrams-as-code generated from the KG; focused views; LLM-generated Mermaid reliability

### Takeaway
Diagrams-as-code (Mermaid, PlantUML, Graphviz, D2, Structurizr) suits chat answers. Generate it **deterministically** from a SPARQL-selected subgraph (ego network, subtree, shortest path) rather than letting an LLM free-write diagram syntax. LLM-written diagram code is measurably unreliable: the only formal benchmark found shows large gaps between models.

### Cited Findings
- **MermaidSeqBench** (IBM Research, arXiv 2511.14967, NeurIPS 2025 workshop):
  - 132 samples, scored by LLM-as-judge on syntax correctness, activation handling, error handling and practical usability.
  - It found "significant capability gaps across models and evaluation modes".
  - The authors state that no formal benchmark or public dataset existed before for evaluating LLM Mermaid generation.
  - It covers sequence diagrams only.
  - Sources: [arXiv](https://arxiv.org/abs/2511.14967), [NeurIPS page](https://neurips.cc/virtual/2025/122389)
- LinkML already provides a deterministic schema → Mermaid/PlantUML path, including the "class + reachable classes" focused view (`gen-erdiagram -c`). — [LinkML ER](https://linkml.io/linkml/generators/erdiagram.html)
- Backstage catalog-graph renders a focused, relation-filtered neighbourhood of one entity (entity card) as well as a full graph page. — [Backstage README](https://cdn.jsdelivr.net/npm/@backstage/plugin-catalog-graph@0.6.6/README.md)

### Inferences
- **Recommended pipeline:**
  1. The user's question selects a view template: ego network (1–2 hops around a concept), subtree (`skos:broader*` / `rdfs:subClassOf*`), path (SPARQL property path or shortest path between two concepts), or compound-resource part-of tree.
  2. A SPARQL CONSTRUCT returns a small subgraph.
  3. A deterministic serializer emits Mermaid flowchart/classDiagram or Graphviz DOT.
  4. Validate it (for example with mermaid-cli parse) before sending it to chat.
  5. The LLM writes only the caption and the 1–3 sentence explanation.
- **Cap chat diagrams at about 15–30 nodes** (see the readability evidence in Q3). When a selection exceeds the cap, truncate with "+N more" aggregate nodes.
- **If an LLM must emit diagram code**, use a parse-validate-repair loop. The benchmark evidence suggests first-pass syntax errors are common for weaker models.

### Gaps
- I found no benchmark for LLM generation of Mermaid flowcharts or class diagrams, or of PlantUML/D2.
- I found no study comparing deterministic versus LLM-authored diagrams in chat.
- Structurizr/C4 and D2 capabilities were not verified in this pass.

## 3. Evidence on effectiveness (readability, ontology visualization studies, tree vs graph vs matrix, diagrams vs text, microlearning)

### Takeaway
The strongest evidence:
- Edge crossings are the main readability killer.
- Node-link diagrams degrade quickly beyond about 50 nodes (dense graphs) or about 100 nodes (sparse graphs) for path tasks.
- Indented lists or trees beat graphs for *search*, while graphs help *relational processing*.
- Matrix vs node-link results are mixed.
- For software documentation, diagrams are *not* reliably better than text for comprehension.

So for busy product teams, short text plus a small focused diagram is the defensible design. A big graph is not.

### Cited Findings
**Graph readability**
- **Purchase et al.:** minimizing edge crossings was "overwhelmingly beneficial" for understanding graph structure, compared with symmetry, angular resolution and orthogonality. More bends and more crossings both reduce understandability. For shortest-path tasks, the crossings *on the path* matter most. — [Purchase, Validating graph drawing aesthetics](https://link.springer.com/chapter/10.1007/BFb0021827); summarised in [arXiv 0810.4431 (eye-tracking on crossings)](https://arxiv.org/pdf/0810.4431.pdf)
- **Körner et al. (hierarchical graphs):** crossings were the most influential variable on response latency. — [via search summary, JGAA](https://jgaa.info/index.php/jgaa/article/download/3102/3028/3669)
- **Yoghourdjian et al. 2018, *Visual Informatics*:** a survey of empirical graph-vis studies. It found that the scalability limits of node-link diagrams are "rarely addressed directly". — [arXiv 1809.00270](https://arxiv.org/abs/1809.00270v1), [Monash](https://research.monash.edu/en/publications/exploring-the-limits-of-complexity-a-survey-of-empirical-studies-/)
- **Follow-up by Yoghourdjian et al.** (25–175 nodes, cognitive-load perspective): people had significant difficulty with shortest-path tasks on high-density graphs above about 50 nodes and low-density graphs above about 100 nodes. — [deepai summary](https://deepai.org/publication/scalability-of-network-visualisation-from-a-cognitive-load-perspective)

**Matrix vs node-link (mixed)**
- **Ghoniem, Fekete & Castagliola (InfoVis 2004):** above about 20 vertices, matrices beat node-link on most tasks, but path finding consistently favoured node-link. — [search summary / IEEE](https://search.isc.ac/inventory/49/2357924.htm)
- **Okoe et al.** (*Network Science*, N=600, 20 or 50 nodes): node-link gave higher accuracy and faster times than the matrix variants. — [Cambridge](https://www.cambridge.org/core/journals/network-science/article/understanding-nodelink-and-matrix-visualizations-of-networks-a-largescale-online-experiment/C293136C4761F09D4C2C328E2BC19287)
- **Quilts replication (2025; 50/100/200 nodes):** node-link beat matrix for path finding at all sizes. — [arXiv 2507.10883](https://arxiv.org/pdf/2507.10883)

**Ontology-specific**
- **Fu, Noy & Storey, eye-tracking study** (*Semantic Web* 8, 2017): indented lists support information *search* better, while graphs support information *processing* (understanding relations) better. — [SWJ](https://www.semantic-web-journal.net/node/861)
- **VOWL:** three user studies found the notation "comparatively intuitive", but reviewers questioned the study design. — [SWJ VOWL](https://www.semantic-web-journal.net/content/visualizing-ontologies-vowl)

**Diagrams vs text in software engineering**
- **Heijstek et al., ESEM 2011:** participants who mainly used text scored significantly better, including on topology questions. Diagrams did not help non-native English speakers. Another summary of the same work says neither format was significantly more efficient. — [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A2920847/view)
- **UML model vs text-only:** no significant difference in surface or deep understanding, for novices or experts. — [Springer EMSE](https://link.springer.com/article/10.1007/s10664-019-09784-9) (attribution per search summary)
- **Design-pattern documentation**, family of 4 experiments, 88 participants: UML class diagrams gave comprehension benefits similar to textual comments. — [academia.edu](https://www.academia.edu/22417252/Documenting_Design_Pattern_Instances_a_Family_of_Experiments_on_Source_Code_Comprehensibility)
- **Umple vs UML:** comparable on simple comprehension tasks. — [uOttawa TR-2011-03](https://www.eecs.uottawa.ca/~tcl/gradtheses/obadreldin/TR-2011-03.pdf)

**Microlearning**
- The peer-reviewed meta-analyses are small: one pooled five studies, and another reports OR 1.87 for retention.
- The robust mechanism is spacing and retrieval practice (Cepeda et al. 2006, 839 assessments).
- Vendor claims such as "80% retention" have no traceable source.
- Sources: [JMTR 2026](https://journals.kln.ac.lk/jmtr/media/attachments/2026/06/30/jmtr_24_22.pdf), [papersflow summary](https://papersflow.ai/research/topics/e-learning-and-covid-19/microlearning-efficacy-meta-analyses)

### Inferences
- **Glossary/taxonomy lookup** ("what is X, where does it sit"): use a breadcrumb or indented tree, consistent with Fu et al.
- **Relational questions** ("what depends on X", "who owns Y"): use a small node-link ego network or path view.
- **Keep chat diagrams well under about 50 nodes.** Prefer hierarchical (Sugiyama/dagre) layouts that minimise crossings, and highlight the answer path.
- **Matrices (DSM-style)** are a reasonable *governance* view for dense service-to-service dependency audits. They are not suitable for product-team explanations.
- **"Concept cards" should lead with text.** The SE evidence does not support diagrams *replacing* text, so diagrams should supplement a short definition.

### Gaps
- I found no study specifically on C4/architecture-diagram onboarding effectiveness (searched; none surfaced).
- I found no controlled study of concept cards or explainer cards inside chat assistants.
- The exact Ghoniem 2005 journal figures and the Purchase 1997 paper details were not read in full text.

## 4. Quality-issue overlays (SHACL violations, duplicates/synonyms, orphans, conflicts, staleness) and visual ontology diffs

### Takeaway
SHACLens (2026) is the most relevant research design for violation exploration. It uses coordinated views (class tree with violation counts, node-link of classes/shapes/grouped violations, UMAP projection, LineUp table, and an LLM chat). Production tools mostly offer tables or grid reports. Ontology diff tooling is mature at the axiom/text level (ROBOT, Bubastis, ecco, OWLDiff), but genuinely *visual* diffs remain immature.

### Cited Findings
- **SHACLens** (Steinparz et al., *Frontiers in Bioinformatics*, 2026), co-designed with a pharma partner:
  - **Views:** node-link of ontology classes, SHACL shapes and grouped violations; a class tree with per-class violation counts; a UMAP projection clustering focus nodes with similar violations; a LineUp table; and an LLM chat that explains violations and drives the dashboard.
  - **Interaction:** selections propagate across all views. Equivalent violations are grouped by default, and only direct violation-object instances are shown.
  - **Evaluation:** a qualitative case study on a transcriptomics KG with 5,203 violating focus nodes. It found schema gaps and an undefined class, and the LLM drafted a SPARQL fix that was reviewed manually. There was no quantitative user study.
  - **Limitations:** clutter when many subtrees are expanded, and slow preprocessing.
  - **Stack:** React/Redux/D3/LineUp, FastAPI, LangChain + GPT-4.1. The code is at GitHub CursedSeraphim/bikg_app; the license is not stated.
  - Sources: [Frontiers](https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2026.1756507/full), [JKU](https://jku-vds-lab.at/publications/2026_frontiers_shaclens/)
- **Other SHACL report UIs:**
  - mjanez shacl-validator imports Turtle reports and shows interactive charts. — [GitHub mirror](https://github.gg22.workers.dev/mjanez/shacl-validator)
  - Roteva shows a grid with violation paths linking to the offending data. — [Roteva](https://roteva.demo.seco.cs.aalto.fi/documentation)
  - The EU ISA² Interoperability Test Bed validator produces PDF or RDF reports. — [Interoperable Europe](https://interoperable-europe.ec.europa.eu/collection/interoperability-test-bed-repository/solution/interoperability-test-bed/news/shacl-validator-user-interface)
  - pySHACL serializes reports as RDF. — [pySHACL](https://github.com/RDFLib/pySHACL)
  - The W3C SHACL 1.2 UI draft notes that implementations may visualise validation messages. — [W3C draft](https://raw.githack.com/w3c/data-shapes/ui/widget-scores/shacl12-ui/index.html)
- **Diffs:**
  - ROBOT `diff` compares ontologies while ignoring serialization differences and produces a text report; it accepts IRIs to compare against releases. — [ROBOT diff](https://robot.obolibrary.org/diff)
  - Bubastis detects asserted logical differences (web and CLI), with XML output that can be styled with XSLT. — [GitHub](https://github.com/EBISPOT/bubastis)
  - ecco (Manchester) links axiom changes to the affected concepts.
  - OWLDiff provides diff/merge and a Protégé plugin. — [OWLDiff](https://kbss.felk.cvut.cz/web/owldiff)
  - owlcompare (pre-alpha) aims at a semantic HTML diff report. It argues that ROBOT and Protégé compare "operate at the axiom level". — [owlcompare FAQ](https://ajala111.github.io/owlcompare/faq/)

### Inferences
- **Overlay design for platform teams.** Reuse the SHACLens pattern in a lighter form:
  - Taxonomy tree with badge counts per concept: SHACL violations, missing definition, orphan (no `skos:broader` / no `rdfs:subClassOf`), duplicate prefLabel or altLabel collisions, and `dcterms:modified` age as a staleness colour.
  - A filterable table as the primary work surface.
  - A node-link drill-down only for the selected concept.
- **Synonym clusters:** render as groups (compound nodes in Cytoscape.js) of `skos:prefLabel`/`altLabel`/`exactMatch` candidates. Flag cross-cluster label collisions in red.
- **Visual diff:**
  - Run ROBOT/Bubastis in CI.
  - Map added, removed and changed classes or concepts onto the tree with green, red and amber colouring.
  - Generate a Mermaid "changed neighbourhood" diagram per PR.
  - This would be custom work, because no mature off-the-shelf visual OWL/SKOS diff was found.

### Gaps
- I found no published user study on staleness heatmaps or on duplicate and conflicting-definition overlays for ontologies.
- Whether TopBraid EDG or PoolParty offer built-in quality-overlay visuals was not verified in this pass.
- The SWJ survey on ontology-change visualization was not read in full.

## 5. Patterns for concept cards / short visual explanations in chat assistants

### Takeaway
I found no direct empirical research on "concept cards" in chat assistants. The design has to be inferred from the adjacent evidence:
- Text is not inferior to diagrams for comprehension.
- Small, low-crossing, focused diagrams are readable.
- Trees suit lookup and graphs suit relations.
- Spacing and retrieval drive retention.

### Cited Findings
- PoolParty GraphViews' Detail View, a single concept with its broader and narrower concepts, is a vendor precedent for a one-concept card. — [PoolParty docs](https://help.poolparty.biz/en/poolparty-graphviews/navigating-the-graphviews-user-interface.html)
- The Backstage catalog-graph entity card is a precedent for an embedded mini relations graph on an entity page. — [Backstage README](https://cdn.jsdelivr.net/npm/@backstage/plugin-catalog-graph@0.6.6/README.md)
- The SHACLens LLM chat demonstrates an assistant that explains graph-quality findings and drives coordinated views. — [Frontiers](https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2026.1756507/full)
- Indented lists help search, and graphs help relational processing. — [Fu et al., SWJ](https://www.semantic-web-journal.net/node/861)
- Microlearning benefits are modest, and the mechanism is spacing and retrieval. — [JMTR 2026](https://journals.kln.ac.lk/jmtr/media/attachments/2026/06/30/jmtr_24_22.pdf)

### Inferences
- **Proposed card template** (an inference, not validated). Every element is generated from the KG with SPARQL; the LLM only paraphrases.
  1. Concept name, type badge (resource kind / service / platform), and owner team.
  2. A definition of at most 2 sentences (`skos:definition`).
  3. A breadcrumb of the broader chain.
  4. A mini diagram of no more than 15 nodes: ego network or part-of tree for compound resources.
  5. Synonyms (altLabels).
  6. A "Don't confuse with" line (siblings or near-synonyms).
  7. Links to the full docs.
  8. A quality badge: last reviewed date, and open SHACL issues, shown to governance users only.
- **Progressive disclosure:** show the card first, with "expand graph" to open the interactive Cytoscape/Reactodia view.
- **Use the same subgraph-selection templates** (ego, subtree, path, components) for both audiences. Platform teams get the quality overlays on top.

### Gaps
- I found no user studies of concept cards or explainer cards in chat UIs.
- I found no evidence on optimal card length or diagram size *inside chat*. The 15-node cap is extrapolated from the graph-readability studies above.
