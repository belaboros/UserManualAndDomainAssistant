# Legal glossaries, taxonomies, ontologies and KGs for a jurisdiction-agnostic succession assistant (as of Nov 2026)

Scope note: brainstorming-level research. About 18 search/fetch calls. Statements of law are given as illustrations for the data model, not as legal advice, and should be re-verified against primary sources before any product use.

## Q1. What existing legal ontologies and vocabularies are relevant to succession, and what are their licenses and maintenance status?

### Takeaway
No reusable open ontology specific to probate or succession turned up. The practical toolkit is a stack of parts. Two upper/core legal ontologies supply roles, actions, norms and rights: LKIF Core, now CC BY 4.0, and UFO-L. FOLIO (CC BY 4.0, 18k+ concepts) supplies a broad, practice-oriented legal taxonomy. EU-level vocabularies supply identifiers and multilingual labels: EuroVoc, IATE, ELI and ECLI. LegalRuleML can encode deontic rules such as "must disclaim within X weeks". The EU Succession Regulation 650/2012, the e-Justice per-country fact sheets and the European Certificate of Succession (ECS) form are the best ready-made, cross-jurisdiction scaffold for the domain content itself.

### Cited Findings

**LKIF Core (Estrella project, 2006-2008; Hoekstra et al.)**
- Organised as modules. Abstract: top, place, mereology, time. Basic: process, role, action, expression. Legal: legal-action, legal-role, norm. Framework: modification, rules. "LKIF Core" imports abstract+basic+legal, and "LKIF Extended" adds the framework modules — [GitHub RinkeHoekstra/lkif-core](https://github.com/RinkeHoekstra/lkif-core)
- The legal-action module covers public acts, public bodies, and legal and natural persons. Release notes mention Act_of_Law, Assignment, Decision, Delegation, Mandate and Transaction. legal-role adds legal professions. The norm module includes "a typology of rights and powers" and treats legal documents and customary law as legal sources. The README excerpt names no explicit Obligation class — [GitHub lkif-core](https://github.com/RinkeHoekstra/lkif-core)
- License: a LICENSE file (CC BY 4.0) was added in a 2026-02-23 release that also generated Turtle versions. The last substantive ontology release is v1.1 (2008-07-22) — [GitHub lkif-core](https://github.com/RinkeHoekstra/lkif-core). A 2007 announcement had stated LGPL — [W3C semantic-web list, Feb 2007](https://lists.w3.org/Archives/Public/semantic-web/2007Feb/0012.html). The 2026 CC BY 4.0 file supersedes it.
- Background — [Wikipedia: Legal Knowledge Interchange Format](https://en.wikipedia.org/wiki/Legal_Knowledge_Interchange_Format); [LKIF Core paper (UvA DARE)](https://dare.uva.nl/id/bd48bad5-d85f-4576-842c-2ff4c128a811)

**UFO-L (Griffo, Almeida, Guizzardi; NEMO/UFES)**
- A core ontology of legal concepts, layered on the Unified Foundational Ontology and based on Hohfeld's fundamental legal concepts and Alexy's theory of constitutional rights. Its key idea is to model legal relations as UFO *relators* — [NEMO UFO-L project page](https://nemo.inf.ufes.br/en/projetos/ufo-l/); [Griffo et al. 2015, SciTePress](https://www.scitepress.org/Papers/2015/56477)
- A 2016 pattern paper gives a taxonomy of legal relators: rights to something, liberties and powers — [NEMO 2016 pattern paper (PDF)](https://nemo.inf.ufes.br/wp-content/papercite-data/pdf/a_pattern_for_the_representation_of_legal_relations_in_a_legal_core_ontology_2016.pdf)
- License and maintenance status were not found (see Gaps).

**FOLIO (Federated Open Legal Information Ontology; ALEA Institute; successor to SALI LMSS)**
- More than 18,000 concepts, each with its own IRI, in `FOLIO.owl`. Data is CC BY 4.0 and code is MIT. Translations are offered for the "ten most common languages". Stated use cases are contract management, case management, generative AI, legal research and compliance. The repo page shows 35 commits, no releases, and docs marked "coming soon" — [GitHub alea-institute/folio](https://github.com/alea-institute/folio)
- SALI LMSS: `LMSS.owl` is described as SALI's primary taxonomy, with more than 11,000 tags. Prior versions were MIT — [SALI LMSS mirror](https://github.imc.re/sali-legal/LMSS)
- The FOLIO README says nothing about estates, probate, trusts or wills. LMSS/FOLIO is known to include area-of-law and actor/player branches, but this was not verified in this session (see Gaps).

**LegalRuleML (OASIS)**
- LegalRuleML Core Specification v1.0 became an OASIS Standard on 30 Aug 2021 (announced 28 Sep 2021). Editors: Palmirani, Governatori, Athan, Boley, Paschke, Wyner — [OASIS announcement](https://www.oasis-open.org/?p=7649); [Spec PDF](https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/legalruleml-core-spec-v1.0.pdf)
- It models deontic operators (obligations, permissions, prohibitions, rights), defeasible rules, override rules, temporal parameters for rule validity, and jurisdiction metadata. It is built on Consumer RuleML 1.02 with XML Schema/Relax NG — [OASIS announcement](https://www.oasis-open.org/?p=7617)
- An EU specialisation exists — [Interoperable Europe, "A LegalRuleML specialisation" (2024)](https://interoperable-europe.ec.europa.eu/sites/default/files/news/2024-07/A%20LegalRuleML%20specialisation.pdf)

**ELI / ECLI**
- ELI is an OWL ontology and metadata model for legislation, based on FRBR. The Publications Office publishes the OWL file, metadata tables and an alignment with the schema.org legal extension. Its four pillars are identifiers, metadata/ontology, website integration and a sync protocol. Extensions are ELI-DL (draft legislation) and ELI-I (impact) — [EU Vocabularies: ELI](https://op.europa.eu/it/web/eu-vocabularies/eli); [Interoperable Europe: ELI ontology](https://interoperable-europe.ec.europa.eu/collection/iopeu-monitoring/solution/european-interoperability-framework-eif-toolbox/solution-eli-ontology)
- Wikipedia lists v1.4 as the latest version and the ELI Task Force as governance (a secondary source) — [Wikipedia: ELI](https://en.wikipedia.org/wiki/European_Legislation_Identifier)
- For the assistant, ELI/ECLI are useful only as stable citation anchors. For example, "§ 1944 BGB" or "Reg. 650/2012 Art. 4" in a letter can be linked to an identifier. They are not concept models.

**EuroVoc**
- Concept 3936, "law of succession" (FR "droit successoral", NL "erfrecht"), created 1995-10-02, appears under the property domain. The Czech alternative labels include "dědění ze zákona" (intestate succession) and "dědění ze závěti" (testamentary succession) — [EuroVoc 3936 (ONKI Light mirror)](https://light.onki.fi/eurovoc/en/page/3936?clang=de)
- False-friend hazard inside EuroVoc: concept 8456, "succession of States", belongs to public international law and has nothing to do with inheritance — [EuroVoc 8456](https://light.onki.fi/eurovoc/en/page/8456)
- STW (the ZBW economics thesaurus) maps "Erbrecht" to the EuroVoc concept "inheritance" as a *near* match, not an exact one — [ZBW STW Erbrecht](https://zbw.eu/stw/version/latest/descriptor/16029-3/about)
- EuroVoc is too coarse for "who-is-who" or deadlines. It works as a top-level subject tag and as a multilingual anchor.

**EU Succession Regulation 650/2012 + ECS + e-Justice**
- Applies to successions opened from 17 Aug 2015 in all EU member states except Denmark and Ireland. Under Art. 4, the courts of the deceased's last habitual residence have jurisdiction over the whole succession. The applicable law defaults to the law of habitual residence unless a choice of law was made. Substantive succession law stays national — [e-Justice: Succession](https://webgate.ec.europa.eu/e-justice/380/EN/succession); [EUR-Lex summary](https://eur-lex.europa.eu/summary/EN/jl0070)
- The ECS is optional and issued by the authority dealing with the succession. Its forms are fixed by Implementing Reg. 1329/2014, and it is recognised in all member states without further procedure. The e-Justice portal lets users fill form V online — [e-Justice: European Certificate of Succession](https://webgate.ec.europa.eu/e-justice/478/EN/european_certificate_of_succession); [e-Justice online forms](https://online-forms.e-justice.europa.eu/node/16_en)
- e-Justice provides structured per-member-state fact sheets on succession, the judicial atlas (competent authorities) and "adapting rights in rem". Example pages for Hungary: [succession/hu](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/succession/hu_en), [judicial atlas/hu](https://e-justice.europa.eu/topics/taking-legal-action/european-judicial-atlas-civil-matters/succession/hu_en), [adapting rights in rem/hu](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/adapting-rights-rem/hu_en)
- Design implication: the ECS form fields are an EU-agreed, multilingual, jurisdiction-neutral schema. They cover the deceased, the applicant, heirs and their shares, legatees, executors/administrators and their powers, and the assets allocated. That makes them a strong seed for the core model's attributes.

**Probate/estate-specific ontologies**
- A search for an OWL/KG ontology of probate, wills or inheritance found no published one. Nearby resources are DBpedia "Probate" ([DBpedia](https://dbpedia.org/page/Probate)), the visual "WTE Knowledge Maps" of wills/trusts/estates topics ([WTE Knowledge Maps](https://maps.willstrustsestates.info/)) and genealogy glossaries ([raogk probate terms](https://raogk.org/probate-records/terms/)).

### Inferences
- Recommended layering: (1) a small hand-built **succession core** (roughly 60-150 concepts) aligned to LKIF Core / UFO-L for roles, acts, norms and rights; (2) **FOLIO IRIs** as cross-references for generic legal actors, document types and areas of law (CC BY 4.0, so attribution is needed); (3) **EuroVoc/IATE IDs** for multilingual labels; (4) **ELI/ECLI** for citations; (5) **LegalRuleML-style** (or simpler JSON) encoding of duties and deadlines per jurisdiction module.
- LKIF Core is effectively frozen (2008 content) but newly licensed CC BY 4.0, which makes it legally reusable as an alignment target. Expect to cite it, not to depend on a maintained upstream.
- The ECS form plus the e-Justice fact sheets amount to an existing, official "jurisdiction module template" for all EU member states (except DK/IE) and are probably the highest-value content source for the EU part.

### Gaps
- UFO-L license and availability as OWL/OntoUML files: not found.
- How deep FOLIO goes into succession (e.g., whether it has classes such as Executor, Heir, Probate Court, Will, or an "Estates & Trusts" area of law): the README does not say. The OWL file needs inspecting.
- Recent FOLIO commit dates and the SALI→FOLIO governance relationship (2024-2026) were not verified.
- ECLI ontology details were not researched separately.
- No source found for a US-specific open probate vocabulary (e.g., Uniform Probate Code terms as linked data).

## Q2. How should a jurisdiction-agnostic core (roles, stages, documents, duties, deadlines, rights, assets/debts) be modelled, and how do jurisdiction modules specialise and map to it?

### Takeaway
The core should be organised around *functions*, not legal titles: "person who is called to inherit", "person who manages/winds up the estate", "authority that certifies heirship", "proof-of-heirship document", "disclaimer act + deadline". Jurisdictions differ structurally, not just lexically. Civil-law systems transfer the estate to heirs automatically (ipso iure, universal succession), with notaries or probate courts certifying it. Common-law systems vest the estate in a personal representative (executor/administrator) who winds it up under a court grant. Because of this, jurisdiction modules must map to the core with typed relations (exact, close, broad/narrow, related, "no equivalent"), never with one-to-one labels.

### Cited Findings

**Civil-law illustration: Hungary (notary-led, ipso iure)**
- Probate is run by the **notary**, whose procedure "shall have the same effect as that of the court of first instance" (Act XXXVIII of 2010). The territorially competent notary also has exclusive competence for supplementary procedures — [njt.hu Act XXXVIII/2010 (EN)](https://njt.hu/jogszabaly/en/2010-38-00-00)
- Stages: (1) an **inventory proceeding** by an inventory official at the local mayor's office; (2) a **notary proceeding** (ex officio, checks the National Register of Wills, usually a hearing); (3) an optional **allocation agreement** among heirs; (4) a **grant of probate** issued by the notary, which can be appealed to the regional court and becomes final. Once final, it is forwarded to the land and other registers. Disputes go to court, not the notary, and heirs cannot choose the notary — [e-Justice: Succession – Hungary](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/succession/hu_en)
- Succession is **ipso iure** at death, so acceptance is not required. A waiver may be oral or written and must reach the notary. It takes effect retroactively to the date of death. The grant is **declaratory** — ownership passes at death — [e-Justice: Succession – Hungary](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/succession/hu_en)
- Debt liability is **limited**: cum viribus (from estate assets) and then pro viribus (own assets up to the estate's value). The ranking is burial costs → estate/probate costs → the deceased's debts → reserved-share claims → legacies. Two legacy types exist: legatum vindicationis (direct transfer) vs legatum damnationis (a claim against the heir). An executor named in a will does not replace the notary — [e-Justice: Succession – Hungary](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/succession/hu_en)
- The same page notes a one-year window to contact the notary if a fact not dealt with in the procedure (e.g., a newly found will) changes the order of succession — [e-Justice HU judicial atlas](https://e-justice.europa.eu/topics/taking-legal-action/european-judicial-atlas-civil-matters/succession/hu_en)

**Civil-law illustration: Germany (court-led certification, short disclaimer deadline)**
- § 1944 BGB: the **disclaimer (Ausschlagung) period is six weeks**. It starts when the heir learns that the estate has devolved to them and why they are called to inherit. If it is missed, the inheritance counts as accepted — [gesetze-im-internet.de § 1944 BGB](https://www.gesetze-im-internet.de/bgb/__1944.html); [german-probate-lawyer.com: Disclaiming](https://www.german-probate-lawyer.com/publications/detail/disclaiming-an-inheritance-under-german-law-1917.html)
- The period is six months if the deceased's last residence was only abroad or the heir was abroad when the period began. This was stated by secondary sites ([smart-rechner.de](https://www.smart-rechner.de/erbausschlagung/rechner.php)) and should be verified against § 1944(3) itself.
- Form: a declaration recorded at the Nachlassgericht (probate court) or a notarially certified declaration. A disclaimer can be contested within six weeks (§ 1954) — [ra-kotz.de](https://www.ra-kotz.de/erbe-ausschlagen-frist-kosten-haeufige-fehler.htm) (secondary)
- Model implication: a **Deadline** needs a duration, a *trigger event* (knowledge of devolution, not the date of death), *conditional variants* (residence abroad) and a *default consequence* (deemed acceptance). The HU vs DE contrast (no fixed statutory deadline found for HU vs six weeks in DE) shows that deadlines must live in jurisdiction modules.

**Common-law illustration: England & Wales (personal representative + grant)**
- The Probate Registry issues a **grant of probate** to executors named in a valid will; **letters of administration with will annexed** if no executor can act; and **letters of administration** on intestacy — [AvMA guide](https://www.avma.org.uk/resource/applying-for-probate-or-letters-of-administration/)
- Applications are made online via MyHMCTS or on paper, and the grant usually arrives within ~12 weeks — [gov.uk: After you've applied](https://www.gov.uk/applying-for-probate/after-youve-applied); [gov.uk practitioner guidance](https://www.gov.uk/guidance/apply-for-probate-on-paper-as-a-practitioner). An older AvMA guide says ~4 weeks, which conflicts; gov.uk is more authoritative.

**False friends / non-equivalence**
- "Executor" vs "Testamentsvollstrecker": powers and duties are similar but not identical. In common law the executor is a core figure in every testate estate, whereas in German law the Testamentsvollstrecker is an optional add-on used e.g. for quarrelling or minor heirs — [crosschannellawyers.co.uk](https://www.crosschannellawyers.co.uk/?p=353); [haufe.de Länderüberblick](https://www.haufe.de/id/beitrag/9-testamentsvollstreckung-iv-laenderueberblick-HI15502131.html)
- German courts applying German succession law to an English will often hold that naming only an "executor" did *not* intend a German Testamentsvollstrecker, whereas "executor and trustee" is more often read as intending one — [crosschannellawyers.co.uk](https://www.crosschannellawyers.co.uk/?p=353)
- German sub-types such as Verwaltungsvollstrecker ("administrative executor") and Dauertestamentsvollstrecker ("durable/extended executor") have no direct English counterpart — [german-probate-lawyer.com glossary](https://www.german-probate-lawyer.com/en/glossary/def/durable-executor.html)
- Translator forums treat the executor ↔ Testamentsvollstrecker translation as problematic — [ProZ KudoZ](https://mlt.proz.com/kudoz/4098763)
- "Grant of probate" is used in English e-Justice text for the Hungarian notary's final order, which has a different legal nature: declaratory, issued by a notary, with ownership already passed at death. In England the grant is constitutive of the PR's authority to deal with the estate — [e-Justice HU](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/succession/hu_en); [AvMA](https://www.avma.org.uk/resource/applying-for-probate-or-letters-of-administration/)
- A Hungarian/German *notary* (közjegyző/Notar) is a public-office lawyer who can conduct probate as a quasi-court ([njt.hu](https://njt.hu/jogszabaly/en/2010-38-00-00); [Notaries of Europe – Hungary](https://www.notariesofeurope.eu/en/faq1/authentic-acts-in-europe/hungary)). That differs from a US "notary public", who certifies signatures. This contrast is common knowledge and was not separately sourced here.

### Inferences
- **Core role classes**, defined functionally, with Hohfeld/UFO-L-style relators carrying the duties and rights:
  - Deceased.
  - Successor, with subtypes Heir (universal, share of the whole) and Legatee (specific item or claim).
  - ForcedShareClaimant (reserved share / Pflichtteil / kötelesrész; elective share in the US).
  - EstateManager, with subtypes TestamentaryExecutor, CourtAppointedAdministrator, and EstateCurator/Nachlasspfleger.
  - CertifyingAuthority (probate court, notary, registry), DisputeAuthority (court), Creditor, LegalRepresentativeOfMinor (guardian), Advisor (lawyer), InventoryOfficial, RegisterKeeper (land registry, will register).
- **Core process model**: Death → (opening/notification) → Will search & opening → Inventory/valuation → Determination of successors → [Acceptance | Disclaimer window] → Debt settlement → Certification (grant / Erbschein / HU grant of probate / ECS) → Distribution/registration → (Disputes, supplementary proceedings). Each jurisdiction module marks stages as present, absent, merged or reordered, and attaches the actor responsible.
- **Duties and deadlines** should be modelled as a Norm/Obligation with: bearer role, action, trigger event, duration, conditional extensions, consequence of non-compliance, legal source (ELI/ECLI or section citation) and a confidence/verification date. LegalRuleML can be the export format, but JSON-LD with these fields is enough for a layperson Q&A layer.
- **Mapping relations**: use SKOS (exactMatch / closeMatch / broadMatch / narrowMatch / relatedMatch) between jurisdiction concepts and core concepts, plus a custom `falseFriendOf` annotation with an explanation text. Example: `uk:Executor skos:broadMatch core:EstateManager`; `de:Testamentsvollstrecker skos:broadMatch core:EstateManager`; `uk:Executor ex:falseFriendOf de:Testamentsvollstrecker`. Never assert that they are equivalent.
- **Structural switch per module**: a module-level property `transferMode ∈ {ipsoIureToHeirs, viaPersonalRepresentative, acceptanceRequired}` drives which explanations, duties and diagrams apply. For example, "do I need to accept?" gets a different answer in HU/DE vs some Romanistic systems (acceptance required) vs UK (PR administers first).
- For the letter-explainer use case: extract entities from the letter → link them to jurisdiction-module concepts → walk up to core concepts → explain them in plain language → show roles and deadlines relevant to "you" as the recipient's likely role (e.g., a statutory heir as a child of the deceased).

### Gaps
- No academic paper found that proposes a formal comparative succession ontology. A comparative-law scholarship search (e.g., Max Planck "Encyclopedia of Private Law", the ECS form literature) could fill this.
- The Hungarian disclaimer deadline was not stated on the e-Justice page. It needs checking in the Hungarian Civil Code (Ptk.) and the probate act.
- The US (Uniform Probate Code, state variation) was not researched in this session.
- The six-month extension in German § 1944 was not verified against the statute text.

## Q3. How reliable is multilingual terminology (same concept across languages, IATE reliability, legal translation pitfalls)?

### Takeaway
IATE and EuroVoc give multilingual labels and EU-level IDs, but a matching label does not mean the concepts are equivalent. IATE reliability stars are partly auto-assigned, and legal terms are system-bound (e.g., the English term in an EU text is often a descriptive equivalent for a national institution). The assistant should store per-jurisdiction concepts with their native-language term as primary. EU translations should be secondary labels with provenance, and the assistant should not translate a term without saying which legal system it belongs to.

### Cited Findings
- IATE reliability measures how well a term matches the anchor-language concept and how reliable the sources are. The levels run from "not verified" up to 3 stars ("reliable") and 4 stars ("very reliable"); 4 stars requires manual terminologist assessment — [IATE online help: reliability](https://online-help.iate.europa.eu/?p=5325)
- IATE warns that 3-star reliability was **automatically assigned** to many entries when the source databases were merged, so some "reliable" terms do not meet the criteria — [IATE online help](https://online-help.iate.europa.eu/?p=5325)
- A Rijeka study benchmarked legal term translations against IATE. It cautions that a non-IATE variant is not necessarily wrong, since legal terminology varies across texts and contexts — [Hrčak (srce.hr) paper](https://hrcak.srce.hr/file/468046)
- A LETRINT-related study reports low adherence to IATE recommendations for certain EU terms (22.58% for one term) — [OAPEN chapter](https://library.oapen.org/bitstream/id/5d3e70b2-cb91-4f2a-bf75-3c758a66eceb/9780429264894_10.4324_9780429264894-10.pdf)
- A Latvian study argues that electronic term databases help less with domain-specific legal terminology, which needs precision — [Baltic Journal of English Language, Literature and Culture](https://journal.lu.lv/bjellc/article/download/101/86/153)
- Concrete examples of mismatches: EuroVoc "Erbrecht" ↔ "inheritance" is a near match, not an exact one ([ZBW STW](https://zbw.eu/stw/version/latest/descriptor/16029-3/about)). The executor/Testamentsvollstrecker non-equivalence ([crosschannellawyers](https://www.crosschannellawyers.co.uk/?p=353)). "Grant of probate" used for the Hungarian notarial decision ([e-Justice HU](https://e-justice.europa.eu/topics/family-matters-inheritance/inheritance/succession/hu_en)).
- A third-party "IATE API" page claiming that all 2.4M terms are 4-star contradicts IATE's own documentation and should be disregarded — [pauhu-eu.pages.dev](https://pauhu-eu.pages.dev/docs/iate-api) vs [IATE help](https://online-help.iate.europa.eu/?p=5325)

### Inferences
- Use IATE as a *candidate generator* for labels and synonyms, filtered by reliability ≥3 and by legal domain, and then human-curate the result for the succession core. Record the IATE ID, stars and retrieval date as provenance.
- The e-Justice fact sheets and the ECS form exist in all EU languages and were drafted by national contact points, so they are probably better parallel sources for national succession terms than generic dictionaries. This inference is based on the official status of the pages and was not tested empirically here.
- UX rule: show the original-language term from the letter (e.g., "hagyatékátadó végzés"), its jurisdiction-specific explanation, then "closest English concept: … (not identical because …)".

### Gaps
- No quantitative study found on IATE accuracy specifically for succession terms.
- IATE licensing/API terms for commercial reuse were not checked in this session (IATE data is downloadable, but the terms were not verified here).

## Q4. What evidence exists of legal KGs/ontologies built for citizen-facing legal information?

### Takeaway
Evidence for citizen-facing legal *knowledge-structure* tools is small but positive. JusticeBot, a deployed, expert-authored decision-tree/knowledge tool for Quebec housing law, is the best-documented example. Graph-based legal information is argued to improve accessibility, as in the Austrian legal KG built on ELI. The literature also documents the gap between how laypeople describe *events* and how the law frames *issues*. That gap is exactly what a succession assistant must bridge when interpreting a letter.

### Cited Findings
- **JusticeBot** (Westermann et al., Cyberjustice Lab, Montréal; ICAIL 2023) guides a layperson through legal criteria, then gives legal information, outcomes of similar cases and next steps. The first deployed version (landlord-tenant, Quebec) has been used by thousands of people. In the authors' own user survey, over 60% said it gave them an understanding of their situation and next steps — [arXiv 2308.02032](https://arxiv.org/pdf/2308.02032)
- A comparison of ChatGPT vs JusticeBot (Tan, Westermann, Benyekhlef) found that ChatGPT "does not always provide accurate and reliable information" but is a powerful, intuitive interface for laypeople. The paper proposes evaluating the whole legal-information process, not just accuracy — [CEUR-WS Vol-3435 short2](https://ceur-ws.org/Vol-3435/short2.pdf)
- Laypeople perceive their situation through facts and events, and mapping these to legal issues is a core limitation of self-help tools — [CEUR-WS Vol-3441 paper5](https://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3441/paper5.cermine)
- A WU Vienna legal knowledge graph (built on ELI and the Austrian RIS) argues that graph-structured legal information increases accessibility "for all citizens" — [SEMANTiCS: A legal knowledge graph for improved law accessibility](https://2022-eu.semantics.cc/node/3158); [Semantics 2019 paper PDF](https://2020-eu.semantics.cc/sites/2020-eu.semantics.cc/files/3.5%20Semantics2019_improved_law_accessibility.pdf); see also [The Linked Legal Data Landscape](https://penni.wu.ac.at/papers/AIandLaw%20The%20Linked%20Legal%20Data%20Landscape.pdf)
- Ontology-based linked data of Brazilian appellate decisions is aimed at citizens and jurists — [CEUR-WS Vol-3564 paper6](https://ceur-ws.org/Vol-3564/paper6.pdf)
- The EU e-Justice Portal itself is an official citizen-facing, multilingual, per-country structured information service on succession, plus an online ECS form-filling tool — [e-Justice succession](https://webgate.ec.europa.eu/e-justice/380/EN/succession); [online forms](https://online-forms.e-justice.europa.eu/node/16_en)
- A curated list of legal ontologies is useful for further scouting — [Liquid Legal Institute: Legal-Ontologies](https://github.com/Liquid-Legal-Institute/Legal-Ontologies)

### Inferences
- The JusticeBot pattern (expert-authored criteria + LLM interface) maps well onto a hybrid design: a curated succession KG/rules core for the facts, roles and deadlines, with an LLM for letter parsing and plain-language explanation. The ChatGPT comparison supports keeping legally load-bearing content (deadlines, who must act) in the curated layer rather than generated.
- The event→issue gap means the assistant's entry point should be the *letter's events and documents* ("you are summoned to a probate hearing"), mapped to stages in the process model, rather than abstract doctrine.

### Gaps
- No deployed citizen-facing tool found that is specifically for *succession/probate* and backed by an ontology or KG. Commercial probate chatbots may exist but were not surveyed.
- No independent (non-author) evaluation of JusticeBot found.
- Germany-specific Rechtsinformatik projects for citizens (e.g., state-run legal-tech) and UK legal-aid knowledge bases were not covered in this session.
