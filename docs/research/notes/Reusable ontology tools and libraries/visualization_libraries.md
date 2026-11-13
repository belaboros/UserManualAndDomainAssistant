# Reusable visualization tools, components and libraries for ontologies, taxonomies, glossaries and knowledge graphs

Scope: embeddable viewers/components for RDF/OWL/SKOS/SHACL data in the "UserManualAndDomain AI Assistant" (small, focused diagrams in Q&A answers) and the "Reviewer" app (interactive governance views with quality-issue overlays, diffs, approve/reject/merge). Status as of 2026-11-13.

Method note: maintenance and license data (latest release, last push, stars, archived flag, SPDX license) were pulled on 2026-11-13 from the GitHub REST API (`gh api repos/<owner>/<repo>` and `/releases/latest`), the npm registry (`npm view`) and the PyPI JSON API. In the findings, "pushed" means the last push to the repo's default or any branch. Unless a finding says otherwise, the GitHub repo page and npm/PyPI package page are the source.

---

## 1. RDF/OWL/SKOS/SHACL-aware viewers and components: which are reusable as embeddable components?

### Takeaway
**Reactodia (`@reactodia/workspace`) is the only actively maintained, open-source, RDF-native, React-embeddable graph *component*.** It has authoring, validation hooks and a SPARQL/RDF data provider, which makes it the best open base for the Reviewer. Most other RDF-aware tools (WebVOWL, LodLive, Skosmos, pyLODE/Widoco, PoolParty GraphViews, metaphactory, SHACLens, OntoGraf) are whole applications or doc generators, not components. Reuse them as design references, as generators, or through iframes, not as libraries.

### Cited Findings

**Reactodia (Ontodia successor)**
- `@reactodia/workspace` 0.35.2 (2026-08-08). LGPL-2.1-or-later. Repo pushed 2026-11-12. 39 stars. Described as "an open-source fork of Ontodia" for exploring, visualizing and changing data as an interactive graph. — [GitHub](https://github.com/reactodia/reactodia-workspace), [npm](https://www.npmjs.com/package/@reactodia/workspace)
- Ships `RdfDataProvider` (loads N3/RDF.js quads) and `SparqlDataProvider`. The README example loads an OWL Turtle file and places all `owl:Class` instances on a canvas, with layout running in a Web Worker. — [README](https://github.com/reactodia/reactodia-workspace)
- Changelog highlights:
  - 0.28 (2025-02-26): i18n, dark theme, CSS variables, experimental property-value editing.
  - 0.29 (2025-03-24): Web-Worker layouts, elliptical elements.
  - 0.30 (2025-06-15): relation-property authoring, inline entity edit/delete, HTML link labels, React 19 support (17 and 18 still supported).
  - 0.31 (2025-11-15): diagram-only annotations (note elements/links) and `applyAuthoringChanges()`.
  - 0.33 (2026-03-16): editing of entities not on the canvas. Validation receives language and re-validates on undo/redo. Validation results have severity levels and related-property IRIs.
  - 0.34 (2026-03-25): touch support, forms moved to `@reactodia/workspace/forms`, configurable `SparqlDataProvider.lookup()`.
  - 0.35 (2026-06-21): accessibility, `createWorkspace()`.
  - No 1.0 roadmap is mentioned.
  
  — [CHANGELOG](https://github.com/reactodia/reactodia-workspace/blob/master/CHANGELOG.md)
- The original Ontodia (`metaphacts/ontodia`) is archived. Last push 2022-12-11, last GitHub release v0.5.3 (2017). npm `ontodia` 0.12.2 (2022-06-22, LGPL-2.1). — [GitHub](https://github.com/metaphacts/ontodia), [npm](https://www.npmjs.com/package/ontodia)
- metaphacts sells a commercial version with extra features. The Sputniq commercial version was folded into metaphactory in 2019. — [metaphacts Ontodia page](https://metaphacts.com/ontodia) (via search summary)

**metaphactory (commercial platform)**
- Its visual ontology modeling maps to OWL and SHACL elements (since 4.0). Version 5.6 added "compositions" with direct translation to SHACL. Version 5.11 (March 2026) added concurrent modeling. Version 6.0 (2026-07-14) added AI-assisted ontology modeling and "modernized diagram management". — [metaphactory 4.0](https://metaphacts.com/metaphactory-4-0), [5.6](https://metaphacts.com/metaphactory-5-6), [6.0](https://metaphacts.com/metaphactory-6-0)
- Visual instance authoring uses an interactive graph component. — [metaphactory 4.7](https://metaphacts.com/metaphactory-4-7)

**WebVOWL / VOWL**
- MIT. Latest release v1.1.7 (2026-06-04). 1,032 stars. 2026 commits are mostly README updates and a Docker local stack that builds OWL2VOWL from source (2026-06-04), not feature work. — [GitHub](https://github.com/VisualDataWeb/WebVOWL), [commits](https://github.com/VisualDataWeb/WebVOWL/commits)
- Widoco (Apache-2.0, v1.4.26 2026-10-23, pushed 2026-11-02) is actively maintained and is commonly used to bundle WebVOWL into generated ontology docs. — [GitHub](https://github.com/dgarijo/Widoco)

**pyLODE**
- BSD-3-Clause. 3.6.1 released 2026-11-06. Active. Generates static HTML ontology documentation. — [GitHub](https://github.com/RDFLib/pyLODE), [PyPI](https://pypi.org/project/pylode/)

**LodLive**
- MIT. Last push 2020-04-22. No releases. — [GitHub](https://github.com/LodLive/LodLive)

**Generic "RDF visualizer" repos**
- All are small and stale. Examples: `usc-isi-i2/ontology-visualization` (last push 2022), `cpetrakis/RDFVisualizer-webapp` (7 stars, 2025-05), `giacomociti/rdf2dot` (2025-06). — [GitHub search results](https://github.com/search?q=rdf+visualizer&type=repositories)

**OntoGraf (Protégé plugin)**
- `protegeproject/ontograf`: last push 2018-05-27. Desktop Protégé plugin only. — [GitHub](https://github.com/protegeproject/ontograf)

**Skosmos (SKOS vocabulary browser with hierarchy view)**
- Skosmos v3.5 (2026-10-22). Pushed 2026-11-12. License shown as NOASSERTION by GitHub (MIT per the project, unverified this round). — [GitHub](https://github.com/NatLibFi/Skosmos)
- The 3.x frontend was reimplemented with Bootstrap 5 and Vue.js 3. — [3.0-alpha announcement](https://groups.google.com/g/skosmos-users/c/lU-5gEQPoLU)
- 3.3 added keyboard navigation for the sidebar hierarchy. — [Skosmos 3.3 Zenodo](https://zenodo.org/records/5767568/latest)
- The 2026 focus is migrating finto.fi to 3.x. — [roadmap thread](https://groups.google.com/g/skosmos-users/c/3w4tYoxmwos)

**PoolParty GraphViews (Graphwise)**
- Commercial PoolParty add-on with three views: a radial Overview, a Tree View and a Detail View. Exports PNG. Public demo available. The UI guide is dated 2025-08-21. — [PoolParty docs](https://help.poolparty.biz/en/user-guide-for-knowledge-engineers/add-on/poolparty-graphviews.html)
- Graphwise is the merger of Semantic Web Company and Ontotext. — [KMWorld](https://www.kmworld.com/Articles/News/News/Semantic-Web-Company-and-Ontotext-merge-to-rebrand-as-knowledge-graph-and-AI-powerhouse-Graphwise-166526.aspx)

**SHACLens**
- Paper: "SHACLens: A Visualization Workflow for SHACL Violation Exploration in Knowledge Graphs", Frontiers in Bioinformatics 2026 (doi 10.3389/fbinf.2026.1756507), JKU VDS Lab.
- Views: a node-link view combining the ontology with groups of equivalent violations, a projection view clustering nodes with similar errors, a LineUp table joining instance data with violation info, a Class Tree and an LLM assistant.
- Selections propagate across views. It was evaluated on 5,203 violating nodes.

  — [JKU publication page](https://jku-vds-lab.at/publications/2026_frontiers_shaclens/), [Frontiers full text](https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2026.1756507/full)
- Source status: the hosted app redirects to shaclens.caleydoapp.org (`jku-vds-lab/shaclens-redirect`, pushed 2026-02-06). A related repo, `CursedSeraphim/bikg_app` (MPL-2.0, pushed 2026-02-01), carries the SHACLens description. No npm package or reusable component was found. — [shaclens-redirect](https://github.com/jku-vds-lab/shaclens-redirect), [bikg_app](https://github.com/CursedSeraphim/bikg_app)

**Zazuko tools**
- `zazuko/rdf-sketch`: "Sketch RDF in the web browser with immediate visualization". MIT. Pushed 2026-11-06. The npm `@zazuko/rdf-sketch` 0.1.3 dates from 2023-09, so the package is stale but the repo is active. — [GitHub](https://github.com/zazuko/rdf-sketch), [npm](https://www.npmjs.com/package/@zazuko/rdf-sketch)
- `zazuko/SPEX`: introspects SPARQL endpoints to visualize the schema. MIT. v0.2.2 (2025-03-07). Pushed 2026-01-22. — [GitHub](https://github.com/zazuko/SPEX)
- `zazuko/cube-creator`: AGPL-3.0, last GitHub release 2021, pushed 2026-02-22. An RDF Data Cube authoring app, not a viz component. — [GitHub](https://github.com/zazuko/cube-creator)
- `@rdfjs-elements/rdf-editor` 0.5.11 (MIT, 2025-12-22) is a web-component RDF text editor, not a graph viewer. — [npm](https://www.npmjs.com/package/@rdfjs-elements/rdf-editor)

**SHACL tooling adjacent to visualization**
- `@ulb-darmstadt/shacl-form` 4.0.1 (MIT, 2026-11-12) generates forms from SHACL shapes. Usable for edit dialogs. — [GitHub](https://github.com/ULB-Darmstadt/shacl-form), [npm](https://www.npmjs.com/package/@ulb-darmstadt/shacl-form)
- `sparna-git/shacl-play` (LGPL-3.0, pushed 2026-11-13) generates SHACL documentation and diagrams. — [GitHub](https://github.com/sparna-git/shacl-play)

**LinkML generators**
- linkml v1.12.1 (Apache-2.0, 2026-10-13). Diagram-relevant generators: ER Diagrams (`gen-erdiagram`, Mermaid output), the PlantUML generator, and the docs generator (markdown sites with UML class diagrams). — [LinkML generators index](https://linkml.io/linkml/generators/index.html), [GitHub](https://github.com/linkml/linkml)

### Inferences
- Reactodia already has most of the Reviewer primitives: RDF/SPARQL data providers, entity and relation authoring with an change set (`applyAuthoringChanges`), validation with severities, annotations, and custom React element templates. Badges for SHACL violations, duplicates and conflicts could be rendered in custom element templates driven by its validation API. A two-pane before/after diff is not built in and would need custom work.
- LGPL-2.1 is acceptable for an npm dependency that is dynamically bundled in a web app, as long as users can replace or relink the library. Confirm with legal. It is weaker than MIT, so prefer keeping Reactodia as an unmodified dependency.
- Reactodia has a small community (39 stars, essentially one maintainer org). Mitigate the bus-factor risk by isolating it behind an adapter.
- WebVOWL is maintenance-only and not componentized (D3 v3-era app). Use it only through Widoco or an iframe for an "OWL overview" button. Do not build the Reviewer on it.
- SHACLens is the best design reference for a SHACL-violation UX (grouped violations, a coordinated table and class tree), but it is not a reusable library. Re-implement its patterns with Cytoscape.js or Reactodia plus a table grid.
- Skosmos, PoolParty GraphViews and metaphactory are full platforms. Use them as UX references for a taxonomy tree plus a concept detail view, or adopt them as a whole. Their views cannot be embedded as components.
- The LinkML `gen-erdiagram` output (Mermaid) fits the Assistant's "schema snippet" answers directly, if the domain model is also kept in LinkML.

### Gaps
- metaphactory 6.0: it is unclear whether the diagram component is still Ontodia-based, and the licensing and price for embedding were not found.
- The PoolParty GraphViews embedding API and its 2026 changes were not found. The docs reviewed date from 2025.
- The SHACLens source license and reusability are unclear (the hosting repo is unconfirmed).
- No explicit ontodia forks besides Reactodia were found (a GitHub search for "ontodia fork" was empty).
- RDF Visualizer (a specific product) could not be identified as a maintained project.
- The Skosmos license (GitHub shows NOASSERTION) was not verified.

---

## 2. General graph libraries (JS): license, maintenance, scale, editing, React integration, overlays

### Takeaway
**Cytoscape.js is the safest MIT default for small and medium interactive KGs and taxonomies in both apps.** It has compound nodes, rich style selectors (good for status classes and badges) and dagre/ELK/fcose layouts. Use Sigma.js v4 with Graphology for very large overview graphs. Use React Flow (xyflow) when nodes must be rich React cards with edit controls (Reviewer approve/reject cards, before/after panels). Avoid Neo4j NVL: its license limits it to Neo4j products. Commercial options (yFiles, Ogma, KeyLines/ReGraph) add polish and scale but have quote-only pricing.

### Cited Findings

**Cytoscape.js and extensions**

| Package | License | Latest | Activity |
|---|---|---|---|
| `cytoscape` | MIT | v3.35.0 (2026-11-10) | 11.3k stars, pushed 2026-11-10 |
| `cytoscape-dagre` | MIT | 4.1.0 (npm modified 2026-11-10) | — |
| `cytoscape-elk` | MIT | 2.4.0 (2026-11-10) | — |
| `cytoscape-cose-bilkent` | MIT | 4.1.0 (2026-08) | — |
| `cytoscape-popper` | MIT | 4.0.1 (2026-08) | — |
| `cytoscape-edgehandles` (interactive edge drawing) | MIT | 4.0.1 (2026-08) | — |
| `cytoscape-fcose` | MIT | 2.2.0 (npm unchanged since 2023-01) | repo pushed 2026-04-17, 188 stars |
| `cytoscape-expand-collapse` | MIT | 4.1.1 (2024-08) | — |
| `cytoscape-context-menus` | MIT | 4.2.1 (2024-08) | — |
| `cytoscape-node-html-label` | MIT | 1.2.2 (2022) | stale |

Sources: [cytoscape GitHub](https://github.com/cytoscape/cytoscape.js), [npm cytoscape-dagre](https://www.npmjs.com/package/cytoscape-dagre), [npm cytoscape-elk](https://www.npmjs.com/package/cytoscape-elk), [npm cytoscape-fcose](https://www.npmjs.com/package/cytoscape-fcose), [fcose repo](https://github.com/iVis-at-Bilkent/cytoscape.js-fcose), [npm cytoscape-expand-collapse](https://www.npmjs.com/package/cytoscape-expand-collapse), [npm cytoscape-node-html-label](https://www.npmjs.com/package/cytoscape-node-html-label)

**Sigma.js and Graphology**
- `sigma` 4.0.6 (MIT, 2026-11-10). 12.2k stars. — [GitHub](https://github.com/jacomyal/sigma.js), [npm](https://www.npmjs.com/package/sigma)
- v4.0.0 (08 Oct, which the npm dates place in 2026) is a rewrite of the rendering programs:
  - Primitives (node shapes, edge paths, extremities) compiled into a single program.
  - A declarative styles API that replaces most reducers.
  - Labels rendered in WebGL via signed distance fields; WebGL 2 only.
  - Built-in node dragging, native parallel edges and self-loops, depth layers, opacity.
  - Breaking: `hidden` became `visibility`.

  — [sigma releases](https://github.com/jacomyal/sigma.js/releases)
- `graphology` 0.26.0 (2025-02-08, MIT, pushed 2026-11-10). `graphology-layout-forceatlas2` 0.10.1 (2024-11). `@react-sigma/core` 6.0.0 (MIT, 2026-10-14). — [graphology GitHub](https://github.com/graphology/graphology), [npm @react-sigma/core](https://www.npmjs.com/package/@react-sigma/core)

**AntV G6 v5**
- `@antv/g6` 5.1.1 (MIT; GitHub release 2026-04-17, npm modified 2026-09-21). 12.4k stars. Pushed 2026-11-13. `@antv/graphin` 3.0.5 is the React wrapper. — [GitHub](https://github.com/antvis/G6), [npm](https://www.npmjs.com/package/@antv/g6), [npm graphin](https://www.npmjs.com/package/@antv/graphin)
- v5 features:
  - Built on `@antv/g` with Canvas, SVG and WebGL renderers.
  - Rust/WASM and GPU layouts via `@antv/layout-wasm`.
  - Built-in combos with collapse/expand.
  - React nodes via `@antv/g6-extension-react`, plus 3D and SSR extensions.
  - UMD bundle shrank from 1.8 MB (v4) to 0.96 MB (v5).

  — [G6 what's new](https://g6.antv.antgroup.com/en/manual/whats-new/feature), [G6 extensions](https://g6.antv.antgroup.com/en/manual/graph/extensions)

**vis-network**
- 10.1.5. Dual-licensed Apache-2.0 OR MIT. Pushed 2026-11-13. 3.6k stars. — [GitHub](https://github.com/visjs/vis-network), [npm](https://www.npmjs.com/package/vis-network)

**React Flow / xyflow**
- `@xyflow/react` 12.12.1 (MIT, 2026-11-08). 39k stars. Pushed 2026-11-12. — [GitHub](https://github.com/xyflow/xyflow), [npm](https://www.npmjs.com/package/@xyflow/react)

**D3 hierarchy**
- `d3-hierarchy` v3.1.3 (ISC, 2026-11-03). — [GitHub](https://github.com/d3/d3-hierarchy)

**ECharts**
- `echarts` 6.1.0 (Apache-2.0, 2026-05-19). 67.7k stars. `echarts-for-react` 3.0.6 (MIT). — [GitHub](https://github.com/apache/echarts), [npm echarts-for-react](https://www.npmjs.com/package/echarts-for-react)

**ngraph**
- `ngraph.graph` 20.1.2 (BSD-3-Clause, 2026-02-14). `vivagraphjs` 0.12.0 last published 2022. — [GitHub](https://github.com/anvaka/ngraph.graph), [npm vivagraphjs](https://www.npmjs.com/package/vivagraphjs)

**Other WebGL options**
- `@cosmos.gl/graph` 3.6.0 (MIT, 2026-11-04; repo `cosmosgl/graph`, 1.3k stars) is GPU force layout for very large graphs. Note: the older `@cosmograph/cosmos` 3.4.1 is CC-BY-NC-4.0, which is non-commercial. — [GitHub](https://github.com/cosmosgl/graph), [npm @cosmos.gl/graph](https://www.npmjs.com/package/@cosmos.gl/graph), [npm @cosmograph/cosmos](https://www.npmjs.com/package/@cosmograph/cosmos)
- `reagraph` 4.32.0 (Apache-2.0, 2026-06), a React WebGL graph. `react-force-graph` 1.48.3 (MIT, 2026-09). — [npm reagraph](https://www.npmjs.com/package/reagraph), [react-force-graph GitHub](https://github.com/vasturiano/react-force-graph)

**Layout engines**
- `elkjs` 0.12.1 (2026-10-28). npm license "EPL-2.0 OR GPL-3.0-or-later". GitHub shows NOASSERTION. — [GitHub](https://github.com/kieler/elkjs), [npm](https://www.npmjs.com/package/elkjs)
- `@dagrejs/dagre` 3.1.3 (MIT, npm 2026-10-24). The GitHub "latest release" shows v2.0.0 (2025-11-23), which is inconsistent with npm 3.x. — [GitHub](https://github.com/dagrejs/dagre), [npm](https://www.npmjs.com/package/@dagrejs/dagre)

**Neo4j NVL**
- `@neo4j-nvl/base` and `@neo4j-nvl/react` 2.1.0 (2026-11-12). The `LICENSE.txt` in the npm tarball states: "NVL may only be used with (i) the Aura software as a service offering … or (ii) the proprietary commercial graph database products developed by Neo4j". — [npm @neo4j-nvl/base](https://www.npmjs.com/package/@neo4j-nvl/base) (LICENSE.txt inspected from the 2.1.0 tarball)

**Ogma (Linkurious)**
- Proprietary license only. 30-day free trial. Has React boilerplates. The `@linkurious/ogma-react` wrapper is Apache-2.0 but requires an Ogma license. — [Ogma trial](https://resources.linkurious.com/ogma-free-trial), [Ogma intro](https://linkurio.us/ogma-js-library-large-scale-graph-visualization/), [Ogma vs sigma comparison](https://doc.linkurious.com/ogma/5.3/compare/sigmajs.html)
- Capterra lists a "$1,851 flat rate per year". This is unverified with the vendor. — [Capterra](https://www.capterra.com/p/10011703/Ogma/)

**KeyLines / ReGraph (Cambridge Intelligence)**
- Subscription licensing. The license term defines access to the SDK and new releases. No public prices. — [CI procurement](https://cambridge-intelligence.com/pricing/procurement/), [G2 KeyLines](https://www.g2.com/products/keylines-graph-visualization-toolkit/pricing)

**yFiles for HTML (yWorks)**
- Commercial, tiered by developers and applications, no royalties. — [yFiles pricing](https://www.yfiles.com/pricing), [license types](https://www.yworks.com/products/yfiles-for-html/license-types)
- A yFiles.NET license agreement says new purchases on or after 2026-08-12 default to term-based licenses rather than perpetual ones. This may also apply to yFiles for HTML; unverified. — [yFiles.NET SLA](https://www.yworks.com/products/yfiles-net/sla)

### Inferences
- **Overlays and badges.** Cytoscape.js selectors and classes (for example `.shacl-violation`, `.duplicate-candidate`, `.added`/`.removed` for diffs), combined with popper tooltips, cover status overlays without custom rendering. Use compound nodes for "merge candidate groups" and for ontology module or namespace grouping. Its HTML-label extension is stale, so put rich badges in popper overlays or SVG background images.
- **Editing.** React Flow gives the richest in-node UI (buttons, forms) for approve/reject/merge cards and side-by-side diffs, but it has no RDF awareness and no large-graph rendering. Pair it with ELK or dagre for hierarchical taxonomy layouts.
- **Scale tiers.**
  - Up to a few hundred nodes (Assistant answer snippets): anything works. Prefer Mermaid/SVG for static output and Cytoscape for small interactive views.
  - Hundreds to low thousands of nodes (Reviewer working views): Cytoscape.js, G6 or Reactodia.
  - More than 10k nodes (whole-KG overview): Sigma v4 or cosmos.gl (WebGL).
- **Sigma v4 maturity.** v4 is about one month old with many breaking changes. Check `@react-sigma` v6 compatibility before adopting.
- **G6 v5** is technically strong (combos, WebGL, React nodes). The trade-off is that much of the documentation and community content is Chinese-first.
- **ELK licensing.** elkjs is EPL-2.0 (or GPL). EPL-2.0 is weak copyleft at the file level and usually fine when the library is used unmodified as a dependency. Cytoscape-dagre (MIT) is the license-simplest hierarchical layout.
- **Do not use NVL.** It is legally restricted to Neo4j Aura and Enterprise customers, and the project's RDF stack is not Neo4j.

### Gaps
- No current, vendor-neutral benchmark numbers for node and edge limits per library were found this round. These widely cited ranges come from prior knowledge, not verified sources: Cytoscape canvas comfortable at about 1–5k elements; Sigma/WebGL at 10^5 nodes. Benchmark with the project's own data.
- Cytoscape.js WebGL renderer status (experimental since ~3.31, per prior knowledge) was not verified this round.
- No library offers a built-in graph diff view. This was not found in any docs reviewed and must be custom-built.
- Actual prices for yFiles, Ogma, KeyLines and ReGraph were not found; quotes are needed.

---

## 3. Diagrams-as-code (Mermaid, Graphviz/viz.js, D2, PlantUML, Structurizr): fitness for small diagrams in AI answers

### Takeaway
**Mermaid is the best fit for LLM-generated, in-answer diagrams.** It is MIT, very active, renders client-side, and LLMs write it reliably. It has hard default limits: 50,000 characters of input and 500 edges. Use viz.js (Graphviz WASM) when deterministic hierarchical layout of ego-networks or taxonomy subtrees matters. D2 and PlantUML are viable but heavier, and Structurizr is C4-specific.

### Cited Findings
- **Mermaid**
  - `mermaid` 12.3.0 (MIT, npm 2026-11-11). 91k stars. Pushed 2026-11-13. — [GitHub](https://github.com/mermaid-js/mermaid), [npm](https://www.npmjs.com/package/mermaid)
  - Config defaults: `maxTextSize` 50000; `maxEdges` 500. Both are in the `secure` list, so only `mermaid.initialize` can change them, not per-diagram directives. — [Mermaid config schema](https://mermaid.js.org/config/schema-docs/config.html)
  - `securityLevel` defaults to `strict` (HTML encoded, clicks disabled). The other levels are `loose`, `antiscript` and `sandbox` (iframe). — [Mermaid config schema](https://mermaid.js.org/config/schema-docs/config.html)
- **viz.js (Graphviz compiled to WASM):** `@viz-js/viz` 3.31.0 (MIT, 2026-09-28). Pushed 2026-11-09. — [GitHub](https://github.com/mdaines/viz-js), [npm](https://www.npmjs.com/package/@viz-js/viz)
- **D2**
  - Repo moved to `d2lang/d2`. MPL-2.0. v0.9.0 (2026-09-07). 25.8k stars. — [GitHub](https://github.com/d2lang/d2)
  - The npm `@terrastruct/d2` 0.1.33 (WASM/JS) was last updated 2025-08-17. — [npm](https://www.npmjs.com/package/@terrastruct/d2)
- **PlantUML:** LGPL-3.0 on GitHub. v1.2026.10 (2026-11-11). Java, so it needs a server or a WASM/Java runtime. — [GitHub](https://github.com/plantuml/plantuml)
- **Structurizr**
  - `structurizr/java` is archived (v5.0.3, 2025-11-21), and `structurizr/lite` and `structurizr/ui` are archived as well. Development continues in `structurizr/structurizr` (Apache-2.0, pushed 2026-11-07). — [structurizr/java](https://github.com/structurizr/java), [structurizr/lite](https://github.com/structurizr/lite), [structurizr/structurizr](https://github.com/structurizr/structurizr)
- **LinkML generators** emit Mermaid ER diagrams and PlantUML. — [LinkML generators](https://linkml.io/linkml/generators/index.html)

### Inferences
- **Assistant pattern.** The backend turns a SPARQL result into a small JSON graph, and a template (not free LLM text) renders it to Mermaid `flowchart`, `classDiagram` or `mindmap`. The frontend renders with `securityLevel: 'strict'`. This keeps the 500-edge limit irrelevant (answer diagrams should have fewer than 50 nodes) and avoids XSS from LLM-authored labels.
- **Choosing the diagram type.**
  - Taxonomy subtrees: Mermaid `mindmap` or `flowchart TD`.
  - Ego-networks and paths between concepts: `flowchart LR`, or Graphviz `dot` for stable layouts.
  - Class/property ("concept card") views: `classDiagram`.
- **Interactivity.** Mermaid output is static SVG; clicks are disabled in strict mode. For "click to expand" in Assistant answers, render the same JSON with Cytoscape.js instead.
- **D2 and PlantUML** add a WASM/Java runtime or server and a license (MPL/LGPL), with no clear gain over Mermaid plus viz.js for this use case.

### Gaps
- Mermaid layout quality and practical performance for diagrams around 100–500 nodes were not benchmarked. The ELK layout option for Mermaid flowcharts exists per prior knowledge but was not verified this round.

---

## 4. Python options for notebooks and prototyping

### Takeaway
**For quick RDF/KG prototyping in notebooks, the best-maintained options are yFiles Graphs for Jupyter (free but proprietary license) and Graphistry (BSD client, server/GPU service).** pyvis and ipycytoscape are stale. Kglab (v1.0.1, Jan 2026) and rdflib together with networkx remain the glue for converting RDF to graphs.

### Cited Findings
- **pyvis:** 0.3.2 on PyPI (2023-02-24), BSD. GitHub last push 2024-04-24. Effectively unmaintained. — [PyPI](https://pypi.org/project/pyvis/), [GitHub](https://github.com/WestHealth/pyvis)
- **ipycytoscape:** 1.3.3 on PyPI (2022-04-04), BSD-3-Clause. Repo pushed 2026-10-05 but with no release since 2022. — [PyPI](https://pypi.org/project/ipycytoscape/), [GitHub](https://github.com/cytoscape/ipycytoscape)
- **kglab:** v1.0.1 (2026-01-23), MIT. — [GitHub](https://github.com/DerwenAI/kglab), [PyPI](https://pypi.org/project/kglab/)
- **rdflib:** 7.6.0 (BSD-3-Clause, 2026-02-13). — [PyPI](https://pypi.org/project/rdflib/)
- **networkx:** 3.7 (BSD-3-Clause, 2026-09-21). — [PyPI](https://pypi.org/project/networkx/)
- **ontospy:** 2.7 (MIT, 2026-10-20) generates ontology docs and visualizations. — [PyPI](https://pypi.org/project/ontospy/)
- **gravis:** 0.1.0 (2021), stale. — [PyPI](https://pypi.org/project/gravis/)
- **yFiles Graphs for Jupyter:** v2.0.0 (2026-08-10).
  - License: "yWorks GmbH – yFiles Graphs for Jupyter Free License" (v1.1). It is proprietary, perpetual and no-charge, granted per user for use within a Jupyter system. — [LICENSE.md](https://github.com/yWorks/yfiles-jupyter-graphs/blob/main/LICENSE.md)
  - Features: hierarchical, organic and circular layouts; attribute-driven color, size and label mapping; neighborhood and search sidebars.
  - Input: networkx, igraph, pygraphviz and dicts. A separate SPARQL integration package exists; rdflib is not mentioned directly. The Neo4j variant is MIT (v2.0.0, 2026-08-25).

  — [GitHub](https://github.com/yWorks/yfiles-jupyter-graphs), [neo4j variant](https://github.com/yWorks/yfiles-jupyter-graphs-for-neo4j)
- **Graphistry:** `graphistry` 0.62.1 (BSD-3-Clause, 2026-11-12). 2.6k stars. Very active. Rendering uses a Graphistry server (hosted or self-hosted). — [GitHub](https://github.com/graphistry/pygraphistry), [PyPI](https://pypi.org/project/graphistry/)
- **Doc generators:** pyLODE 3.6.1 (2026-11-06) and LinkML 1.12.1 (2026-10-13) are both Python and active. — [pyLODE](https://pypi.org/project/pylode/), [LinkML](https://pypi.org/project/linkml/)

### Inferences
- **Prototype path.** rdflib (or kglab) produces a networkx graph, which yFiles Jupyter (best UX) or a minimal Cytoscape.js HTML export (same library as production) visualizes. Prefer the latter so prototypes port directly to the web apps.
- **Licensing.** yFiles Jupyter is free to use, but its license is proprietary and limited to Jupyter. It is not reusable in the production web apps.
- **Graphistry** suits only very large exploratory analytics. It adds a server dependency.
- **Avoid pyvis** for new work, given no release since 2023.

### Gaps
- The full yFiles Jupyter license (commercial-use conditions beyond §1.2) was only partially read.
- Graphistry server licensing and pricing were not checked.

---

## 5. Recommendation per use (synthesis)

### Takeaway
Base the stack on open-source parts:
- **Mermaid (+ viz.js)** for static diagrams in Assistant answers.
- **Cytoscape.js** as the shared interactive graph engine for both apps.
- **Reactodia** as the RDF-native exploration and authoring workspace in the Reviewer.
- **React Flow** for card-style review and diff panels.
- **Sigma v4** only if whole-KG overviews exceed a few thousand nodes.

Evaluate yFiles for HTML only if open-source layout or diff quality proves insufficient.

### Cited Findings
- The license and maintenance evidence for each recommended part is in sections 1–4. Key data points:
  - Cytoscape v3.35.0 (2026-11-10, MIT) — [GitHub](https://github.com/cytoscape/cytoscape.js)
  - Reactodia 0.35.2 (LGPL-2.1, authoring and validation) — [CHANGELOG](https://github.com/reactodia/reactodia-workspace/blob/master/CHANGELOG.md)
  - Mermaid 12.3.0 (MIT, 500-edge default limit) — [config](https://mermaid.js.org/config/schema-docs/config.html)
  - @xyflow/react 12.12.1 (MIT) — [npm](https://www.npmjs.com/package/@xyflow/react)
  - sigma 4.0.6 (MIT, WebGL 2) — [releases](https://github.com/jacomyal/sigma.js/releases)
  - NVL restricted to Neo4j products — [npm @neo4j-nvl/base](https://www.npmjs.com/package/@neo4j-nvl/base)

### Inferences

**Assistant answers: concept cards, ego-networks, taxonomy subtrees, paths, compound-resource views**
- **Primary.** A server-side SPARQL query (k-hop, path, subtree) is converted by a deterministic template to Mermaid and rendered client-side in strict mode:
  - concept card: `classDiagram`, or an HTML card;
  - taxonomy subtree: `mindmap` or `flowchart TD`;
  - path or ego-network: `flowchart LR`.
- **Optional interactive upgrade.** The same JSON graph rendered in Cytoscape.js with the dagre layout (trees and paths) or cose-bilkent/fcose (ego-networks), with compound nodes for compound resources.
- **Static export.** viz.js for Graphviz-quality hierarchical SVGs.
- **Schema snippets.** LinkML `gen-erdiagram` (Mermaid), if the model is maintained in LinkML.

**Reviewer: interactive taxonomies, ontologies and KGs with quality overlays, diffs and editing actions**
- **Exploration and authoring of RDF.** Reactodia, using its RdfDataProvider/SparqlDataProvider, its validation API (map SHACL report results to element and link validation with severities) and its authoring change set (as the approve/reject staging layer). Custom element templates render badges.
- **Issue triage views.** Cytoscape.js or React Flow, with status classes for SHACL violations, duplicate and synonym candidates, and conflicts. Compound nodes represent merge-candidate clusters. The context-menus extension provides approve/reject/merge actions.
- **Diffs.** Build a custom view: compute the triple-level delta, then render a union graph with `added`/`removed`/`changed` classes (Cytoscape), or two synchronized panes (React Flow).
- **Taxonomy tree.** Use a tree component (d3-hierarchy, or a plain React tree list as in Skosmos 3) with per-node status chips. A tree list scales better than node-link layouts for deep SKOS hierarchies.
- **SHACL violation analytics.** Take SHACLens patterns (violation grouping, a coordinated table and class tree) as the UX reference and re-implement them.
- **Forms.** Use `@ulb-darmstadt/shacl-form` (MIT) for SHACL-driven edit dialogs.

**Large overview or exploration (both apps, optional)**
- Sigma v4 with Graphology, or cosmos.gl (MIT). Avoid `@cosmograph/cosmos` (CC-BY-NC).

**Prototyping**
- rdflib or kglab to networkx, visualized with yFiles Jupyter (notebook only) or a Cytoscape.js HTML export.

**Avoid or limit**
- Neo4j NVL (license).
- LodLive, OntoGraf, pyvis, gravis, vivagraphjs (stale).
- WebVOWL as a component (maintenance-mode app). Keep it only via Widoco or an iframe.
- Ontodia (archived). Use Reactodia instead.

**Commercial fallback**
- yFiles for HTML (best layouts; licensing moving to term-based) or Ogma/KeyLines, if open-source quality is insufficient for a governance UI at scale. All are quote-only.

### Gaps
- No hands-on validation was done that Reactodia's validation API can display externally computed SHACL reports. This is inferred from changelog entries and needs a spike.
- The LGPL-2.1 (Reactodia) and EPL-2.0 (elkjs) implications for the project's distribution model need legal confirmation.
