# Systematic Experimentation for a Knowledge-Structured Domain QA Assistant (evaluation methodology, frameworks, experimentation plan)

Scope note: research done 2026-11-13 with ~15 tool calls. Primary sources (arXiv papers, Microsoft Research, Neo4j blog) are used where possible. Tool-comparison claims come mostly from vendor-authored blogs and are marked as such. Anything from background knowledge that was not verified in this session is labeled "(background, unverified)" and kept under Inferences or Gaps.

---

## 1. Evaluation frameworks and metrics for RAG / GraphRAG / KGQA, and LLM-as-judge weaknesses

### Takeaway
Two layers are needed. A metrics layer (RAGAS / DeepEval / TRACe-style: faithfulness, context precision/recall, answer correctness) covers per-answer scores. An experiment/statistics layer (ARES-style prediction-powered inference, error bars, paired comparisons) tells you whether a difference between stacks is real. GraphRAG-specific benchmarks (GraphRAG-Bench, Microsoft BenchmarkQED) show that the "right" stack depends on the question type, so all metrics should be broken down by question class. LLM judges are biased: the largest current effect is style/verbosity, and position bias is now small. Use pairwise swap checks, rubrics, assertion-based scoring and a human-calibrated subset.

### Cited Findings
**Core metric definitions**
- RAGAS faithfulness is the share of claims in the answer that the retrieved context supports. An LLM splits the answer into claims and checks each one. It is reference-free. Context precision is the mean precision@k: are relevant chunks ranked above irrelevant ones? Context recall needs ground truth. — [benchmarkingagents.com/ragas](https://benchmarkingagents.com/ragas); [helpmetest.com](https://helpmetest.com/blog/ragas-rag-pipeline-evaluation/); [RAGAS docs (v0.1 metrics)](https://docs.ragas.io/en/v0.1.21/concepts/metrics/) (secondary sources disagree slightly on which metrics need references, so check the docs for the version you use).
- RAGAS test-set generation uses "evolutions" (simple, reasoning, multi-context questions) mixed by a weighted distribution. Newer versions build a knowledge graph of entities, themes and relationships to drive generation. — [helpmetest.com](https://helpmetest.com/blog/ragas-rag-pipeline-evaluation/); [agentwiki.org](https://agentwiki.org/ragas)
- A 2025 paper proposes a KG-based RAGAS extension (multi-hop reasoning, community detection), arguing that atomic-fact and embedding-only metrics discriminate poorly. — [emergentmind summary](https://api.emergentmind.com/topics/ragas-framework) (secondary summary, not verified against the paper).
- **ARES** (Stanford: Saad-Falcon, Khattab, Potts, Zaharia) fine-tunes lightweight judges on synthetic data for three scores: context relevance, answer faithfulness and answer relevance. It uses **prediction-powered inference (PPI)**: a small human-labeled set corrects the judge's predictions over a large unlabeled set and gives tighter confidence intervals (95% in the paper). It needs "only a few hundred human annotations", and systems are ranked by interval midpoints. — [arXiv 2311.09476](https://arxiv.org/html/2311.09476v2); code at stanford-futuredata/ARES.
- **RAGBench / TRACe** (Galileo): 100k examples across 12 datasets, including the customer-support/manual sets **EManual, TechQA, DelucionQA**, legal **CUAD**, biomedical **PubMedQA, CovidQA**, and finance **FinBench, TAT-QA**. The TRACe metrics are uTilization, Relevance, Adherence (hallucination) and Completeness. A fine-tuned ~400M DeBERTa-large evaluator outperformed few-shot LLM judges across domains. — [arXiv 2407.11005](https://arxiv.org/html/2407.11005v2); dataset at HF `rungalileo/ragbench`. (Summaries differ on exactly which baselines it beat, e.g. whether RAGAS/TruLens were included.)

**GraphRAG-specific evaluation**
- **GraphRAG-Bench** ("When to use Graphs in RAG", Xiang et al., arXiv 2506.05690, ICLR 2026) has two corpora: Novel (loosely structured Gutenberg texts) and Medical (tightly structured NCCN guidelines). There are four question levels: Fact Retrieval, Complex Reasoning, Contextual Summarization, Creative Generation. The paper evaluates graph construction (node/edge count, average degree, clustering coefficient), retrieval (Evidence Recall, Context Relevance) and generation (ROUGE-L, answer accuracy, faithfulness, evidence coverage). — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3)
- GraphRAG-Bench results: on simple fact retrieval, basic RAG matches or beats GraphRAG (RAG reaches 83.2% evidence recall on novel fact retrieval). GraphRAG wins on complex reasoning and summarization (MS-GraphRAG 50.9 vs RAG+rerank 42.9 accuracy on novel complex reasoning). Denser graphs (HippoRAG2, average degree 8.75–13.31) correlate with higher recall. Methods covered: MS-GraphRAG, HippoRAG, HippoRAG2, LightRAG, Fast-GraphRAG, RAPTOR, LazyGraphRAG. — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3)
- Token cost per query in GraphRAG-Bench: vanilla RAG ~879, HippoRAG2 ~1,008, RAPTOR ~3,400, LightRAG >100k, MS-GraphRAG global the highest (the table shows ~331k while the text says ~40k, so the paper is internally inconsistent). — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3)
- The authors note that "GraphRAG frequently underperforms vanilla RAG on many real-world tasks" and that HotpotQA and MultiHop-RAG do not properly test graph structure. — [arXiv 2506.05690](https://arxiv.org/pdf/2506.05690)
- **Microsoft BenchmarkQED** (open source, PyPI `benchmark-qed`) has three parts:
  - AutoQ synthesizes queries along a local-to-global spectrum and can generate "assertions", testable factual statements that act as unit tests.
  - AutoE does LLM-as-judge pairwise comparison, reference-based scoring and assertion-based scoring, with the metrics comprehensiveness, diversity, empowerment and relevance.
  - AutoD summarizes datasets.

  Microsoft's example used 50 queries per class (200 total), 6 judge trials per query and GPT-4.1 as judge. — [Microsoft Research blog](https://www.microsoft.com/en-us/research/?p=1140429); [docs](https://microsoft.github.io/benchmark-qed); [AutoE notebook](https://microsoft.github.io/benchmark-qed/notebooks/autoe)
- LazyGraphRAG has indexing cost equal to vector RAG and 0.1% of full GraphRAG, with query cost about 4% of GraphRAG global search (Microsoft's own claim). — [Microsoft Research](https://microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost)
- KEO (Oct 2025), a KG+RAG system on the aviation-maintenance OMIn dataset: the KG "markedly improves global sensemaking", while "text-chunk RAG remains effective for fine-grained procedural tasks". It used stronger LLMs (GPT-4o, Llama-3.3) as judges for smaller local models. — [arXiv 2510.05524](https://arxiv.org/html/2510.05524v1)
- Neo4j's internal studies found Text2Cypher to be "relatively the most consistent retrieval approach across question variations". This is a vendor study with no published method. — [Neo4j blog](https://neo4j.com/blog/developer/effortless-rag-text2cypherretriever/)

**Tool landscape (mostly vendor blogs, low-to-medium reliability)**
- RAGAS is the de facto RAG metrics library but weak on CI ergonomics. DeepEval runs pytest-style assertions for CI and includes faithfulness, contextual recall/precision and answer relevancy plus agent metrics. Promptfoo is CLI/YAML-first and strongest at multi-model prompt comparison and red-teaming. Phoenix is OpenTelemetry-native tracing (ELv2 license, source-available rather than OSI open source). LangSmith suits LangChain/LangGraph teams for dataset experiments. TruLens provides the "RAG triad" (now owned by Snowflake via TruEra). — [machinelearningmastery.com](https://machinelearningmastery.com/llm-evaluation-frameworks-compared-how-to-actually-measure-what-your-model-does/); [futureagi.com](https://futureagi.com/blog/best-rag-evaluation-tools-2026/); [adaline.ai](https://www.adaline.ai/blog/best-rag-evaluation-tools-in-2026)
- One source claims RAGAS shows a fading maintenance signal (last commit 24 Feb 2026). This is unverified, and the source is a competitor (futureagi). — [futureagi.com/ragas-alternatives](https://futureagi.com/blog/ragas-alternatives-2026/)
- A common pattern is RAGAS for retrieval metrics plus DeepEval for CI gating in the same pipeline, with separate tools for tracing and prompt versioning. — [futureagi.com](https://futureagi.com/blog/best-rag-evaluation-tools-2026/)

**LLM-as-judge biases and mitigations**
- Survey (arXiv 2412.05579): swap-and-check (run both orderings and drop inconsistent verdicts) is the simplest fix for position bias. Verbosity fixes include CALM perturbation-based evaluation and Con-J contrastive-rationale judges. — [arXiv 2412.05579](https://arxiv.org/pdf/2412.05579)
- Shi et al. 2024 ("Judging the Judges", position bias): the quality gap between candidate answers is the main driver of position bias, and prompt length has only a weak effect. — [themoonlight review](https://www.themoonlight.io/review/judging-the-judges-a-systematic-evaluation-of-bias-mitigation-strategies-in-llm-as-a-judge-pipelines); [arXiv 2406.07791](https://arxiv.deeppaper.ai/papers/2406.07791v7/similar)
- An April 2026 preprint finds position bias in current models is small (≤0.04) while style bias is largest (0.76–0.92). Verbosity preference varies by model family. Position swapping reduced style bias but could increase verbosity bias, and rubric-based calibration gave the largest verbosity reduction. Single author, not peer-reviewed. — [arXiv 2604.23178](https://arxiv.org/html/2604.23178)
- Length-controlled win rates (Dubois et al. 2024) are a post-hoc correction for verbosity. — cited in [arXiv 2412.05579](https://arxiv.org/pdf/2412.05579)
- A small fine-tuned evaluator (DeBERTa) beat few-shot LLM judges on RAGBench, so a trained judge is a viable, cheaper and less biased alternative once labels exist. — [arXiv 2407.11005](https://arxiv.org/html/2407.11005v2)

### Inferences
- Break every metric down by question class. Averages will hide the GraphRAG/vector-RAG crossover documented in GraphRAG-Bench and KEO (graphs help global/multi-hop/summarization questions and hurt or don't help factoid/procedural ones).
- For a manuals assistant, add metrics beyond the RAGAS set:
  - **Citation accuracy**: does the cited chunk or section actually support the sentence? This can be implemented as faithfulness computed per citation.
  - **Abstention quality**: precision/recall of "I don't know" on unanswerable questions.
  - **Terminology correctness** against the glossary.
  - **Cost/latency per query**, including indexing cost amortized over queries.
- Prefer assertion-based scoring (BenchmarkQED-style "unit tests" per question) over holistic 1–10 scores. It is less sensitive to style and verbosity bias.
- Judge protocol: pairwise with both orderings, a rubric, a judge from a different model family than the generator, repeated trials (Microsoft used 6), and calibration against a human-labeled subset (ARES/PPI-style).

### Gaps
- No independent, primary-source head-to-head of the eval tools themselves (RAGAS vs DeepEval vs TruLens agreement with humans). The comparisons found are vendor blogs.
- No standard "citation accuracy" or "abstention" metric was found in a primary source this session. ALCE (Gao et al. 2023, citation recall/precision) is the likely reference (background, unverified).
- Current versions and licensing of RAGAS, Phoenix and TruLens were not verified against the repositories.
- No GraphRAG-Bench figures were found for ontology/OWL-reasoner-backed QA. KGQA-specific metrics (Hits@k, SPARQL/Cypher execution accuracy) were not researched in depth.

---

## 2. Building test sets for a domain (synthetic, ontology-driven, taxonomy, human gold, size)

### Takeaway
Use a stratified test set: a human-written gold core of a few hundred questions, plus a larger synthetic set generated from manuals (RAGAS/AutoQ-style) and from the ontology (competency questions). Synthetic questions rank *retriever* configurations reliably but rank *generators* poorly. Keep generator and LLM comparisons on human questions. Size the sets with power analysis on paired, question-level differences rather than picking a round number.

### Cited Findings
- **Synthetic validity** ("Can we Evaluate RAGs with Synthetic Data?", arXiv 2508.11758): synthetic benchmarks reliably rank RAGs that vary by retriever configuration, in line with human-labeled baselines. They fail to produce consistent rankings across generator architectures, which the authors attribute to task mismatch and stylistic bias. — [arXiv 2508.11758](https://arxiv.org/html/2508.11758)
- LLM-generated questions spread their focus across the whole context and follow more consistent patterns. Human questions favor the beginning of texts and are more diverse. — [arXiv 2501.03491](https://arxiv.org/pdf/2501.03491v2.pdf) (via [alphaxiv](https://alphaxiv.org/overview/2501.03491v2))
- ExpertGenQA (specialized domains): reward models scored questions higher when only the wording was made more human-sounding. This shows style bias when filtering synthetic questions automatically. — [arXiv 2503.02948](https://arxiv.org/pdf/2503.02948)
- RAGAS generator question types are simple, reasoning and multi-context, mixed by a distribution, and built from a KG of the corpus. — [helpmetest.com](https://helpmetest.com/blog/ragas-rag-pipeline-evaluation/); [agentwiki](https://agentwiki.org/ragas)
- BenchmarkQED AutoQ generates queries in local-to-global classes (Microsoft example: 50 per class) plus assertions for scoring. AutoQ does not provide ground-truth answers. Microsoft used the best system as the reference, which is circular, so be careful. — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=1140429); [AutoE docs](https://microsoft.github.io/benchmark-qed/notebooks/autoe)
- GraphRAG-Bench's four-level taxonomy (fact retrieval, complex reasoning, contextual summarization, creative generation) is a ready-made template for question classes. — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3)
- **Competency questions (CQs) from the ontology:** VSPO (AAAI 2026) argues that LLM CQ generation has mostly been judged by similarity to human CQs. Its authors propose generating CQs aimed at exposing semantic pitfalls such as missing disjointness. NeOn-GPT uses CQ generation, then reuse, then formalization, then validation. — [arXiv 2511.07991](https://arxiv.org/html/2511.07991v2); [NeOn-GPT](https://eprints.soton.ac.uk/511839/1/neon_gpt_2_final.pdf)
- **Statistics:** "Adding Error Bars to Evals" (Miller, Anthropic, arXiv 2411.00640) treats questions as samples from a super-population. It recommends reporting the standard error with each mean, using question-level *paired* differences when comparing two systems, doing power analysis to plan sample size, and reducing variance by resampling answers. It argues bootstrapping is usually unnecessary. — [arXiv 2411.00640](https://arxiv.org/abs/2411.00640?context=cs)
- ARES/PPI: a few hundred human labels plus many judge-labeled items gives valid confidence intervals. — [arXiv 2311.09476](https://arxiv.org/html/2311.09476v2)
- TechQA's real user questions number only about 600 train, 310 dev and 490 eval, illustrating how expensive real domain gold sets are. — [arXiv 1911.02984](https://arxiv.org/abs/1911.02984)

### Inferences
- Suggested question taxonomy for this project, stratified and tagged on every item:
  1. factoid/lookup
  2. procedural (step sequences from manuals)
  3. conceptual/definitional ("what is X, how does it differ from Y"), with glossary/ontology as gold
  4. comparison
  5. multi-hop / relational
  6. global/sensemaking ("what are the main failure modes across…")
  7. cross-domain (e.g. medicine × CS: term collisions such as "model", "protocol", "agent")
  8. emerging-domain (terms newer than the LLM cutoff or absent from the ontology)
  9. unanswerable / false-premise, for abstention
  10. ambiguous, needing clarification
- Sources for each class:
  - Manuals produce classes 1–2 and 4–5 via RAGAS/AutoQ-style generation.
  - The ontology produces CQs as SPARQL/Cypher templates. Each CQ is instantiated for many entities, and the answer is computed *from the KG*, which gives free, exact gold answers for classes 3 and 5.
  - Perturbing entities or using out-of-corpus entities produces class 9.
  - Human SMEs write classes 6–8 and 10 and review samples of the rest.
- Sizing rule of thumb, derived from binomial standard error (background stats, not from a cited source): SE ≈ sqrt(p(1−p)/n). At p≈0.7 this gives ~±4.5 pp 95% CI at n=400 and ~±9 pp at n=100. Paired comparisons need fewer items because per-question variance cancels.
  - Plan ≥100 items per class you want to report separately.
  - Plan ~300–500 human gold items overall, used for PPI calibration.
  - Plan thousands of synthetic items for retriever sweeps.
- Hold out a frozen "regression" split that is never used for tuning (especially if you use DSPy-style optimizers).

### Gaps
- No primary source gives a specific recommended test-set size for RAG evaluation. The numbers above are derived from basic statistics.
- No source found that evaluates CQ-derived QA sets as RAG benchmarks (as opposed to ontology validation).
- No published benchmark found for cross-domain (e.g. medicine × CS) term-collision QA.

---

## 3. Evaluating KG / ontology / glossary quality itself

### Takeaway
Evaluate the knowledge structures separately from end-to-end QA, because a component ablation is only interpretable if you know how good the KG is. Use three tools together:
- **Correctness:** estimate it by sampled human annotation of triples (cluster/stratified sampling cuts cost 60–80%).
- **Structural and modeling errors:** run OOPS! pitfall scanning, reasoner consistency checks and SHACL validation.
- **Fitness for purpose:** answer the competency questions.

LLM-generated ontologies have known characteristic defects.

### Cited Findings
- Gao et al., "Efficient Knowledge Graph Accuracy Evaluation" (VLDB 2019): estimate KG accuracy by human annotation of *sampled* triples. Cluster sampling (by entity) with unequal probabilities, plus stratified and two-stage sampling, gives statistically valid estimates. It reports up to 60% annotation cost reduction for static KGs and 80% for evolving KGs (incremental evaluation via stratified and reservoir sampling). — [arXiv 1907.09657](https://arxiv.org/abs/1907.09657v1); [Amazon Science](https://amazon.science/publications/efficient-knowledge-graph-accuracy-evaluation)
- OOPS! is the main rule-based ontology pitfall scanner, with a catalog built from analysis of 693+ ontologies. Semantic pitfalls such as "P10 missing disjointness" cannot be detected by reasoners or rules and need expert review or targeted CQs (VSPO). — [arXiv 2511.07991](https://arxiv.org/html/2511.07991v1)
- Pitfalls specific to LLM-generated ontologies include semantic redundancy, hierarchy conflicts and property-modeling artifacts. Unconstrained LLM generation shows superfluous elements, flat hierarchies and inconsistent domain/range axioms. — [CEUR Vol-4246 LLMs4KGOE](https://ceur-ws.org/Vol-4246/llms4kgoe-4.pdf)
- In Lippolis et al.'s experiments, OOPS! checks and CQ verification each caught issues the other missed, so use both. This is a slide-level claim. — [Lippolis slides](https://geist.re/_media/aira:slides-anna-sofia-lippolis-2025-12-11.pdf)
- NeOn-GPT validation covers syntax, consistency (reasoner) and modeling-pitfall checks. — [NeOn-GPT](https://eprints.soton.ac.uk/511839/1/neon_gpt_2_final.pdf)
- GraphRAG-Bench reports graph structural statistics (nodes, edges, average degree, clustering) and finds denser graphs correlate with higher evidence recall. These are useful cheap proxies for auto-extracted property graphs. — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3)

### Inferences
Suggested KG/ontology/glossary scorecard:
- **Correctness:** triple precision from a sampled, SME-annotated set (Gao-style).
- **Coverage/completeness:** the share of a gold term list or index of the manuals present as concepts. For glossary/SKOS, also check that every term in the gold set has a prefLabel, a definition and altLabels for synonyms and abbreviations.
- **Consistency:** OWL reasoner (e.g. HermiT/ELK) unsatisfiable-class count, SHACL violation count, OOPS! pitfall counts by severity.
- **Fitness:** % of CQs answerable with a correct query result.
- **Structure:** depth, branching, orphan concepts, average degree.
- **Glossary-specific:** definition faithfulness to source text (an LLM judge vs the source paragraph) and ambiguity flags for terms with multiple meanings across domains. The ambiguity flags are critical for medicine × CS overlap.

Then correlate KG quality with downstream QA scores across KG versions to learn how much KG quality matters.

### Gaps
- OQuaRE and other ontology-metric frameworks returned no results this session.
- No source found for formal SKOS glossary quality metrics (qSKOS is the likely reference; background, unverified).
- No published completeness-estimation method for LLM-extracted property graphs was found.

---

## 4. Modular/pluggable frameworks and reference stacks

### Takeaway
No single framework spans the whole design space. A practical setup is:
- an orchestration layer that can swap retrievers (LlamaIndex, LangGraph or Haystack);
- specialist GraphRAG engines run as interchangeable "retriever backends" behind a common interface (MS GraphRAG/LazyGraphRAG, LightRAG, HippoRAG2, Neo4j GraphRAG Python, Cognee, Graphiti);
- one eval harness on top.

Vendor benchmarks between memory/GraphRAG tools are not trustworthy. Run your own.

### Cited Findings
- Neo4j GraphRAG Python provides VectorRetriever, HybridRetriever (vector + full-text), HybridCypherRetriever (hybrid search plus a custom Cypher traversal) and Text2CypherRetriever. Version numbers in secondary sources conflict (1.8 vs 1.18). — [Neo4j blog](https://neo4j.com/blog/developer/effortless-rag-text2cypherretriever/); [GraphAcademy](https://graphacademy.neo4j.com/courses/workshop-graphrag-introduction/3-querying/1-retrievers); [docsearch](https://docsearch.algolia.com/mcp/docs/repo/neo4j/neo4j-graphrag-python)
- LightRAG (HKU, arXiv 2410.05779) does dual-level (entity + theme) graph retrieval with incremental updates, so changing document sets don't need full re-indexing. — [memoryplugin landscape](https://www.memoryplugin.com/wiki/landscape.html)
- Graphiti (Zep, arXiv 2501.13956) is a temporally-aware KG: edges carry validity windows, and contradicted facts are invalidated rather than deleted. This is relevant for emerging domains where facts change. — [zby ingest notes](https://zby.github.io/commonplace/sources/graphiti-temporal-knowledge-graph.ingest/); [vectorize.io](https://vectorize.io/articles/zep-vs-cognee)
- Cognee is a KG plus embeddings pipeline with many retrieval modes (one source says 14). Its comparative benchmarks against LightRAG, Graphiti and Mem0 are vendor-run. — [cognee blog](https://www.cognee.ai/blog/guides/open-source-memory-frameworks-llm-agents); [vectorize.io](https://vectorize.io/articles/zep-vs-cognee)
- The GraphRAG-Bench repo (github.com/GraphRAG-Bench/GraphRAG-Benchmark) already wraps MS-GraphRAG, HippoRAG/2, LightRAG, Fast-GraphRAG, RAPTOR and LazyGraphRAG against vanilla RAG. It is a usable reference harness for swapping GraphRAG engines. — [arXiv 2506.05690](https://arxiv.org/pdf/2506.05690)
- MedRAG is a reference toolkit that factorially combines 5 corpora, 4 retrievers and 6 LLMs. It found that combining retrievers (fusion) beats single retrievers and that a domain-specific retriever (MedCPT) was best. — [arXiv 2402.13178](https://arxiv.org/abs/2402.13178)

### Inferences
These are background and were not verified this session.
- LlamaIndex (PropertyGraphIndex, multiple retrievers plus router/fusion) and Haystack 2.x (typed component pipelines) are the most "swap-friendly" for factorial experiments.
- LangGraph suits agentic routing (deciding which store to query per question type).
- DSPy is useful for *optimizing* prompts and modules per configuration, so each configuration is compared at its best rather than with one hand-tuned prompt. This needs a strict train/dev/test split.

Recommended architecture: define one `Retriever` interface that returns ranked passages plus provenance, with implementations for BM25, dense, hybrid, KG/Text2Cypher, SPARQL-over-OWL with a reasoner, glossary lookup, and each GraphRAG engine. Define one `Generator` interface, and drive everything from a YAML config so that every run equals one config hash. Log traces to OpenTelemetry (Phoenix/Langfuse) for cost and latency.

### Gaps
- Feature, API and version details of LlamaIndex, Haystack, DSPy, LangGraph and MS GraphRAG were not verified against current (Nov 2026) docs in this session.
- No independent benchmark found comparing Cognee, Graphiti and LightRAG on document QA (as opposed to agent memory).
- No reference open-source stack combining OWL reasoning with RAG was located.

---

## 5. Experimental design (ablation, factorial, cost/latency, regression, A/B)

### Takeaway
Run a staged design:
1. Use cheap retrieval-only metrics on a large synthetic set to screen many configurations (a fractional-factorial or one-factor-at-a-time ablation from a strong hybrid baseline).
2. Run end-to-end, judge-scored, paired comparisons of the top few configurations on the human gold set, with error bars, broken down by question class.
3. Put the winner behind CI regression gates and online A/B testing.

Always track tokens, indexing cost and latency next to quality, because GraphRAG token costs vary by more than 100×.

### Cited Findings
- Report the standard error of every mean, compare systems on question-level paired differences, plan sample size with power analysis, and reduce variance by resampling multiple answers per question. — [arXiv 2411.00640](https://arxiv.org/abs/2411.00640?context=cs)
- PPI combines a small human-labeled set with a large judge-labeled set to get confidence intervals. ARES ranks systems by interval midpoint. — [arXiv 2311.09476](https://arxiv.org/html/2311.09476v2)
- Factorial precedent: MedRAG (corpora × retrievers × LLMs) found up to 18% accuracy gain over chain-of-thought, and retriever fusion helped. — [arXiv 2402.13178](https://arxiv.org/abs/2402.13178)
- Cost spread in GraphRAG-Bench: ~879 tokens/query for vanilla RAG vs >100k for LightRAG and far more for MS-GraphRAG global. LazyGraphRAG claims 0.1% of GraphRAG indexing cost. — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3); [Microsoft Research](https://microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost)
- Synthetic sets are fine for retriever sweeps but not for generator comparisons. — [arXiv 2508.11758](https://arxiv.org/html/2508.11758)
- Run multiple judge trials per query (Microsoft used 6). — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=1140429)
- DeepEval provides pytest-style CI gating, and Promptfoo provides YAML-based regression and red-team runs. — [machinelearningmastery.com](https://machinelearningmastery.com/llm-evaluation-frameworks-compared-how-to-actually-measure-what-your-model-does/)

### Inferences
Concrete plan. These are the researcher's synthesis.

**Phase 0 – Baselines**
- B0: no retrieval (the LLM alone).
- B1: BM25.
- B2: dense.
- B3: hybrid BM25+dense plus a reranker.

This tells you how much each layer adds.

**Phase 1 – Factor screening.** Score each run on retrieval metrics (evidence recall, context precision) on the synthetic set, per question class. Factors:
- A: lexical retrieval {off, BM25}
- B: dense retrieval {off, model1, model2}
- C: glossary/SKOS query expansion and definition injection {off, on}
- D: taxonomy-based filtering/routing {off, on}
- E: KG retrieval {off, Text2Cypher, entity-neighborhood}
- F: GraphRAG engine {none, LazyGraphRAG/MS local+global, LightRAG, HippoRAG2}
- G: ontology+reasoner (inferred facts materialized) {off, on}
- H: agentic router (LLM picks the tools) {off, on}

Use a 2^(k−p) fractional factorial or an ablation from the full stack: remove one component at a time, and note that interaction effects such as glossary × KG matter.

**Phase 2 – End-to-end.** Take the 3–5 best configurations plus the baselines. Use the human gold set, at least 3 samples per question, a pairwise swap-checked judge from a different model family, and assertion-based scoring. Correct with PPI. Report per class: correctness, faithfulness/citation accuracy, abstention F1, tokens, $/query, p50/p95 latency, and indexing cost/time. Choose on a Pareto frontier (quality vs cost), possibly with *routing by question class*: vector RAG for factoid/procedural questions, graph for global/multi-hop questions, ontology for conceptual questions.

**Phase 3 – Robustness.** Test four conditions:
- Emerging domain: hold out the newest documents, add them incrementally, and measure update cost and quality. This is where LightRAG/Graphiti incremental updates matter.
- Cross-domain: a term-collision set.
- Paraphrase robustness: question variations.
- KG-quality sensitivity: deliberately degrade the KG by 10/20% and measure the QA drop.

**Phase 4 – Production.**
- Run the frozen regression suite on every change (DeepEval/promptfoo in CI with thresholds and tolerance bands sized from the standard errors).
- Run shadow mode, then an A/B test on user metrics: thumbs up/down, escalation-to-human rate, time to resolution, citation click-through.
- Feed sampled production questions back into the gold set.

### Gaps
- No primary source found on formal factorial/DoE methodology applied specifically to RAG configurations. The plan above is synthesized.
- No published guidance found on online A/B metrics for documentation assistants.

---

## 6. Public datasets usable as proxies

### Takeaway
Several public datasets are good proxies:
- **Manuals / technical support:** TechQA, EManual, DelucionQA (all packaged in RAGBench), and OMIn/KEO for maintenance.
- **Graph-vs-RAG with structured domain text:** GraphRAG-Bench Medical (NCCN guidelines).
- **Medical:** MIRAGE.
- **Legal retrieval:** LegalBench-RAG and CUAD.

None covers ontology-backed or cross-domain conceptual QA, so a custom set is unavoidable.

### Cited Findings
- **TechQA** (IBM, ACL 2020): real user questions from IBM developer forums, answered by IBM Technotes. About 600 train, 310 dev and 490 eval items, plus ~800k Technotes as a corpus. Designed for domain adaptation. — [arXiv 1911.02984](https://arxiv.org/abs/1911.02984)
- **RAGBench** packages EManual, TechQA and DelucionQA (customer support), CUAD (legal), PubMedQA and CovidQA (biomedical), FinBench and TAT-QA (finance), and HotpotQA, MS Marco, HAGRID and ExpertQA (general), with TRACe labels. HF: `rungalileo/ragbench`. — [arXiv 2407.11005](https://arxiv.org/html/2407.11005v2)
- **OMIn**: 2,748 FAA aviation maintenance/incident records of 1–3 sentences each, on Zenodo. The **KEO** paper builds a KG and a QA benchmark on it covering global sensemaking and procedural tasks. — [arXiv 2510.05524](https://arxiv.org/html/2510.05524v1)
- **GraphRAG-Bench**: Medical (NCCN guidelines) and Novel corpora with a 4-level question taxonomy. — [arXiv 2506.05690v3](https://arxiv.org/html/2506.05690v3)
- **MIRAGE**: 7,663 questions from 5 medical QA datasets, with the MedRAG toolkit (Findings of ACL 2024). — [arXiv 2402.13178](https://arxiv.org/abs/2402.13178)
- **LegalBench-RAG**: 6,858 query–answer pairs over a 79M+ character corpus. Evaluates retrieval of minimal relevant spans. — [arXiv 2408.10343](https://arxiv.org/html/2408.10343v1)
- **BenchmarkQED** ships with AP News health articles (1,397 docs) as an example dataset for local/global queries. — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=1140429)

### Inferences
- Use TechQA, EManual and DelucionQA as "manual QA" proxies for factoid and procedural classes. Use GraphRAG-Bench Medical and OMIn/KEO for the graph-vs-chunk crossover. Combine MIRAGE (medicine) with a CS corpus to build a synthetic medicine × CS cross-domain stress test.
- Use proxies only to validate the harness and get prior rankings. Final decisions should come from the domain's own gold set, given the synthetic-vs-human and domain-shift findings above.

### Gaps
- No public QA dataset with an accompanying OWL ontology/SKOS glossary for technical manuals was found. Candidates to check (background, unverified) are KGQA sets such as LC-QuAD/QALD (DBpedia/Wikidata) and SciQA (ORKG) for the ontology-QA component.
- Not verified: current availability and licensing of TechQA (the original leaderboard link ibm.biz/Tech_QA may be dead) and the OMIn Zenodo record.
- No cross-domain (medicine × CS) QA benchmark was found.
