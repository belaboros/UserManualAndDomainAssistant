# Automated Construction of Glossaries, Taxonomies, Ontologies and Knowledge Graphs from Documents with LLMs

Scope: state of the art (as of Nov 2026), achievable quality, tooling, and pipeline design for a "downloader" that ingests user manuals / technical and business documentation and builds indexes, a glossary, a taxonomy/ontology, and a KG for an expert-like domain assistant. Evidence labels: **[BENCH]** = peer-reviewed or shared-task benchmark number; **[CLAIM]** = author/vendor claim or secondary-source summary that was not checked against primary tables; **[DOC]** = vendor documentation describing behaviour, not quality.

## How well do LLMs perform at term/definition extraction, glossary building, entity/relation extraction, taxonomy induction and ontology learning?

### Takeaway
Quality varies sharply by subtask. LLMs do well at **term typing** (assigning a known term to a type: F1 often 0.7–0.94) and reasonably at **term/type extraction from text** (F1 about 0.6–0.83). They do poorly at **full taxonomy discovery** (is-a F1 about 0.12–0.66 depending on the ontology) and at **schema-constrained triple extraction** against gold standards (F1 about 0.35–0.45 for 2023–24-era models). Ontology *conformance* is far higher than factual precision/recall. Treat LLM outputs as high-recall *candidates* that need canonicalization, validation and (for core terms) human review, not as finished artifacts.

### Cited Findings
**Ontology learning: LLMs4OL challenge (ISWC 2024, ISWC 2025)**
- The 2nd LLMs4OL Challenge (ISWC 2025, Nara) had these tasks: A Text2Onto (extract terms A1 and types A2 from raw documents), B Term Typing, C Taxonomy Discovery (is-a between types), plus non-taxonomic relation extraction. **[DOC]** — [LLMs4OL 2025 site](https://sites.google.com/view/llms4ol2025/challenge-overview); [Overview paper, TIB OCP](https://www.tib-op.org/ojs/index.php/ocp/article/view/2913)
- Organizers' conclusion: the strongest results came from hybrid pipelines that combine commercial LLMs with domain-tuned embeddings and fine-tuning. Specialized domain models helped in biomedical and technical settings. LLMs "excel" at Term Typing and Taxonomy Discovery relative to the other tasks. **[BENCH, qualitative]** — [Overview paper](https://www.tib-op.org/ojs/index.php/ocp/article/view/2913)
- Leaderboard snapshot (16 Jul 2025), as reproduced in a participant paper (team Alexbek). Best F1 per subtask: **[BENCH]** — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1)
  - Text2Onto terms: Scholarly 0.70, **Engineering 0.62**. Text2Onto types: Ecology 0.66, Scholarly 0.83, **Engineering 0.675**.
  - Term typing (few-shot): OBI 0.94, MatOnto 0.67, SWEET 0.69. Blind/unseen domains: 0.76, 0.93, and 0.17 (opaque label set).
  - Taxonomy discovery: OBI 0.40, MatOnto 0.66, SWEET 0.50, DOID 0.18, Schema.org 0.66, PROCO 0.39, FoodOn 0.12, PO 0.48.
- On engineering-domain term extraction the same team reports **precision 0.825 but recall 0.30**: LLMs are conservative and miss many terms. They also report a large validation-to-test gap in taxonomy discovery (domain shift), and very low F1 on sparse taxonomies (FoodOn, DOID). Their approach was retrieval-augmented few-shot prompting (Qwen3-Embedding + TF-IDF keywords) for extraction, embedding ensembles for zero-shot typing, and a small LoRA-tuned encoder with cross-attention for is-a prediction. Their argument: lightweight prompting plus small trainable modules can compete with heavy fine-tuning. **[BENCH + author interpretation]** — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1)

**Schema-guided KG generation: Text2KGBench**
- Text2KGBench (ISWC 2023) has two parts: Wikidata-TekGen (10 ontologies, 13,474 sentences) and DBpedia-WebNLG (19 ontologies, 4,860 sentences). It measures precision/recall/F1 of triples against gold, ontology conformance, and subject/relation/object hallucination. **[BENCH]** — [arXiv 2308.02357](https://arxiv.org/pdf/2308.02357)
- Baseline Vicuna-13B on Wikidata-TekGen averaged **P 0.38 / R 0.34 / F1 0.35**, but **ontology conformance was 0.83** and hallucination about 0.17 for each of subject, relation and object. Per-ontology F1 ranged from about 0.24 (Military) to 0.66 (Space). The authors note that recall counts only against possibly incomplete gold triples. **[BENCH]** — [arXiv 2308.02357](https://arxiv.org/pdf/2308.02357)
- Lettria re-ran DBpedia-WebNLG with GPT-4-1106, Claude 3 Opus and Mistral-Large in zero-shot, few-shot and LLM-generated few-shot setups. Their findings: Claude 3 Opus had the best F1 (larger margin in few-shot), relation hallucination was insignificant for all models, and **LLM-generated few-shot examples increased hallucination** compared with real examples. Exact numbers appear only in charts. **[CLAIM, vendor benchmark]** — [Lettria blog](https://www.lettria.com/blogpost/benchmarking-of-text2graph-methods-across-multiple-llms-a4e43)

**Schema-guided extraction with ontology grounding: OntoGPT / SPIRES**
- SPIRES (in OntoGPT; Caufield et al., *Bioinformatics* 2024) works zero-shot. It recursively prompts the LLM against a user-defined LinkML schema, then grounds the extracted elements to ontology identifiers. The authors say accuracy is "comparable to the mid-range of existing Relation Extraction methods" and "greatly surpasses an LLM's native capability of grounding entities with unique identifiers." **[BENCH, abstract]** — [OSTI record](https://www.osti.gov/biblio/2322444); [Monarch blog](https://monarchinit.medium.com/spires-building-structured-knowledge-bases-from-unstructured-text-using-large-language-models-eb68c12dea75)
- Secondary summary (not checked against the paper): BC5CDR chemical–disease relation F1 0.44 with GPT-4-turbo. Supervised systems reach about 0.57. **[CLAIM]** — [EmergentMind summary](https://www.emergentmind.com/topics/structured-prompt-interrogation-and-recursive-extraction-of-semantics-spires)

**Schema-free extraction plus clustering: KGGen (NeurIPS 2025)**
- On the MINE-1 benchmark, KGGen retains **66.1%** of facts, against **GraphRAG 47.8%** and **OpenIE 29.8%**. MINE-1 is 100 LLM-generated articles of about 600 words, with 15 facts each. A fact counts as retained if an LLM judge can infer it from a retrieved 2-hop subgraph; the judge agreed with humans 90.2% of the time. Caveat: the corpus is synthetic and short, and the metric is retrievability, not triple precision. **[BENCH]** — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)

**Term extraction, definitions and glossaries**
- SciDef (2026) introduces DefExtra, a benchmark of 268 human-labeled definitions from 75 papers. Across 16 LLMs, **multi-step prompting generally beat one-step**, and NLI-based similarity was a reliable way to score extracted definitions. **[BENCH]** — [arXiv 2602.05413](https://arxiv.org/html/2602.05413)
- An English–Russian fashion-corpus study found ChatGPT definitions generally correct, but sometimes missing core elements or adding unnecessary elaboration. Classical ATE tools (TBXTools, SketchEngine) had high recall and lower precision as term counts grew. **[BENCH, small study]** — [Moonlight review](https://www.themoonlight.io/review/benchmarking-terminology-building-capabilities-of-chatgpt-on-an-english-russian-fashion-corpus)
- A 2025 thesis on synset/synonym building found a multi-step approach worked best: LLM term identification and definition generation, then unsupervised clustering, then LLM cluster refinement. **[CLAIM, thesis]** — [PoliTo thesis](https://webthesis.biblio.polito.it/36445/1/tesi.pdf)
- A 2026 GWLN paper builds an AI-terminology glossary as a KG. It validates against DefExtra plus two independent human annotators, which is a template for glossary evaluation. **[CLAIM]** — [GWLN 2026](https://globalex.link/wp-content/uploads/2026/07/GWLN-8_09_Saputra-Barbosa.pdf)

**Surveys**
- "LLM-empowered knowledge graph construction: A survey" (arXiv 2510.20345, Oct 2025). It organizes the field into ontology engineering (top-down "LLM as ontology assistant" vs bottom-up), knowledge extraction (schema-based vs schema-free), and knowledge fusion. **[DOC]** — [arXiv 2510.20345](https://arxiv.org/html/2510.20345v1)

### Inferences
- For technical manuals, the closest benchmark analog is LLMs4OL "Engineering": expect about 0.6–0.7 F1 for automatic term/type extraction, and low recall unless you add classical candidate generation (noun-phrase/TF-IDF/C-value). A hybrid (statistical candidates + LLM filtering/typing) should beat LLM-only extraction on recall.
- Term typing into a *given* type system is much easier than inducing the type system. Design the pipeline so humans (or an existing standard) fix a small top-level schema, and the LLM types terms into it.
- Automatic is-a hierarchy induction is the weakest link (often below 0.5 F1). Treat generated hierarchies as proposals for review.
- The gap between ontology conformance and factual F1 means schema-constrained extraction gives *well-formed* output, not *correct* output. Schema validity is not a proxy for factual accuracy.
- Absolute numbers from 2023–24 models (Vicuna-13B, GPT-4-turbo) likely understate 2026 frontier models. However, no 2025–26 head-to-head on Text2KGBench with current frontier models was found.

### Gaps
- Could not get the official LLMs4OL 2025 overview tables directly (PDF unreadable). The numbers above come from a participant paper's leaderboard snapshot (July 2025, possibly before final rankings). No LLMs4OL 2026 results were found.
- No benchmark found specifically for glossary or term extraction from *software/product user manuals*.
- No verified per-model Text2KGBench numbers for 2025–26 frontier models.
- SPIRES per-task F1 was not verified against the primary paper.

## Entity resolution / canonicalization / synonym merging across manuals and versions; schema-guided vs schema-free extraction

### Takeaway
State-of-the-art pipelines split the work into two stages. First, open (schema-free) extraction. Second, a dedicated canonicalization stage that clusters entities and relations by embedding, then has an LLM adjudicate merges (EDC, KGGen) or maps them to a fixed or retrieved schema. Pure schema-guided extraction gives consistency but breaks when the schema is large or incomplete. Pure schema-free extraction gives fragmented, redundant graphs. Tool defaults are weak: GraphRAG merges only on exact title+type.

### Cited Findings
- **EDC (Extract–Define–Canonicalize, EMNLP 2024):**
  - It runs few-shot open IE, then has the LLM write a natural-language *definition* for each induced entity/relation type.
  - It embeds those definitions, retrieves the nearest existing schema elements, and lets the LLM decide whether to map (e.g., "participatedIn" becomes "mission") or keep a new type.
  - It works without a schema (self-canonicalization) or with a large target schema via a trained schema retriever (EDC+R). This addresses schemas that are too large to fit in a prompt.
  - **[BENCH, authors]** — [arXiv 2404.03868](https://arxiv.org/html/2404.03868v1)
- **KGGen resolution:**
  - Entities and edges are resolved separately. Items are S-BERT embedded and k-means clustered (clusters of about 128).
  - For each item, the top 16 candidates come from BM25 plus semantic similarity. An LLM picks true duplicates (tense, plural, case, abbreviation) and a canonical alias, and prompts warn against merging distinct concepts (e.g., Type 1 vs Type 2 diabetes).
  - Extraction is two-step: entities first, then triples restricted to those entities.
  - **[BENCH]** — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)
- **GraphRAG** merges entities with identical *title and type* and relationships with identical source+target. It concatenates descriptions and has an LLM summarize them. No further dedup is described. Chunks default to 1,200 tokens; larger chunks are faster but lower fidelity. **[DOC]** — [GraphRAG dataflow](https://microsoft.github.io/graphrag/index/default_dataflow/)
- **Neo4j:**
  - The neo4j-graphrag KG builder accepts a hand-written schema, an LLM-inferred schema, or none. It has an entity-resolution step (can be turned off with `perform_entity_resolution=False`).
  - Neo4j guidance: pass previously extracted node types into later chunk prompts so near-synonym labels collapse. Dedup by combining embedding similarity with edit distance and tuning thresholds. They call disambiguation a problem with "no perfect solutions."
  - **[DOC]** — [Neo4j KG builder guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html); [Neo4j blog](https://neo4j.com/blog/developer/property-graph-index-llamaindex)
- **LlamaIndex PropertyGraphIndex:**
  - `DynamicLLMPathExtractor` treats allowed entity/relation lists as soft guidance.
  - `SchemaLLMPathExtractor` enforces allowed entities, relations and valid (head, relation, tail) patterns; `strict=True` rejects out-of-schema triples.
  - A third-party project reports tool-calling problems with the schema extractor on some LLM providers. **[DOC / CLAIM]**
  - — [LlamaIndex LPG guide](https://developers.llamaindex.ai/python/framework/module_guides/indexing/lpg_index_guide/); [Flexible GraphRAG notes](https://stevereiner.github.io/flexible-graphrag/DATABASES/GRAPH-DATABASES/KNOWLEDGE-GRAPH-EXTRACTORS/)
- The 2025 survey frames schema-based vs schema-free extraction as the main design axis, with knowledge fusion (alignment/dedup) as its own stage. **[DOC]** — [arXiv 2510.20345](https://arxiv.org/html/2510.20345v1)
- Hybrid ontology discovery: a 2026 cyber-threat-intelligence paper proposes schema-agnostic KG construction with *hybrid* ontology discovery (seed ontology plus discovered types) and SHACL-checked closed-loop repair. **[CLAIM]** — [arXiv 2606.01208](https://arxiv.org/pdf/2606.01208)
- Deterministic IRI minting plus ontology alignment had the strongest ablation effects in DOPKG-SHACL. The authors' point: stable identifiers must come from deterministic code, not from the LLM. **[CLAIM]** — [Edge Hill record](https://research.edgehill.ac.uk/en/publications/deterministic-and-trustworthy-llm-driven-semantic-knowledge-graph/)

### Inferences
- For multi-manual, multi-version corpora, use a **seeded hybrid schema**:
  - A small hand-curated core: Product, Version/Release, Module/Feature, UIElement, Procedure, Step, Setting/Parameter, ErrorMessage, Role, BusinessObject, Term.
  - EDC-style canonicalization for everything new, with new types queued for human approval.
- Synonym merging should be **blocked by scope**: same product family, overlapping versions. Without this, the system will wrongly merge homonyms across products (e.g., "Workspace" in two different tools).
- Version handling is mostly *not* covered by the canonicalization literature. Model versioned entities explicitly (a stable concept ID, plus version-specific assertions with validity ranges) rather than letting dedup collapse them.
- Generate canonical IDs deterministically, e.g., normalized label + type + product scope → hash or slug. Keep surface forms as `altLabel` / aliases.

### Gaps
- Found no benchmark of entity resolution across *versions* of documentation, or across vendor manuals.
- No quantitative comparison of EDC vs KGGen vs GraphRAG canonicalization quality on the same dataset was found.

## Proposing higher-level concepts/abstractions (concept clustering, community summaries, taxonomy generation)

### Takeaway
Two practical mechanisms exist:
1. **Graph-community abstraction**: GraphRAG's hierarchical Leiden communities plus LLM-written community reports. These yield thematic "topic" layers, not formal is-a classes.
2. **LLM taxonomy generation/completion**: fine-tuned or prompted hypernym prediction and insertion, which yields is-a structure.

Placing *inner* (abstract, intermediate) nodes remains hard. Community reports are expensive to compute; LazyGraphRAG defers that cost to query time.

### Cited Findings
- **GraphRAG indexing pipeline:**
  - Hierarchical Leiden community detection recursively clusters the entity graph down to a size threshold.
  - An LLM writes a report per community (key entities, relationships, claims) and a shorthand summary.
  - Text units, entity descriptions and community reports are embedded.
  - Optional "claims" (time-bounded facts) extraction is off by default. "FastGraphRAG" swaps LLM extraction for NLP.
  - **[DOC]** — [GraphRAG dataflow](https://microsoft.github.io/graphrag/index/default_dataflow/)
- **LazyGraphRAG** (Microsoft) is claimed to have indexing cost identical to vector RAG and 0.1% of full GraphRAG, with comparable global-query answer quality at more than 700× lower query cost. **[CLAIM, vendor]** — [Microsoft Research blog](https://microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost)
- Secondary sources say graph extraction, not community reports, is the main share (about 75%) of GraphRAG indexing cost. **[CLAIM, unverified]** — [Olostep](https://www.olostep.com/blog/what-is-graphrag)
- An ACL 2025 Industry paper on LLM taxonomy completion and generation from known concepts (Llama-3, five taxonomies) found **placing inner nodes difficult**. **[BENCH]** — [ACL 2025 industry.55](https://preview.aclanthology.org/landing_page/2025.acl-industry.55.pdf)
- TaxoLLaMA, fine-tuned on WordNet, reported SOTA on 11 of 16 taxonomy tasks (construction, hypernym discovery, enrichment, lexical entailment). Moskvoretskii et al. (Semantic Web Journal) extend instruction data to hyponym prediction and node insertion. **[BENCH]** — [arXiv 2403.09207](https://arxiv.org/html/2403.09207v2); [SWJ paper](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2026-moskvoretskiietal-swj.pdf)
- The LLM-Hype framework (VLDB 2025 workshop) evaluates LLM hypernym inference against taxonomy graphs. **[BENCH]** — [VLDB LLM+Graph 2025](https://www.vldb.org/2025/Workshops/VLDB-Workshops-2025/LLM+Graph/LLMGraph-4.pdf)
- LLMs4OL taxonomy discovery F1 ranges from 0.12 to 0.66 across ontologies (see above). **[BENCH]** — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1)

### Inferences
- For "proposing higher-level concepts", combine three signals:
  - Embedding clustering of glossary terms and their definitions.
  - Graph communities, which suggest functional groupings like "billing workflow" or "user administration".
  - Structural cues already present in the manuals: TOC hierarchy, chapter titles, menu paths. These are free, high-precision parent concepts.
- Then have an LLM name each cluster and draft a definition, and send it to a human as a *proposed* concept.
- Keep community reports as an *index/summary layer* for global questions. Do not treat them as ontology classes. Promote a community to a formal concept only after review.
- Given costs, consider LazyGraphRAG-style deferred summarization, or summarize only the top levels of the hierarchy.

### Gaps
- No benchmark found evaluating the *quality/usefulness* of LLM-proposed abstractions or community summaries for technical-documentation QA.
- Microsoft's own indexing cost breakdown was not verified.

## Tooling: graph builders, document parsers, and SKOS/OWL/RDF vs property graphs

### Takeaway
A mature, open toolchain exists:
- **Parsing:** Docling (layout + TableFormer) or Unstructured.
- **Extraction/indexing:** Microsoft GraphRAG, LlamaIndex PropertyGraphIndex, Neo4j LLM Graph Builder / neo4j-graphrag, LangChain LLMGraphTransformer, KGGen, OntoGPT/SPIRES.
- **Ontology learning research code:** LLMs4OL participants' code.

A practical split for the knowledge model: **SKOS for the glossary/thesaurus layer** (prefLabel/altLabel/definition/broader/related), **OWL/SHACL for the core schema and validation**, and a **property graph (Neo4j) or RDF store for the operational KG**.

### Cited Findings
- **Docling** (IBM, MIT-licensed, arXiv 2408.09869):
  - TableFormer table-structure scores: simple 95.4, complex 90.1, all 93.6.
  - A secondary source cites Tabula at 67.9% and Camelot at 73.0% for comparison.
  - Layout analysis uses an RT-DETR model trained on DocLayNet-style classes.
  - **[BENCH via model card / CLAIM for comparisons]** — [Docling models, HF](https://huggingface.co/docling-project/docling-models); [PromptLayer summary](https://www.promptlayer.com/models/docling-models)
- A third-party guide claims Docling reaches 97.9% cell accuracy on complex tables vs Unstructured 75%. Unverified and possibly marketing. **[CLAIM]** — [IDP guide](https://idp-software.com/guides/docling-guide/)
- LlamaIndex publishes its own table-extraction benchmark comparisons (vendor). **[CLAIM]** — [LlamaIndex table benchmark](https://www.llamaindex.ai/insights/table-extraction-benchmark)
- **Microsoft GraphRAG** dataflow (TextUnits → entity/relationship extraction → description summarization → Leiden communities → community reports → embeddings). Documents are linked to TextUnits for provenance. **[DOC]** — [GraphRAG docs](https://microsoft.github.io/graphrag/index/default_dataflow/)
- **Neo4j graph builders**: the LLM Graph Builder app and the neo4j-graphrag `SimpleKGPipeline` support manual, LLM-inferred, or no schema, plus entity resolution. **[DOC]** — [Neo4j KG builder guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html); [Neo4j blog](https://neo4j.com/blog/developer/unstructured-text-to-knowledge-graph/)
- **LlamaIndex PropertyGraphIndex**: Simple, Schema (strict or non-strict) and Dynamic path extractors, with a comparison notebook. **[DOC]** — [LlamaIndex dynamic KG example](https://developers.llamaindex.ai/python/examples/property_graph/dynamic_kg_extraction/)
- **OntoGPT/SPIRES**: LinkML-schema-driven extraction with grounding to ontology IDs, which suits RDF/OWL output. **[DOC]** — [Monarch blog](https://monarchinit.medium.com/spires-building-structured-knowledge-bases-from-unstructured-text-using-large-language-models-eb68c12dea75)
- **KGGen**: pip-installable, open source. **[DOC]** — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)
- **SHACL + LLM**: NL2SHACL-Bench (2026) benchmarks translating natural-language constraints into SHACL. LLMs could help author validation shapes. **[BENCH]** — [arXiv 2608.07530](https://arxiv.org/pdf/2608.07530)

### Inferences
- **Recommended stack for manuals:**
  - Docling (or Unstructured) to get a structured DOM: headings, lists, tables, figures with captions, page numbers.
  - Section-aware chunking that keeps the heading path.
  - A custom extraction layer: KGGen/EDC-style canonicalization over either a LlamaIndex `SchemaLLMPathExtractor` (strict, seeded schema) or the neo4j-graphrag pipeline.
  - Neo4j for the operational graph.
  - SKOS export for the glossary.
  - SHACL (via RDF export, e.g., neosemantics/n10s) for validation.
- SKOS fits glossaries well:
  - `skos:prefLabel` / `altLabel` for canonical term and synonyms.
  - `skos:definition` plus provenance notes.
  - `skos:broader` / `narrower` for the proposed taxonomy.
  - `skos:exactMatch` / `closeMatch` for cross-manual or cross-vendor alignment.
  - SKOS concept schemes per product or version.
- OWL is worth it only for a small core where reasoning or strict typing matters. A property graph is more convenient for per-relationship provenance and confidence properties.
- GraphRAG out of the box is optimized for global sensemaking Q&A, not for precise procedural answers. Use it as one retrieval mode, not as the KG of record.

### Gaps
- No independent 2026 benchmark comparing Docling vs Unstructured vs LlamaParse vs commercial parsers on *user manuals* (screenshots, callouts, numbered procedures) was found.
- Did not verify LangChain LLMGraphTransformer's current features. Did not verify current LLM Graph Builder release notes.
- No direct primary source found on SKOS-based LLM glossary pipelines; the inference is based on the SKOS data model.

## Handling manual-specific structure: procedures/steps, UI elements, versions/releases, product variants, provenance

### Takeaway
There is little specific research. The best evidence suggests:
- Procedural knowledge should be extracted into explicit Procedure→Step graphs, using few-shot prompts and a domain vocabulary.
- **Where manuals already contain structure (numbered steps, cross-references, menu paths), deterministic extraction beats LLM extraction for reproducibility.**
- Provenance (doc → section → chunk → page) should be first-class. GraphRAG and Neo4j pipelines already link extracted elements to text units.

### Cited Findings
- Procedural text mining (arXiv 2310.03376) uses LLM few-shot in-context learning to extract *procedural knowledge graphs* from maintenance manuals (e.g., lathe maintenance), guided by a domain vocabulary. The motivation: keyword search fails on multi-step questions. **[BENCH, small-scale]** — [arXiv 2310.03376](https://arxiv.org/pdf/2310.03376)
- An SAE 2026 helicopter troubleshooting paper combines KGs of fault causality and maintenance history with RAG over manuals. The authors argue plain RAG risks hallucinating unsafe procedures. **[CLAIM]** — [SAE 2026-0328](https://saemobilus.sae.org/papers/a-knowledge-graph-rag-based-troubleshooting-guide-helicopter-systems-f-0082-2026-0328)
- "The Graph Is Already Written" (SunExpress, aircraft maintenance docs) builds the KG *deterministically* from the manuals' existing cross-reference notation, with no LLM at construction time. It reports 95% seed-retrieval accuracy (self-reported, seen only via LinkedIn posts). **[CLAIM]** — [LinkedIn post](https://tr.linkedin.com/in/muhammetduzparmak)
- Vendor overviews (Addepto, Context-Clue) agree that human experts must validate critical relationships in safety-sensitive documentation. **[CLAIM, vendor]** — [Addepto](https://addepto.com/blog/the-power-of-knowledge-graphs-in-managing-complex-technical-documentation/)
- GraphRAG links Documents → TextUnits → entities/relationships, which gives chunk-level provenance. **[DOC]** — [GraphRAG docs](https://microsoft.github.io/graphrag/index/default_dataflow/)
- In GraphRAG, optional "claims/covariates" capture time-bounded facts, a possible mechanism for version-scoped assertions. **[DOC]** — [GraphRAG docs](https://microsoft.github.io/graphrag/index/default_dataflow/)

### Inferences
- **Proposed manual schema:**
  - Structure: `Document(product, version, language, url, retrieved_at, hash)` → `Section(heading_path, page_range)` → `Chunk`.
  - Procedures: `Procedure` -[HAS_STEP {order}]→ `Step` -[ACTS_ON]→ `UIElement` (menu path, button, field, dialog).
  - Prerequisites and results: `Procedure` -[REQUIRES]→ `Precondition/Role/Permission`, and `Step` -[RESULTS_IN]→ `State/Message`.
  - Features: `Feature` -[AVAILABLE_IN {from_version, to_version, edition}]→ `Product`.
  - Glossary: `Term` -[DEFINED_IN]→ `Section`.
  - Provenance: every extracted node and edge carries `source_chunk_id`, page, `extractor_model`, `prompt_version`, and confidence.
- Parse procedures with rules first: numbered lists under task headings, "Click X > Y" patterns, bold/monospace UI labels. Use the LLM only to normalize and link. This mirrors the "graph is already written" finding.
- Versions: download all available versions. Diff sections by heading path and content hash. Assert facts with validity intervals rather than overwriting. Feature-availability edges carry version and edition ranges. Variants are handled the same way, as an `edition/variant` property or node.
- Screenshots and figures: Docling yields figure crops and captions. A VLM can caption them to extract UI element names. No benchmark evidence was found for accuracy here.

### Gaps
- No benchmark or dataset found for LLM extraction from *software* user manuals (UI elements, menu paths, release-specific behaviour).
- No primary paper found on version-aware KG construction from documentation.

## Known failure modes and mitigation (hallucinated relations, inconsistent granularity, schema drift; SHACL, confidence, provenance)

### Takeaway
The documented failure modes are:
- Hallucinated subjects/objects (about 7–17% in benchmarks).
- Low recall / conservative extraction.
- Label and type drift across chunks.
- Redundant near-duplicate nodes.
- Over-merging of distinct concepts.
- Poor inner-node placement in taxonomies.
- Domain shift.

The strongest mitigations reported:
- Constrained schemas plus **SHACL validation with bounded repair loops** (structural errors).
- **Deterministic ID minting and ontology alignment**.
- Real (not synthetic) few-shot examples.
- Two-step entity-then-relation extraction.
- Provenance to the source span, so claims can be checked.
- Human review for core concepts.

SHACL catches structural errors, not plausible-but-false facts.

### Cited Findings
- **Text2KGBench baselines** had about 17% subject, relation and object hallucination, despite 83% ontology conformance. **[BENCH]** — [arXiv 2308.02357](https://arxiv.org/pdf/2308.02357)
- **LLM-generated few-shot examples** raised hallucination compared with real examples, for GPT-4, Claude 3 Opus and Mistral. **[CLAIM, vendor benchmark]** — [Lettria](https://www.lettria.com/blogpost/benchmarking-of-text2graph-methods-across-multiple-llms-a4e43)
- **OntoLogX**: SHACL violations trigger targeted correction prompts. If no valid graph emerges within the retry budget, the output is an **empty graph** rather than invalid triples. **[CLAIM]** — [arXiv 2510.01409](https://arxiv.org/pdf/2510.01409)
- **ANCHOR (CTI)**: SHACL node shapes plus closed-loop repair, capped at 3 retries. The most common violation was missing required properties. **[CLAIM]** — [arXiv 2606.01208](https://arxiv.org/pdf/2606.01208)
- **KastorKG** (Semantic Web Journal): SHACL-shape-guided small models report 0 hallucinated subjects/relations, vs 12–16% and 7–9% for LLM baselines. The evaluation setup is unclear. **[CLAIM]** — [SWJ 4053](https://semantic-web-journal.net/system/files/swj4053.pdf)
- **DOPKG-SHACL**: determinism comes from deterministic IRI minting, ontology alignment and SHACL, "not by the LLM alone." Ablations show IRI minting and alignment matter most. **[CLAIM]** — [Edge Hill](https://research.edgehill.ac.uk/en/publications/deterministic-and-trustworthy-llm-driven-semantic-knowledge-graph/)
- **Scientific-KG validation framework** (NeurIPS 2026 listing): SHACL as a deterministic post-generation gate caught missing links, invalid types, broken references and cross-document identity issues before expert review. **[CLAIM]** — [NeurIPS 2026](https://neurips.cc/virtual/2026/158007)
- **Granularity/drift**: Neo4j recommends feeding prior node types into later prompts to stop label proliferation, and threshold-tuned dedup. **[DOC]** — [Neo4j blog](https://neo4j.com/blog/developer/unstructured-text-to-knowledge-graph/)
- **Over-merging**: KGGen prompts explicitly guard against merging distinct concepts. **[BENCH method]** — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)
- **Recall failure**: engineering-domain term extraction reached P 0.825 but R 0.30. Validation-to-test drops occurred under domain shift. **[BENCH]** — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1)
- **Chunk size**: larger chunks lower extraction fidelity in GraphRAG. **[DOC]** — [GraphRAG docs](https://microsoft.github.io/graphrag/index/default_dataflow/)
- **Evaluation**: MINE uses an LLM judge (90.2% agreement with humans) to test fact retrievability from the KG. SciDef finds NLI-based scoring reliable for definitions. Both are reusable for regression testing. **[BENCH]** — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2); [arXiv 2602.05413](https://arxiv.org/html/2602.05413)

### Inferences
- **Recommended pipeline design**, combining the evidence above:
  1. **Acquire**: download manuals with metadata (product, version, edition, language, URL, date, hash). Dedup identical content across versions by hash.
  2. **Parse**: Docling into a structured DOM (headings, lists, tables, figures, pages). Keep the heading path and page numbers.
  3. **Deterministic structure extraction**: TOC → section tree, numbered steps → Procedure/Step, menu paths and UI labels via regex/format cues, existing glossary sections, cross-references. Treat this as high-precision ground truth.
  4. **Indexes**: BM25 plus vector index over section-aware chunks (about 300–800 tokens, with heading-path prefix). The GraphRAG default of 1,200 tokens is a cost/fidelity trade-off.
  5. **Term candidates**: statistical ATE (C-value/TF-IDF/noun phrases) unioned with LLM-proposed terms to fix LLM low recall. Then LLM filtering, typing into the seeded core schema, and multi-step definition extraction (prefer definitions *quoted* from the text, with span provenance; generated definitions flagged as such).
  6. **Relation extraction**: two-step (entities, then relations restricted to them), under a seeded schema with non-strict mode plus EDC-style "define and canonicalize" for new types. Use real few-shot examples from the corpus.
  7. **Canonicalization/ER**: KGGen-style clustering, blocked by product scope. LLM adjudicates merges. Deterministic IDs. Synonyms become `skos:altLabel`. Version-specific facts are kept separate.
  8. **Validation**: SHACL shapes (LLM-drafted, human-approved) with at most 3 repair retries, then reject. Also an LLM-judge or NLI "is this triple entailed by its source span?" check that sets a confidence score.
  9. **Abstraction**: Leiden communities plus term-embedding clusters plus TOC structure feed LLM-proposed parent concepts and community summaries. All are *proposals* in a review queue.
  10. **Human-in-the-loop**: review core terms, new types, merges above a risk threshold, and proposed abstractions. Log decisions to retrain or re-prompt.
  11. **Evaluate continuously**: a small gold set per product (terms, definitions, procedures, Q&A). Use MINE-style fact retention and an NLI definition score, and track drift across model/prompt versions.
- Assistant answers should cite source sections via the provenance edges. This is the main defense against residual hallucinated relations, which SHACL cannot catch.

### Gaps
- Several SHACL+LLM numbers come from preprints or snippets that were not checked in full text.
- No quantitative study found on confidence calibration of LLM-assigned triple confidence scores.
- No evidence found on how errors compound across a full pipeline (parse → extract → resolve) for technical manuals.
