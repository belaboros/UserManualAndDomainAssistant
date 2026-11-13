# Glossaries, Taxonomies and Ontologies for Emerging / Still-Forming Domains, and How They Evolve

Scope: support for domains whose concepts are still forming (generative/agentic AI, quantum computing) in a manual-grounded domain assistant with glossary + taxonomy + ontology + KG curated by a domain admin with a "Reviewer AI assistant". Research cutoff: November 2026. Evidence is marked [E] (empirical study / normative standard text), and claims, opinions or vendor material are marked [C].

## 1. How do terminology and concepts behave in emerging fields, and where does standardization stand?

### Takeaway
In emerging fields, terms show up before their definitions settle. There are several competing definitions (for example, "AI agent" vs "agentic AI" has no binding legal definition), and formal vocabularies trail practice by years. ISO/IEC 22989 (2022) only began a generative-AI amendment in 2025. ISO/IEC 4879 (quantum computing vocabulary, 2024) was put under revision about 18 months after publication. Even authoritative sources therefore treat definitions as plural and versioned, not single and fixed.

### Cited Findings
- [E] ISO/IEC 22989:2022 (AI concepts and terminology) has a draft Amendment 1 that "adds terms relating to Generative AI". The DAmd1 draft is dated 2025-08-01, with public enquiry until 2025-10-01. As of the sources found, I could not confirm that it has been published as final. — [DIN draft listing](https://www.din.de/en/wdc-beuth:din21:394126785); [DIN Media DAM 1](https://www.dinmedia.de/en/draft-standard/iso-iec-22989-dam-1/395325101)
- [E] A second amendment to ISO/IEC 22989 was approved as a new project on 2025-10-26 and is at the preparatory stage. — [ISO 93144](https://www.iso.org/standard/93144.html?browse=tc)
- [E] Quantum: ISO/IEC 4879:2024 "Quantum computing — Vocabulary" was published in 2024 (originally under JTC 1, now under JTC 3). At the November 2025 JTC 3 plenary its revision was validated. Parallel vocabulary projects are IEC/ISO AWI 63655 (Quantum technologies — General vocabulary), 63622 (Quantum photonics vocabulary) and 63607 (General quantities). — [ISO 80432](https://www.iso.org/standard/80432.html); [ITnation plenary report](https://itnation.lu/news/highlights-from-the-iec-iso-jtc-3-plenary-meeting-on-quantum-technology-standardization/); [ISO 94926 (63655)](https://www.iso.org/standard/94926.html)
- [E] BSI says the planned general quantum vocabulary will seed itself from foundational terms in ISO/IEC 4879, with terms carried over from quantum physics and quantum information. This shows vocabularies being split and re-homed as a field grows. — [BSI project page](https://standardsdevelopment.bsigroup.com/projects/9025-11499)
- [E] NIST AI 100-2 E2025 ("Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations", March 2025) supersedes the 2023 edition. NIST states it plans to update the report annually, so it is an explicitly versioned taxonomy. — [NIST CSRC](https://csrc.nist.gov/pubs/ai/100/2/e2025/final); [NIST](https://www.nist.gov/node/1878291)
- [C] A secondary review says the 2025 edition expands attack categories and adds GenAI-specific attacks such as prompt-injection classes. The review is internally inconsistent about edition numbering, so treat its details with caution. — [Adversa](https://adversa.ai/?p=135310)
- [E] The NIST Trustworthy & Responsible AI glossary (companion to NIST AI 100-3, 2023) was released in beta as a spreadsheet. Its stated goal is not to declare one meaning, but to give "broader awareness of the multiple meanings of commonly used terms", with source attribution per definition. — [NIST publication page](https://www.nist.gov/publications/language-trustworthy-ai-depth-glossary-terms); [AIRC glossary](https://airc.nist.gov/glossary/); [NIST AI 100-3 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-3.pdf)
- [E] The NIST CSRC glossary states that many terms "have multiple, varying definitions that reflect the different contexts of various publications written at different times". — [CSRC glossary](https://csrc.nist.gov/glossary?index=A)
- [E/C] A 2026 arXiv paper reports that there is "no widely adopted, binding legal definition of Agentic AI" in major treaties or statutes. Laws regulate such systems under "AI system" or sectoral concepts. The paper synthesizes a technical definition from six developers' documentation. — [arXiv 2603.27075](https://arxiv.org/html/2603.27075v1)
- [E/C] A 2026 compendium on defining AI agents says conceptual ambiguity "undermines the reproducibility of AI agent research" and leads to "AI agents" being conflated with "agentic AI". — [arXiv 2609.11018](https://arxiv.org/pdf/2609.11018)
- [C] A vendor survey (Nylas, n=1,026, Dec 2025) found respondents split across several interpretations of "agentic AI", with no single model clearly leading. The source has a commercial interest. — [Nylas 2026 report](https://www.nylas.com/agentic-ai-report-2026)
- [C] Industry commentary notes that analysts call agentic systems "autonomous" while CMU calls them "semi-autonomous". The difference changes risk assessment. — [FinTech Global](https://fintech.global/2025/07/14/ai-agents-explained-from-confusion-to-clarity/)
- [E] Emerging-concept detection: King, Downey & Weld (SIGIR 2020) extract new concepts from CS papers using the signal that a concept is introduced by one paper that later papers cite disproportionately. They report Precision@1000 of 99% vs 86% for prior work on arXiv CS. — [arXiv 2006.06877](https://arxiv.org/abs/2006.06877)
- [E] An older PNNL study on "morphing terminology" observes that emergent terms lose their emergent status as the associated vocabulary specializes. This is a lifecycle from novelty to normalization. — [PNNL-19493](https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-19493.pdf)
- [E] Classical terminology standards (ISO 1087:2019) structure an entry as preferred term(s), admitted term(s), abbreviated forms, definition, examples and notes. Earlier editions mark deprecated forms inline (e.g., "genus" deprecated for "generic concept"). — [ISO 1087:2019 sample](https://cdn.standards.iteh.ai/samples/62330/aa6fcc8f52e34cf39acee86fa098fc22/ISO-1087-2019.pdf); [ISO 1087:1990 sample](https://cdn.standards.iteh.ai/samples/5591/5e5a858511bf45ce916ea9b8fff136c7/ISO-1087-1990.pdf)

### Inferences
- Standardization lag here is measured in years. ISO 22989 was published in 2022, and its GenAI terms were still in draft amendment in late 2025, roughly three years after ChatGPT. An assistant for forming domains cannot wait for standards. It should treat standards as one source among several, with higher authority but lower freshness.
- Authoritative bodies (NIST AI 100-3, CSRC) model plural, attributed definitions explicitly. This supports a glossary design where a term has N definitions, each with source, date and context, rather than one canonical definition.
- Term-status vocabulary already exists in terminology science (preferred / admitted / deprecated) and can be reused for lifecycle states rather than inventing new ones.
- Citation-based and frequency-burst signals (King et al.; PNNL) suggest how a Reviewer AI could flag candidate new terms in incoming manuals. Examples are terms that appear in new documents, are absent from the glossary, and recur across sources.

### Gaps
- I could not confirm whether ISO/IEC 22989 Amd 1 (GenAI) was published as final by Nov 2026, or the stage of the ISO/IEC 4879 revision. Check the ISO pages directly.
- I found no quantitative study of how fast definitions of "agentic AI" or quantum terms (e.g., "logical qubit", "quantum advantage") change over time. The evidence is qualitative.
- The exact normative definitions of "admitted" and "deprecated" in ISO 1087:2019 / ISO 10241-1 are behind paywalls. Only previews were seen.

## 2. LLM limitations for new concepts: knowledge cutoff, context vs parametric conflict, hallucinated definitions

### Takeaway
LLMs measurably degrade on new terms. NEO-BENCH found machine translation quality nearly halves with a single neologism in a sentence. LLMs also readily invent definitions for non-existent terms (HypoTermQA). Retrieval helps a lot for fresh knowledge (FreshQA). However, models both over-trust their parametric memory in some conflicts and adopt wrong retrieved content in others (more than 60% in ClashEval). Grounding must therefore be explicit, attributed and checked, not assumed.

### Cited Findings
- [E] NEO-BENCH (ACL 2024): a benchmark of recent English neologisms (2020–2023, 2,505 items per secondary summary). Machine translation performance "nearly halves" when a single neologism is in a sentence. Models with later knowledge cutoffs get lower perplexity and do better downstream, and performance varies with the linguistic origin of the neologism. — [arXiv 2402.12261](https://arxiv.org/abs/2402.12261); item count from [review](https://www.themoonlight.io/review/neo-bench-evaluating-robustness-of-large-language-models-with-neologisms)
- [E] HypoTermQA (2024) builds hypothetical, non-existent compound terms (e.g., "Wolf LLM"; 790 terms validated by web search out of about 1,000 generated). It tests whether LLMs admit a term does not exist or fabricate an explanation, and uses retrieved similar real terms to make the questions harder. This directly measures the "hallucinated definition of a new term" failure mode. — [arXiv 2402.16211](https://arxiv.org/html/2402.16211v1)
- [C] A secondary report on a Chinese-neologism study across 18 models says models produce plausible definitions without grasping compositional rules. I did not verify this against the primary paper. — [Modelwire summary](https://themodelwire.com/article/chinese-neologisms-expose-llm-reasoning-gaps-across-18-models-01M1AQ8509CE03SFBCTFWK9QEX); likely primary [arXiv 2512.21577](https://arxiv.org/html/2512.21577v2)
- [E] Knowledge Conflicts survey (Xu et al., EMNLP 2024) sorts conflicts into context-memory, inter-context and intra-memory. Under context-memory conflict, models show "a marked tendency towards over-relying on parametric knowledge". Most solutions are tested on artificial conflicts, not "in the wild" RAG. — [arXiv 2403.08319](https://arxiv.org/html/2403.08319); [ACL Anthology](https://preview.aclanthology.org/setup/2024.emnlp-main.486)
- [E] ClashEval (NeurIPS 2024 D&B): over 1,200 questions in six domains, with retrieved context perturbed from subtle to blatant errors. Six top LLMs (incl. GPT-4o) adopted incorrect retrieved content, overriding a correct prior, more than 60% of the time. Adoption falls as the perturbation becomes more blatant and rises when the model's own token-probability confidence is low. — [arXiv 2404.10198](https://www.arxiv.org/abs/2404.10198); [NeurIPS poster](https://neurips.cc/virtual/2024/poster/97658)
- [E] FreshLLMs / FreshQA (ACL Findings 2024): 600 questions, including fast-changing and false-premise ones, with answers updated weekly. FreshPrompt (search results placed in the prompt) substantially improves accuracy. The often-quoted +49% absolute for GPT-4 under STRICT comes from a summary, so check it against the paper. — [arXiv 2310.03214](https://arxiv.org/abs/2310.03214); [ACL Anthology](https://aclanthology.org/2024.findings-acl.813)

### Inferences
- For forming domains, the two failure modes point in opposite directions, which makes them dangerous together:
  - (a) Old meaning wins. The model's parametric knowledge from before the cutoff overrides the new definition in the manual. This is especially likely when a term was renamed or redefined.
  - (b) Wrong document wins. A single sloppy or vendor-hype document overrides correct knowledge (ClashEval).
  The glossary/ontology should act as an arbiter. Answers should cite which glossary definition and which source were used, and the Reviewer AI should flag answers where the generated definition is not entailed by an approved or attributed definition.
- HypoTermQA-style tests are directly reusable as an acceptance test. Before go-live on a new domain, the team can probe the assistant with fabricated terms and check that it says "not in my sources" rather than defining them.
- Low model confidence correlates with adopting context (ClashEval). For truly novel terms the model has no prior, so it will follow whatever is retrieved. Source quality and curation therefore matter most exactly for the newest concepts.

### Gaps
- I found no study specifically measuring RAG accuracy on concepts coined after a model's cutoff in technical manuals (as opposed to news-style facts). Applicability to user manuals is inferred.
- I did not verify per-model differences in ClashEval (a secondary summary claims Claude Opus is more robust).

## 3. Existing ontologies and taxonomies for AI and quantum computing: stability and maintenance

### Takeaway
AI-domain ontologies exist but are young and thinly maintained. AIO is beta and LLM-assisted, with no tagged releases on GitHub. NIST taxonomies are the most actively versioned but cover narrow slices (adversarial ML, trustworthiness terms). Quantum-computing ontologies are research prototypes (PlanQK) or ISO vocabularies without a machine-readable ontology. They are useful as seed vocabularies and alignment targets, not as authoritative, stable backbones.

### Cited Findings
- [E] Artificial Intelligence Ontology (AIO), Joachimiak, Mungall et al. It was built with LLM assistance and maintained with the Ontology Development Kit (ODK), and published in *Applied Ontology* (Nov 2024). — [arXiv 2404.03044](https://arxiv.org/abs/2404.03044); [Crossref](https://api.crossref.org/works/10.1177%2F15705838241304103)
- [E] AIO's structure changed between preprint and journal. The arXiv abstract lists six top-level branches (Networks, Layers, Functions, LLMs, Preprocessing, Bias). The journal version lists eight (Bias, Layer, Machine Learning Task, Mathematical Function, Model, Network, Preprocessing, Training Strategy). This is evidence of early instability. — [arXiv](https://arxiv.org/abs/2404.03044); [eScholarship](https://escholarship.org/uc/item/9315g04c)
- [E] Maintenance status: BioPortal lists AIO as "Beta", with the last listed release 2024-11-11. The GitHub repo (294 commits) has no tagged releases ("latest version ... in aio.owl"), takes term requests through GitHub Issues, and does not document an obsoletion policy on the landing page. — [BioPortal](https://bioportal.bioontology.org/ontologies/AIO); [GitHub](https://github.com/berkeleybop/artificial-intelligence-ontology)
- [E] NIST AI 100-2 E2025 taxonomy has a glossary and index and is to be updated annually. Its dimensions are system type, lifecycle stage, attacker goals, capabilities and knowledge. — [NIST CSRC](https://csrc.nist.gov/pubs/ai/100/2/e2025/final); [OECD.AI entry](https://oecd.ai/en/dashboards/policy-initiatives/adversarial-machine-learning-a-taxonomy-and-terminology-of-attacks-and-mitigations-nist-ai-100-2e2025)
- [E] NIST AI 100-3 glossary is beta, with a final release promised "at a later date". I could not confirm whether the final version was released. — [NIST](https://www.nist.gov/publications/language-trustworthy-ai-depth-glossary-terms)
- [E] Quantum: the PlanQK ontology (Martyniuk et al., 2021) defines core concepts Publication, Algorithm and Implementation as OWL classes and properties for a quantum-computing knowledge platform. A later Semantic Web paper (SSW 2023) uses it as the schema of the PlanQK knowledge graph with semantic search. — [CEUR Vol-2836](https://ceur-ws.org/Vol-2836/qurator2021_paper_15.pdf); [IOS Press SSW230017](https://ebooks.iospress.nl/pdf/doi/10.3233/SSW230017)
- [E] Other quantum-related ontologies are adjacent rather than about QC engineering: a KEOD 2019 quantum-mechanics ontology method (toy example) and OntoCompChem for quantum chemistry calculations. — [SciTePress](https://www.scitepress.org/Papers/2019/83659/83659.pdf); [CORE](https://core.ac.uk/download/211243158.pdf)
- [E] ISO/IEC 4879:2024 is a terminology standard (text definitions), not an OWL ontology, and is itself under revision. — [ISO 80432](https://www.iso.org/standard/80432.html); [ITnation](https://itnation.lu/news/highlights-from-the-iec-iso-jtc-3-plenary-meeting-on-quantum-technology-standardization/)

### Inferences
- Treat external AI and quantum ontologies as import or alignment sources with pinned versions. Record the version IRI or date imported and expect upstream churn (AIO branch reorganization). Do not hard-depend on their IRIs for core concepts without a local mapping layer, e.g. local concept skos:exactMatch / skos:closeMatch to external IRIs.
- ISO and NIST vocabularies are best modeled as authoritative definition sources with status "standardized", attached to local concepts, rather than as the ontology itself.

### Gaps
- I did not verify whether MLSO (ML Schema / ML ontology) or other AI ontologies (e.g., ML-Schema W3C CG, DMOP) are still maintained in 2026.
- I did not verify the current maintenance status of the PlanQK ontology or a public OWL file and namespace.
- I found no machine-readable (OWL/SKOS) release of the NIST AI RMF taxonomy.

## 4. Ontology evolution, versioning and change management, and handling contested concepts

### Takeaway
There are mature, standard building blocks:
- OWL version IRIs plus priorVersion / backwardCompatibleWith / incompatibleWith.
- owl:deprecated.
- SKOS changeNote and historyNote, with creator and date.
- OBO Foundry obsoletion practice: never delete; mark obsolete, strip logical axioms, point to a replacement.
- PROV-style provenance.

What is missing is (a) a standard way to represent contested status and multiple competing definitions, and (b) a fully integrated automated evolution pipeline. Recent LLM-based work on ontology evolution is promising but early, and its authors themselves argue for hybrid workflows that combine automated extraction with human validation.

### Cited Findings
**Standards for versioning and deprecation**
- [E] OWL 2: an ontology MAY have an ontology IRI and a version IRI. owl:priorVersion, owl:backwardCompatibleWith and owl:incompatibleWith link to earlier versions. owl:deprecated "true" marks an IRI as deprecated. — [OWL 2 Structural Spec §3.1, §3.5, §5.5](https://www.w3.org/TR/owl2-syntax/)
- [E] SKOS Reference: at most one skos:prefLabel per language tag (S14). Multiple altLabels are allowed. Documentation properties (definition, scopeNote, changeNote, historyNote, editorialNote) are sub-properties of skos:note, with no cardinality limit, so multiple skos:definition values are formally allowed. — [SKOS Reference](https://www.w3.org/TR/skos-reference/)
- [E] SKOS Primer:
  - historyNote "describes significant changes to the meaning or the form of a concept" (example: "estab. 1975; heading was: Cruelty to children [1952-1975]").
  - changeNote "documents fine-grained changes ... for administration and maintenance".
  - Notes can be structured with rdf:value, dct:creator and dct:date.
  - The primer says provenance and ownership tracking is "outside the scope of SKOS" and suggests named graphs.
  — [SKOS Primer](https://www.w3.org/TR/skos-primer/)
- [E] W3C PROV-O provides Entity / Activity / Agent and relations such as prov:wasDerivedFrom, prov:wasRevisionOf and prov:wasAttributedTo. It is suitable for tracing which document or reviewer produced a definition or change. — [PROV-O](https://www.w3.org/TR/prov-o/)

**OBO Foundry practice**
- [E] Principle 19 (stability of term meaning): a term whose meaning changes should be obsoleted, not redefined in place. To obsolete a term:
  - mark it owl:deprecated / is_obsolete;
  - prefix the label with "obsolete ";
  - remove its logical axioms;
  - point to a replacement via "term replaced by" (IAO_0100001).
  — [OBO Principle 19](https://obofoundry.org/principles/fp-019-term-stability.html); [OBO Academy how-to](https://oboacademy.github.io/obook/howto/obsolete-term)
- [E] OBO Principle 13 recommends notifying users in advance of planned obsoletions. In 2024 the "obsolete" label prefix became mandatory, and revisions to Principle 19 dominated 2024–25 discussions. Obsoletion policy is still being refined even in the most mature community. — [Principle 13](https://obofoundry.org/principles/fp-013-notification.html); [Newsletter 6](https://obofoundry.org/newsletter/2024/10/14/6th-issue-newsletter.html); [Newsletter 7](https://obofoundry.org/newsletter/2025/01/23/7th-issue-newsletter.html)

**Surveys and recent work on ontology evolution**
- [E] Ontology-evolution surveys: Flouris et al. 2008 (classification of change); Zablith et al. 2013 (process-centric survey: change capture, representation, semantics, propagation, validation). Khattak et al. 2013 found that components exist but "a complete integrated system for automated ontology evolution is not available yet". — [Zablith, KER](https://www.cambridge.org/core/journals/knowledge-engineering-review/article/abs/ontology-evolution-a-processcentric-survey/CE4387A954917B7CA3282CE25FAC09FA); [Leipzig survey listing](https://pubs.dbs.uni-leipzig.de/se/node/985)
- [E/C] Evo-DKD (arXiv, July 2025): a dual-decoder LLM proposes candidate ontology edits together with natural-language justifications for autonomous ontology evolution. This is a research prototype. — [arXiv 2507.21438](https://arxiv.org/abs/2507.21438)
- [E/C] A 2025 CEUR workshop paper argues for "hybrid ontology evolution strategies that combine automated extraction with human validation" and notes that earlier work focused on concept-drift detection with manual conflict resolution. TRACE-OU-Bench (CEUR 2025–26) is a benchmark for snapshot-aware, continual, human-in-the-loop ontology evolution, and argues that schema change is harder than ordinary temporal drift. — [CEUR Vol-4020](https://ceur-ws.org/Vol-4020/Paper_ID_13.pdf); [CEUR Vol-4316](https://ceur-ws.org/Vol-4316/pd-short-8.pdf)

**Practice for contested, multi-definition terms**
- [E] NIST AI 100-3 is an existing model: multiple attributed definitions per term, with no single winner declared. — [NIST](https://www.nist.gov/publications/language-trustworthy-ai-depth-glossary-terms)
- [E] ISO 1087 entry model: preferred / admitted terms, plus deprecated forms marked. — [ISO 1087:2019 sample](https://cdn.standards.iteh.ai/samples/62330/aa6fcc8f52e34cf39acee86fa098fc22/ISO-1087-2019.pdf)

### Inferences (practical design guidance; these are recommendations, not tested results)

**Identity and change**
- Keep concept identity stable and versions explicit. Use opaque concept IRIs; labels and definitions change while the IRI does not. When meaning changes substantively (not just wording), follow OBO Principle 19:
  1. Mint a new concept.
  2. Mark the old one owl:deprecated with "term replaced by" / dct:isReplacedBy.
  3. Keep the old IRI resolvable, so older manuals and chats remain interpretable.
  4. Never hard-delete.
- Version the vocabulary as a whole with an owl:versionIRI per release, plus owl:priorVersion. Use backwardCompatibleWith / incompatibleWith as the semantic-versioning signal:
  - patch = wording or notes;
  - minor = additions or new deprecations;
  - major = removed axioms or re-parented concepts.
  This mapping is a design proposal; I found no standard that defines SemVer for vocabularies.

**Definitions and status**
- Model definitions as first-class reified objects, not single literals. Each concept gets 1..N Definition nodes with: text; source document (prov:wasDerivedFrom → manual/page/section); source type (standard / vendor manual / paper / internal); date; scope or context (e.g., "vendor X SDK v3"); and status. SKOS allows multiple skos:definition values but cannot attach metadata to a literal, so use a reified node, RDF-star or named graphs (SKOS Primer §5.3).
- Suggested status lattice:
  - concept level: candidate → proposed → accepted (or contested) → deprecated / superseded;
  - term level: preferred / admitted / deprecated, reusing the ISO 1087 vocabulary;
  - "hype" marking: a term-level flag ("marketing term; maps to concepts X, Y") rather than a concept.
- Allow a concept to be contested. Keep competing definitions side by side, with a reviewer note on what differs (e.g., autonomy level) rather than forcing a merge. The assistant should present "Source A defines X as…; Source B as…" when definitions disagree, mirroring NIST AI 100-3.

**Change logs and review**
- Use skos:changeNote with dct:creator and dct:date for every admin or Reviewer-AI edit, and skos:historyNote for meaning changes visible to end users. Export a PROV-O graph per release, so "why does the assistant now say this?" is answerable.
- Detection inputs for the Reviewer AI:
  - new documents introducing terms absent from the glossary (frequency and burst; citation-like signals per King et al.);
  - existing terms whose contexts in new documents diverge from the accepted definition (drift);
  - conflicts between a new source definition and the accepted one.
- All automated proposals go to the human admin, in line with the hybrid-evolution consensus and Khattak's finding that no integrated automated system exists.
- Pitfalls:
  - LLM-generated definitions for brand-new terms with no source: HypoTermQA shows these are readily fabricated, so require a source citation for any definition before "proposed".
  - Silently overwriting definitions, which breaks the reproducibility of past answers.
  - Importing unstable external ontologies by reference without pinning versions (AIO restructured within a year).
  - Treating standards as current: they lag years.
  - Over-trusting a single new document (ClashEval).

### Gaps
- I found no W3C or ISO standard property for "contested" or "proposed" concept status. Status values would be local, though annotation vocabularies such as the OBO "has curation status" / IAO metadata exist (not verified here).
- I found no empirical evaluation of LLM-assisted ontology evolution in production (Evo-DKD and TRACE-OU-Bench are research or benchmark stage).
- I did not verify SKOS-XL, ISO 25964, DCAT/PAV or VoID versioning guidance, or semantic-versioning practice for vocabularies (e.g., schema.org, FIBO release process). These would strengthen the versioning recommendations.
- I did not fetch the end of the SKOS Reference (truncated) to confirm there is no deprecation guidance there; the Primer contains none.
