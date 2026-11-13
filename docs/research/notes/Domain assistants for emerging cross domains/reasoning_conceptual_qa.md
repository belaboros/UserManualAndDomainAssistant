# Reasoning over Taxonomies, Ontologies and Knowledge Graphs for Conceptual QA (vs Keyword Search / Standard RAG)

Scope note: research run 2026-11-13, about 15 searches and fetches. Peer-reviewed and arXiv results are kept apart from vendor or practitioner claims. Numbers from different papers use different LLMs, metrics and datasets, so they are **not directly comparable**.

## 1. Neuro-symbolic approaches (LLM + OWL/RDFS reasoners, rules, SPARQL/Cypher generation, KGQA) vs RAG

### Takeaway
Structured querying clearly helps on **schema-heavy, multi-hop and aggregation questions**. The best evidence is the enterprise benchmark where GPT-4 went from 16% on SQL to 54% on a KG. Text-to-SPARQL and Text-to-Cypher accuracy is still moderate (about 30–60% execution accuracy on public KGQA benchmarks) and drops as query complexity rises. I found **no controlled study showing that "LLM + OWL reasoner" beats RAG on QA accuracy**. Most of the reasoner work uses it for validation and consistency, not for answering.

### Cited Findings
- **Enterprise KG vs SQL benchmark (Sequeda, Allemang, Jacob; data.world, Nov 2023).** On insurance-domain enterprise questions, GPT-4 zero-shot reached 16% accuracy against SQL and 54% when the same questions were posed over a KG/ontology representation. On high-schema-complexity questions, SQL scored 0% and the KG scored 35.7–38.7%. — [arXiv 2311.07509](https://arxiv.org/pdf/2311.07509). The authors are data.world staff, so this is a vendor-affiliated but published benchmark.
- **Follow-up from the same authors (2024).** They used the ontology to check LLM-generated SPARQL and had the LLM repair failing queries, and report that this further supports investing in ontologies for accuracy. The search snippets did not show the repair figures. — [arXiv 2405.11706](https://arxiv.org/html/2405.11706v1)
- **Text-to-SPARQL on public KGQA (2025).** Execution accuracy (EA): LC-QuAD 2.0 about 49% (ReAct) and about 52% (AutoGen); QALD-9 Plus about 59% (AutoGen); QALD-10 about 49% (Spinach), against about 30% for a vanilla LLM. These figures come from search snippets of the Schemaforge paper, not its full tables. — [arXiv 2508.01815](https://arxiv.org/pdf/2508.01815)
- **Spider4SPARQL** is described as much harder than LC-QuAD and QALD, with LLMs reaching about 45% EA in a citing summary. The paper's versions disagree on dataset size (10,181 questions vs 4,721 queries). — [arXiv 2309.16248](https://arxiv.org/html/2309.16248v2)
- **Text2Cypher (Neo4j, Dec 2024).** The dataset has 44,387 instances (39,554 train, 4,833 test), and only 2,471 test items can be scored by execution. Fine-tuning improved every model. Approximate exact-match gains: Llama-3.1-8B +0.11, Gemini-1.5-Flash +0.09, GPT-4o-mini +0.06, GPT-4o +0.01, so models that were already strong gained least. One public community model had seen 14.4% of the test data, which shows contamination risk. Absolute scores were only shown in a figure. — [arXiv 2412.10064](https://arxiv.org/html/2412.10064v1)
- **CypherBench.** Execution accuracy on full-scale modern KGs falls consistently as query pattern complexity grows. — [alphaxiv 2412.18702](https://alphaxiv.org/overview/2412.18702v2)
- **Text2Cypher across languages (Neo4j, 2025).** Accuracy is highest in English, lower in Spanish and lowest in Turkish. English-only fine-tuning widens that gap, while multilingual fine-tuning narrows it. — [arXiv 2506.21445](https://arxiv.org/abs/2506.21445v2)
- **"Mind the Query" (EMNLP 2025 Industry)** is a multi-domain Text2Cypher dataset over 11 real-world KGs. It was built because earlier datasets (Neo4j Text2Cypher, SynthT2C) did not cover enough domains. — [ACL Anthology](https://aclanthology.org/anthology-files/pdf/emnlp/2025.emnlp-industry.133.pdf)
- **KG-augmented LLM agents on KGQA.** Think-on-Graph has a GPT-4 agent run beam search over the KG. It beat fine-tuned methods on most multi-hop KBQA sets, with CWQ about 69.5%. Replacing LLM pruning with BM25 or SentenceBERT cost an average of 8.4 points on CWQ and 15.1 on WebQSP. — [arXiv 2307.07697](https://arxiv.org/pdf/2307.07697). Reasoning on Graphs reports 62.6% Hits@1 on CWQ (via a secondary summary). — [alphaxiv 2310.01061](https://www.alphaxiv.org/overview/2310.01061v2)
- **OG-RAG (Microsoft Research, EMNLP 2025).** It builds an ontology-grounded hypergraph and retrieves a minimal set of hyperedges as context. Against RAG, RAPTOR and GraphRAG across four LLMs it reports +55% recall of accurate facts and +40% response correctness. It also reports 30% faster attribution of answers by users and +27% on fact-based reasoning. Evaluation covered agriculture and news only. — [arXiv 2412.15235](https://arxiv.org/html/2412.15235v1); [EMNLP 2025](https://aclanthology.org/anthology-files/pdf/emnlp/2025.emnlp-main.1674.pdf)
- **Reasoner-in-the-loop.** HermiT checks LLM outputs against OWL ontologies, and explanations of any inconsistency are fed back to the LLM for correction. This targets consistency, not QA accuracy versus RAG. — [arXiv 2504.07640](https://arxiv.org/abs/2504.07640)
- **ORACLE.** It builds a question-specific ontology and formal logic chains for multi-hop QA without training, and is compared against multi-hop methods rather than plain RAG. — [arXiv 2508.01424](https://arxiv.org/html/2508.01424v2)
- **Proposed ontology + RAG architecture (2026).** It combines RDF/OWL, SPARQL, SHACL and vector RAG, and argues RAG is only a retrieval layer. No head-to-head benchmark was seen. — [arXiv 2604.20795](https://www.alphaxiv.org/abs/2604.20795)

### Inferences
- For "what kinds of X exist", "what is needed before X" and "which X have property P" questions, generated or **templated** graph queries are more reliable than vector RAG. Given 30–60% free-form text-to-query accuracy, free-form generation alone is too unreliable for an assistant. Templates plus constrained generation, validation and repair are the realistic route.
- The largest gains appear where the question depends on schema or structure (the 0% → about 36% case), which is exactly the profile of taxonomy and prerequisite questions.
- A symbolic reasoner's evidenced value today is **materialising entailments offline** (subclass closure, transitive prerequisites, inverse properties) and **validating** LLM output. I did not find evidence that it improves QA accuracy at query time.

### Gaps
- No controlled benchmark compares LLM + OWL/RDFS reasoner (or SWRL/Datalog) against RAG on the same conceptual questions.
- I did not retrieve the full TEXT2SPARQL 2025 challenge leaderboard ([arXiv 2512.14277](https://arxiv.org/pdf/2512.14277)) or absolute Text2Cypher accuracy for 2025–2026 frontier models.
- I found no reliable published numbers from Stardog (Voicebox) or Ontotext (GraphDB Talk-to-Your-Graph) on accuracy versus RAG. Treat any such claims as unverified vendor marketing.

## 2. LLMs' own taxonomic and ontological reasoning (and when external reasoners are needed)

### Takeaway
LLMs handle shallow subsumption and common-domain is-a facts reasonably well. They degrade sharply on **specialised domains, leaf-level concepts, negative-inclusion transitivity, large instance sets (ABoxes) and full query answering**. For an assistant over a proprietary domain ontology, the hierarchy and its entailments should come from the ontology and a reasoner, not from the LLM's parametric knowledge.

### Cited Findings
- **TaxoGlimpse (VLDB 2024).** Ten taxonomies and 18 LLMs were tested with zero-shot, few-shot and chain-of-thought prompting. The best LLM's is-a accuracy drops by **up to 30%** going from common to specialised domains and from root to leaf levels. — [arXiv 2406.11131](https://arxiv.org/abs/2406.11131v1); [VLDB](https://vldb.org/pvldb/vol17/p2919-sun.pdf)
- **DL-Lite study (2024).** Models tested: GPT-3.5, GPT-4o and LLaMA3-8B. — [arXiv 2406.17532](https://arxiv.org/html/2406.17532v2)
  - Syntax checking: GPT-4o scored F1 92–100, but models accepted some invalid axioms and confused concepts with roles.
  - Subsumption on small TBoxes looked promising.
  - Transitivity: models did well with positive inclusions and ABox rules, but **poorly with negative-inclusion (disjointness) transitivity**, even with instructions and examples. Their explanations for those cases were sometimes wrong.
  - Instance checking: nothing was inferred on the largest ABoxes, which exceeded the context window. Performance fell to near 0% past a size threshold.
  - Query answering on LUBM with GPT-4o: **no query was fully correct**, and several answers were hallucinated.
  - Satisfiability: GPT-4o reached F1 94.5 on a simple ontology but 69.0 on a complex one.
  - The ground truth was computed with the HermiT reasoner.
- **ONTOLAMA (subsumption probing).** Zero-shot accuracy is about 50–60%, rising to 90%+ with 128 examples. It tests subsumption only, not transitivity. — [alphaxiv ONTOLAMA](https://alphaxiv.org/benchmarks/university-of-oslo/ontolama). This is a secondary listing.
- **LLM simulating an OWL reasoner via RAG over LUBM (CEUR KGNeSy 2025).** The study grades queries by inference depth. I could not extract its numbers because the PDF text was unreadable. — [CEUR Vol-4064](https://ceur-ws.org/Vol-4064/kgnesy-paper1.pdf)
- **LLMs for OWL proofs (2026).** Performance depends strongly on whether input is formal logic or natural language, and degrades with noisy or incomplete input. — [arXiv 2601.12444](https://arxivlens.com/PaperView/Details/large-language-model-for-owl-proofs-1820-490079e9). This is a secondary listing.

### Inferences
- Rule of thumb: use the LLM to **explain** entailments that a reasoner or graph query has already computed. Do not use it to compute them, especially for disjointness ("X is not a Y"), deep or transitive chains, or many instances.
- Because ontology text in context degrades with size, the right pattern is retrieval of the relevant ontology slice or materialised facts, not "ontology-as-context" for the whole ontology.

### Gaps
- No 2025–2026 benchmark tests frontier reasoning models (o-series, Claude, Gemini 2.5+) on inheritance of properties and constraints. The studies above mostly used GPT-4o-era models.
- I could not get per-depth accuracy curves from the LUBM study.

## 3. Results on conceptual, definitional and relational question types

### Takeaway
Graph and hierarchy-aware retrieval helps most on **complex reasoning, summarisation and synthesis across concepts**, and helps little or even hurts on **simple fact or definition lookup**, where vanilla RAG with reranking is as good or better. On textbook-style conceptual questions, gains over a strong LLM baseline are small (about 1–2 points). Hierarchical (RAPTOR) and PageRank (HippoRAG) retrieval do best. Structure-heavy methods can fall below a no-retrieval baseline.

### Cited Findings
- **GraphRAG-Bench (Xiao et al., 2506.02404; 1,018 questions from 20 CS textbooks).** Results with GPT-4o-mini. — [arXiv 2506.02404](https://arxiv.org/html/2506.02404v2)
  - Overall accuracy: no retrieval 74.29; BM25 74.28; TF-IDF 75.71; MS-GraphRAG 75.24; RAPTOR 76.67 (best); HippoRAG 70.48; LightRAG 65.24; DALK 70.00; G-Retriever 70.95. My mapping of the table columns is an interpretation and should be verified against the paper.
  - DALK and G-Retriever fell below the no-retrieval baseline because structure-heavy retrieval added noise.
  - Multiple-choice accuracy sometimes dropped because noisy retrieval overrode answers the LLM already knew.
  - All GraphRAG methods reduced accuracy in mathematics.
  - Reasoning quality improved: the rationale score R went from 55.45 (base) to about 59–61, and accuracy-with-sound-reasoning AR went from 39.78 to 43–45.5 (RAPTOR 45.53, HippoRAG 44.55, BM25 44.15). The base LLM often reached correct answers by conjecture or pattern matching.
  - The authors conclude that accuracy alone is insufficient and rationale quality must also be scored.
- **"When to use Graphs in RAG" GraphRAG-Bench (Xiang et al., ICLR 2026).** Accuracy on the novel dataset with GPT-4o-mini. — [arXiv 2506.05690](https://arxiv.org/html/2506.05690v3)

  | Method | Fact retrieval | Complex reasoning | Contextual summarisation |
  |---|---|---|---|
  | RAG + rerank | 60.92 | 42.93 | 51.30 |
  | MS-GraphRAG | 49.29 | 50.93 | 64.40 |
  | HippoRAG2 | 60.14 | 53.38 | 64.10 |
  | LightRAG | 58.62 | 49.07 | 48.85 |

  RAG with reranking had the best evidence recall for fact retrieval (83.21%). The authors conclude that graphs help with reasoning and synthesis across concepts, while for simple lookups basic RAG is enough and graphs add noise.
- **Vendor leaderboard (FalkorDB, Aug 2026).** On the novel subset, averaged over task types, FalkorDB reports its GraphRAG-SDK at 66.09, against 48.35 for RAG + rerank and 45.09 for LightRAG. Competitor figures were copied from the leaderboard, not re-run. **This is a vendor claim.** — [FalkorDB docs](https://docs.falkordb.com/graphrag/benchmark)

### Inferences
- In this user's terms:
  - "What is X" (definitional) is closest to fact retrieval. A curated glossary lookup or good RAG is sufficient, and graph machinery adds little.
  - "How does X relate to Y", "difference between X and Y", "what kinds of X" and "what is needed before X" are relational, comparative or enumerative. They map to complex reasoning and summarisation, where graph or hierarchical methods gain about 8–13 points.
- Routing by question type, rather than always taking the graph path, is supported by both benchmarks.
- RAPTOR's success on textbooks suggests the manual's own **document hierarchy** (chapters and sections) is a cheap, strong structural signal alongside the ontology.

### Gaps
- No benchmark isolates "what is X", "difference between X and Y" or "prerequisites of X" as categories. These mappings are my own.
- I did not find an education-oriented KGQA study with concept-explanation metrics in this search pass.

## 4. Explainability: reasoning paths and subgraphs as justification; user-trust evidence

### Takeaway
Explicit graph queries and paths make answers **auditable**, and ontology-grounded context speeds up attribution. However, the only user study found suggests that visual query and path explanations can cause **over-trust even when the answer is wrong**. Explanations should be designed to calibrate trust, not maximise it.

### Cited Findings
- **OG-RAG.** Users attributed responses to context 30% faster with ontology-grounded hyperedge context. — [arXiv 2412.15235](https://arxiv.org/html/2412.15235v1)
- **LinkQ.** In a qualitative study with 14 practitioners, users including KG experts **over-trusted** the system's outputs because of its "helpful" query and path visualisations, even when the LLM was wrong. — [arXiv 2406.15859](https://emergentmind.com/papers/2406.15859). The source is a summary page.
- **GradPath (ACL 2024).** Explanations help users only if they are plausible, and implausible explanations increase doubt. Paths connecting the entities of an answer were judged more plausible. — [ACL 2024](https://aclanthology.org/2024.acl-long.654.pdf)
- **Human-in-the-loop KGQA (2026).** An explicit SPARQL or Cypher query gives an auditable trail from data to answer, whereas embedding retrieval keeps the reasoning implicit. Users refine queries conversationally. — [arXiv 2602.05512](https://arxiv.org/pdf/2602.05512)
- **GraphRAG-Bench.** Retrieval improved rationale soundness: AR rose from 39.78 to about 45.5. — [arXiv 2506.02404](https://arxiv.org/html/2506.02404v2)
- **Practitioner claim.** Empty Cypher results are easier to interpret than low vector similarity scores, which can be misleading. — [Neo4j GraphAcademy and practitioner blogs](https://graphacademy.neo4j.com/courses/workshop-genai/3-agents/4-text2cypher-retriever). This is not peer-reviewed.

### Inferences
- Show the subgraph or path and the source passages, but also show **provenance and confidence**: "derived by inheritance from class Y" versus "stated in manual §3.2". Flag answers that rely on inferred rather than asserted facts.

### Gaps
- I found no controlled experiment comparing user trust or accuracy with paths shown versus hidden.

## 5. Failure modes: incomplete ontologies, open vs closed world, brittle query generation, cost and latency

### Takeaway
The main risks:
- **Incompleteness.** KG-RAG methods degrade when key triples are missing and fall back on the LLM's memorised knowledge.
- **Closed-world misreading.** An absent edge gets reported as "no", while OWL is open-world.
- **Brittle query generation.** Accuracy drops with query complexity, non-English input and distribution shift.
- **Cost.** Graph construction and some graph retrievers cost 10–300× more tokens per query than vanilla RAG.

### Cited Findings
- **Incompleteness, Zhou et al. (2025).** ToG, RoG and G-Retriever still benefit from incomplete KGs but drop when key knowledge is missing. Earlier evaluations overstated robustness. — [arXiv 2504.05163](https://arxiv.org/html/2504.05163v2)
- **BRINK (EACL 2026).** It uses questions with no single explicit supporting triple. Current KG-RAG methods reason poorly and lean on memorised knowledge. Trained methods (RoG, GNN-RAG) are more robust. — [arXiv 2508.08344](https://arxiv.org/html/2508.08344v4)
- **IKGWQ (2025).** Random triple deletion does not reflect real incompleteness, which also involves missing entities and outdated facts. The paper proposes multi-agent debate mixing KG and LLM knowledge. — [arXiv 2511.12208](https://arxiv.org/html/2511.12208)
- **LLMs over ontologies.** They miss disjointness-based entailments and hallucinate query answers. — [arXiv 2406.17532](https://arxiv.org/html/2406.17532v2)
- **Brittleness of generated queries.**
  - Accuracy declines with Cypher pattern complexity. — [CypherBench](https://alphaxiv.org/overview/2412.18702v2)
  - Accuracy is lower for non-English questions. — [arXiv 2506.21445](https://arxiv.org/abs/2506.21445v2)
  - Train and test splits share a distribution and there is contamination, so real-world accuracy is likely lower. — [arXiv 2412.10064](https://arxiv.org/html/2412.10064v1)
- **Per-query token cost** (ICLR 2026 GraphRAG-Bench, novel dataset): vanilla RAG 879; HippoRAG2 1,008; RAPTOR 3,441; Fast-GraphRAG 4,204; HippoRAG 7,208; MS-GraphRAG local 38,707; LightRAG 100,832; MS-GraphRAG global 331,375. — [arXiv 2506.05690](https://arxiv.org/html/2506.05690v3)
- **Indexing and latency** (textbook GraphRAG-Bench):
  - Graph construction took 10–84M tokens (GraphRAG 79.9M, LightRAG 83.9M).
  - Per-query time: RAPTOR 0.02 s, HippoRAG 2.44 s, LightRAG 13.95 s, GraphRAG 44.87 s.
  - Methods that call the LLM during traversal (ToG, KGP, DALK) were slow.
  - [arXiv 2506.02404](https://arxiv.org/html/2506.02404v2)
- **Practitioner experience (secondhand podcast summary).** Expect to iterate on KG construction after retrieval testing. — [Breaktime Tech Talks Ep71](https://zeno.fm/podcast/breaktime-tech-talks/episodes/ep71-graphrag-learnings-langchain4j-apps-for-production)

### Inferences
- With a **curated** glossary, taxonomy and ontology, the cost of LLM-based graph extraction mostly disappears. The remaining costs are query-time traversal and agent loops.
- For open vs closed world: the answer layer should distinguish "the ontology states not-X" (asserted disjointness) from "no information". Constraint checks such as SHACL are closed-world by design and should be labelled that way.
- Curated ontologies avoid extraction noise but are still incomplete. Answers derived only from the graph should fall back to manual-passage RAG and say what is missing.

### Gaps
- I found no study that specifically measures wrong deductions caused by an incomplete **TBox** (missing subclass or disjointness axioms), as opposed to missing ABox triples.
- I found no published wall-clock latency for an OWL reasoner in the loop of an LLM assistant.

## 6. Concrete architecture patterns

### Takeaway
The pattern with the most support is a **tool-calling agent** that combines:
- glossary or definition lookup
- vector or hierarchical RAG over the manuals
- **parameterised graph-query templates** (with a Text2Cypher or Text2SPARQL fallback that is validated and repaired against the schema)
- graph traversal or expansion from entities found by vector search
- an offline or on-demand reasoner that materialises entailments and checks consistency

Questions are routed by type.

### Cited Findings
- **Neo4j Aura Agent** offers three tool types: vector similarity search, Text2Cypher, and **Cypher templates**. Templates are parameterised, expert-reviewed queries the agent can choose. The reference example also adds community detection and is called "minimal", not robust. — [Neo4j](https://neo4j.com/news/how-to-create-ai-agents-with-neo4j-aura-agent/); [Neo4j customer graph agent](https://neo4j.com/developer/genai-ecosystem/customer-graph-agent/). **These are vendor sources.**
- **Hybrid retrieval**, where vector search finds entry nodes and Cypher expands their relationships, is described as the common production pattern. — [practitioner blog](https://activewizards.com/blog/graph-rag-neo4j-knowledge-graphs-agent-memory/). Not peer-reviewed.
- **Ontology-validated SPARQL with LLM repair.** Generate the query, check it against the ontology, repair, then execute. — [arXiv 2405.11706](https://arxiv.org/html/2405.11706v1)
- **Reasoner feedback loop (HermiT).** Validate LLM claims and feed explanations of inconsistencies back to the LLM. — [arXiv 2504.07640](https://arxiv.org/abs/2504.07640)
- **Ontology-grounded context packing (OG-RAG).** Retrieve the minimal set of ontology-structured fact clusters (hyperedges). Code is released at github.com/microsoft/ograg2. — [arXiv 2412.15235](https://arxiv.org/html/2412.15235v1)
- **LLM-guided graph exploration (Think-on-Graph).** Agentic beam search with LLM pruning beat BM25 or SBERT pruning by 8–15 points, at higher latency. — [arXiv 2307.07697](https://arxiv.org/pdf/2307.07697)
- **Routing evidence.** Plain RAG is as good or better on fact lookup, and graphs win on reasoning and summarisation. — [arXiv 2506.05690](https://arxiv.org/html/2506.05690v3)

### Inferences
Suggested design for this assistant, mapping each question type to tools:
- **"What is X"**: glossary entry, plus the parent class, plus 1–2 manual passages.
- **"What kinds of X exist"**: a templated query over the subclass closure (materialised `rdfs:subClassOf+` / `:IS_A*`).
- **"How does X relate to Y"**: a shortest or explained path template between the two concepts, then the LLM verbalises it, citing triples and manual sections.
- **"Difference between X and Y"**: fetch both concept cards (properties, inherited constraints, siblings) plus their lowest common ancestor, then the LLM contrasts them.
- **"What is needed before X"**: a transitive prerequisite closure, with SHACL or rule checks.

Supporting practices:
- Use free-form Text2Cypher or Text2SPARQL only as a fallback, with schema validation and an empty-result or repair loop.
- Materialise RDFS/OWL-RL entailments offline, which avoids reasoner latency at query time.
- Keep the LLM in the role of planner and explainer, not deducer.

### Gaps
- No peer-reviewed head-to-head comparison of these architecture variants (templates vs free text-to-query vs ontology-as-context) on manual or documentation QA was found.
