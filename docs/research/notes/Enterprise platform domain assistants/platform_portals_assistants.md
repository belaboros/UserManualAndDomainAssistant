# Internal developer platforms, portals, and AI assistants: existing solutions, evidence, and gaps (as of Nov 2026)

Scope note: These notes were compiled from about 20 web searches and fetches on 2026-11-13. Most "impact" numbers come from vendors or from companies' own engineering blogs, so they are self-reported. Each claim below is labelled as evidence (survey or research), self-reported (an engineering blog), or vendor (marketing, or a study the vendor paid for).

## 1. Internal developer portals and catalogs as knowledge graphs (Backstage, Port, Cortex, OpsLevel, Humanitec, Roadie)

### Takeaway
Backstage, Port, Cortex and OpsLevel all model the platform landscape as a typed property graph: entities of different kinds, plus named relations such as ownership, dependency and part-of. Since mid-2025 every major portal exposes that graph to AI agents through MCP servers. However, none of them provides a formal ontology or an RDF/OWL export. Their schemas are pragmatic and centred on engineering artifacts. Business-capability terms, glossaries, synonyms and contradictory documentation are mostly outside their models.

### Cited Findings
- **Backstage graph model.** The official docs describe the catalog as a graph: entities are nodes, relations are edges, and "kinds" and "types" classify the entities — [backstage.io: creating the catalog graph](https://backstage.io/docs/next/features/software-catalog/creating-the-catalog-graph)
- **Backstage entity kinds.** The system model defines Domain, System, Component, API and Resource. Ownership uses Group and User. Location and Template are supporting kinds. — [backstage.io system model](https://backstage.io/docs/features/software-catalog/system-model)
- **Backstage relations.** The well-known relations come in pairs: ownedBy/ownerOf, providesApi/apiProvidedBy, consumesApi/apiConsumedBy, dependsOn/dependencyOf, partOf/hasPart, memberOf/hasMember and parentOf/childOf — [backstage.io well-known relations](https://backstage.io/docs/features/software-catalog/well-known-relations)
- **Backstage says the catalog is not the source of truth.** Its docs say the catalog should not be treated as the ultimate source of truth. It is better treated as a cache served over a REST API. — [backstage.io](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph)
- **New AI entity types in Backstage.**
  - The `@backstage/plugin-catalog-backend-module-ai-model` module adds an `AiResource` kind. Its types are `skill` ("reusable contextual knowledge for AI coding tools") and `rule` (governance constraints, with required `category` and `rationale` fields).
  - It also adds an `mcp-server` subtype of the API kind.
  - Backstage also has an MCP Actions backend at `/api/mcp-actions/v1`.
  - Source: [backstage.io AI in the catalog](https://backstage.io/docs/ai/ai-in-the-catalog)
- **No RDF or ontology export for Backstage.** No built-in or community RDF/OWL exporter turned up. Third-party tools such as Knowledge Tree publish infrastructure into the catalog using the dependsOn and dependencyOf relations, without RDF. — [Knowledge Tree Backstage integration](https://knowledge-tree-web-docs.pages.dev/integrations/backstage/)
- **Community MCP and graph layers on Backstage.** These include:
  - TeraSky's Catalog MCP plugin, which queries entities by owner or by filter — [TeraSky catalog-mcp](https://terasky-oss.github.io/backstage-plugins/plugins/catalog-mcp/overview)
  - Roadie's "Rich Catalog Entity" MCP server, published July 2025, which serves entities, relations and docs — [Roadie docs](https://roadie.io/docs/details/roadie-mcp/rich-catalog-entity)
  - Red Hat Developer Hub stories for MCP tools that read and register catalog entities — [Red Hat Jira RHIDP-10507](https://issues.redhat.com/browse/RHIDP-10507)
- **Roadie's position.** Roadie markets the internal developer platform (IDP) as an "AI goldmine" for "context engineering". (Vendor.) — [Roadie blog](https://roadie.io/blog/idp-ai-goldmine-context-engineering/)
- **Port.**
  - "Blueprints" are user-defined schemas, so the data model is customisable rather than fixed.
  - Port's "Context Lake" combines the modelled catalog data (blueprints, entities, scorecards) with MCP connectors that fetch live external data such as tickets, logs and docs.
  - Port's MCP server lets Claude, Cursor and Copilot query the catalog and run governed actions.
  - Sources: [Port docs: Context Lake](https://docs.port.io/context-lake/overview/); [Port AI interfaces](https://docs.port.io/ai-interfaces/overview)
  - Port also claims an 80% cut in AI token costs. This is unverified vendor marketing. — [Port blog](https://www.port.io/blog/context-layer-for-ai-sdlc)
- **OpsLevel.** It announced an MCP server on 2025-06-25. The server exposes ownership, dependencies, custom properties and maturity data. — [OpsLevel](https://opslevel.com/resources/opslevels-new-mcp-server-powers-your-ai-assistant-with-real-time-context); [OpsLevel MCP docs](https://docs.opslevel.com/docs/mcp)
- **Cortex.** Its MCP server was announced on 2025-07-29 and brings portal context into the IDE. Do not confuse it with Palo Alto Networks' unrelated "Cortex MCP". — [Cortex blog](https://www.cortex.io/post/mcp-server)
- **Spotify Portal.** Spotify's commercial Backstage registers MCP server entities and can connect AiKA to third-party MCP servers. — [Spotify Portal third-party MCP](https://backstage.spotify.com/docs/portal/core-features-and-plugins/mcp/third-party-servers)
- **Adjacent: the data-catalog world.**
  - DataHub began as LinkedIn's internal metadata tool — [LinkedIn Engineering 2019](https://engineering.linkedin.com/blog/2019/data-hub)
  - It is now marketed as a "metadata knowledge graph" or context graph for AI agents. (Vendor.) — [DataHub blog](https://datahub.com/blog/metadata-knowledge-graph/)
  - Data catalogs model datasets, not platform services, but they are architecturally the closest open-source precedent for a KG-backed assistant.

### Inferences
- **The portals are about halfway to an ontology.** Backstage's model is a fixed, lightweight upper ontology (about eight kinds and seven relation pairs). Port's blueprints are a user-defined schema, similar to a property-graph schema. None has class hierarchies, formal semantics, SKOS-style concepts or synonyms, or provenance of facts. These are exactly the things needed to reconcile overlapping or contradictory platform terminology.
- **An RDF/SKOS layer would have to be custom-built.** The practical route is to map the catalog REST API's kinds, relations and annotations onto it. "Capability" or "concept" nodes would be new entity kinds, linking the glossary terms product teams hear to Systems, APIs and Resources.
- **MCP gives agents a ready interface.** Through MCP, catalogs have quickly become the standard "structured context" source for agents. An assistant can use the catalog for facts (owner, dependencies, lifecycle) and retrieval over docs for explanations.

### Gaps
- No published RDF/OWL mapping of the Backstage or Port models turned up, and no academic paper on IDP catalogs as ontologies.
- Humanitec's resource-graph model and its AI features were not researched, because the search budget ran out.
- No source gives a measured accuracy improvement from adding catalog or graph context to an assistant, compared with retrieval over docs alone.

## 2. AI assistants over internal platforms and docs, with measured outcomes

### Takeaway
The best evidence is self-reported numbers from in-house assistants: Uber Genie, GoDaddy Katana and Spotify AiKA. They show substantial deflection of platform-support questions. Vendor figures (Glean's Forrester study, ticket-deflection case studies) are commissioned or marketing. No independent controlled study of internal-platform assistants turned up.

### Cited Findings
- **Uber Genie (self-reported).**
  - Genie is a Slack copilot that answers platform-support questions. It was built because support channels received about 45K questions a month.
  - It uses RAG over the internal wiki, Uber's internal Stack Overflow and engineering requirement documents.
  - By 2024 it covered 154 channels, had answered more than 70K questions, had a 48.9% helpfulness rate, and had saved an estimated 13K engineering hours.
  - Sources: [Uber blog](https://www.uber.com/blog/genie-ubers-gen-ai-on-call-copilot); [InfoQ](https://www.infoq.com/news/2024/10/uber-genie-rag-copilot)
- **Uber "Enhanced Agentic RAG" follow-up.** For security and privacy questions, acceptable answers rose by a relative 27% and incorrect advice fell by a relative 60%. It is built with LangGraph in the Michelangelo Genie framework. — [Uber blog](https://www.uber.com/en-AU/blog/enhanced-agentic-rag/)
- **GoDaddy Katana (self-reported, Aug 2026).**
  - Katana is an internal AWS app platform run by 5 engineers supporting more than 500 production apps.
  - The assistant's sources are curated Slack history, custom instructions, internal docs and the live platform API (logs and config).
  - It handles more than 80% of requests autonomously, and about 1 in 5 interactions need a human.
  - Escalation by emoji creates a Jira ticket with the gathered context.
  - A weekly report tracks volume, escalation rate and negative sentiment, and the weekly on-call engineer fixes bad answers.
  - After a two-week experiment, direct posting to the support Slack channel was disabled permanently.
  - Sources: [GoDaddy](https://www.godaddy.com/resources/news/how-we-scaled-platform-support-10x-without-scaling-the-team)
- **Spotify AiKA.**
  - AiKA came out of Hack Week 2023 and went live internally in December 2023. It uses Slack support channels, TechDocs and the catalog.
  - It was announced for Portal customers at KubeCon EU 2025, and later versions add MCP and actions.
  - Usage figures conflict: "over 1,000 employees" ([The New Stack](https://thenewstack.io/introducing-aika-backstage-portal-ai-knowledge-assistant/)), "25% of workforce weekly" ([TechCrunch](https://techcrunch.com/2025/05/04/backstage-access-spotifys-dev-tools-side-hustle-is-growing-legs)) and "85% WAU" ([LinearB](https://linearb.io/blog/how-spotify-turned-internal-chaos-into-an-industry-standard)).
  - Product page: [Spotify Portal AiKA](https://backstage.spotify.com/blog/aika-data-plugins-coming-to-portal)
- **Elastic Support Assistant (customer-facing, self-reported).**
  - Six months after launch, 5% of Support Hub visitors used it.
  - Elastic reports 6x more "hard" deflections (users abandoned ticket creation) and 20x more "soft" deflections.
  - Source: [Elastic](https://www.elastic.co/resources/article/elastic-support-assistant)
- **LinkedIn SQL Bot.**
  - SQL Bot is a text-to-SQL assistant in LinkedIn's DARWIN data platform. It uses a knowledge graph built from DataHub metadata, query logs and crowdsourced domain knowledge.
  - It is the closest published example of a KG-backed internal assistant, though it covers data tables rather than services.
  - Sources: [arXiv 2507.14372 (prereview)](https://prereview.org/preprints/doi-10.48550-arxiv.2507.14372); [ZenML summary](https://www.zenml.io/llmops-database/building-a-production-text-to-sql-assistant-with-multi-agent-architecture)
- **Glean (vendor-commissioned).**
  - The Forrester TEI study (Sept 2024) was based on interviews with only 4 customers. It reports 141% ROI over 3 years.
  - Glean's own summary says the study found a 20% reduction in internal support requests.
  - Sources: [Forrester TEI of Glean](https://tei.forrester.com/go/Glean/workAIplatform/); [Glean summary](https://www.glean.com/resources/guides/forrester-study-the-total-economic-impact-of-glean)
- **Glean's "Enterprise Graph".** Launched in September 2025, it models people, content and apps, and the index is permissions-aware. — [Glean press](https://www.glean.com/press/glean-introduces-third-generation-ai-assistant-new-enterprise-graph-to-enable-the-superintelligent-enterprise)
- **Other vendor-commissioned TEI studies.** Stack Overflow for Teams (191% ROI) — [SO blog](https://stackoverflow.blog/forrester); Cortex — [Forrester TEI Cortex](https://tei.forrester.com/go/cortex/idp/)
- **Ticket-deflection case studies (vendor; IT or customer support, not platform engineering).**
  - Apollo with Tray.ai: 40% of IT tickets deflected in the first two weeks — [casestudies.com](https://www.casestudies.com/company/tray-ai/case-study/apollo-deflects-40-of-it-tickets-with-trayai)
  - InDebted with eesel: 15% Jira ticket deflection — [casestudies.com](https://www.casestudies.com/company/eesel/case-study/indebteds-new-helpdesk-agent-eesel-ai)
  - Definitions of "deflection" vary widely between these studies.

### Inferences
- **The successful assistants share one pattern:**
  - They sit in the support channel, usually Slack.
  - They retrieve from historical Q&A and docs, plus live platform APIs or the catalog.
  - They have an explicit escalation path.
  - A human-in-the-loop process fixes bad answers.
  - They report weekly metrics.
- **Realistic targets.** Uber's 48.9% helpfulness rate and GoDaddy's 80% autonomous handling roughly bracket what can be expected.
- **A useful baseline.** A program to replace consultations could adopt GoDaddy's metrics (volume, escalation rate, sentiment) and Uber's (helpfulness, hours saved).
- **The graph component is rare.** Only LinkedIn's SQL Bot clearly uses a KG. Most assistants use plain RAG plus a catalog API, so "assistant + platform KG" is a relatively unoccupied niche.

### Gaps
- No independent, peer-reviewed measurement of an internal-platform assistant reducing consultations or onboarding time turned up.
- Product-specific evidence was not found for Atlassian Rovo, GitHub Copilot knowledge bases or Spaces, OverflowAI, Kapa.ai or Sourcegraph.
- No source quantified the reduction in consultation sessions specifically, as opposed to tickets or Slack questions.

## 3. Cognitive load, platform-as-product, and the evidence that docs and usability matter

### Takeaway
DORA gives the strongest independent (survey-based) evidence:
- Documentation quality is associated with about 25% higher team performance, and it amplifies technical practices.
- Platforms help productivity but can hurt throughput and stability when mandated.
- In 2025, platform quality and internal-context quality were identified as what determine whether AI pays off.

Separately, the Atlassian 2025 survey shows information-finding friction cancels out much of the AI time savings.

### Cited Findings
- **DORA 2023 on documentation.**
  - High-quality documentation is associated with 25% higher team performance than low-quality documentation, and it amplifies technical capabilities. The reliability amplification is given as 1.4x. — [Google Cloud DORA 2023](https://cloud.google.com/blog/products/devops-sre/announcing-the-2023-state-of-devops-report?hl=en); [dora.dev documentation quality capability](https://dora.dev/capabilities/documentation-quality/)
  - Secondary summaries cite 2.4x amplification for CI and 2.7x for CD. These were not confirmed in a primary source. — [DX newsletter](https://newsletter.getdx.com/p/2023-dora-report)
- **DORA 2024 on platforms.**
  - Platform users report higher productivity.
  - They also show about 8% lower throughput and about 14% lower change stability, especially when the platform is mandated for the whole lifecycle.
  - Having a dedicated platform team is associated with about 6% higher team productivity.
  - Sources: [DORA 2024 infographic](https://dora.dev/research/2024/2024-DORA-Report-Infographic.pdf); [The New Stack](https://thenewstack.io/dora-2024-ai-and-platform-engineering-fall-short/)
- **DORA 2025** ("State of AI-assisted Software Development", about 5,000 respondents):
  - 90% of organizations have adopted at least one platform.
  - There is a direct correlation between high-quality internal platforms and the ability to unlock AI value.
  - One recommendation is to "connect AI to your internal context".
  - Seven capabilities amplify AI's impact. Their names were not extracted here; see the full report.
  - Sources: [Google Cloud DORA 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report); [report PDF](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf)
  - InfoQ summarizes that organizations with high-quality docs, searchable knowledge repositories and structured internal data get more out of AI — [InfoQ](https://infoq.com/news/2026/03/ai-dora-report/)
- **Atlassian State of DevEx 2025** (3,500 developers and managers):
  - 50% of developers lose more than 10 hours a week to organizational inefficiencies, and 90% lose at least 6 hours.
  - Coverage identifies "finding information" as the top productivity drain.
  - Much of the time AI saves is lost again to searching, tool switching and cross-team collaboration.
  - Atlassian's 2026 edition reports that the share of developers saving 10+ hours a week with AI fell to 25%.
  - Sources: [Atlassian blog](https://www.atlassian.com/blog/developer/developer-experience-report-2025); [ShiftMag](https://shiftmag.dev/the-number-one-productivity-killer-for-devs-finding-information-5700/)
- **CNCF frameworks.**
  - The CNCF TAG App Delivery Platforms White Paper (April 2023) covers the "what and why" of platforms.
  - The Platform Engineering Maturity Model (v1, October 2023) has 5 aspects (investment, adoption, interfaces, operations, measurement) and 4 levels. It states that no level is inherently good, and that each level needs more funding and people.
  - Sources: [CNCF maturity model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/); [CNCF blog](https://www.cncf.io/blog/2023/11/20/announcing-the-platform-engineering-maturity-model/)
- **Team Topologies.** It frames platform teams as reducing the cognitive load of stream-aligned teams through a "thinnest viable platform" offered as a product — [Team Topologies key concepts](https://teamtopologies.com/key-concepts)
- **SPACE framework.** It covers Satisfaction, Performance, Activity, Communication/collaboration and Efficiency/flow — [ACM Queue 2021](https://queue.acm.org/detail.cfm?id=3454124)
- **DX Core 4.** It combines DORA, SPACE and DevEx into four dimensions: speed, effectiveness, quality and impact. (Not verified in this session.) — [DX](https://getdx.com/research/measuring-developer-productivity-with-the-dx-core-4/)
- **Backstage adoption.**
  - A widely repeated figure says external Backstage deployments average about 10% developer adoption. It is attributed to Spotify staff but could not be verified against a primary source.
  - Spotify reports about 99% internal adoption.
  - Most sources here are competitors' blogs or forums.
  - Sources: [Port newsletter "Backstage is dead"](https://newsletter.port.io/p/backstage-is-dead); [devops.com](https://devops.com/is-backstage-the-right-internal-developer-portal-for-you/)

### Inferences
- **The evidence supports the core thesis.** DORA links documentation quality to performance, and the 2025 report says AI amplifies whatever internal context quality already exists. Bad or contradictory platform docs therefore limit any assistant. Part of the assistant's value is surfacing those doc defects back to platform teams.
- **Mandating a tool can backfire.** DORA's finding of lower throughput under mandated platforms is a warning against forcing the assistant on teams as the only channel. GoDaddy did this successfully only after an experiment.

### Gaps
- No study directly measures how "new terminology" or the need for glossaries adds to cognitive load for platform consumers.
- The section of the DORA 2025 report on internal documentation and the names of its seven AI capabilities were not extracted.

## 4. Enterprise knowledge graphs for IT and platform landscapes, and ontology-based ITSM

### Takeaway
Some KG case studies of IT landscapes exist, especially at banks (connected inventory, semantic layers). The big tech companies publish metadata graphs (LinkedIn DataHub) and RAG assistants, but no published service-and-terminology ontology combined with an assistant for platform consumers turned up.

### Cited Findings
- **A global bank's "connected inventory" KG** (Graphwise/GraphDB, vendor case study). It linked employees, hardware, software, networks, customers and locations. The bank used it for real-time incident management and regulatory compliance. — [Graphwise](https://graphwise.ai/?p=242108)
- **A multinational bank's semantic layer for risk management** (Enterprise Knowledge, consultancy). The KG connects 3 or more applications, with 6 more planned. — [EK PDF](https://enterprise-knowledge.com/wp-content/uploads/2024/12/A-Semantic-Layer-to-Enable-Risk-Management-at-a-Multinational-Bank-1.pdf)
- **A global development bank's KG** (Enterprise Knowledge). It combined auto-tagging and an enterprise KG to power a content recommender and chatbot for disseminating in-house expertise. — [EK PDF](https://enterprise-knowledge.com/wp-content/uploads/2021/04/Knowledge-AI_-Content-Recommender-and-Chatbot-Powered-Auto-Tagging-and-an-Enterprise-Knowledge-Graph.pdf)
- **A US patent on an automatically generated IT-asset ontology.** It describes a curated, auto-updated graph of applications and their dependencies across products. It notes that enterprise-wide dependency graphs are often hard to access. — [USPTO 11171835](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11171835)
- **Neo4j's "enterprise knowledge layer" series.** It models organizational structure as a graph for enterprise AI, using a fictional bank. — [Neo4j](https://neo4j.com/blog/genai/the-enterprise-knowledge-layer-operating-structure/)
- **LinkedIn.** DataHub serves as a metadata graph, and SQL Bot as a KG-backed assistant (see section 2). — [LinkedIn](https://engineering.linkedin.com/blog/2019/data-hub)

### Inferences
- **Most experience lies with consultancies and graph vendors.** Typical projects are bank inventory, risk and data semantic layers, and they are usually built on RDF triple stores. Developer-portal vendors use property-graph or relational models. Bridging the two worlds (a SKOS glossary plus a Backstage or Port catalog) is a plausible novel contribution.

### Gaps
- No published platform-landscape KG was found at Zalando, Airbnb, Uber, Spotify or the telcos. ITSM ontologies such as ITIL-based ontologies, or CMDB-to-RDF work, were not researched within the budget.

## 5. Failure modes of internal AI assistants

### Takeaway
The documented failure modes are stale or contradictory sources, wrong answers, permission leakage, inability to see live state, availability of the assistant itself, and low trust. Trust is the biggest adoption barrier: developers say they fall back to humans when they do not trust the AI.

### Cited Findings
- **Trust (Stack Overflow 2025 survey).**
  - 46% of developers distrust the accuracy of AI output, up from 31% the previous year. Another summary instead reports trust at 33%, so the figures conflict between summaries.
  - 87% worry about the accuracy of AI agents.
  - Most developers defer to humans when they don't trust AI answers.
  - Sources: [TechRepublic](https://www.techrepublic.com/article/news-developer-trust-in-ai-declines/); [ShiftMag](https://shiftmag.dev/stack-overflow-survey-2025-ai-5653/)
- **Wrong answers.** Uber's agentic-RAG rework was motivated by incorrect advice in security and privacy answers, which it reduced by a relative 60%. Baseline helpfulness was only 48.9%. — [Uber](https://www.uber.com/en-AU/blog/enhanced-agentic-rag/); [InfoQ](https://www.infoq.com/news/2024/10/uber-genie-rag-copilot)
- **Operational failures (GoDaddy).**
  - The assistant itself was down twice in a year, so a fallback route was needed.
  - It cannot detect upstream outages such as GitHub's.
  - Answer quality needs continuous on-call curation.
  - Source: [GoDaddy](https://www.godaddy.com/resources/news/how-we-scaled-platform-support-10x-without-scaling-the-team)
- **Hallucination in RAG over internal docs.** It depends on the chunking strategy and embedding model, according to a University of Twente thesis on Canon Medical docs. — [UTwente thesis](https://essay.utwente.nl/fileshare/file/107394/de%20Jong_BA_EEMCS.pdf)
- **Onboarding assistant at Bosch.** "Bosch Onboarding Buddy" is an agentic-RAG onboarding assistant, evaluated with senior developers (Lund master's thesis, 2026). — [Lund](https://lup.lub.lu.se/student-papers/record/9231368/file/9231374.pdf)
- **Permissions.** Glean mirrors the source systems' access rights in near real time. Its docs say results depend on connector coverage and how source permissions are configured. (Vendor.) — [Glean](https://www.glean.com/product/enterprise-graph)
- **Stale catalog data.** Backstage itself says the catalog is a cache rather than the source of truth, which implies staleness risk — [backstage.io](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph)

### Inferences
- **Mitigations seen in practice:**
  - Live API or catalog grounding for facts that change fast (GoDaddy, Port).
  - Escalation paths that carry the gathered context.
  - Weekly human curation of answers.
  - Ingesting historical Slack Q&A, which captures tacit knowledge but also old, outdated answers.
  - Agentic retrieval with source filtering (Uber).
- **Not addressed by any tool found:** detecting contradictions between overlapping docs, and versioning or dating terms, which matters because platforms change extremely fast. A KG with provenance and validity dates could fill this gap.

### Gaps
- No empirical study turned up that measures how often internal assistants hallucinate internal API names or endpoints.
- No study of incidents where permission leakage occurred in deployed internal assistants turned up.
