# Aligning multi-team platform documentation: governance, freshness, terminology and AI feedback loops

Scope: how many platform teams in a large enterprise can turn overlapping, stale, contradictory docs into a coherent end-to-end experience for product teams, keep it fresh, govern shared terminology, and use an AI assistant plus KG/glossary to cut down on personal consultation sessions. Researched as of 2026-11-13. Evidence labels used below: **[Research]** = peer-reviewed or arXiv study; **[Survey]** = large practitioner survey (DORA, Stack Overflow); **[Self-reported]** = an organisation describing its own internal results; **[Vendor]** = vendor marketing or docs; **[Practitioner]** = blog or forum anecdote.

## 1. Docs-as-code and docs governance at scale (Diátaxis, TechDocs, ownership, freshness, linting, terminology)

### Takeaway
The proven setup is docs-as-code: Markdown in the owning repo, rendered centrally in a portal (Backstage TechDocs), reviewed in PRs, owned via CODEOWNERS, and linted in CI with a controlled vocabulary (Vale accept/reject lists generated from the glossary). Diátaxis then gives every team the same content-type structure. The strongest outcome evidence for documentation quality is DORA's survey correlations. Most tool and process claims are self-reported or vendor claims.

### Cited Findings
- **[Survey] DORA:** high-quality documentation amplifies the effect of technical capabilities on organisational performance. In the 2023 report, trunk-based development was estimated to have 12.8x more impact with high-quality docs than with low-quality docs — [DORA 2023 report](https://dora.dev/research/2023/dora-report/2023-dora-accelerate-state-of-devops-report.pdf); [DORA capability: documentation quality](https://dora.dev/capabilities/documentation-quality/)
- **[Survey] DORA 2022:** the documentation interaction effect applied to every technical capability studied. Example: version control lifted organisational performance by 27% with below-average docs and by 278% with above-average docs — [Google Cloud blog, 2022 DORA deep dive on documentation](https://cloud.google.com/blog/products/devops-sre/deep-dive-into-2022-state-of-devops-report-on-documentation/)
- **[Survey] DORA (via DORA researcher Michelle Irvine):** teams with high-quality documentation report 25% higher team performance — [DORA capability page](https://dora.dev/capabilities/documentation-quality/)
- **[Survey] DORA measures documentation quality as:** usefulness, accuracy/completeness, and findability/clarity. Per a secondary summary, about 25% of 2021 respondents reported high-quality docs — [Waydev summary](https://waydev.co/state-of-devops-report-2023) (secondary; verify against the DORA PDF)
- **[Survey] Caveat:** a newsletter reading of DORA 2023 says documentation showed no effect on the core software delivery metrics that year, and was linked to more burnout for respondents who identified as underrepresented (possibly because they do a disproportionate share of doc work) — [DX newsletter on 2023 DORA](https://newsletter.getdx.com/p/2023-dora-report); [RDEL #18](https://rdel.substack.com/p/rdel-18-can-better-documentation). Relevant to incentives: doc work needs explicit recognition.
- **[Research] What goes wrong with documentation:**
  - Aghajani et al. (ICSE 2019) analysed 878 artifacts (emails, forum posts, issues, PRs) and built a taxonomy of 162 documentation issue types in four groups: information content, presentation, process, and tool support — [ICSE 2019 paper](https://2019.icse-conferences.org/details/icse-2019-Technical-Papers/49/Software-Documentation-Issues-Unveiled); [PDF](https://emadpres.github.io/pdfs/icse2019.pdf)
  - The ICSE 2020 follow-up surveyed 146 practitioners on which issues matter and which fixes they apply — [ICSE 2020 Practitioners' Perspective](https://2020.icse-conferences.org/details/icse-2020-papers/28/Software-Documentation-The-Practitioners-Perspective); [PDF](https://www.inf.usi.ch/faculty/lanza/PUBS/P/Agha2020a.pdf)
- **Diátaxis:** splits documentation into four types (tutorials, how-to guides, reference, explanation) by user need — [diataxis.fr](https://diataxis.fr/)
  - **[Self-reported] Canonical** adopted Diátaxis company-wide from 2021 as a long-term documentation transformation. The MAAS team used the four buckets to reduce context switching for readers — [Canonical: Diátaxis, a new foundation](https://canonical.com/blog/diataxis-a-new-foundation-for-canonical-documentation); [Canonical documentation practice](https://canonical.com/documentation); [Moving toward Diátaxis](https://canonical.com/blog/moving-toward-diataxis?format=md)
  - **Cloudflare** used Diátaxis as the "north star" for the information architecture of its developer-docs redesign, per the Diátaxis site — [diataxis.fr](https://diataxis.fr/)
  - No quantitative before/after outcome data was found for any Diátaxis adoption.
- **[Self-reported] Spotify TechDocs:** docs-like-code built into Backstage. Engineers write Markdown that lives next to the code, and the docs are rendered in the portal — [Backstage TechDocs](https://backstage.io/docs/features/techdocs/); [Announcing TechDocs](https://backstage.io/blog/2020/09/08/announcing-tech-docs)
  - Before TechDocs, the stated problem was that engineers could not find information and could not tell whether it was current. The design goal was to keep docs as close to the code as possible — [Spotify: Solving documentation for monoliths and monorepos](https://engineering.atspotify.com/2019/10/solving-documentation-for-monoliths-and-monorepos)
  - Spotify attributes TechDocs' success to the docs-like-code approach, but no metrics are published — [Announcing TechDocs](https://backstage.io/blog/2020/09/08/announcing-tech-docs)
- **[Self-reported] Pinterest docs-as-code rollout:** reported success rests on internal surveys — [InfoQ: Docs as code at Pinterest](https://www.infoq.com/news/2025/06/docs-as-code-at-pinterest)
- **Ownership (Google):** *Software Engineering at Google*, ch. 10, says documents without owners become stale and hard to maintain. g3doc (docs living in the source tree) made it much easier to find a doc's owner to review suggested changes — [SWE at Google ch. 10](https://abseil.io/resources/swe-book/html/ch10.html)
  - Chromium's public documentation best-practices (derived from Google) recommend minimum viable docs and updating docs in the same CL as the code change — [Chromium documentation best practices](https://chromium.googlesource.com/chromium/src.git/+/b95c2d2c8a7ea8efcec38e091c19bfbeac6af8d1/docs/documentation_best_practices.md)
  - No public source describes Google's internal freshness mechanism; the search found only third-party descriptions.
- **Freshness SLAs (no primary evidence):** "last reviewed" metadata and visual freshness indicators are widely recommended in vendor and practitioner content — [Mintlify: regular reviews](https://www.mintlify.com/library/how-to-keep-documentation-up-to-date-with-regular-reviews); [example handbook doc lifecycle](https://handbook-docs-d0v.pages.dev/docs/how-our-docs-work/the-doc-lifecycle). No study measuring their effect was found.
- **Vale controlled vocabulary:**
  - Each vocabulary is a folder `config/vocabularies/<name>/` holding `accept.txt` and `reject.txt`, one regex per line — [Vale docs: Vocabularies](https://vale.sh/docs/keys/vocab); [docs.vale.sh](https://docs.vale.sh/keys/vocabularies)
  - `reject.txt` entries feed the `Vale.Avoid` existence rule and are flagged as errors. `accept.txt` entries also enforce casing (accept `JavaScript` and `javascript` gets flagged) — [Vale docs](https://vale.sh/docs/topics/vocab)
  - Accepted terms apply across all `BasedOnStyles`. If vocabularies conflict, the last one wins. A synonym-to-preferred-term mapping ("use X instead of Y") needs a `substitution` rule rather than a plain reject list — [Vale docs](https://vale.sh/docs/keys/vocab)
  - Vale also publishes an AGENTS.md for coding agents — [vale.sh/AGENTS.md](https://vale.sh/AGENTS.md)
  - Open-source projects keep project vocabularies in the repo and run Vale in CI, for example Ray — [Ray: how to use Vale](https://github.com/ray-project/ray/blob/ray-2.9.2/doc/source/ray-contribute/how-to-use-vale.md)
- **[Vendor] Acrolinx is now Markup AI:** positioned as "Content Guardian Agents", including a Terminology Agent and a Consistency Agent. Governance rules can rewrite automatically or require human review. The product is described as API-first and MCP-powered, with integrations for GitHub Actions, Cursor, and others — [Markup AI launch](https://markup.ai/blog/introducing-markup-ai-your-enterprise-content-guardian/); [Gilbane](https://gilbane.com/2025/09/introducing-markup-ai-your-enterprise-content-guardian-agent/); [Acrolinx is now Markup AI](https://markup.ai/lets-talk-acrolinx-to-markup-ai/)
  - Launch dates conflict: Gilbane is dated Sept 2025, Markup AI's own post Dec 2025.
  - No independent effectiveness data was found.
- **[Vendor] Swimm "continuous documentation":**
  - Docs are stored as Markdown in the repo and reference code directly (snippets, tokens, paths) — [Swimm docs: Continuous Documentation](https://docs.swimm.io/new-to-swimm/continuous-documentation)
  - Verification runs on each commit. Small changes are auto-synced by a patented algorithm. Significant changes fail the check and route to a human — [Swimm docs](https://docs.swimm.io/new-to-swimm/continuous-documentation)
  - No independent accuracy evaluation was found.

### Inferences
- For a multi-platform enterprise, the low-regret baseline is:
  - each platform's docs live in its repos with CODEOWNERS;
  - one portal renders all of them (TechDocs or similar);
  - Diátaxis page types are required, and the type is recorded as front-matter metadata so the AI assistant and IA can use it;
  - a central Vale package is generated from the glossary/KG: preferred terms go to `accept`, deprecated synonyms to `substitution` rules with a suggested replacement, banned terms to `reject`. It is distributed to all repos as a versioned style package.
- This turns terminology governance from a meeting into a CI check: the "computational" part of federated governance (see Q5).
- Because the DORA evidence is correlational and its quality dimensions (accurate, findable, useful) map directly onto the stated problems (outdated, overlapping, synonyms), DORA's three dimensions are a defensible measurement frame for a doc-quality survey.

### Gaps
- No published controlled before/after data for Diátaxis, TechDocs, or freshness SLAs.
- No primary source on Google's internal freshness tooling.
- alex, write-good, and the Good Docs Project templates were not researched in depth in this pass. They are commonly paired with Vale (alex: inclusive language; write-good: style), and Good Docs provides doc-type templates, but this is not sourced here.
- CODEOWNERS mechanics were not fetched; standard GitHub/GitLab documentation applies.

## 2. Detecting staleness and drift (docs vs. specs, code, changelogs; research and tools; analytics)

### Takeaway
Drift detection is maturing along three tracks:
1. Deterministic checks: references to removed code elements; spec diffs (oasdiff) as triggers for doc review; generated reference docs.
2. LLM-based inconsistency detectors (DocPrism, 2025): useful but still about 62% precision.
3. Repo-wide auto-doc generators (DeepWiki, CodeWiki): helpful drafts, with documented hallucinations.

Best practice is deterministic first, then LLM triage, with a human owner deciding.

### Cited Findings
- **[Research] Tan, Wagner & Treude**, "Detecting Outdated Code Element References in Software Repository Documentation" (Empirical Software Engineering, 2024):
  - flags code element names in READMEs/wikis whose code has since been removed;
  - across 3,000+ GitHub projects, most had at least one outdated reference at some point in their history;
  - issues filed by the authors led to fixes;
  - the tool is publicly available — [arXiv 2212.01479](https://arxiv.org/pdf/2212.01479); [Springer](https://link.springer.com/content/pdf/10.1007/s10664-023-10397-6.pdf)
- **[Research] ICSME 2023 tool paper:** a GitHub Actions workflow that scans docs for outdated references on every PR — [arXiv 2307.04291](https://arxiv.org/pdf/2307.04291)
- **[Research] DocPrism** (arXiv 2511.00215, Oct 2025):
  - off-the-shelf LLM, no fine-tuning, covers Python, TypeScript, C++ and Java;
  - its "Local Categorization and External Filtering" step cut the flag rate from 98% (naive LLM) to 14%;
  - final flag rate 15% and precision 0.62 on 1,991 code–doc pairs;
  - most false positives came from incorrect LLM reasoning — [arXiv 2511.00215](https://arxiv.org/html/2511.00215v1)
- **[Research] CASCADE** (arXiv 2604.19400, Apr 2026): detects description–code inconsistencies by generating tests from documentation, evaluated on Java — [emergentmind summary of 2604.19400](https://www.emergentmind.com/papers/2604.19400) (secondary; read the paper itself before relying on details)
- **[Research] CodeWikiBench** (arXiv 2510.24428): a benchmark that derives rubrics from official docs and uses LLM judges to evaluate repo-level generated documentation, including DeepWiki — [arXiv 2510.24428](https://arxiv.org/html/2510.24428v5). DeepWiki-specific scores were not extracted in this pass.
- **[Practitioner] DeepWiki accuracy:**
  - Bitovi rated DeepWiki 4–4.5/5 for accuracy, with a misleading section on one codebase — [Bitovi](https://bitovi.com/blog/comparing-ai-documentation-engines-deepwiki-vs-code2tutorial)
  - an OpenWrt maintainer warned that users filed bugs based on wrong DeepWiki content — [OpenWrt forum](https://forum.openwrt.org/t/important-consideration-deepwiki-ai-generated-docs-may-contain-inaccuracies/249471)
  - HN users report it is good where it restates existing docs and invents things where docs are missing — [HN thread](https://hn.svelte.dev/item/45884169)
- **API spec drift:**
  - oasdiff compares two OpenAPI versions, detects 100–250+ kinds of breaking change (the count depends on version) at ERR/WARN/INFO levels, and is commonly run in CI with `--fail-on ERR`. It outputs markdown/HTML/JSON reports — [oasdiff BREAKING-CHANGES](https://github.com/tufin/oasdiff/blob/v1.10.16/BREAKING-CHANGES.md); [Nordic APIs](https://nordicapis.com/using-oasdiff-to-detect-breaking-changes-in-apis/)
  - Note: oasdiff compares spec to spec, not prose docs to spec. No source was found for a standard "prose-to-spec" drift checker.
- **[Vendor] Swimm** detects code-coupled doc drift on every commit (see Q1) — [Swimm docs](https://docs.swimm.io/new-to-swimm/continuous-documentation)
- **[Vendor] Atlassian Compass + Swimm integration:** advertised a doc "health score" plus auto-sync — [Atlassian Community](https://community.atlassian.com/t5/App-Central-articles/Get-a-Health-Score-amp-Auto-sync-Your-Docs-With-the-Swimm-and/ba-p/2135802)
- **[Vendor] Usage analytics for gaps (Kapa.ai):**
  - "Coverage Gaps" clusters topics where the assistant gave uncertain/inconclusive answers and generates recommendations for what to document;
  - needs a minimum volume of uncertain conversations;
  - an Analytics API exports conversations, top questions, and gaps;
  - "Source Analytics" shows which sources are cited most — [Kapa docs: Coverage gaps](https://docs.kapa.ai/analytics/coverage-gaps); [Kapa analytics](https://docs.kapa.ai/analytics/); [Kapa blog: from "I don't know" to insight](https://www.kapa.ai/blog/from-“i-don’t-know”-to-insight-using-ai-to-find-documentation-gaps)

### Inferences
- For platform docs, the sources of truth are machine-readable: OpenAPI, CRD OpenAPI schemas, Terraform provider schemas, Helm values schemas, changelogs. A practical pipeline:
  1. generate the reference layer of Diátaxis from those schemas, so reference docs never drift;
  2. on each schema diff (oasdiff-style), automatically open a "docs review needed" task for the how-to and explanation pages that reference the changed entities. The KG can hold the page→entity links; Tan et al.-style reference scanning can find them;
  3. run an LLM consistency check (DocPrism-style) only as triage, given about 0.62 precision.
- Auto-generated repo wikis (DeepWiki-like) are best treated as internal drafts or as retrieval context, not as published truth. The documented failure mode is confident invention where human docs are missing — exactly the gap areas.
- An entity-level staleness score from the KG can drive freshness SLAs better than calendar-based review alone. Example: "page cites API v2 field X, which is deprecated in v3".

### Gaps
- No peer-reviewed evaluation of Swimm, Mintlify auto-update, or DeepWiki accuracy at enterprise scale.
- No source found on drift checks specifically for CRDs or Terraform schemas versus prose docs. This is an inferred extension of the above.
- CASCADE was seen only through a secondary summary.

## 3. End-to-end journey documentation across teams (golden paths, journey maps, IA)

### Takeaway
Spotify's Golden Path tutorials are the canonical pattern: one opinionated, step-by-step, end-to-end tutorial per discipline, rendered in the portal, with new hires as the feedback loop. Spotify itself reports that cross-team ownership of these journeys causes coordination gaps, which is directly relevant here. No quantitative outcome data was published.

### Cited Findings
- **[Self-reported] Spotify Golden Paths:**
  - "the opinionated and supported path" to build something (backend service, website, data pipeline);
  - created to end "rumour-driven development", where autonomous teams produced fragmented tools and finding out how meant asking a colleague;
  - tutorials are written in TechDocs and surfaced in Backstage;
  - one tutorial per discipline, aimed at new engineers, containing every step — [Spotify Engineering, Aug 2020](https://engineering.atspotify.com/2020/8/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem)
- **[Self-reported] Ownership evolution at Spotify:**
  - dedicated technical writers per tutorial did not scale;
  - ownership moved to many teams, one per discipline, which "creates coordination gaps" both within a single tutorial and across the set;
  - teams with little doc time should prioritise their Golden Path tutorial;
  - when a tool changes (e.g., Kubernetes adoption), the tutorial must change with it — [same source](https://engineering.atspotify.com/2020/8/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem)
- **[Self-reported] Feedback loop at Spotify:** new hires complete the tutorial in their first two weeks, then build an end-to-end product in a week-long bootcamp. The tutorials are described as Spotify's most read technical docs. Planned: a "Golden State" checklist and team-level end-to-end product tutorials. No metrics given — [same source](https://engineering.atspotify.com/2020/8/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem)
- **CNCF Platform Engineering Maturity Model:**
  - five aspects: Investment, Adoption, Interfaces, Operations, Measurement;
  - four levels: Provisional, Operational, Scalable, Optimizing;
  - "Interfaces" covers how users discover and consume capabilities, which is where docs and self-service sit — [CNCF maturity model TL;DR](https://maturitymodel.cncf.io/tldr/); [CNCF blog Sept 2026](https://www.cncf.io/blog/2026/09/01/platform-engineering-maturity-from-toolchain-to-self-service/)
- **[Practitioner] Golden-path heuristics:**
  - "If a developer has to ping someone on Slack or open a Jira ticket, it's not a golden path";
  - start with one high-friction workflow and iterate — [Improving: Building golden paths](https://www.improving.com/thoughts/building-golden-paths/)

### Inferences
- For product teams whose journeys cross several platforms, give each end-to-end journey a single named owner: a journey or "golden path" owner, often the platform-engineering/DevEx team or a rotating lead platform. That owner holds:
  - the narrative tutorial;
  - the link structure into each platform's own how-to/reference pages, which those platforms own via CODEOWNERS.
- This mirrors Spotify's per-discipline ownership while fixing the coordination gap Spotify named.
- The KG can encode journeys as ordered steps → capabilities → owning platform → canonical pages. That makes "which journeys break when platform X changes?" answerable automatically.
- Portal IA: top level by user journey/task (product-team view). Second level by platform (owner view). Each page carries Diátaxis type, owner, last-verified date, and glossary-linked entities.
- Use the "would someone need to ping a person?" test as a direct proxy for the consultation-reduction goal.

### Gaps
- No published metrics (time-to-first-deploy, onboarding time) tied specifically to golden-path docs were found.
- No sourced examples of formal multi-team journey-map governance (RACI for cross-platform tutorials) beyond Spotify's description.

## 4. AI assistant feedback loops (unanswered questions → doc backlog, deflection measurement, closing the loop)

### Takeaway
The mechanics are well productised: log questions the assistant answers with low confidence or can't answer, cluster them into topics, route each cluster to the owning team as a doc backlog item, and track citation/usage per source. Evidence of impact is almost entirely self-reported (Spotify AiKA) or vendor-reported (Harness, Kapa). No independent measurement of deflection was found.

### Cited Findings
- **[Vendor] Kapa.ai Coverage Gaps loop:** see Q2. Uncertain answers feed topic clusters plus AI recommendations, exportable via API/CSV for an agent or a backlog — [Kapa docs](https://docs.kapa.ai/analytics/coverage-gaps); [Kapa blog: users are telling you what's missing](https://www.kapa.ai/blog/your-users-are-telling-you-whats-missing)
  - Design point: the assistant is built to say "uncertain" rather than guess, and that is what makes the gap signal possible.
- **[Self-reported] Spotify AiKA (Backstage AI knowledge assistant):**
  - "reduced how long it takes to resolve internal support requests … by 47%";
  - over 86% of engineers use it weekly and over 1,000 employees daily;
  - "more than 6,000 hours" saved in 20 months;
  - no methodology given; a linked New Stack summary says "nearly 50%" — [Spotify Portal: AiKA](https://backstage.spotify.com/aika-hub/)
  - The page says nothing about a gap/unanswered-question loop.
- **[Vendor] Harness:** reports AI deflected about 95% of internal platform support tickets. Methodology unverified — [Harness blog](https://www.harness.io/blog/harness-ai-helps-scale-platform-wide-support)
- **[Self-reported] Mercedes-Benz.io:** a small effort to reduce internal support grew into a company-wide GenAI platform; no metrics in the snippet — [Mercedes-Benz.io blog](https://www.mercedes-benz.io/blog/2025-10-31-from-bottleneck-to-backbone-how-we-accidentally-built-a-company-wide-genai-platform)
- **[Self-reported] Elastic Support Assistant (customer support, not internal):** mean time to first response improved 23% and assisted case volume fell 7% — [Elastic](https://www.elastic.co/resources/article/elastic-support-assistant)
  - The modest 7% is a useful realism anchor compared with 70–95% vendor claims.
- **[Survey] Context on demand:**
  - in Stack Overflow 2024, over 60% of developers spent ≥30 min/day searching for solutions (including asking colleagues and waiting), and about 1 in 4 spent ≥60 min — [Stack Overflow blog 2024](https://stackoverflow.blog/2024/09/23/where-developers-feel-ai-coding-tools-are-working-and-where-they-re-missing-the-mark)
  - in 2025, only 33% trusted the accuracy of AI output (down from 43%) — [SO 2025 results](https://stackoverflow.blog/2025/08/01/diving-into-the-results-of-the-2025-developer-survey/)
  - in 2026, top answer methods were search online (83%) and ask an AI agent (70%) — [SO 2026 results](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/)

### Inferences
- Close the loop as a pipeline:
  1. log every assistant turn with confidence, retrieved sources, KG entities, and user feedback;
  2. weekly, cluster unanswered/low-confidence/thumbs-down turns, plus consultation-request tickets, by KG entity, so each cluster maps to an owning platform via the KG;
  3. auto-file backlog items in that team's tracker with sample questions;
  4. measure "gap closed" when that cluster's confidence and answer acceptance rise.
- Also feed unrecognised terms (synonyms the glossary misses) to the terminology stewards. The assistant's query log is the best synonym-discovery corpus available.
- Deflection measurement should use a counterfactual-friendly design: track consultation-session requests per product team per month before and after rollout, ideally staggered by platform or team. Also ask "did this answer stop you from booking a consultation?" at session end. Vendor ratios (deflected / total conversations) overstate impact.
- Low trust in AI output (33%) argues for always citing owned, dated sources in answers. It also argues for routing high-stakes or low-confidence questions to humans, while still logging them as gaps.

### Gaps
- No independent or peer-reviewed study measuring support/consultation reduction from an internal docs assistant.
- No published "unanswered question → doc PR" cycle-time data.

## 5. Operating model (federated vs central governance, terminology stewards, incentives, metrics, change management)

### Takeaway
The best-fitting analogy is data-mesh federated computational governance. Platform teams own their docs and local terms. A small federated body (platform reps, DevEx/doc lead, terminology stewards, KG/ontology owner) owns cross-cutting terms, page-type standards and journey ownership, and encodes them as automated checks (lint, schema, freshness) rather than manual review. Metrics should combine DORA-style doc-quality survey items, consultation hours, and assistant gap metrics.

### Cited Findings
- **Data mesh principle:** "federated computational governance" (Dehghani): domain owners plus a federated team set global standards, which the platform automates — [Fowler/Dehghani: Data Mesh Principles](https://martinfowler.com/articles/data-mesh-principles.html)
- **[Research — gray literature review]** The federated governance team includes domain experts, SMEs, governance experts, legal, the platform team and management. A common business glossary keeps definitions consistent across the organisation — [arXiv 2304.01062](https://arxiv.org/pdf/2304.01062)
- **[Research]** Decentralized data governance concepts and approaches within a data mesh platform — [arXiv 2307.02357](https://arxiv.org/pdf/2307.02357) (not read in depth)
- **[Vendor/Practitioner] Splitting term ownership:**
  - a central council owns cross-domain terms, while domains own local terms. Stewards sit "inside the business, because the people who use the data know first when a definition is wrong" — [Atlan](https://atlan.com/know/data-governance/how-to-scale-data-governance-across-business-domains/)
  - an ontology serves as the shared upper model, with domain models mapped to it bottom-up — [Towards Data Science](https://towardsdatascience.com/challenges-and-solutions-in-data-mesh-part-3-dacb917f3c91)
  - "governance of meaning (ontology, centrally managed)" is separate from "governance of implementation (locally managed)" — [Promethium](https://promethium.ai/guides/metadata-management-data-mesh-federated-ownership-patterns/)
- **[Self-reported] Spotify central vs federated:** a centralised writer model did not scale, and per-discipline team ownership created coordination gaps (see Q3) — [Spotify Golden Paths](https://engineering.atspotify.com/2020/8/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem)
- **Ownership principle:** unowned docs go stale — [SWE at Google ch. 10](https://abseil.io/resources/swe-book/html/ch10.html)
- **[Survey] Incentive risk:** documentation work linked to burnout for underrepresented groups in DORA 2023 — [DX newsletter](https://newsletter.getdx.com/p/2023-dora-report)
- **Measurement aspect:** the CNCF maturity model treats Measurement as a separate maturity aspect alongside Adoption and Interfaces — [CNCF maturity model](https://maturitymodel.cncf.io/tldr/)

### Inferences
- **Proposed operating model** (synthesis, not a sourced blueprint):
  - **Federated:** each platform team is accountable for its pages (CODEOWNERS), its local terms, and its freshness SLA.
  - **Central enabling team (DevEx/docs):** owns the portal, IA, Diátaxis templates, the Vale package, the assistant, gap triage, and the end-to-end journey tutorials (or assigns journey owners).
  - **Terminology/ontology working group:** one steward per platform plus the KG owner. Owns cross-platform terms, synonym → preferred-term mappings, and deprecations. Decisions are published as KG changes that regenerate the Vale vocabularies and the assistant's synonym expansion. That is the "computational" part.
- **Metric set:**
  - Outcome: consultation hours and requests per product team; time-to-first-deploy/first-successful-integration via golden path; DORA doc-quality items (findable, accurate, useful) in a quarterly survey.
  - Assistant: answer acceptance, low-confidence rate per platform, gap-cluster closure time.
  - Hygiene: % pages with owner, % within freshness SLA, lint violations, open drift alerts.
- **Incentives:** make doc health visible per team (scorecards in the portal). Count doc and gap fixes as platform-roadmap work. Spread doc load deliberately, given DORA's burnout signal.
- **Change management:** start with one or two high-traffic cross-platform journeys and the top gap clusters (the CNCF/practitioner advice to start from one high-friction workflow). Use new-joiner walkthroughs as acceptance tests, as Spotify did.

### Gaps
- No sourced enterprise case with measured outcomes for a "terminology governance board" for engineering/platform docs specifically. The evidence comes from data governance.
- No benchmark values for doc NPS or consultation-hours reduction.

## 6. Case studies with measured results (support/consultation reduction via docs + AI)

### Takeaway
Measured results exist but are almost all self- or vendor-reported, with undisclosed methodology. Spotify AiKA's 47% faster internal support resolution is the most relevant internal-platform datapoint. Vendor deflection figures of 70–95% should be treated as upper-bound marketing. Elastic's 7% reduction in case volume is a sober counterpoint.

### Cited Findings
- **[Self-reported] Spotify AiKA:** 47% reduction in internal support resolution time; 86%+ weekly engineer usage; 6,000+ hours saved in 20 months — [Spotify AiKA](https://backstage.spotify.com/aika-hub/)
- **[Vendor] Harness:** about 95% of internal support tickets deflected by AI — [Harness](https://www.harness.io/blog/harness-ai-helps-scale-platform-wide-support)
- **[Self-reported] Elastic:** −7% assisted case volume and +23% faster mean time to first response (customer-facing) — [Elastic](https://www.elastic.co/resources/article/elastic-support-assistant)
- **[Vendor] Ksolves AI-assisted Backstage portal:** before the portal, routine developer requests were platform tickets with 2–5 day lead times; no reduction figure; unnamed client — [Ksolves](https://www.ksolves.com/case-studies/ai-ml/ai-assisted-backstage-developer-self-service-portal)
- **[Research] Outdated-reference detection:** the authors' GitHub issues led to real doc fixes (qualitative) — [arXiv 2212.01479](https://arxiv.org/pdf/2212.01479)
- **[Survey] DORA:** correlational evidence that doc quality amplifies performance outcomes (see Q1) — [DORA](https://dora.dev/capabilities/documentation-quality/)
- Other results were discarded as not credible or not relevant: Rakuten/Enjo IT helpdesk, Kroger/Dynatrace "99%" (observability, not docs), and a "TechCorp 60%" page that appears to be a sample/placeholder story.

### Inferences
- Plan to measure locally with a baseline instead of relying on external benchmarks. A realistic expectation is a moderate reduction in routine consultations, with the big wins concentrated in repetitive "how do I…/which platform…/what does term X mean" questions. This is an inference from the spread between Elastic's 7% and vendor claims.
- Resolution-time reduction (Spotify) may be easier to achieve and prove than volume reduction.

### Gaps
- No independent, peer-reviewed case study of an internal platform documentation + AI assistant program reporting consultation-hour reduction.
- No public metrics from Backstage adopters on TechDocs alone.
