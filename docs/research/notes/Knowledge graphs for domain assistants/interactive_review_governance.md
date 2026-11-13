# Interactive Human-in-the-Loop Review and Governance of an Extracted Domain Model (the "Reviewer AI assistant")

Scope: is it feasible for an LLM assistant to drive the review of extracted terms, concepts, relations, abstractions and quality issues, with a domain admin approving or correcting? This covers evidence, products, prioritization, visualization, governance and agent design. Current as of Nov 2026. "Evidence" means peer-reviewed or preprint studies with measurements. "Vendor claim" means product docs or marketing.

## 1. Research on LLM-assisted ontology engineering with humans in the loop: what worked, what failed, measured gains

### Takeaway
The research consistently supports **LLM-proposes, human-disposes** hybrids, but the evidence base is thin: small user studies (N ≈ 3–24), mostly academic ontologies, and almost no time-to-completion data. Three findings carry over directly to a reviewer assistant:
- LLM suggestions raise human accuracy when they are correct.
- They pull accuracy down when they are wrong, which is automation bias.
- LLM-generated models are typically incomplete yet carry superfluous elements, so human refinement remains essential.

### Cited Findings
- **OntoChat** (King's College London et al.) is a conversational LLM tool for ontology requirements engineering. It covers user story creation, competency question (CQ) extraction, CQ filtering/analysis and ontology testing support. It was first evaluated by replicating the Music Meta Ontology engineering. — [arXiv 2403.05921](https://arxiv.org/abs/2403.05921v1)
- OntoChat's early evaluation found that **users struggle to write effective prompts**. Follow-up work added "participatory prompting" with pre-defined prompt templates for personas, goals, scenarios, sample data and data resources. The later version reports a formative study (N=10) plus a user evaluation with knowledge engineers (N=24), and claims to be the first validated prompt-guidance framework for LLM ontology requirements. — [arXiv 2408.15256v3](https://arxiv.org/html/2408.15256v3)
  - Design implication: the assistant should drive the conversation and offer structured choices rather than expect the admin to prompt well. This is an inference from the finding.
- **Ontogenia** (Lippolis, Ceriani, Zuppiroli, Nuzzolese; ESWC 2024 satellite) applies metacognitive prompting plus eXtreme Design / ontology design patterns to ontology generation from CQs. — [ESWC 2024 paper](https://2024.eswc-conferences.org/wp-content/uploads/2024/04/ESWC_2024_paper_311.pdf)
- **"Ontology Generation using LLMs"** (arXiv 2503.05388, Mar 2025) used 10 ontologies, 100 CQs and 29 user stories:
  - Memoryless CQbyCQ modelled 91% of CQs correctly (94% ignoring minor issues). Ontogenia reached 84% (89%).
  - o1-preview + Ontogenia "produces ontologies of sufficient quality to meet the requirements of ontology engineers, significantly outperforming novice ontology engineers."
  - Generated ontologies showed a **significant presence of superfluous elements**.
  - No independent replication found.
  - [arXiv 2503.05388](https://arxiv.org/abs/2503.05388v1)
- **OE-Assist** (Lippolis, Saeedizade, Keskisärkkä, Gangemi, Blomqvist, Nuzzolese; arXiv 2507.14552, Jul 2025) is an LLM assistant for CQ verification inside Protégé, built on a dataset of 1,393 CQs. Automated verification with o1-preview / o3-mini performed at a level similar to the average user. — [arXiv 2507.14552](https://arxiv.org/abs/2507.14552v1)
- OE-Assist user study (19 knowledge engineers from 8 institutions; 20 CQ verification tasks, 10 with and 10 without LLM suggestions):
  - LLM help **improved accuracy, especially when suggestions were correct**, and markedly lowered perceived difficulty.
  - **Human performance dropped when the LLM gave incorrect guidance.**
  - Overall performance "did not change significantly" in the semi-automatic setup, and "LLMs still need a human-in-the-loop."
  - No timing data was found.
  - [arXiv 2507.14552 PDF](https://arxiv.org/pdf/2507.14552v1); [Lippolis talk slides, Dec 2025](https://geist.re/_media/aira:slides-anna-sofia-lippolis-2025-12-11.pdf). The slide content came via search snippet; the PDF text was not extractable.
- **IDEA2** (Watkiss-Leek & Jacoby, arXiv 2604.01344, Apr 2026) is an expert-in-the-loop CQ workflow:
  - Workflow: LLM extraction (Gemini 2.5 Pro), then a shared dashboard (Notion) where experts accept/reject, tag, prioritise and comment, then LLM reformulation of rejected items with the full history and anonymised comments injected. Stopping criteria are convergence, an iteration cap or a quota. Per-item provenance (lineage, generation params, review logs) is exported as JSON-LD.
  - AnIML case (4 experts, 103 CQs, 3 iterations): final acceptance 92.7%, about 0.85 min per CQ.
  - Cultural-heritage case (3 experts, 23 previously rejected CQs): final acceptance 73.3%, about 2.97 min per CQ, and 6 of 7 reformulated CQs accepted.
  - Raw agreement was about 90%. Krippendorff's α was 0.177 for AnIML (a prevalence effect; Gwet's AC1 = 0.884) and 0.843 for cultural heritage.
  - Lessons:
    - **Free-text expert comments drive good reformulation; generic "improve this" requests do not.**
    - Vague feedback hurts.
    - Majority voting hides real ambiguity.
    - **Annotator fatigue is expected at 100+ items.**
    - The text and table timing figures are inconsistent.
  - [arXiv 2604.01344](https://arxiv.org/html/2604.01344v1)
- **Parkinson's ontology study** (arXiv 2512.14288, Dec 2025): LLM-only outputs "were not comprehensive and required substantial human refinement". The hybrid X-HCOME method significantly improved comprehensiveness. — [arXiv 2512.14288](https://arxiv.org/abs/2512.14288v1)
- **García-Fernández et al.** (ESWC 2025 Text2KG workshop) used Design Science Research to build a human-LLM collaboration workflow for ontology *extension*. Its evaluation of LLM performance per extension task is qualitative. — [CEUR Vol-4020](https://ceur-ws.org/Vol-4020/Paper_ID_8.pdf)
- **Agentic ontology induction/enrichment with humans in the validation loop.** — [CEUR Vol-4233 Text2KG](https://ceur-ws.org/Vol-4233/Text2KG_Paper_ID_13.pdf)
- **Role-playing multi-agent ontology engineering** (Soularidis et al., Knowledge Engineering Review 2025): LLM agents simulate OE roles, and human experts judge acceptability of the results. — [Cambridge KER](https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/C4DFC9BD18020226B4CC763BE7056659/S026988892510009Xa.pdf/automating-agentic-collaborative-ontology-engineering-with-role-playing-simulation-of-llm-powered-agents-and-rag-technology.pdf)
- **Evo-DKD** (arXiv 2507.21438) pursues fully autonomous ontology evolution and contrasts itself with OntoGenix-style post-generation human review. It represents the opposite design pole. — [arXiv 2507.21438](https://arxiv.org/html/2507.21438v1)
- **Biomedical review** (MDPI Bioengineering, Nov 2025): scaling human-in-the-loop validation remains a key hurdle for LLM-assisted ontology creation and curation. — [MDPI](https://www.mdpi.com/2306-5354/12/11/1260)
- **Knowledge elicitation study:** LLM-led interviews worked as stand-ins for experts, but humans were still preferred for ontology generation. This Semantic Web Journal submission was **rejected**, with reviewers citing experimental design concerns, so treat it as weak evidence. — [SWJ](https://semantic-web-journal.net/content/investigating-knowledge-elicitation-automation-large-language-models)
- **"From human experts to machines"** (arXiv 2403.08345) recommends human-in-the-loop evaluation of LLM-generated ontologies/KGs. — [arXiv 2403.08345](https://arxiv.org/pdf/2403.08345)

### Inferences
- **Feasibility.** Each component exists in research prototypes: LLM extraction, CQ-based checking, item-level accept/reject with comments, and LLM reformulation from feedback. IDEA2 is the closest published analogue to the proposed Reviewer assistant (a queue, votes and comments, LLM revision, provenance), but it covers CQs, not full domain models.
- **CQs as the validation backbone.** Competency questions (NeOn / eXtreme Design tradition) are a well-supported way to define "complete enough". The assistant could derive CQs from the domain's user manuals and test the model against them, turning completeness from subjective judgment into checkable tests.
- **Expected gains.** Gains come mostly from accuracy uplift and lower perceived effort when suggestions are good. Speedup claims are largely unmeasured. Budget design must account for the accuracy *drop* on wrong suggestions.
- **Compactness checks.** "Superfluous elements" in LLM output argue that compactness/redundancy checks should be a first-class part of the review.

### Gaps
- No controlled study measured end-to-end time or quality gains for LLM-*driven* (proactive) review of a whole business domain model. Studies cover CQs, ontology generation or verification subtasks.
- Full OntoChat N=24 results were not retrieved.
- OE-Assist effect sizes were not available.
- There is little evidence on enterprise or business glossaries, as opposed to academic or biomedical ontologies.

## 2. Existing tools/products for collaborative ontology/taxonomy/glossary governance, and their AI-assisted review features (as of 2026)

### Takeaway
By 2026 every major vendor ships some "AI suggests, steward accepts" feature, usually per-item accept/edit/discard plus bulk actions and an activity log. None documents a *proactive, conversational, multi-session review driver* across a whole domain model with quality-issue detection and diagrams. That combination appears to be white space. All product statements below are vendor claims, not independent evaluations.

### Cited Findings
- **Graphwise PoolParty 10.1** (Jan 2026), Taxonomy Builder: LLM-powered hierarchical generation "keeping humans in the loop" with integrated review workflows. All generated concepts, alternative labels and definitions are presented as suggestions to accept, edit or deselect before commit. — [Graphwise docs 10.1](https://help.graphwise.ai/en/graphwise-documentation/poolparty-10-1---ai-powered-taxonomy-creation.html); [Graphwise blog](https://graphwise.ai/blog/poolparty-10-1-ai-assisted-taxonomy-building-for-the-graphwise-era/); [Taxonomy Builder help](https://help.graphwise.ai/en/graph-modeling/thesaurus/taxonomy-builder.html)
- PoolParty's earlier **Taxonomy Advisor** (2024) suggests narrower concepts, alt labels and definitions via tick-box selection. It became "Extend Your Taxonomy" in 10.2. PoolParty also has "proposed concepts" that need approval before use, and a separate Thesaurus Management approval mechanism for multi-user changes. — [Taxonomy Advisor](https://help.poolparty.biz/en/user-guide-for-knowledge-engineers/advanced-features/taxonomy-advisor.html); [Graphwise glossary](https://help.graphwise.ai/en/glossary.html)
- **TopQuadrant TopBraid EDG 8.5** "Copilot for Linking" includes:
  - a **"Problems & Suggestions" panel** surfacing missing, conflicting or suggested links, with term previews and an "apply all" action (backed by a vector DB, optionally Weaviate);
  - draft definition generation;
  - Copilot Classification;
  - LLM entity/class/relationship extraction to populate taxonomies and ontologies.

  This is the closest vendor analogue to "proposed quality issues". — [TopBraid EDG 8.5](https://www.topquadrant.com/?p=21009); [TopQuadrant LLM blog](https://topquadrant.com/blog/how-topquadrant-is-embracing-large-language-models-llms). No documentation was found on how EDG suggestions are audited.
- **Collibra**: AI suggestions are marked with an AI icon and a "Ready for review" tag. Stewards can bulk-discard unapproved suggestions. The AI writing assistant follows "steward reviews, refines and accepts". The semantic-layer AI is in preview. — [Collibra Business Glossary 2026.08](https://productresources.collibra.com/docs/collibra/2026.08/Content/BusinessGlossary/to_business-glossary.htm); [Collibra semantic layer preview](https://productresources.collibra.com/docs/collibra/sigma/private-preview/Content/Catalog/GuidedStewardship/SemanticLayer/ta_semantic-layer.htm); [Collibra blog](https://www.collibra.com/blog/governance-by-design-automatically-enforce-standards-with-the-ai-powered-writing-assistant-smart)
- **Atlan**: Atlan AI drafts term descriptions, which the user edits and accepts or discards. The activity log records AI-suggested documentation. — [Atlan demo](https://atlan.com/demos/use-atlan-ai-document-terms.md)
- **Microsoft Purview Unified Catalog**: AI generates suggested glossary terms for a governance domain from the domain's name and description plus general knowledge. Users must check accuracy, relevance and format and pick which terms to add. The feature was labelled preview in the docs found. — [Purview Responsible AI FAQ](https://learn.microsoft.com/en-us/purview/unified-catalog-responsible-ai-faq)
- **DataHub**: AI Glossary Term Suggestion (closed beta) suggests terms for tables and columns. **OvalEdge**: accept/reject AI term recommendations. — [DataHub](https://datahubproject.io/docs/automations/ai-term-suggestion); [OvalEdge release notes](https://docs.ovaledge.com/minor-release/release7.2/release-notes/governance-catalog)
- **Stardog Voicebox for Designer**: an agent helps create an ontology, map sources and check the KG. Docs list human-in-the-loop review of mappings, conflict resolution and provenance validation, and the user reviews the suggested ontology and mappings before publishing. Generated classes and properties must carry labels, descriptions and usage examples. The docs warn the external LLM agent "may contain hallucinations". — [Stardog docs](https://docs.stardog.com/voicebox/guided-ontology-creation-and-mapping/); [Stardog blog](https://www.stardog.com/blog/stardog-voicebox-makes-building-data-models-dead-simple/)
- **WebProtégé** (open source):
  - entity-attached threaded discussions with Markdown, entity links and @mentions;
  - threads usable as issues (open/close);
  - all changes grouped into revisions with author, timestamp and description, which can be reverted and downloaded;
  - watches and email notifications;
  - per-project permissions.

  It has no native AI review found. — [WebProtégé paper arXiv 1902.08251](https://arxiv.org/pdf/1902.08251.pdf); [PMC article](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176057)
- **ODK-AI** (Monarch/BBOP ecosystem): a Docker container running Claude Code on Ontology Development Kit projects, with ROBOT preinstalled and GitHub CLI for issues and PRs. The agent proposes changes as PRs and human reviewers approve before merge. It is early development, tested mainly on `.obo` sources, and reports no evaluation. — [ODK-AI](http://ai4curation.io/odk-ai)

### Inferences
- The industry-standard interaction primitive is **per-item suggestion → accept / edit / reject, plus bulk accept/discard, plus an activity log tagging AI origin**. The Reviewer assistant should match this as a baseline.
- Differentiation can come from:
  - proactive orchestration (deciding what to review next);
  - cross-item quality issues (contradictions, drift, gaps) rather than per-asset descriptions;
  - abstraction proposals;
  - evidence-grounded explanations.
- An exporter to SKOS/OWL, or to Collibra/Purview/PoolParty, would let approved decisions flow into whatever catalog the customer already runs.

### Gaps
- No vendor publishes accuracy or acceptance-rate metrics for its AI suggestions.
- Neo4j (Bloom, LLM Graph Builder) schema-review features were not verified in this pass.
- Alation features were not verified.
- GA versus preview status for Purview and Collibra features needs checking against the latest docs.

## 3. Active learning / prioritization: what the human should review first; fatigue; batching

### Takeaway
KG-quality literature supports **budgeted review**:
- score or stratify candidate facts;
- send the most uncertain, informative or error-likely items to humans;
- group items by shared source text to cut cost;
- propagate labels via thresholds.

Human-factors evidence warns that review design itself changes reviewer behaviour, and fatigue is real past roughly 100 items.

### Cited Findings
- **ACTC** (Sedova & Roth) selects a small set of triples for manual annotation (random or active), auto-labels more from the unlabeled pool, and estimates **per-relation confidence thresholds**. Few human labels calibrate acceptance for many. — [arXiv 2305.06395](https://arxiv.org/pdf/2305.06395v3.pdf)
- **KAEL** (Dong et al., WSDM 2023) ensembles multiple KG error detectors and actively queries experts on suspicious triples. The annotation budget is far smaller than the number of potentially false triples. — [WSDM 2023 PDF](https://www4.comp.polyu.edu.hk/~xiaohuang/docs/2023WSDM_Junnan.pdf)
- **ALADDIN** (Irrera, Marchesin et al., CIKM 2025) shows entity cards with top-ranked facts and recommends likely defects under a budget, collecting feedback where validation matters most. — [CIKM 2025 PDF](https://www.dei.unipd.it/~marches1/papers/ims_etal-cikm-2025.pdf)
- **Cost-aware accuracy estimation** (Qi & Zheng): annotating triples or mentions **from the same source text in succession reduces overall cost**, so the selection order is optimized. — [PKU PDF](https://www.wict.pku.edu.cn/docs/20221201164039326398.pdf)
- **LLM-assisted KG auditing** (Marchesin et al., PVLDB vol. 19) uses LLM-generated signals to stratify the KG and reserves human annotation for ground truth. It reports large cost reductions (the snippet mentions annotating only about 0.25% of facts; exact figures were truncated in the source snippet). — [PVLDB p2005](https://www.vldb.org/pvldb/vol19/p2005-marchesin.pdf)
- **IDEA2** let experts tag and prioritise items and flagged **annotator fatigue risk for 100+ items**. — [arXiv 2604.01344](https://arxiv.org/html/2604.01344v1)
- **"Bias in the Loop"** (arXiv 2509.08514; N=2,784, preregistered 2³ factorial Wizard-of-Oz on Prolific):
  - **Requiring reviewers to correct flagged AI errors reduced engagement and increased acceptance of incorrect suggestions.**
  - Financial incentives had no consistent effect.
  - Attitude toward AI was the strongest predictor of performance, and skeptics caught more errors.
  - Automation bias grows when the system's strengths are shown before its weaknesses.
  - [arXiv 2509.08514](https://arxiv.org/html/2509.08514v1)
- PoolParty and Collibra both provide **bulk accept/discard**. TopBraid EDG offers "apply all" in Problems & Suggestions. — [Collibra](https://productresources.collibra.com/docs/collibra/2026.08/Content/BusinessGlossary/to_business-glossary.htm); [TopBraid EDG 8.5](https://www.topquadrant.com/?p=21009)

### Inferences
- **A priority score** could combine:
  - **impact**: node centrality or degree, number of dependent relations, frequency in source docs, use in CQs or user-manual tasks;
  - **uncertainty**: extractor/LLM confidence, disagreement between multiple extraction runs or models, conflicting evidence;
  - **error likelihood**: outputs of rule-based checks such as SHACL violations, label duplicates or cycles.

  Review high-impact × high-uncertainty items first. Auto-accept low-impact, high-confidence items only after calibrating thresholds per relation type on a human-labelled sample (ACTC-style), and spot-check them.
- **Batch by topic or source document**, for example "all terms from the Billing chapter" or one taxonomy subtree per session. Shared context reduces cost (Qi & Zheng) and suits batch-approve with exceptions.
- **Session sizing:** keep sessions well under roughly 100 decisions and resumable. Interleave "easy confirm" items with hard ones. Show the admin a progress and coverage meter.
- **Seed known-error items:** insert occasional known-incorrect "honeypot" proposals to measure reviewer vigilance. This is a design idea; no direct evidence was found for it in ontology review.

### Gaps
- No study was found on prioritizing *ontology-level* proposals (abstractions, taxonomy restructurings) as opposed to individual triples.
- No published optimal batch size for glossary or ontology review.

## 4. Visualization: effective diagrams for non-experts and scaling issues

### Takeaway
For non-experts, **indented trees are more familiar and organized**, while node-link graphs feel more intuitive for multiple inheritance. VOWL was designed for casual users but rests on small studies. Whole-graph views become unreadable "hairballs" at scale, so review UIs should show small, task-scoped views (subtree, ego-graph, diff) generated on demand.

### Cited Findings
- **Fu, Noy & Storey (ISWC 2013)**, controlled study:
  - the **indented tree** was more organized and familiar to novices;
  - the **graph** visualization was more controllable and intuitive without visual redundancy, *particularly for ontologies with multiple inheritance*;
  - the tasks were class-mapping tasks.
  - [Springer ISWC 2013](https://link.springer.com/content/pdf/10.1007/978-3-642-41335-3_8.pdf)
- **VOWL** (Lohmann et al., Semantic Web Journal) is a visual notation for OWL meant to be understandable by "casual ontology users with only little training". It was evaluated in three user studies. An early ProtégéVOWL study (6 non-expert participants, compared with SOVA) found it comparatively intuitive. The sample was very small. — [VOWL SWJ](https://journals.sagepub.com/doi/full/10.3233/SW-150200); [Springer EKAW](https://link.springer.com/chapter/10.1007/978-3-319-11955-7_55)
- **Multi-view tools** combine radial, indented-tree and graph views, but no scalability usability results were found. — [VOWL SWJ](https://journals.sagepub.com/doi/full/10.3233/SW-150200)
- **ALADDIN** presents entity cards with top-ranked facts as the unit of review rather than a full graph. — [CIKM 2025](https://www.dei.unipd.it/~marches1/papers/ims_etal-cikm-2025.pdf)

### Inferences
- Use **context-specific views**:
  - taxonomy → collapsible indented tree with proposed changes highlighted (add/move/merge in a diff colour scheme);
  - ontology concept → ego-graph of depth 1–2 around the concept under review;
  - contradiction or drift issue → a minimal subgraph showing just the conflicting statements plus their source snippets;
  - abstraction proposal → before/after side-by-side tree.
- **Mermaid or Graphviz** are good for LLM-generated small diagrams in chat, since text-to-diagram works reliably for small graphs. **Cytoscape.js** (or similar) suits interactive exploration. Cap rendered nodes at about 30–50 per view.
- **Stay simple for business admins:** prefer plain-language node-link diagrams with labelled edges over full OWL notation like VOWL, unless users are ontologists.

### Gaps
- No found study evaluates LLM-generated (Mermaid/Graphviz) diagrams for ontology review comprehension.
- No quantitative node-count limits for comprehension were found in this pass.
- Recent (2023–2026) KG visualization usability studies were not retrieved.

## 5. Governance: versioning, provenance, approval workflows, audit trails, roles, and feedback loops

### Takeaway
Mature patterns exist:
- **Git + PR + CI quality checks + semantic-versioned releases** (ODK/ROBOT);
- **revision history with author, timestamp and message plus entity-attached discussion threads** (WebProtégé);
- **AI-origin flags and activity logs** (Collibra, Atlan).

Per-decision provenance as structured data (IDEA2 JSON-LD) enables feeding approvals back into extraction.

### Cited Findings
- **ODK editors' workflow:**
  - feature branch → PR → CI runs automatically (green/red);
  - reviewers comment on the PR;
  - two reviews are ideal but hard in practice;
  - recommends **branch protection requiring review before merge**.
  - [ODK EditorsWorkflow (OBO COB)](https://obofoundry.org/COB/odk-workflows/EditorsWorkflow/)
- **ODK release pipeline:** assigns version IRIs, produces several serialisations and enforces semantic versioning. An ontology-diff GitHub action produces diffs on PRs. ROBOT runs reasoning and QC. — [ODK paper, PMC9547537](https://pmc.ncbi.nlm.nih.gov/articles/PMC9547537); [ODK releases](https://www.github.com/INCATools/ontology-development-kit/releases)
- **ODK-AI** puts an AI agent (Claude Code) into this flow as a PR author, with human reviewers approving before merge. — [ODK-AI](http://ai4curation.io/odk-ai)
- **WebProtégé:** revisions record author, timestamp and description, and can be reverted and downloaded. Comment threads act as issues. Collaborative Protégé logged all user actions as structured entries. — [arXiv 1902.08251](https://arxiv.org/pdf/1902.08251.pdf); [PMC4176057](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176057)
- **IDEA2** tracks each item's lineage, generation parameters and review logs, exportable as JSON-LD. It feeds anonymised expert comments back to the LLM for reformulation. — [arXiv 2604.01344](https://arxiv.org/html/2604.01344v1)
- **Vendor patterns:**
  - Collibra marks AI suggestions with an icon and "Ready for review";
  - Atlan's activity log records AI-suggested docs;
  - PoolParty requires "proposed concepts" to be approved and supports multi-user approval;
  - Stardog lists provenance validation.
  - [Collibra](https://productresources.collibra.com/docs/collibra/2026.08/Content/BusinessGlossary/to_business-glossary.htm); [Atlan](https://atlan.com/demos/use-atlan-ai-document-terms.md); [Graphwise glossary](https://help.graphwise.ai/en/glossary.html); [Stardog](https://docs.stardog.com/voicebox/guided-ontology-creation-and-mapping/)

### Inferences
- **Data model:** each proposal is a first-class object with:
  - id, type (term / relation / abstraction / issue), payload (proposed triples or patch);
  - evidence (source doc spans), generator (model, prompt version, run id), confidence, status (proposed → in-review → accepted / edited / rejected / deferred);
  - reviewer, timestamp, rationale.

  PROV-O can represent it. Approved state goes into a versioned store (Git-backed Turtle/SKOS, or a named-graph per release) with diffs and semantic version tags.
- **Roles:**
  - extractor agent (proposes);
  - Reviewer assistant (orchestrates and explains, cannot commit);
  - domain admin / steward (approves);
  - optional second approver for high-impact changes such as top-level taxonomy restructuring or deletions;
  - auditor (read-only history).
- **Feedback loop:**
  - rejected or edited proposals with rationales become few-shot examples or negative constraints for the next extraction run;
  - accepted decisions become regression tests (SHACL shapes, CQ SPARQL tests) so later extraction cannot silently reintroduce rejected items;
  - per-relation acceptance rates recalibrate auto-accept thresholds (ACTC-style).

### Gaps
- No published measurement was found of extraction-quality improvement from feeding back human review decisions in ontology settings (IDEA2's reformulation is the nearest).
- Not verified: which vendors expose AI-suggestion provenance via API.

## 6. Agentic workflow design: driving multi-session review, explaining proposals, pitfalls

### Takeaway
A stateful agent driving a review queue is feasible with current LLMs and matches IDEA2, ODK-AI and vendor accept/reject patterns. The main risks are human-factors risks rather than technical ones:
- **Automation bias:** wrong suggestions lower human accuracy.
- **Sycophancy:** the LLM caves to or flatters the admin.
- **Hallucinated proposals or evidence.**

Mitigations: evidence-grounded proposals, cognitive-forcing interactions for high-stakes items, and separating the proposing agent from deterministic validators.

### Cited Findings
- **Automation bias in ontology tasks:** OE-Assist users' performance dropped when the LLM's guidance was incorrect. — [arXiv 2507.14552](https://arxiv.org/pdf/2507.14552v1)
- **Review design and order effects:** requiring corrections of flagged AI errors increased acceptance of wrong suggestions. Showing system strengths before weaknesses increases automation bias. — [arXiv 2509.08514](https://arxiv.org/html/2509.08514v1)
- **Cognitive forcing functions** (Buçinca, Malaya & Gajos, CSCW 2021; N=199): checklists, time-outs and "decide first, then see the AI" designs reduced overreliance compared with simple explainable-AI designs, but did not eliminate it. Participants rated the most effective designs least favourably, and benefits were larger for high Need-for-Cognition users. — [Harvard page](https://www.eecs.harvard.edu/~kgajos/papers/2021/bucinca2021trust.shtml); [arXiv 2102.09692](https://arxiv.org/abs/2102.09692v1)
- **Sycophancy** (Sharma et al., ICLR 2024): five assistants consistently showed sycophancy. Humans and preference models sometimes prefer convincingly-written sycophantic answers over correct ones, and sycophancy is a general behaviour of RLHF-trained assistants. — [arXiv 2310.13548](https://arxiv.org/abs/2310.13548)
- **Hallucination:** Stardog explicitly labels its external LLM agent output as possibly containing hallucinations. — [Stardog docs](https://docs.stardog.com/voicebox/guided-ontology-creation-and-mapping/)
- **LLM over-generation:** LLM-generated ontologies contain significant superfluous elements. — [arXiv 2503.05388](https://arxiv.org/abs/2503.05388v1)
- **IDEA2 loop:** a stopping-criteria-driven loop (convergence threshold, iteration cap, resource quota) with history-aware reformulation. Vague feedback degraded results. — [arXiv 2604.01344](https://arxiv.org/html/2604.01344v1)
- **OntoChat:** users struggle to prompt, and templates or guided steps help. — [arXiv 2408.15256v3](https://arxiv.org/html/2408.15256v3)

### Inferences (design guidance)
- **State machine per session:**
  1. Load the review backlog and model version.
  2. Show a summary dashboard: counts by type and severity, coverage of CQs.
  3. Agree the session goal, for example "Billing subtree + top 10 contradictions".
  4. Loop over prioritized items: present the proposal, its evidence and a diagram; the admin decides (accept / edit / reject / defer / ask); the agent records it, re-runs dependent checks and updates the queue.
  5. Session summary and changelog.
  6. Persist state for resume.

  Keep the queue and state in a database, not in the LLM context.
- **Explain with evidence:** every proposal cites verbatim source spans (doc, page, section) and states which rule or check produced it. Spans are verified by string match, so the agent is never trusted to quote. A proposal without verifiable evidence is labelled "inferred" and routed to stricter review.
- **Deterministic validators first:** run SHACL/OWL reasoning (consistency, cycles, disjointness), label-duplicate or near-synonym detection (embeddings), orphan or isolated nodes, and CQ-coverage tests. The LLM explains and proposes fixes; detection is grounded in tools. This reduces hallucinated "issues".
- **Anti-automation-bias tactics:**
  - for high-impact items, ask the admin to predict or decide before revealing the AI's recommendation (cognitive forcing);
  - show calibrated confidence and the strongest counter-evidence;
  - present alternatives, not one answer;
  - do not lead with a streak of easy wins (order effect);
  - track per-reviewer acceptance rate, and flag rubber-stamping, for example more than 95% accept with fast dwell times.
- **Anti-sycophancy:**
  - when the admin rejects or edits, the agent should check the edit against evidence and constraints and push back respectfully if it creates inconsistency, rather than agreeing;
  - use a separate critic/validator pass (a different prompt or model) that cannot see the admin's sentiment.
- **Proactivity with control:** the agent proposes the next step but lets the admin redirect ("skip to contradictions", "show me the whole Order taxonomy"). It asks structured questions with options rather than open prompts, per the OntoChat finding.
- **Compactness and abstraction proposals:** treat merges, generalizations and deletions as higher-risk. Show impact (affected terms, relations, CQs) and require explicit confirmation, possibly a second approver.
- **Pitfalls to expect:**
  - reviewer fatigue past roughly 100 items;
  - majority-vote hiding ambiguity in multi-reviewer setups;
  - vague rejection rationales giving poor feedback (so require a reason code plus optional text);
  - LLM context loss across sessions (mitigated by externalized state);
  - drift between the extracted model and the evolving source docs (mitigated by re-extraction diffs routed back into the queue).

### Gaps
- No published study was found of an LLM agent *proactively driving* multi-session ontology or glossary review with measured outcomes. The Reviewer assistant concept is novel in combination, though each element has precedent.
- No ontology-specific evidence quantifies sycophancy (the LLM accepting wrong admin corrections).
- No found evidence on the effectiveness of honeypot or vigilance checks in ontology curation.
