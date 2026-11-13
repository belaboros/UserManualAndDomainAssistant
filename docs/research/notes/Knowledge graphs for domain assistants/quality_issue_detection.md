# Automated Detection of Quality Issues in Documentation Corpora (contradictions, gaps, terminology drift, outdated content)

Scope note: Notes compiled 2026-11-13 from web searches of arXiv/ACL/RE literature, vendor docs and practitioner blogs. Most numbers come from abstracts or search-result summaries; full paper tables were usually not checked. "Benchmarked" means a reported number on a named dataset; "claim" means vendor or practitioner material with no independent evaluation.

## 1. LLM- and NLI-based contradiction detection (within and across documents): methods, accuracy, false positives

### Takeaway
Contradiction detection with frontier LLMs works but is unreliable. On long technical documents, the best model (gpt-5) recovers about 64% of planted inconsistencies, and roughly 1/3 of its suggestions are not judged legitimate. Explicit, numeric and negation contradictions are easy. Implicit ones that need context or multiple reasoning steps are hard. Hybrid pipelines do best: LLM extraction followed by formal or rule checking, or by an NLI pre-filter and an LLM verifier. Pure-LLM approaches have high false-positive rates.

### Cited Findings
**Single-document (self-contradiction) benchmarks**
- ContraDoc (Li, Raheja, Kumar; NAACL 2024) is described as the first human-annotated dataset of self-contradictions in long documents, covering multiple domains, document lengths, contradiction types and scopes. It evaluated GPT-3.5, GPT-4, PaLM2 and LLaMAv2. GPT-4 performed best and "can outperform humans", but it is still unreliable and struggles with contradictions that need nuance and context — [arXiv 2311.09182](https://arxiv.org/abs/2311.09182v2); [HF page](https://huggingface.co/papers/2311.09182)
- ContraDoc has two tasks: (a) binary detection (does the document contain a contradiction?) and (b) ranking the top-5 evidence sentences, where random guessing gives an Evidence Hit Rate of 16%. Contradiction type drives difficulty more than other factors. Negation and numeric contradictions are easiest — [UT Austin poster](https://cs.utexas.edu/~ml/posters/li.naacl24.poster.pdf). (Exact per-model numbers not verified.)
- FIND, "On Finding Inconsistencies in Documents" (Lovering et al., Kensho, arXiv Dec 2025): domain experts inserted inconsistencies into long, technical, complex documents. Motivating use cases are academic, legal and financial auditing. The best model, gpt-5, recovered 64% of inserted inconsistencies, so even the best models miss "almost half" — [arXiv 2512.18601](https://arxiv.org/abs/2512.18601)
- FIND, in the wild: on 50 original arXiv papers, the authors judged 136 of gpt-5's 196 suggestions to be legitimate inconsistencies the authors had missed (about 69%, so about 31% were false or not-useful flags) — [arXiv 2512.18601](https://arxiv.org/abs/2512.18601). A search summary of the same work reports exact-match precision of 53% on the planted-error set, expert-judged usefulness of 67%, and about 2.6 findings per document. Many "extra" findings were real pre-existing issues — [project page](https://cjlovering.github.io/pages/find) (summary-derived; not verified in the full text).

**Multi-document / RAG context conflicts**
- Gokul, Tenneti, Nakkiran (arXiv 2504.00180, 2025), "Contradiction Detection in RAG Systems: Evaluating LLMs as Context Validators", covers three conflict types: self-contradiction in one document, conflicting document pairs, and conditional conflicts across three documents. Pairwise checking scales quadratically (20 docs → 190 pairs). Larger models do better, but the best prompting strategy varies by task and model. Chain-of-thought helps some models and hurts others. Context validation remains hard even for SOTA LLMs — [arXiv 2504.00180](https://arxiv.org/html/2504.00180v1); [aitopics summary](https://aitopics.org/doc/arxivorg:6A93E384)
- ContraGen (arXiv 2510.03418) generates synthetic enterprise documents with self and pairwise contradictions as a benchmark. It mines conflicts by combining NLI models with LLM reasoning and a confidence-weighted score. The legal variant is LegalWiz. Its argument is that existing benchmarks rarely go beyond single-sentence pairs — [arXiv 2510.03418](https://arxiv.org/html/2510.03418v1)
- eTracer (EMNLP 2026): polarity-aware grounding roughly doubled contradiction detection over a document-level baseline (27.9% → 51.9%, n=30, small study). It notes that NLI models only classify polarity on isolated sentence pairs — [ACL Anthology 2026.emnlp-main.314](https://aclanthology.org/2026.emnlp-main.314.pdf)
- WikiContradict (IBM, NeurIPS 2024 D&B): 253 human-annotated instances of real Wikipedia contradictions, tested both as single-passage RAG and as RAG with two contradictory passages. LLMs struggle most with implicit conflicts that require reasoning. The human evaluation covered 5 LLMs and more than 3,500 judgments. An automated judge built on Llama-3-70B-instruct reached F-score 0.8 — [arXiv 2406.13805](https://arxiv.org/html/2406.13805v1); [NeurIPS](https://nips.cc/virtual/2024/poster/97844)
- CONFLICTS benchmark, "DRAGged into Conflicts" (Cattan et al., arXiv 2506.08500, 2025): proposes a taxonomy of conflict types in search-augmented generation, each with a target model behavior, and an expert-annotated benchmark. LLMs often fail to resolve source conflicts. Failure modes include misclassification, omission and arbitrary preference. Explicitly prompting models to recognize and reason about conflicts improves responses, but large headroom remains — [arXiv 2506.08500](https://arxiv.org/abs/2506.08500v2); [aitopics](https://aitopics.org/doc/arxivorg:D2DCAAE1)
- Other conflict benchmarks: MAGIC (2025) builds KG-based conflicts between two similar contexts, and models struggle especially with multi-hop conflicts — [emergentmind 2507.21544](https://www.emergentmind.com/papers/2507.21544). ConfRAG (ACL 2026) has 1,814 questions with web-retrieved paragraphs, 57.2% of them with explicit contradictions, and shows gaps for GPT-4.1 and Claude-3.7-Sonnet — [papers.cool ACL 2026](https://papers.cool/venue/2026.acl-long.11@ACL). RAMDocs covers conflicting evidence in RAG — [fugumt](https://fugumt.com/fugumt/paper_check/2506.08500v2_enmode)

**Requirements-engineering (RE) inconsistency detection: the closest analogue to manuals with normative statements**
- SAT-LLM (Fazelnia, Mirakhorli, Bagheri, 2024) pairs LLMs with SMT solvers for conflicting requirements and reports P=1.00, R=0.83, F1=0.91. The plain-ChatGPT baseline in the same paper got P=0.85, R=0.31, i.e. LLM-alone has low recall — [search summary of RE literature](https://par.nsf.gov/servlets/purl/10574434) (small, domain-specific evaluation)
- Gärtner and Göhlich (DESIGN 2024) combine formal logic with GPT-3 and report 99% accuracy and 60% recall on a real e-bus project. Their logic-based ALICE tool (ASE journal 2024) found 60% of contradictions and beat an LLM-only baseline — [Cambridge DESIGN 2024](https://cambridge.org/core/journals/proceedings-of-the-design-society/article/towards-an-automatic-contradiction-detection-in-requirements-engineering/C7D7E69A58BBC2BC6054AF0BB972A3E1)
- Pereira et al. (SBQS 2024, journal 2026) compared requirements anomaly tools including ChatGPT. Recall and precision were unsatisfactory, averaging below 66% and 57% respectively — [JSERD](https://journals-sol.sbc.org.br/index.php/jserd/article/download/5919/3998/39763)
- RE@Next! 2025 reports that combining LLM detection with rule-based clustering improves both precision and recall — [RE 2025](https://conf.researchr.org/details/RE-2025/RE-2025-re-next--papers/19/Combining-Established-and-Emerging-Techniques-to-Detect-Inconsistencies-in-Requireme)

**Docs-vs-code inconsistency: precision engineering lessons**
- DocPrism (arXiv 2511.00215) keeps a 15% flag rate and reaches precision of 0.62 without fine-tuning: 0.70 on Python/TS and 0.56–0.58 on C++/Java. 48% of false positives come from incorrect reasoning, and lack of API knowledge is next. Plain LLM use produced false positives "high enough to be unusable", largely because the model treats normal abstraction gaps between high-level docs and detailed code as inconsistencies. The fix was local categorization plus external filtering — [arXiv 2511.00215](https://arxiv.org/html/2511.00215v1)
- METAMON (arXiv 2502.02794) uses generated tests plus LLM reasoning and reaches precision 0.72 on 9,482 doc/code pairs from Defects4J — [arXiv 2502.02794](https://arxiv.org/abs/2502.02794v1)
- CASCADE (arXiv 2604.19400) takes an explicitly precision-first stance, trading recall for fewer false alarms — [arXiv 2604.19400](https://arxiv.org/pdf/2604.19400)
- Trust-allocation study (arXiv 2604.03447): detection of explicit documentation errors was 68–95%, but it dropped when the implementation drifted while the documentation still looked plausible — [arXiv 2604.03447](https://arxiv.org/html/2604.03447v1)

### Inferences
- For a manual corpus, expect frontier-LLM recall of about 50–65% on non-trivial contradictions, and about 60–70% "useful" precision on raw LLM flags. Precision figures are not comparable across studies because they use different definitions (exact-match vs expert-judged usefulness).
- The RE results consistently show that LLM-alone has decent precision but poor recall (≈0.3). Formalizing statements first (an LLM extracts structured facts or constraints, then a solver or rules compare them) raises both precision and recall. This supports a KG-mediated design: extract (entity, attribute, value, condition, version) facts and compare them structurally, rather than asking an LLM to compare free text.
- Pairwise all-vs-all comparison is quadratic. Candidate generation (blocking) by shared KG entity or attribute, or by embedding similarity, is needed before LLM/NLI verification.
- Many apparent contradictions in manuals are conditional (different product variant, version, mode or role). Recording conditions and scope in the extracted facts is key to suppressing false positives, as the ContraDoc "nuance and context" difficulty and the DocPrism abstraction-gap false positives both suggest.

### Gaps
- No public benchmark found specifically for contradictions in user manuals or procedural technical documentation across documents.
- Exact per-model numbers for ContraDoc and Gokul et al. were not retrieved from the full texts.
- No head-to-head NLI-vs-LLM comparison found on long-document self-contradiction in a single study.

## 2. Gap / completeness detection: how "gap" is operationalized

### Takeaway
"Gap" is operationalized in four main ways:
1. Coverage of a reference set of questions or concepts (competency questions, user queries, ontology classes).
2. Missing terminology or concepts relative to a domain model or language model (masked-LM prediction).
3. Violations of structural completeness rules: missing definitions, labels, references or required procedure fields, often checked with SHACL-style cardinality constraints.
4. Unanswerable real user questions.

Peer-reviewed accuracy data is thin. LLM-prompted completeness detection shows low F1 (~0.3 in one non-peer-reviewed study).

### Cited Findings
- Luitel, Hassani, Sabetzadeh (REJ / REFSQ'23, arXiv 2308.03784) mask words in requirements and use BERT predictions to surface missing terminology. They evaluated on 40 PURE specifications and added an ML filter to cut noise. BERT beat simpler baselines. Limitation: incompleteness was simulated by withholding content, because no expert-labelled incompleteness existed — [arXiv 2308.03784](https://arxiv.org/abs/2308.03784); [Springer REJ](https://link.springer.com/10.1007/s00766-024-00416-3)
- Bachelor thesis (Karaca, 2024; not peer-reviewed): GPT-4o detecting completeness-type violations with generated-knowledge, few-shot and CoT prompting reached overall F1 ≈ 0.3. Precision was consistently higher than recall. Missing labels and references had the lowest recall — [GitHub](https://www.github.com/yavuzkaraca/bachelor-thesis)
- OE-Assist: an LLM gives Yes/No verification of whether an ontology answers each competency question (CQ), plus a SPARQL query, over 1,393 CQs cross-checked by two ontology engineers. Human accuracy dropped when the LLM's guidance was wrong (automation bias), giving an efficiency/accuracy trade-off — [arXiv 2507.14552](https://arxiv.org/abs/2507.14552v1)
- NeOn-ACE adds iterative LLM coverage evaluation against regulatory CQs inside ontology construction. OntoScope organizes candidate CQs by coverage and granularity to expose gaps (user study, 15 ontology engineers). CompCQ measures CQ-set coverage as the share of CQs matched above an embedding-similarity threshold. A life-insurance benchmark compares a text-only LLM pipeline with a SPARQL-over-ontology pipeline for gap and overlap determinations — [CEUR Vol-4205](https://ceur-ws.org/Vol-4205/paper10.pdf); [CEUR Vol-4293](https://ceur-ws.org/Vol-4293/paper7.pdf); [SWJ](https://semantic-web-journal.net/system/files/swj4014.pdf)
- An earlier NeOn-GPT evaluation used only the Wine ontology, which is likely memorized by LLMs, and the authors call for broader domains. This is a caution against over-trusting LLM coverage judgments on familiar domains — [search summary / SWJ](https://www.semantic-web-journal.net/system/files/swj3980.pdf)
- SHACL used as a post-extraction quality gate (materials-science KG, NeurIPS 2026 listing) detected missing links, invalid types, broken references and cross-document identity cases before expert review — [NeurIPS 2026](https://neurips.cc/virtual/2026/158007)

### Inferences
- Practical gap types for manuals map to checkable rules:
  - A term is used but never defined: glossary or KG lookup.
  - A procedure has no prerequisites, expected result or error recovery: a SHACL shape on a Procedure/Step model.
  - A UI element, setting or error code appears in one manual but has no description anywhere: entity coverage.
  - A frequent user question has no supporting passage: log-driven gap detection from QA retrieval failures or abstentions.
- Competency questions can be generated from the domain ontology or glossary and from real user queries. Running them through the QA system yields a coverage matrix: unanswered or low-confidence CQs are gap candidates.
- Because of the OE-Assist automation-bias finding, the review UI should show evidence (retrieved passages, query result) rather than only an LLM verdict.

### Gaps
- No benchmark found for procedure-completeness detection in user manuals specifically (e.g., missing steps).
- No peer-reviewed accuracy numbers found for LLM-based "missing definition" detection in documentation.

## 3. Terminology drift / inconsistent terminology

### Takeaway
Industry practice (Acrolinx, Markup AI, Congree) is controlled-vocabulary enforcement. A termbase holds preferred, admitted and deprecated/forbidden terms linked as concept entries, and deprecated variants are flagged with suggested replacements. "Term discovery" clusters candidate variants for a terminologist to approve. Academic work covers synonym and overloaded-term detection (requirements), "nonuniform language" detection (same action, different wording), and embedding comparison of term usage across domains or corpora. No end-to-end benchmark of embedding-based drift detection across document versions was found.

### Cited Findings
- Acrolinx terminology: terms have statuses (preferred, admitted, deprecated). Deprecated terms are always flagged. Terms grouped into one concept entry are linked, so a flagged deprecated term triggers a suggestion of the linked preferred or admitted term. Unwanted variants are marked deprecated — [Markup AI/Acrolinx support](https://support.markup.ai/hc/en-us/articles/10228296536082); [terminology quick start](https://support.markup.ai/hc/en-us/articles/10304675174418) (vendor documentation, not independent evaluation)
- Acrolinx Term Discovery groups similar terms, filters duplicates and exports discovered variants into the termbase (candidate harvesting plus human approval) — [Markup AI support](https://support.markup.ai/hc/en-us/articles/10228296813074) (vendor claim)
- Markup AI glossaries define preferred, deprecated and forbidden terms and scan as writers type — [Markup AI blog](https://markup.ai/?p=1833) (vendor)
- Vendor case studies claim business impact, e.g., Pepperl+Fuchs "33% translation cost savings" from consistent terminology — [casestudies.com](https://www.casestudies.com/company/acrolinx/case-study/how-acrolinx-is-helping-pepperlfuchs-increase-content-quality) (vendor claim, unverified)
- Congree advocates starting terminology management small, then expanding — [Congree blog](https://www.congree.com/en/blog/new-approach-to-terminology-management) (vendor)
- Wang et al. (NLDB 2013) rank concepts to detect overloaded terms (one term, many meanings) and synonyms (many terms, one meaning) in software requirements, and report them effective — [NLDB 2013 PDF](https://www.eecis.udel.edu/~yuewang/paper/nldb2013.pdf)
- "Nonuniform language in technical writing: detection and correction" (Natural Language Engineering, 2021) detects sentences that describe the same action with different wording, e.g., "show" vs "display" for making a control unit visible — [Cambridge NLE](https://www-cambridge-org.ezproxyberklee.flo.org/core/services/aop-cambridge-core/content/view/5D05C80A7B6BEB03165B649A07F453D9/S1351324920000133a.pdf/nonuniform-language-in-technical-writing-detection-and-correction.pdf)
- Hamon and Nazarenko (1998) infer synonymy among candidate terms extracted from a technical document using a general dictionary — [ACL P98-1082](https://preview.aclanthology.org/fix_video/P98-1082.pdf)
- Ferrari and Esuli (2019) compare word embeddings trained on different domain corpora to measure cross-domain differences in term usage, as an ambiguity estimate. The same technique can compare manual versions or product lines to detect drift — summarized in [search results](https://aclanthology.org/2023.iwcs-1.26v1.pdf) (the original paper URL was not retrieved)
- Ontology-reuse study: clustering labels by intra-cluster similarity flagged 115 clusters of possibly invalid synonyms. Many flagged "synonyms" were only singular/plural or hyphenation variants, a noise source to normalize first — [arXiv 2205.02892](https://arxiv.org/pdf/2205.02892)
- USPTO patent "Semantics mismatch in service information" compares terms extracted from service documents against a target part-name list using an overlap threshold, then rewrites mismatches. This is lexical, not embedding-based — [USPTO 8924363](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8924363)

### Inferences
- A glossary or SKOS-style termbase (prefLabel, altLabel, hiddenLabel/deprecated, with scope notes per product or version) gives deterministic, high-precision drift detection: any hiddenLabel or deprecated occurrence is a flag. The ML part is candidate generation, i.e. clustering surface variants by embeddings, string similarity or lemmatization, with an admin confirming merges. This matches the vendor workflow (Term Discovery → approve → enforce).
- Normalize inflection, plural and hyphenation before clustering to cut noise (ontology-reuse finding).
- The two error types need different detectors: synonym/variant drift (many terms, one concept) and overloaded terms (one term, several concepts across manuals). Overloading is better found by contextual-embedding divergence per term across documents or versions (Ferrari and Esuli style).

### Gaps
- No published precision/recall found for Acrolinx-style term discovery or for LLM-based terminology auditing.
- No peer-reviewed study found on embedding-based terminology drift detection across successive versions of user manuals.

## 4. Logical consistency checking via ontology reasoners (OWL, SHACL) on extracted knowledge

### Takeaway
SHACL is the practical workhorse. It is used as a deterministic quality gate after LLM extraction (catching missing links, invalid types, dangling references and duplicates), and its violation reports feed LLM repair or explanation loops. OWL-DL reasoners (HermiT, Pellet, ELK) detect unsatisfiable classes and inconsistent ABoxes, but only for contradictions that are formally axiomatized (disjointness, functional properties, cardinality). Most natural-language contradictions in manuals need conditional and numeric comparison that is better expressed as SHACL/SPARQL rules. I found no source combining OWL reasoning with LLM-extracted manual content.

### Cited Findings
- OntoLogX (arXiv 2510.01409) uses a three-stage validation of LLM-generated KGs: syntax, SHACL shape compliance, then semantic checks (missing or duplicate event nodes, dangling references). Failures go back to the LLM with targeted correction prompts. If no valid graph results, it stores an empty graph so bad output never enters the KB. It does not use OWL reasoning — [arXiv 2510.01409](https://arxiv.org/pdf/2510.01409)
- Materials-science KG validation (NeurIPS 2026): SHACL as a deterministic gate after LLM extraction found missing links, invalid types, broken references and cross-document identity cases before expert review — [NeurIPS 2026](https://neurips.cc/virtual/2026/158007)
- Lin et al. (arXiv 2507.22419, 2025), a systematic evaluation of LLM-based KG repair of SHACL violations on cyber-physical graphs. Best results came from concise prompts containing the violated SHACL constraints plus key KG context — [arXiv 2507.22419](https://arxiv.org/abs/2507.22419v1)
- xpSHACL uses RAG plus an LLM to explain SHACL violations in plain language for non-experts. This is relevant to the admin review UI — [arXiv 2507.08432](https://arxiv.org/html/2507.08432v1)
- A 2026 Frontiers visual-analytics tool combines SHACL violation reports with an LLM chat assistant to help users find inconsistencies — [Frontiers Bioinformatics 2026](https://public-pages-files-2025.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2026.1756507/pdf)
- The RE hybrid results (SAT-LLM: P 1.00 / R 0.83 vs ChatGPT-alone R 0.31; ALICE logic beats LLM-only) are the strongest quantitative evidence that formalizing and then reasoning beats LLM-only comparison for contradictions — see section 1 sources ([Cambridge DESIGN 2024](https://cambridge.org/core/journals/proceedings-of-the-design-society/article/towards-an-automatic-contradiction-detection-in-requirements-engineering/C7D7E69A58BBC2BC6054AF0BB972A3E1))

### Inferences
- Recommended pattern for manuals:
  1. An LLM extracts typed facts into a schema (Product, Version, Feature, Setting with value range and default, Procedure/Step, ErrorCode, Term), with provenance (doc, section, version, date).
  2. SHACL shapes enforce completeness, e.g., every ErrorCode has a resolution and every Term used has a definition. Cardinality violations then mean gaps.
  3. SPARQL/SHACL-SPARQL rules flag conflicts, e.g., the same Setting × same applicability scope with different default value or range across documents. These are contradiction candidates, which an LLM then verifies with the source passages.
  4. Optionally declare OWL functional properties and disjointness so a reasoner detects logical inconsistencies.
- Precision of the formal layer is very high: violations are real with respect to the schema. Its recall is bounded by extraction quality, so extraction errors become the main false-positive source (a "contradiction" caused by mis-extraction). Keep provenance so a reviewer can check quickly.
- LLM-generated natural-language explanations of violations (xpSHACL) suit the domain-admin review app.

### Gaps
- No measured precision/recall found for SHACL/OWL-based contradiction detection on LLM-extracted documentation content.
- OWL-reasoner use specifically on LLM-extracted manual knowledge was not found (a follow-up search on "HermiT/ELK + LLM extraction" was suggested but not done).

## 5. Presenting conflicting / low-quality source information to end users in QA answers

### Takeaway
Research converges on making the conflict explicit, not silently picking a side. Models should recognize the conflict type and respond per type (e.g., present both claims with sources, prefer the newer/authoritative source when the conflict is due to staleness, and qualify uncertainty). Explicit conflict-reasoning prompting improves this but leaves large headroom. User studies show that clear, actionable explanations and confidence cues raise trust and source checking. No study was found that isolates the effect of disclosing source disagreement versus hiding it.

### Cited Findings
- CONFLICTS ("DRAGged into Conflicts") defines a target behavior per conflict type. LLM failures are misclassification, omission and arbitrary preference. Explicit conflict reasoning ("Chain-of-Conflict"-style prompting) improves answers — [arXiv 2506.08500](https://arxiv.org/abs/2506.08500v2); [newx summary](https://newx.sg/paper/detail/87908bbe-f823-11f0-b84c-00163e10baa7)
- WikiContradict found LLMs often fail to reflect both sides when given two contradictory passages, especially for implicit conflicts. The evaluation judged whether answers acknowledged the contradiction — [arXiv 2406.13805](https://arxiv.org/html/2406.13805v1)
- Łajewska and Balog (arXiv 2601.14460, 2026) ran a two-stage user study comparing RAG answers with and without explanations (source attribution, factual grounding, information coverage). Trust was not determined solely by objective answer quality. It was significantly moderated by the clarity and actionability of explanations and by users' prior knowledge. The authors say RAG systems still lack signals of low confidence and known limitations — [arXiv 2601.14460](https://arxiv.org/html/2601.14460v1)
- CEUR workshop study (n=26): color-coded confidence marks on quotes raised trust ratings and increased source views, even though perceived ease of verification did not change. Time pressure modulated uptake — [CEUR Vol-4265](https://ceur-ws.org/Vol-4265/paper4.pdf)
- "Information Discernment in LLMs" (arXiv 2607.19355, 2026): a Prolific study on whether chatbots should weight conflicting sources by reliability rather than by closeness to the model's prior, including users' reactions when that principle is violated — [arXiv 2607.19355](https://arxiv.org/pdf/2607.19355)
- Practitioner guidance (not empirical): answer phrasing like "Sources differ on X", with uncertainty signaling, and evaluation of whether responses fairly represent conflicting evidence — [Zilliz FAQ](https://zilliz.com/ai-faq/what-happens-if-the-retrieval-strategy-returns-contradictory-information-from-different-sources-how-should-the-llm-handle-it-and-how-do-we-evaluate-whether-it-handled-it-correctly.md)
- Stale docs produce confident wrong answers. A chunk describing a deprecated auth flow can still score ~0.92 similarity to a current question, so semantic retrieval alone will not demote it. Date or version metadata ("freshness watermarks") lets the model qualify answers — [tianpan.co blog](https://tianpan.co/blog/2026-05-07-stale-docs-confident-wrong-answers-rag-knowledge-base); [AI Engineering Patterns](https://prajwalamte.github.io/AI-Engineering-Patterns/patterns/retrieval-and-memory/retrieval-freshness-watermark/) (practitioner, illustrative number)

### Inferences
- For the assistant, attach known open issues from the issue store to retrieved passages and KG facts. When an answer depends on a fact with an open contradiction or staleness issue, surface a short, actionable notice: what differs, both sources with version/date, which one the system prefers and why (newer version, authoritative doc type), and a "reported to admin" status. Do not block the answer.
- Show issues only when they affect the answer: the question's entities intersect the issue's entities. This avoids alert fatigue and matches the "actionability" finding.
- Resolved issues (admin decision) should become KG overrides or preferred-source rules that the answering pipeline follows. This closes the loop.

### Gaps
- No controlled user study found that compares disclosing a source disagreement with silently choosing one, in technical or enterprise documentation QA.

## 6. Outdated content detection, plus practical precision concerns: noise volume, triage, severity scoring

### Takeaway
Outdated-content detection in practice relies on metadata and heuristics: document date/version, decay scores relative to the expected update frequency of each document class, superseding versions, and cross-checks against an authoritative source such as the current product or API. Research and practitioner evidence agree that raw LLM flagging is too noisy. Usable systems control the flag rate, filter by category, use precision-first thresholds and route findings through human review. No published severity-scoring scheme for documentation issues was found. Severity has to be designed (impact × confidence × reach).

### Cited Findings
- Freshness dimensions: content age, embedding lag, stale-retrieval rate (share of queries returning outdated docs) and coverage drift (share of corpus past its staleness threshold) — [Atlan](https://atlan.com/know/llm-knowledge-base-freshness-scoring/) (vendor/practitioner)
- Decay heuristic: staleness_score = days_since_last_update / acceptable_update_frequency_for_doc_class. It is only as reliable as the dates, which are often missing or mixed in scraped content — [tianpan.co](https://tianpan.co/blog/2026-05-06-rag-knowledge-freshness-tiered-reindex-staleness); [twig.so](https://www.twig.so/dev/rag-scenarios-and-solutions/data-quality/temporal-staleness) (practitioner)
- Agent-based detect → correct → validate loops start with API reference and configuration docs, where discrepancies are mechanically checkable. They must distinguish stale docs (describe the past) from aspirational docs (describe the future) — [VirtusLab Visdom guide](https://visdom-maturity-matrix.virtuslab.com/guides/organization/agent-detects-stale-context-updates-validates) (practitioner)
- DocPrism's design lesson: cap the flag rate (15%) and apply local categorization plus external filtering. Plain-LLM false positives were "unusable" — [arXiv 2511.00215](https://arxiv.org/html/2511.00215v1)
- CASCADE: precision-first, deliberately accepting lower recall to minimize false alarms — [arXiv 2604.19400](https://arxiv.org/pdf/2604.19400)
- FIND: about 2.6 findings per document from gpt-5, with about 31% not judged legitimate on real papers. At corpus scale that is a large review load — [arXiv 2512.18601](https://arxiv.org/abs/2512.18601)
- OE-Assist: wrong LLM guidance degraded expert accuracy (automation bias), a risk in review apps that pre-label issues — [arXiv 2507.14552](https://arxiv.org/abs/2507.14552v1)
- ContraGen uses a confidence-weighted score combining NLI and LLM signals, a template for ranking contradiction candidates — [arXiv 2510.03418](https://arxiv.org/html/2510.03418v1)

### Inferences
Proposed triage design, synthesized from the above:
- Use deterministic detectors first: termbase hits, SHACL violations, explicit version supersession. They have high precision and are cheap.
- Gate LLM detectors with candidate blocking (shared KG entity) and a confidence score (NLI × LLM agreement, self-consistency over samples). Show only items above a precision-calibrated threshold, and keep the rest in a "low-confidence" backlog.
- Severity score ≈ impact class × reach × confidence:
  - Impact class: safety/compliance or data loss > wrong procedure or value > missing info > terminology/style.
  - Reach: query traffic hitting the affected entities, from QA logs, plus the number of manuals affected.
  - Confidence: detector score.
- Deduplicate and cluster issues by KG entity so one root cause, e.g., a renamed feature, yields one review item rather than dozens.
- Calibrate per category with a small labeled sample (e.g., 100 flags per detector type) before production, and track admin accept/reject rates as ongoing precision. Rejected flags become suppression rules or few-shot negatives.
- Separate "conflict due to scope/version" (often legitimate) from "true contradiction". Requiring the extractor to capture applicability conditions is the biggest false-positive reducer.

### Gaps
- No peer-reviewed benchmark found for outdated-content detection in documentation. Most sources are practitioner or vendor blogs.
- No published, validated severity-scoring model for documentation quality issues was found.
- No data found on the real-world volume of issues per manual page in industrial documentation corpora.
