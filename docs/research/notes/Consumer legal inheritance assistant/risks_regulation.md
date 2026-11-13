# Risks, Regulatory Constraints and Safeguards: Consumer AI Assistant Explaining Legal (Inheritance/Probate) Documents

Scope: a consumer app where a bereaved layperson uploads or forwards an official inheritance letter (notary, probate court, lawyer) and asks about their role, duties and deadlines. The app answers with an LLM grounded in a legal glossary, ontology or knowledge graph (KG), plus definitions and diagrams. EU and US are the main reference points. Status as of Nov 2026. Search coverage was limited to about 15 tool calls, so some items rest on secondary sources; they are flagged where that applies.

## 1. Accuracy evidence: legal hallucinations, does retrieval/KG grounding help, jurisdiction confusion

### Takeaway
General-purpose LLMs hallucinate heavily on legal questions: 58–88% on verifiable case-law questions in the published Dahl et al. paper. Commercial RAG legal tools, built and sold to lawyers, still hallucinated on 17–33% of queries. Grounding helps but does not remove errors, and many "hallucinations" in RAG systems are really retrieval failures. Local-law and jurisdiction-specific questions perform worse, which matters a lot here because probate law is mostly state/national law.

### Cited Findings
- Dahl, Magesh, Suzgun & Ho, "Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models", *Journal of Legal Analysis* 16(1):64–93 (2024), DOI 10.1093/jla/laae003. On direct, verifiable questions about randomly selected US federal cases, the published version reports hallucination rates of 58% (GPT-4) to 88% (Llama 2). The arXiv preprint gave 69% (GPT-3.5) to 88%; cite the published 58–88% range. — [Stanford summary](https://impact.stanford.edu/article/large-legal-fictions-profiling-legal-hallucinations-large-language-models); [arXiv preprint](https://arxiv.org/html/2401.01301v1)
- The same paper also found that models often fail to correct users' false premises (counterfactual bias) and are poorly calibrated about their own confidence (they "don't know when they don't know"). This is from the paper's abstract and preprint; the exact figures were not re-verified in this pass. — [arXiv](https://arxiv.org/html/2401.01301v1)
- Magesh, Surani, Dahl, Suzgun, Manning & Ho, "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools", *Journal of Empirical Legal Studies* 22(2):216–242 (2025), DOI 10.1111/jels.12413. This was the first preregistered evaluation, using 200+ queries.
  - Lexis+ AI, Westlaw AI-Assisted Research and Ask Practical Law AI hallucinated less than GPT-4 but still did so on 17–33% of queries.
  - Westlaw AI-AR hallucinated about twice as often as the others.
  - The authors conclude that vendor claims of "hallucination-free" RAG are overstated.
  - The query set included jurisdiction- and time-specific questions.
  — [Stanford Law page](https://law.stanford.edu/publications/hallucination-free-assessing-the-reliability-of-leading-ai-legal-research-tools); [PDF](https://nlp.stanford.edu/~manning/papers/Magesh-Hallucination%E2%80%90Free-2025.pdf); [Stanford HAI](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-queries); [RePEc](https://econpapers.repec.org/RePEc:wly:empleg:v:22:y:2025:i:2:p:216-242)
- The Magesh paper defines a hallucination as a response that is either incorrect or "misgrounded", meaning it cites a source that does not support the claim. Misgrounding is the RAG-specific failure that a citation UI can make look trustworthy. — [arXiv 2405.20362](https://arxiv.org/pdf/2405.20362)
- Legal RAG Bench (Isaacus, March 2026) used 4,876 passages from the Victorian Criminal Charge Book and 100 hand-written questions. It concluded that many errors attributed to "hallucination" in legal RAG are in fact retrieval failures. — [Isaacus blog via mirror](https://hn.jakechampion.name/reader/https://isaacus.com/blog/legal-rag-bench); [arXiv 2603.01710](https://arxiv.org/pdf/2603.01710.pdf)
- An August 2026 study of eight legal RAG systems over GDPR text (English) and a French civil-law corpus reportedly found error rates of roughly 10–50% depending on the system. These figures come from secondary coverage and were not verified against the paper. — [papers.cool arXiv 2608.14210](https://papers.cool/arxiv/2608.14210); [ModelWire](https://themodelwire.com/article/legal-rag-systems-still-hallucinate-in-up-to-half-of-responses-01M06R8FV9NQV0BKDFX0T3402R)
- A 2025 "Place Matters" study reportedly found hallucination rates varying by location: Los Angeles 45%, London 55%, Sydney 61%. LexRAG (2025) reportedly reached only 33% best-case retrieval recall in multi-turn conversations, and other 2025 work found hallucinations rise when prompts contain false premises. All of this comes via an LLRX review (Feb 2026) that returned HTTP 403 on fetch; it is unverified at primary level. — [LLRX, Feb 2026](https://www.llrx.com/2026/02/what-the-science-says-about-hallucinations-in-legal-research/)
- Real-world harm signal: Damien Charlotin's database of court decisions involving AI-hallucinated content held 1,981 cases (1,363 US) as of 29 Aug 2026, up from about 1,227 in early 2026 and 1,598 on 9 June 2026. An October 2026 CSV analysis counted 885 US entries involving **pro se litigants** against 587 involving lawyers, so laypeople relying on AI are a large share of the cases. — [HAQQ tracker](https://haqq.ai/blog/ai-legal-hallucination-audit); [Vaquill analysis](https://vaquill.ai/blog/ai-hallucination-sanctions-tracker); [UNC Law Library, June 2026](https://library.law.unc.edu/2026/06/handling-hallucinations-a-reflection/)

### Inferences
- This product does not mainly answer case-law questions. It explains a specific document (the letter) plus terms and deadlines. That makes it a document-grounded plus glossary-grounded task, which is closer to "reading comprehension with legal context" than to open legal research, and it should have lower base error rates. However, the highest-stakes outputs are the riskiest: deadlines, consequences of inaction (e.g., deemed acceptance of an inheritance, or failing to disclaim within a window), and "what is my role". These depend on jurisdiction-specific rules that LLMs get wrong most often.
- Jurisdiction confusion is the signature risk. Examples:
  - US "executor/personal representative" concepts applied to a civil-law "Erbe" (heir) taking by universal succession.
  - Common-law probate processes conflated with notarial succession procedures (e.g., the French notaire, the German Nachlassgericht/Erbschein).
  - Disclaimer deadlines that differ by country and state. Germany's 6-week Ausschlagungsfrist (§1944 BGB) and the US federal 9-month qualified-disclaimer rule (26 U.S.C. §2518) are from general knowledge and should be verified.
- A KG/ontology helps definitions and relationship diagrams, because terms are curated and stable. It does not by itself guarantee correct application to the user's facts. The KG must be jurisdiction-scoped (term + jurisdiction + validity period), or it will smuggle in the wrong-system definition.
- Misgrounding is a UX trap. Showing a citation next to a wrong claim increases trust, so citations need entailment checks.

### Gaps
- No study was found that measures LLM accuracy specifically on consumer explanations of inheritance/probate documents, or on deadline extraction from official letters.
- The "Place Matters" and 8-system RAG figures need primary verification.
- No quantitative evidence was found on whether KG grounding, as opposed to plain-text RAG, reduces legal hallucinations. Claims in vendor blogs were not treated as evidence.

## 2. Legal information vs legal advice (UPL in the US; reserved legal services in the EU) and how products draw the line

### Takeaway
In the US, giving individualized legal advice without a licence is unauthorized practice of law (UPL) in most states. Courts have just confirmed that states may enforce UPL even against free, non-profit, one-to-one advice (*Upsolve v. James*, 2d Cir. 2025). Reform is happening through sandboxes and alternative business structures (Utah, Arizona), not through general deregulation, and Utah's sandbox is winding down. The FTC's DoNotPay action shows that the bigger near-term enforcement risk is consumer-protection claims about "AI lawyer" capability. EU member states vary: Germany's BGH allowed the rule-based Smartlaw generator, but expressly on the basis of schematic handling of typical cases, which leaves generative, individualized advice open.

### Cited Findings
- **FTC v. DoNotPay:** complaint in September 2024 (Operation AI Comply); final order approved 5–0 on 16 Jan 2025 and announced February 2025.
  - The company pays $193,000 and must notify subscribers from 2021–2023.
  - It is barred from claiming the service can substitute for a human lawyer, or similar claims, without competent and reliable evidence.
  - The FTC alleged DoNotPay never tested whether its output matched a human lawyer's and hired no attorneys to check quality.
  - After the order, DoNotPay rebranded as an "AI Consumer Champion" and says it is not a law firm.
  — [FTC](https://www.ftc.gov/node/87474); [MyChesCo summary](https://www.mychesco.com/a/news/national/ftc-cracks-down-on-misleading-ai-robot-lawyer-what-every-consumer-should-know)
- ***Upsolve, Inc. v. James*, No. 22-1345 (2d Cir. 9 Sept 2025), 155 F.4th 133.**
  - The court vacated a preliminary injunction that had shielded a non-profit's trained non-lawyer debt-collection advice from New York's UPL rules.
  - It held the rules regulate speech but are content-neutral, so only intermediate scrutiny applies.
  - A cert petition is pending as No. 25-948, and a March 2026 S.D.N.Y. ruling went against Upsolve on remand (via Volokh Conspiracy).
  - Supreme Court action on cert was not confirmed.
  — [Public Citizen blog](https://clpblog.citizen.org/second-circuit-holds-unlawful-practice-law-can-apply-to-debt-collection-advice/); [SCOTUS docket brief](https://www.supremecourt.gov/DocketPDF/25/25-948/400716/20260312132759863_Upsolve%20v.%20James_Final.pdf); [Volokh, Mar 2026](https://reason.com/volokh/2026/03/08/court-upholds-new-yorks-limits-on-unauthorized-practice-of-law/printer/)
- ***Nippon Life Insurance Co. of America v. OpenAI*** (N.D. Ill., filed March 2026) pleads defamation and UPL against a general chatbot. OpenAI moved to dismiss on 15 May 2026, and no merits ruling was found. It is an early test of whether chatbot output itself can be "practice of law". — [AI Lawsuit Tracker](https://ailawsuittracker.com/issues/openai-unauthorized-law-practice/)
- **US reform status:**
  - Utah's sandbox fell from 39 entrants (2022) to 11 (April 2025) and to 6 regulated entities by August 2026. The Utah Supreme Court's Phase 3 focuses on sunsetting the sandbox (sunset date 14 Aug 2027) and institutionalizing reforms.
  - Arizona's Alternative Business Structure regime has about 136 licences.
  - The NCSC white paper (Aug 2025) proposes sandboxes and narrowing UPL definitions for AI. It notes that no Utah sandbox entity had deployed advanced generative AI.
  - These are secondary summaries; the counts are not verified against the Utah Office of Legal Services Innovation.
  — [NCSC white paper (Aug 2025)](https://www.ncsc.org/sites/default/files/media/document/AI_UPL_WhitePaper.pdf); [Practitioner landscape, Apr 2026](https://ethanbholland.com/2026/04/22/ai-legal-landscape-2026/); [Thomson Reuters Institute, Feb 2026](https://www.thomsonreuters.com/en-us/posts/government/ai-impacts-unauthorized-practice-of-law/); [Utah tracker](https://legalaigovernance.com/tracker/states/utah/)
- Academic proposal to recast UPL for generative AI: Avery, Abril & del Riego, "ChatGPT, Esq.", 26 Yale J.L. & Tech. 64. — [YJoLT PDF](https://yjolt.org/sites/default/files/avery_abril_delriego_26yalejltech64.pdf)
- **Germany:**
  - The BGH (I ZR 113/20, 9 Sept 2021) held that the Smartlaw contract generator is not an unlawful "Rechtsdienstleistung" under the RDG. Commentary stresses that this rests on the algorithm's schematic handling of typical cases and flags open questions for AI that drafts individually evaluative content.
  - Earlier, the BGH in *wenigermiete.de* (VIII ZR 285/18, 2019) allowed legal tech under a debt-collection licence.
  — [LTO](https://www.lto.de/recht/juristen/b/bgh-urteil-izr11320-vertragsgenerator-smartlaw-keine-unzulaessige-rechtsdienstleistung-rak-hamburg-rdg-legal-tech); [Der Betrieb](https://der-betrieb.de/meldungen/das-smartlaw-urteil-des-bgh-siegeszug-der-legal-tech-anwendungen); [Wolters Kluwer](https://www.wolterskluwer.com/de-de/news/bgh-erklaert-dokumentengenerator-smartlaw-fuer-zulaessig)
- ABA Formal Opinion 512 (29 July 2024) applies the existing Model Rules to lawyers using generative AI. Lawyers must:
  - understand tool capabilities and limits;
  - verify output, with the level of review proportionate to the task and tool;
  - protect confidentiality, including informed client consent before inputting client information into some tools.
  It binds lawyers, not consumer apps, but it is relevant if the app refers users to lawyers or partners with firms. — [ABA RPTE, Sept/Oct 2026](https://www.americanbar.org/groups/real_property_trust_estate/resources/probate-property/2026-september-october/artificial-ethics-aba-formal-opinion-512-role-ethics-artificial-intelligence); [FKKS summary](https://technologylaw.fkks.com/post/102jwnl/aba-issues-comprehensive-formal-ethics-opinion-on-lawyers-use-of-generative-ai)

### Inferences
- The usual line products draw is between **general legal information** (what a term means, how the process typically works, what the letter literally says, which authority sent it) and **advice** (applying law to the user's facts to recommend a course of action, e.g., "you should disclaim", "you are liable for the debts"). Inheritance questions push hard toward advice ("Should I accept?", "Do I have to pay the debts?"), so the product must redirect those questions deliberately.
- Defensible design pattern: explain, quote and define; give a neutral overview of options with general consequences and pointers to official sources; never recommend. For decision points (accept/disclaim, deadlines, signing documents), route the user to the notary, court registry, a lawyer or legal aid.
- Marketing language is a separate enforcement vector (FTC Act s.5; EU UCPD). Avoid "AI lawyer", "replaces a notary" or "guaranteed accurate" unless substantiated by testing against lawyers, which DoNotPay never did.
- A lawyer-partnered model (e.g., an Arizona ABS, or a referral to licensed professionals) is the main US path to giving actual advice.

### Gaps
- CCBE guidance on AI (2025) was not retrieved; check ccbe.eu directly.
- No consolidated survey was found of EU member-state legal-advice monopolies as applied to generative AI (e.g., France's reserved "consultation juridique", Austria). The German Smartlaw line is the best-documented example.
- Supreme Court action on *Upsolve* (No. 25-948) and the outcome of *Nippon Life v. OpenAI* are unconfirmed as of Nov 2026.

## 3. Regulation: EU AI Act classification, GDPR, consumer protection, liability, disclaimers

### Takeaway
A consumer-facing explainer of legal letters is most likely **not high-risk** under AI Act Annex III point 8. That point covers AI used **by or on behalf of judicial authorities** (or in ADR) to research and interpret facts and law, not private parties' self-help tools. It is a **limited-risk / Article 50** system: chatbot disclosure has applied since 2 Aug 2026. If it uses a third-party foundation model, the GPAI provider carries the GPAI duties. GDPR is the heavier constraint, because the letter contains third parties' data and potentially special-category data. From 9 Dec 2026, software and AI are "products" under the new EU Product Liability Directive, which raises strict-liability exposure for defective outputs causing damage.

### Cited Findings
- **AI Act text and dates:** Regulation (EU) 2024/1689.
  - Annex III point 8(a) covers "AI systems intended to be used by a judicial authority or on their behalf to assist a judicial authority in researching and interpreting facts and the law and in applying the law to a concrete set of facts, or to be used in a similar way in alternative dispute resolution" (quoted from memory of the Act text; verify on EUR-Lex). — [EUR-Lex AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
  - Secondary commentary on the May 2026 draft guidelines frames point 8 as AI that supports judicial authorities/ADR, including tools that help judges research or apply the law. No source was found that addresses consumer legal-information chatbots. — [Pearl Cohen](https://www.pearlcohen.com/?p=18297); [Wolters Kluwer Arbitration Blog](https://legalblogs.wolterskluwer.com/arbitration-blog/we-still-need-to-talk-about-the-eu-ai-act-and-before-23-july-now-the-draft-high-risk-guidelines-are-here/)
- **Commission draft high-risk classification guidelines** (19 May 2026; consultation to 23 June 2026; non-binding, with the CJEU as final interpreter):
  - Article 6(3) exemptions are read narrowly: a narrow procedural/preparatory task, improving a previously completed human activity, or detecting deviations.
  - There must be no profiling.
  - Providers must document the exemption assessment.
  - Multiple AI components jointly influencing a decision are assessed as one "complex" system.
  — [Jones Day, June 2026](https://jonesday.com/en/insights/2026/06/draft-eu-guidelines-clarify-when-ai-systems-are-highrisk-under-the-ai-act); [Faegre Drinker](https://www.faegredrinker.com/en/insights/publications/2026/5/eu-ai-act-high-risk-systems-european-commission-issues-draft-guidelines)
- **Digital Omnibus on AI** (provisional agreement 6/7 May 2026; Council confirmation 13 May 2026):
  - Annex III high-risk obligations are postponed to **2 Dec 2027**, and Annex I to 2 Aug 2028.
  - Article 50(1) chatbot disclosure is unchanged and applies from **2 Aug 2026**.
  - Article 50(2) watermarking gets a grace period to 2 Dec 2026 for systems placed on the market before 2 Aug 2026.
  - The Article 4 AI-literacy duty is softened to "support" literacy.
  - GPAI duties have applied since 2 Aug 2025 and are unchanged.
  - Formal Official Journal adoption was expected before 2 Aug 2026 but **was not confirmed** in this research.
  — [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines/); [Hogan Lovells](https://www.hoganlovells.com/en/publications/eu-legislators-agree-to-delay-for-highrisk-ai-rules); [Simmons & Simmons](https://www.simmons-simmons.com/en/publications/cmoveo6ke00icuxskpgueb0od/ai-omnibus-update)
- **GDPR and deceased persons:** Recital 27 says the GDPR does not apply to personal data of deceased persons, and member states may provide rules. The result is a national patchwork; some states protect data of the deceased, and professional secrecy (medical, banking) persists regardless. — [GDPR Recital 27](https://gdpr-text.com/de/read/recital-27); [De Miguel Beriain et al.](https://publikationen.ub.uni-frankfurt.de/files/64580/Article_4_Data_of_Deceased_People_DE_MIGUEL+BERIAIN_et_al.pdf)
- **New Product Liability Directive (EU) 2024/2853:**
  - Transposition deadline is **9 Dec 2026**, applying to products placed on the market after that date.
  - Software and AI systems are "products", and AI Act providers are treated as manufacturers.
  - It adds disclosure duties and rebuttable presumptions of defect/causation where technical complexity makes proof excessively difficult.
  - Germany is transposing 1:1 via a new ProdHaftG effective 9 Dec 2026.
  — [CMS](https://cms.law/en/int/publication/the-new-eu-product-liability-directive-eu-2024-2853); [Jones Day, June 2026](https://www.jonesday.com/en/insights/2026/06/the-revised-eu-product-liability-directive-state-of-play-across-eu-member-states-and-evolving-risk-landscape); [Inside Privacy, Aug 2026](https://www.insideprivacy.com/european-union-2/eu-member-states-begin-rolling-out-new-product-liability-rules/)
- **US consumer protection:** FTC Act s.5 deception theory applied to AI legal capability claims (DoNotPay, above). — [FTC](https://www.ftc.gov/node/87474)

### Inferences
- **AI Act classification reasoning:** The intended purpose is to help private individuals understand documents, not to assist a judicial authority or ADR. So Annex III 8(a) should not apply, unless the product is sold to courts, notaries acting in a quasi-judicial capacity, or ADR bodies. Document the intended purpose and the classification rationale in writing, and re-check against the final guidelines. The notary angle needs care: in some civil-law states notaries perform official succession functions, so a version sold *to* notaries for case handling could approach point 8.
- **Article 50(1):** Disclose clearly that the user is interacting with AI. Because the app makes text that explains official documents, consider labelling generated summaries as AI-generated even where 50(2) technically targets synthetic content marking.
- **GDPR:** The deceased's data may fall outside the GDPR depending on the member state, but the letter typically contains **living third parties' data**: other heirs, addresses, birth dates, the notary's file numbers, sometimes the estate's asset and debt details. It may also reveal special categories under Art. 9, e.g., religion via church-tax mentions, or health via cause of death. Implications:
  - lawful basis for processing third-party data (the uploader's legitimate interest vs. third parties' rights);
  - Art. 14 transparency challenges;
  - data minimisation and redaction before sending to the LLM;
  - no training on uploads by default;
  - EU data residency / LLM processor DPAs and transfers;
  - a DPIA is likely warranted (novel tech + vulnerable users + third-party data);
  - short retention.
  EDPB Opinion 28/2024 on AI models (Dec 2024) addresses legitimate interest and anonymity of models. It was not retrieved here; see [EDPB](https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en) (URL from prior knowledge, not fetched).
- **Liability:** Disclaimers are a weak shield. Under the PLD, strict liability cannot be excluded by contract against the injured person. Under EU consumer law, unfair-terms rules limit exclusions. In the US, disclaimers help on the UPL line and on contract claims but do not cure deceptive marketing (FTC). The PLD's damage categories (death/injury, property, data loss) may not cover pure economic loss from a missed inheritance deadline, but national tort and contract law still applies. This last point is my reading; verify with counsel.
- Disclaimer effectiveness is undermined by user behaviour (see section 5): people trust LLM legal advice even when told it is AI.

### Gaps
- The Official Journal publication of the Digital Omnibus was not confirmed, and neither was the final (vs. draft) high-risk guideline text.
- Commission Article 50 transparency guidelines / Code of Practice on AI-generated content labelling: details not retrieved.
- EDPB opinions/guidance and CJEU case law on uploading documents containing third-party data into LLM apps were not retrieved.
- US state AI laws (e.g., Colorado AI Act timing; California chatbot disclosure laws) were not researched in this pass.

## 4. Safeguards: sources, jurisdiction detection, deadlines, abstention, escalation, human review, versioning, audit

### Takeaway
The evidence (RAG still errs 17–33%; retrieval failure is a major error source; misgrounding; jurisdiction variance; false-premise susceptibility) points to a layered design. Ground answers in the letter itself plus a curated, jurisdiction- and time-versioned KG. Confirm jurisdiction explicitly. Treat deadlines as deterministic extraction with mandatory verification, never generation. Abstain and escalate on advice-type or low-confidence questions. Keep audit trails.

### Cited Findings
- RAG reduces but does not eliminate hallucination, and misgrounded citations are a distinct failure mode. — [Magesh et al. 2025](https://law.stanford.edu/publications/hallucination-free-assessing-the-reliability-of-leading-ai-legal-research-tools)
- Retrieval failures drive many legal RAG errors. — [Legal RAG Bench / arXiv 2603.01710](https://arxiv.org/pdf/2603.01710.pdf)
- LLMs accept false premises and are poorly calibrated, so their self-reported confidence is unreliable. — [Dahl et al. 2024](https://arxiv.org/html/2401.01301v1)
- The FTC treated the absence of testing against lawyers and the absence of attorney quality review as central to deception. — [FTC](https://www.ftc.gov/node/87474)
- ABA 512's verification principle: review proportional to risk. — [FKKS](https://technologylaw.fkks.com/post/102jwnl/aba-issues-comprehensive-formal-ethics-opinion-on-lawyers-use-of-generative-ai)

### Inferences (design safeguards, brainstorming level)
- **Authoritative sourcing:**
  - Every substantive claim links to (a) the exact span of the user's letter, and/or (b) a versioned source: statute section, official court/notary chamber page, government guidance.
  - Run an entailment check that the cited span actually supports the claim, to counter misgrounding.
  - Show "not found in your letter" explicitly.
- **Jurisdiction:**
  - Detect candidate jurisdiction from sender, letterhead, language, court names and statute references, then **ask the user to confirm** before any jurisdiction-specific content.
  - Store jurisdiction (and, for cross-border estates, the EU Succession Regulation 650/2012 habitual-residence question, from general knowledge) as context.
  - Scope every KG node and edge by jurisdiction and validity period.
  - Refuse to mix systems; flag cross-border cases for professional help.
- **Deadlines ("never miss, never invent"):**
  - Extract dates and periods from the letter with a deterministic/structured parser plus an LLM, and display the **verbatim source text** next to each one.
  - Distinguish deadlines **stated in the letter** from **statutory deadlines** that might apply. Show the latter only from curated KG rules, with "how it starts running" (e.g., from knowledge of the inheritance or from service of the letter), and say explicitly that the calculation depends on facts the app cannot verify.
  - Never compute a final date silently. Show the calculation and tell the user to confirm it with the sender or a professional.
  - Calendar export only after the user acknowledges this.
  - Red-team the "no deadline mentioned" case: the app must say "the letter doesn't state a deadline; one may still apply under law".
- **Confidence and abstention:**
  - Use classifier-based routing (definition / document-reading / process overview / advice / emergency) rather than the LLM's own confidence.
  - Abstain on advice questions and on any question the KG lacks coverage for.
  - Prefer "I don't know, here is who to ask" over a guess.
- **Escalation and referral:**
  - Context-specific handoff to the sender of the letter (notary, court registry, probate clerk), legal aid, bar referral services, and grief/financial-hardship resources.
  - Prepare a "questions to ask your notary/lawyer" sheet and a structured summary the user can bring along. This is high value and low risk.
- **Human review:**
  - Lawyer-curated KG and templates per jurisdiction.
  - Periodic expert evaluation on a golden set of real (anonymised) letters, with published error rates (FTC substantiation).
  - Optional paid lawyer review tier via licensed partners (the US ABS/referral model).
- **Versioned legal content:**
  - Bitemporal KG: valid-time of the law plus record-time of curation.
  - Show the "law as of" date and the source version.
  - Monitor legislative changes and set expiry/re-review dates per node.
  - Apply the rules in force at the date of death where relevant (an inheritance-specific temporal rule; general knowledge, verify per jurisdiction).
- **Audit logs:** Log the inputs (redacted), retrieved sources and versions, model/version, prompts, outputs, the user's jurisdiction confirmation and disclaimers shown. This supports PLD disclosure obligations, complaint handling and quality monitoring. Balance it against GDPR minimisation through pseudonymisation and retention limits.
- **Marketing and claims hygiene:** Avoid "lawyer" language and substantiate accuracy claims with testing (DoNotPay lesson).

### Gaps
- No empirical study was found that evaluates these specific safeguards (jurisdiction confirmation, deadline verbatim display) in consumer legal tools. These are reasoned design proposals, not evidence-backed results.

## 5. Ethical and UX risks with bereaved users: over-reliance, automation bias, emotional sensitivity, accessibility

### Takeaway
Laypeople are more willing to act on LLM legal advice than on lawyers' advice, and disclosing that it is AI did not reduce that trust (CHI 2025). A grieving, time-pressured user is especially prone to automation bias. Safeguards must work by design (friction at decision points, verbatim evidence, prompts to verify), not by disclaimers alone. Pro se litigants already make up a large share of the AI-hallucination court cases.

### Cited Findings
- Schneiders, Krook, Seabrooke et al., "Objection Overruled! Lay People can Distinguish Large Language Models from Lawyers, but still Favour Advice from an LLM" (CHI 2025; 288 participants, 3 experiments):
  - Participants were more willing to act on LLM-generated advice than lawyer advice when the source was unknown.
  - When sources were disclosed, trust in the AI did not decrease.
  - Participants could distinguish sources only slightly above chance (AUC about 0.59).
  - The authors suggest the LLM's more complex language may drive preference.
  — [arXiv 2409.07871](https://arxiv.org/html/2409.07871v2); [Southampton eprints](https://eprints.soton.ac.uk/494609/); [The Conversation via Cyprus Mail](https://cyprus-mail.com/2025/04/30/people-trust-legal-advice-generated-by-chatgpt-more-than-a-lawyer-new-study)
- A 2026 study (Durham Law School, arXiv 2607.05680) reportedly found that attributing advice to AI did not change evaluations, but AI-attributed advice was perceived as more objective. This was not verified at primary level. — [alphaXiv 2607.05680](https://www.alphaxiv.org/abs/2607.05680)
- Pro se litigants account for 885 US entries in the hallucination case database, against 587 for lawyers (Oct 2026). — [Vaquill](https://vaquill.ai/blog/ai-hallucination-sanctions-tracker)

### Inferences
- **Over-reliance mitigations:**
  - Show the letter's own words beside every explanation.
  - At high-stakes junctions (accept/disclaim, signing, paying debts, deadlines), insert a "this is a decision, please confirm with X" interstitial.
  - Avoid authoritative tone. Use plain language: since complex language raised trust in the CHI study, simpler, hedged language may calibrate trust better (hypothesis).
- **Emotional sensitivity:**
  - Use a trauma-informed tone; no upbeat chatbot persona.
  - Let users pause and save.
  - Avoid unsolicited estimates of value or debt.
  - Handle family-conflict signals (disputes between heirs) by referring out rather than taking sides.
  - Signpost bereavement support.
  - Be careful with the deceased's sensitive data, and never surface it gratuitously in diagrams.
- **Vulnerability:**
  - Bereaved users are vulnerable consumers in the EU UCPD sense. No upselling under time pressure, and no dark patterns around "urgent deadline" fear.
  - Elderly users, non-native speakers and low legal literacy argue for multilingual output with the original-language legal term preserved (terms often don't translate across systems), plain-language levels and screen-reader-compatible diagrams. EU Accessibility Act obligations for consumer e-services have applied since June 2025 (from general knowledge; not verified here).
- **Equity:** Such tools can improve access to justice for people who cannot afford a lawyer. The same population is the most exposed to errors, so errors are regressive.

### Gaps
- No study was found specifically on bereaved users and AI legal/administrative assistants, or on grief and automation bias.
- The applicability of the European Accessibility Act to this product type was not verified in this pass.
