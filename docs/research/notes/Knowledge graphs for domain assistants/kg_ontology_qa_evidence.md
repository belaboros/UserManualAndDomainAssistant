# Knowledge Graphs, Glossaries and Ontologies vs Plain Vector RAG for Manual/Documentation QA

Research date: 2026-11-13. Evidence labels used below: **[IND]** independent academic evaluation; **[AUTH]** authors evaluating their own method (self-reported); **[VEND]** vendor or vendor-affiliated marketing or engineering blog; **[PRAC]** practitioner blog or anecdote.

## 1. What do benchmarks show for GraphRAG / LightRAG / HybridRAG / KG-RAG / ontology RAG vs vector RAG, and which question types benefit?

### Takeaway
No graph approach beats vector RAG across the board. Graph and community methods help on multi-hop, comparison, temporal, and some global or summarization questions, typically by a few points. Vector RAG wins or ties on single-hop, detail-oriented, and "no answer exists" questions. Pure-triplet KG retrieval is much worse than chunk retrieval. Many headline GraphRAG and LightRAG gains come from biased LLM-as-judge setups and shrink to near zero once those biases are corrected. Combining both retrievers (integration) gives the most consistent gains.

### Cited Findings
**RAG vs. GraphRAG: A Systematic Evaluation (Han et al., arXiv 2502.11371, v3 Mar 2026) [IND]**
- NQ (single-hop), Llama-3.1-70B F1: RAG 68.18; Community-GraphRAG Local 65.44; HippoRAG2 64.03; Community Global 55.05; KG-GraphRAG triplets+text 53.88; triplets only 28.50. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- HotpotQA (multi-hop), 70B F1: HippoRAG2 64.93; Community Local 64.60; RAG 63.88; Global 46.99; KG triplets+text 48.75; triplets only 30.73. Multi-hop gains are small (~1 point). — [Han et al.](https://arxiv.org/html/2502.11371v2)
- MultiHop-RAG accuracy (70B): RAG 65.77; Community Local 71.17; HippoRAG2 69.87; Global 65.69; KG triplets only 50.98. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- MultiHop-RAG by question type (70B):
  - Comparison: Local 60.16 vs RAG 56.31.
  - Temporal: Local 49.06 vs RAG 25.73. This is the largest graph gain.
  - Null queries (correct answer is "insufficient information"): RAG 91.36, Local 88.70, Global **13.95**. Global community summaries badly hurt abstention. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- The methods are complementary. On MultiHop-RAG (8B), 13.6% of queries were answered correctly only by GraphRAG and 11.6% only by RAG. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- NovelQA (8B): RAG 57.12 vs Community Local 53.03 vs KG 37.80. RAG led on single-hop (68.73) and detail-oriented (55.28) questions. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- Query-based summarization, ROUGE-2 (8B): RAG ≥ GraphRAG on QMSum, ODSum-story, and ODSum-meeting, and roughly tied on SQuALITY. Global search was worst everywhere. On SQuALITY, BERTScore favoured Local (84.66 vs 77.62), so the ranking depends on the metric. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- **Token-matched control:** giving vector RAG the same token budget as GraphRAG nearly closes the gap (70B: 71.01 vs 71.17; 8B: RAG 69.33 > GraphRAG 69.01). Part of GraphRAG's "advantage" is simply more context. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- Hybrids:
  - Selection (routing per query) adds +1.1 points (72.3).
  - Integration (concatenating both retrievals) adds +6.4 points (77.62 on MultiHop-RAG 70B), and gives 65.97 vs RAG 61.42 on NovelQA.
  - Neither hybrid gives a significant gain on summarization. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- Using a stronger LLM (GPT-4o) for graph construction raised Community Local on MultiHop-RAG from 71.17 to 75.08. Extraction quality matters. — [Han et al.](https://arxiv.org/html/2502.11371v2)

**GraphRAG-Bench, "When to Use Graphs in RAG" (Xiang et al., ICLR 2026, arXiv 2506.05690) [IND]**
- The motivation is stated directly: recent studies report that GraphRAG frequently underperforms vanilla RAG on real-world tasks. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- Fact retrieval (novel corpus): RAG with reranking 60.9 vs MS-GraphRAG 49.3. Basic RAG is sufficient for simple lookups, and graph-induced redundancy hurts. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- Complex reasoning:
  - Novel corpus: HippoRAG2 53.4 and MS-GraphRAG 50.9 vs RAG 42.9.
  - Medical corpus: HippoRAG2 62.0 and LightRAG 61.3 vs RAG 58.6, a small gain. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- Contextual summarization:
  - Novel corpus: MS-GraphRAG 64.4 vs RAG 51.3.
  - **Medical (structured domain) corpus: RAG 65.8 vs HippoRAG2 63.1 vs MS-GraphRAG 41.9.** The summarization benefit did not carry over to the structured, domain-knowledge corpus. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- Graph quality guidance:
  - Denser, tightly clustered graphs (HippoRAG2: average degree 8.75, clustering coefficient 0.657, vs MS-GraphRAG 1.48 / 0.315) correlated with higher recall.
  - "More relationships ≠ better performance."
  - The authors recommend precise retrieval and bounding context growth. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)

**Microsoft GraphRAG and LazyGraphRAG [AUTH/VEND]**
- The original GraphRAG paper ("From Local to Global", arXiv 2404.16130) reports improved comprehensiveness and diversity over naive RAG on global sensemaking questions, judged pairwise by an LLM. The commonly cited 72–83% comprehensiveness win rates come from that paper. I have not re-verified them in this session, and they are challenged by the bias study below. — [Edge et al.](https://arxiv.org/abs/2404.16130)
- LazyGraphRAG (MSR blog, 25 Nov 2024; integrated into Microsoft Discovery / Azure Local per a June 2025 note):
  - Setup: 5,590 AP news articles; 100 synthetic queries (50 local, 50 global); LLM-judged pairwise wins on Comprehensiveness, Diversity, and Empowerment.
  - Claims: at budget 500 it beats all conditions, including 8K and 64K vector RAG, GraphRAG local/global/DRIFT, and RAPTOR. Global-search quality comes at more than 700× lower query cost.
  - Win rates are shown only in a chart, without confidence intervals. The evaluation uses a single news corpus, synthetic queries, and an LLM judge. — [Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)

**Evaluation-bias critique (Zeng et al., arXiv 2506.06331, 2025) [IND]**
- Evaluating LightRAG against itself should produce a tie. Instead, swapping answer order shifted win rates by more than 30%, and one copy "won" 90% vs 10% because of position, length, and single-trial biases. — [Zeng et al.](https://arxiv.org/html/2506.06331v1)
- Under the original protocol LightRAG beat NaiveRAG 72%–28%. After de-biasing, NaiveRAG slightly beat LightRAG. The best method (FGRAG) gained under 10% win rate except against LightRAG. — [Zeng et al.](https://arxiv.org/html/2506.06331v1)
- Han et al. likewise found that swapping answer order can fully flip judgments between RAG and Community-Local. — [Han et al.](https://arxiv.org/html/2502.11371v2)

**HybridRAG (Sarmah et al., BlackRock + NVIDIA, arXiv 2408.04948, Aug 2024) [AUTH, vendor-affiliated]**
- Domain: financial earnings-call transcripts.

  | Method | Faithfulness | Answer relevance | Context precision | Context recall |
  |---|---|---|---|---|
  | VectorRAG | 0.94 | 0.91 | 0.84 | 1.00 |
  | GraphRAG | 0.96 | 0.89 | 0.96 | 0.85 |
  | HybridRAG | 0.96 | 0.96 | 0.79 | 1.00 |

  — [Sarmah et al.](https://arxiv.org/html/2408.04948v1)
- Failure modes:
  - GraphRAG fails on abstractive questions and on questions that don't name an entity explicitly.
  - VectorRAG struggles with multi-document and long-context retrieval.
  - Hybrid has the lowest context precision because the merged context adds noise.
  - The evaluation covers a single domain with RAGAS-style LLM metrics. — [Sarmah et al.](https://arxiv.org/html/2408.04948v1)

### Inferences
- For a manual assistant, most questions are likely to be single-hop, procedural, or definitional ("how do I configure X", "what does parameter Y mean"). On these, vector or hybrid lexical retrieval is as good as or better than graph retrieval. Graph value concentrates on cross-manual comparison, version/temporal reasoning, dependency chains, and "which components are affected by X".
- Integration (graph context added to chunk context), not replacement, is the empirically safest pattern. Graph context should always carry source text (triplets + text or chunk-linked nodes), never bare triplets.
- Global community-summary search should not drive "is this documented?" answers, because it collapses abstention (null-query accuracy 13.95%).
- Treat any GraphRAG claim based on pairwise LLM-judge win rates as weak unless it controls for position, length, and token budget.

### Gaps
- I found no independent benchmark specifically on consumer or industrial product user manuals that compares vector RAG with GraphRAG at scale.
- LightRAG's own reported numbers (arXiv 2410.05779) were not fetched here. They rely on the pairwise-judge protocol that Zeng et al. criticise.
- The original GraphRAG win-rate figures were not re-verified this session.

## 2. Evidence specific to technical documentation, manuals, and enterprise domains (telecom, manufacturing, finance, SAP-like)

### Takeaway
Domain-specific evidence is thin, small-scale, and mostly self-reported. It consistently shows modest gains (high single digits) for hybrid graph+vector over vector-only on specification-style documents. Ontology-guided KGs only compete when chunk text is attached.

### Cited Findings
- **Telecom (O-RAN specifications, Ahmad et al., arXiv 2507.03608) [AUTH]:** GraphRAG and Hybrid GraphRAG both outperform vector RAG. Hybrid GraphRAG improves factual correctness by 8%, and GraphRAG improves context relevance by 11%. Absolute scores were not visible in the abstract. — [Ahmad et al.](https://arxiv.org/abs/2507.03608)
- **Finance (earnings calls):** HybridRAG improved answer relevance 0.91 → 0.96 but lowered context precision (see Section 1). — [Sarmah et al.](https://arxiv.org/html/2408.04948v1)
- **Ontology-learning comparison (da Cruz et al., arXiv 2511.05991, Nov 2025) [IND/small]:**
  - Ontology-guided KGs that include chunk information are competitive with state-of-the-art GraphRAG and substantially outperform vector baselines.
  - Ontologies derived from relational databases perform about as well as text-derived ones and need only one-time ontology learning, which cuts LLM cost and avoids ontology merging. — [da Cruz et al.](https://arxiv.org/abs/2511.05991)
  - A search snippet reported a 20-question set where vector RAG scored 60% (12/20) and ontology graphs *without* chunk text did substantially worse. This is unverified detail and a tiny sample. — [ResearchGate listing](https://www.researchgate.net/publication/397480452_Ontology_Learning_and_Knowledge_Graph_Construction_A_Comparison_of_Approaches_and_Their_Impact_on_RAG_Performance)
- **Ontology-grounded RAG with SPARQL for technical documentation [small regional-journal study]:** on 10 real user queries, 7 were answered precisely via SPARQL-grounded retrieval, 2 via lexical fallback with ontology traceability, and 1 out-of-domain query got an explicit knowledge-limit acknowledgment. — [ESPOL Revista Tecnológica](https://rte.espol.edu.ec/index.php/tecnologica/en/article/view/1603)
- **OG-RAG (EMNLP 2025):** ontology-driven hypergraph retrieval over domain documents. The authors report better recall and factual accuracy than standard RAG. — [OG-RAG, ACL Anthology](https://aclanthology.org/2025.emnlp-main.1674.pdf)
- **Medical (structured domain) corpus in GraphRAG-Bench:**
  - Graph methods gave only small complex-reasoning gains (+2.7 to +3.4 points).
  - They lost on summarization (MS-GraphRAG 41.9 vs RAG 65.8). — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- **Related 2026 preprints (not read in full):**
  - Evidence Units: ontology-grounded *document-structure* graphs, complementary to content GraphRAG. — [arXiv 2604.00500](https://arxiv.org/pdf/2604.00500)
  - VDGR-RAG: vectors + directories + graphs + reflection over hierarchical enterprise knowledge. — [arXiv 2608.07994](https://arxiv.org/pdf/2608.07994)
  - Power-grid CIM standards QA. — [arXiv 2609.02011](https://arxiv.org/pdf/2609.02011)

### Inferences
- Manuals have strong inherent structure: chapters, procedures, parameter tables, product/version hierarchies. A document-structure graph (section hierarchy, cross-references, product → version → feature) is probably cheaper and more reliable than open LLM triple extraction. It also directly supports citations and "see also" reasoning.
- Ontology-first designs (a fixed schema for Product, Component, Parameter, Procedure, ErrorCode, Version) look more promising for manuals than schema-free LLM extraction, provided nodes link back to source chunks.

### Gaps
- I found no independent evaluation on SAP-like ERP documentation, manufacturing equipment manuals, or multi-vendor product manuals.
- The O-RAN paper's absolute numbers and question-type breakdown were not accessible (PDF could not be parsed).

## 3. Role of glossaries, synonym mapping, and terminology normalization

### Takeaway
Practitioners widely agree that curated domain glossaries help. They support acronym expansion, synonym/alias mapping, and entity linking for query rewriting and for keyword/BM25 retrieval. Controlled public benchmarks quantifying the gain are scarce, and over-broad expansion causes query drift.

### Cited Findings
- **Fintech agentic RAG (arXiv 2510.25518) [IND/industrial]:**
  - A dedicated component manages a local glossary and appends in-line acronym definitions so downstream agents don't misread shorthand.
  - It failed in edge cases where acronyms were neither defined nor grounded in the documents. — [arXiv 2510.25518](https://arxiv.org/html/2510.25518v1)
- **Palo Alto Networks [PRAC]:**
  - Uses a rule-based synonym layer for domain jargon and product names.
  - Indexes a separate embedding of synonym-expanded document text and queries original and expanded fields separately. — [Medium / Palo Alto Networks engineer](https://medium.com/@impuneetgupta/bridging-the-language-gap-our-journey-to-a-synonym-aware-rag-system-at-palo-alto-networks-e95c35f40004)
- **Allganize [VEND]:** argues that synonym mismatch is a long-standing cause of missed retrievals in enterprise search, citing examples such as "EMR" vs "Electronic Medical Records". — [Allganize](https://www.allganize.ai/en/blog/rags-long-standing-challenge-synonyms)
- **Risk of query drift:** over-broad or incorrect synonyms retrieve unrelated passages, so generic synonym expansion should be avoided unless domain-specific. — [apxml course](https://apxml.com/courses/optimizing-rag-for-production/chapter-2-advanced-retrieval-optimization/query-augmentation-rag)
- **Entity-name dependency:** HybridRAG's GraphRAG component fails when a question doesn't name an entity explicitly. Graph retrieval therefore depends on entity linking, which a glossary/alias table directly supports. — [Sarmah et al.](https://arxiv.org/html/2408.04948v1)
- **Specialized terminology extraction:** generic NLP toolkits fail to extract specialized terminology and relations in technical domains such as telecom. This supports domain-tuned extraction and ontology-driven extraction (reported in the 2511.05991 search context). — [da Cruz et al.](https://arxiv.org/abs/2511.05991)

### Inferences
- In this architecture the glossary is the cheapest structured artifact with the highest leverage. It serves four purposes:
  - Query normalization and expansion (acronyms, aliases, product renames across versions).
  - The entity-linking dictionary for graph lookup.
  - The direct source for definitional answers.
  - A detector for terminology drift: the same term defined differently across manuals, or a different term for the same concept.
- Expansion should be scoped: per product, per manual version, and per tenant, since acronyms collide across organizations.

### Gaps
- I found no peer-reviewed controlled study quantifying recall or accuracy gains from glossary-based query expansion in RAG over technical manuals. The evidence is practitioner and vendor reporting.

## 4. Costs and failure modes

### Takeaway
Full GraphRAG indexing costs about three orders of magnitude more than vector indexing. It inflates retrieved context (and therefore query cost and latency) and loses a third of answer entities during extraction. Lazy or deferred approaches cut indexing cost to vector-RAG levels.

### Cited Findings
- **Build and retrieval time (Han et al.):**

  | Measure (MultiHop-RAG) | RAG | KG-GraphRAG | Community-GraphRAG |
  |---|---|---|---|
  | Construction time | 135 | 7,702 | 5,560 |
  | Retrieval time | 1,724 | 14,434 | 1,249 |
  | Retrieved tokens | 3,631 | not reported | 9,770 |

  - Units were not stated in the paper.
  - Generation time (70B): RAG 3,640 vs GraphRAG 6,272 vs Integration 9,674. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- **KG extraction noise:** only about 65.8% (HotpotQA) and 65.5% (NQ) of answer entities appear in the LLM-built KG. Retrieval accuracy:
  - RAG 0.886 (HotpotQA) / 0.867 (NQ)
  - KG triplets only 0.392 / 0.322
  - KG triplets+text 0.698 / 0.615 — [Han et al.](https://arxiv.org/html/2502.11371v2)
- **Prompt-token cost per query (GraphRAG-Bench, novel corpus):**
  - Vanilla RAG about 879; HippoRAG2 about 1,008; RAPTOR about 3,441.
  - MS-GraphRAG local about 38.7K; LightRAG about 100.8K; MS-GraphRAG global about 331K.
  - The paper's text contradicts its own table for the global figure. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- **Context explosion:** GraphRAG can cause sudden context explosions, and the authors recommend search-boundary limits. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- **Indexing cost:**
  - LazyGraphRAG indexing costs the same as vector RAG and about 0.1% of full GraphRAG.
  - Secondary sources cite about $1,544 vs $1.45 per million tokens (GraphRAG vs vector) from Microsoft's AP News benchmark. I could not confirm this figure in the primary blog text. — [Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/); [beri.net, PRAC](https://www.beri.net/article/graphrag-vs-vector-rag-indexing-query-cost-lightrag-lazygraphrag-2026)
- **Latency:** a study cited within GraphRAG-Bench reports graph retrieval improving HotpotQA multi-hop reasoning by 4.5% at 2.3× average latency. This is a secondary citation; the original was not identified. — [GraphRAG-Bench search snippet](https://arxiv.org/abs/2506.05690v3)
- **Where GraphRAG underperforms:**
  - Single-hop and detail questions.
  - Null/abstention questions (Global search).
  - Abstractive questions.
  - Questions without named entities.
  - Summarization on structured domain corpora. — [Han et al.](https://arxiv.org/html/2502.11371v2); [Sarmah et al.](https://arxiv.org/html/2408.04948v1); [Xiang et al.](https://arxiv.org/html/2506.05690v2)

### Inferences
- Maintenance matters for manuals because new versions arrive regularly. Community-summary approaches need re-clustering and re-summarization on updates. Lazy or deferred graph construction and schema-bound ontology extraction are easier to keep incremental.
- The LLM used for extraction is a major quality lever (+3.9 points with GPT-4o in Han et al.). A strong model should be budgeted for offline indexing, with cheaper models at query time.

### Gaps
- I found no rigorous public data on the ongoing maintenance cost of enterprise KGs (human curation hours, update latency).

## 5. Recommended hybrid architectures, citation/grounding, and presenting source conflicts

### Takeaway
The evidence favours hybrid retrieval: dense + lexical + graph/structure, with graph nodes linked back to source chunks, merged and reranked under a bounded token budget, plus a query router. Models handle conflicting sources poorly by default. Explicitly prompting them to detect and reason about conflicts measurably improves answers, but this remains an open problem.

### Cited Findings
- **Integration outperforms selection:** +6.4 vs +1.1 points on MultiHop-RAG. Selection is cheaper. — [Han et al.](https://arxiv.org/html/2502.11371v2)
- **Ordering and noise:** HybridRAG appends graph context after vector context. The merged context lowers precision (0.79), so reranking or filtering after merge is needed. — [Sarmah et al.](https://arxiv.org/html/2408.04948v1)
- **Text attached to graph nodes:** ontology-guided KGs only compete when chunk text is attached, and triplet-only retrieval loses 20–35 F1 points. — [da Cruz et al.](https://arxiv.org/abs/2511.05991); [Han et al.](https://arxiv.org/html/2502.11371v2)
- **Bounded graph search:** use precise retrieval and graph search boundaries; prefer dense, high-quality graphs. — [Xiang et al.](https://arxiv.org/html/2506.05690v2)
- **Traceability and declared limits:** SPARQL-grounded answers with ontology traceability, a lexical fallback, and explicit knowledge-limit acknowledgment for out-of-domain queries form a viable small-scale pattern for technical documentation. — [ESPOL](https://rte.espol.edu.ec/index.php/tecnologica/en/article/view/1603)
- **CONFLICTS benchmark (arXiv 2506.08500, 2025) [IND]:**
  - Defines a taxonomy of inter-source conflict types (for example, outdated information), each with a desired behaviour.
  - Models frequently fail to resolve conflicts.
  - Explicitly prompting the model to reason about potential conflicts noticeably improves responses, with considerable room left for improvement. — [arXiv 2506.08500](https://arxiv.org/abs/2506.08500v2)
- **WikiContradict (NeurIPS 2024 D&B) [IND]:**
  - 253 human-annotated contradictory-passage instances.
  - Given two contradictory passages, LLMs struggle to produce answers that reflect the conflict, especially implicit conflicts.
  - An automated evaluator reached an F-score of 0.8 against human judgments. — [WikiContradict](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c63819755591ea972f8570beffca6b1b-Abstract.html)

### Inferences
Candidate architecture for the manual assistant (synthesis, not directly benchmarked):
1. **Query understanding.** Normalize with the glossary (acronyms, aliases, product and version), link entities, and classify the question type (definitional, procedural, lookup, comparison, cross-manual, global).
2. **Retrieval.**
   - Always run hybrid dense + BM25 over chunks.
   - Add graph or ontology traversal for comparison, dependency, and cross-manual questions.
   - Add the structure graph (section hierarchy, cross-references) for context expansion.
   - Use precomputed community or summary indexes only for global questions.
3. **Merge, rerank, and deduplicate** under a fixed token budget.
4. **Generate** with mandatory per-claim citations (manual, version, section, page).
5. **Run a separate conflict/gap pass.** Compare the claims retrieved per source, flag contradictions, version differences, and terminology drift (glossary mismatches), and present them in a distinct "Documentation notes" block. Never silently pick one source.

Precomputed contradiction and gap detection at indexing time (claim extraction, then cross-document comparison keyed by ontology entities) is probably more reliable than relying on in-context detection alone, given the WikiContradict and CONFLICTS results.

### Gaps
- I found no benchmark that evaluates *how* to present conflicts to end users (UX studies on user trust or comprehension).
- I found no controlled study of conflict detection specifically across product manual versions.

## 6. What makes answers "expert-like"? (clarifying questions, cross-concept reasoning, citations, uncertainty)

### Takeaway
By default, LLMs in RAG rarely clarify or abstain. They produce plausible but unsupported answers to underspecified or unanswerable questions. Expert-like behaviour therefore has to be engineered explicitly as an Answer / Ask / Abstain decision, with clarification grounded in what the corpus actually covers, plus citations and explicit uncertainty or conflict reporting.

### Cited Findings
- **MTRAG-UN:** a multi-turn RAG benchmark covering unanswerable, underspecified, and non-standalone questions. Most LLMs generate plausible but unsupported answers instead of deferring or clarifying. — [arXiv 2604.04565 (search result)](https://arxiv.org/pdf/2604.04565)
- **"Clarify, Abstain or Answer?" (2026):** frames the task as a joint Answer/Ask/Abstain decision. Standard RAG gets 26.7% decision accuracy, and improved methods plateau at 34–38%. Abstain recall rose from 13.3% to 58.1% only when the behaviour was learned. LLMs by default rarely clarify or abstain. — [arXiv 2605.25831](https://arxiv.org/html/2605.25831)
- **DQA (Amazon, enterprise IT troubleshooting):** a policy chooses among clarifying questions, investigative steps, and resolution proposals, which mirrors how a human support expert works. — [search result, arXiv 2601.11722 / 2604.05350](https://arxiv.org/pdf/2601.11722)
- **RAC:** generating clarifying questions conditioned on retrieved passages reduces hallucinated clarifications about aspects the corpus doesn't cover. — [search results](https://arxiv.org/pdf/2604.05350)
- **AskBench:** separates intent-deficient queries (which need clarification) from false-premise queries. — [AlphaXiv 2602.11199](https://www.alphaxiv.org/abs/2602.11199.md)
- Graph/community Global search sharply degrades correct "insufficient information" answers (13.95% vs RAG 91.36%). Abstention should be driven by chunk-level evidence. — [Han et al.](https://arxiv.org/html/2502.11371v2)

### Inferences
- Expert-like behaviours that the structured artifacts directly enable:
  - Disambiguation questions driven by the ontology (product, version, or role ambiguity, e.g., "which model/firmware?").
  - Definitions grounded in the glossary.
  - Cross-concept reasoning via graph relations (prerequisites, dependencies, affected components).
  - Explicit "the manuals do not cover this" statements backed by retrieval evidence.
  - Conflict and terminology-drift notes.
- The evaluation should include underspecified, unanswerable, and conflicting-source test items, not just answerable single-hop questions, because default systems fail these silently.

### Gaps
- The numbers for MTRAG-UN, "Clarify, Abstain or Answer?", DQA, and RAC come from search snippets and were not verified against the full papers. Paper-to-arXiv-ID mapping for DQA and RAC is uncertain.
- I found no study that defines or measures "expert-likeness" for manual QA with human experts as the reference.
