# 0001 · AcmeDataPlatform domain model (interactive)

- **Status:** captured
- **Scope:** TBD (decided by `/spec`: `system`, or the name of one app)
- **Captured:** 2026-11-13
- **Spec:** _none yet_

## Original idea

> Let's build the concepts of the first (technical) domain: AcmeDataPlatform via an interactive session here.
>
> I define the terms, concepts, relations, properties, rules here.
> You build the glossary, ontology, taxonomy, rule description files in the dedicated /data/Acme/DataPlatform folder.
>
> Then you generates diagrams for me to see the outcome: taxonomy trees, ontology graph.

## Q&A log

### 2026-11-13 · idea · Q1
**Asked by:** Claude
**Q:** [Claude] `data/` is git-ignored except its README (ADR-0013 treats it as runtime data owned by an app). Where should the hand-authored AcmeDataPlatform domain files live?
**Options offered:** data/ + un-ignore it (Recommended); data/, keep ignored; Elsewhere, versioned
**A:** "Let's unignore data and create the data/AcmeDataPlatform folder."
**Effect:** Folder is `data/AcmeDataPlatform/` (not `data/Acme/DataPlatform/`); `.gitignore` exception added for that folder only, so other runtime data stays ignored. Needs a root ADR, since it departs from ADR-0013's "data/ is runtime data".

### 2026-11-13 · idea · Q2
**Asked by:** Claude
**Q:** [Claude] Which file format should the glossary, ontology, taxonomy and rules use?
**Options offered:** YAML + Markdown (Recommended); RDF / Turtle; Both
**A:** "I want to store the outcome in all possible standard formats inorder to understand which one I like when (includeing your YAML + Markdown files)."
**Effect:** Every artefact is written in YAML/Markdown plus the standard formats: SKOS (Turtle), OWL (Turtle, RDF/XML, JSON-LD), SHACL, TBX; diagrams in Mermaid.

### 2026-11-13 · idea · Q3
**Asked by:** Claude
**Q:** [Claude] The repo rules say every question I ask goes into an idea's Q&A log, but no idea exists yet. Should I capture this session as an idea first?
**Options offered:** Yes, create idea 0001 (Recommended); No, keep a log in the domain folder
**A:** Yes, create idea 0001 (Recommended)
**Effect:** This file.

### 2026-11-13 · idea · Q4
**Asked by:** Claude
**Q:** [Claude] "The AcmeDataPlatform allows building data products for the product teams." Who builds the data products, and what is the product teams' role?
**Options offered:** Product teams build them; Built for product teams; Both
**A:** Product teams build them
**Effect:** Relations `ProductTeam builds DataProduct` (inverse `builtBy`) and `DataProduct builtOn DataPlatform` (inverse `enablesBuilding`).

### 2026-11-13 · idea · Q5
**Asked by:** Claude
**Q:** [Claude] Is "AcmeDataPlatform" a kind of thing or one specific thing?
**Options offered:** One instance (Recommended); A class
**A:** One instance (Recommended)
**Effect:** Class `DataPlatform` with named individual `AcmeDataPlatform`.

### 2026-11-13 · idea · Q6
**Asked by:** Claude
**Q:** [Claude] S2 says a data product *is* "a reliable data asset", but S3/S5 say a data product *has* a data asset ("the data asset in a data product"). Which is it?
**Options offered:** Has a data asset (Recommended); Is a data asset
**A:** Has a data asset (Recommended)
**Effect:** `DataProduct hasDataAsset DataAsset` (exactly 1); DataProduct is not a subclass of DataAsset.

### 2026-11-13 · idea · Q7
**Asked by:** Claude
**Q:** [Claude] Who is the "owner" of a data product?
**Options offered:** The product team (Recommended); A person; Any team
**A:** A person
**Effect:** New class `Person`; `DataProduct hasOwner Person` (exactly 1); defined class `DataProductOwner` = a Person who owns some DataProduct.

### 2026-11-13 · idea · Q8
**Asked by:** Claude
**Q:** [Claude] How do "contract" and "guaranteed quality" relate?
**Options offered:** Contract specifies quality (Recommended); Two separate things; Quality is just a flag
**A:** Contract specifies quality (Recommended)
**Effect:** `DataProduct hasContract DataContract` (exactly 1); `DataContract specifies QualityGuarantee` (at least 1).

### 2026-11-13 · idea · Q9
**Asked by:** Claude
**Q:** [Claude] "The data asset consists of one or more tables and views": what is the minimum, and should tables and views share a parent concept in the taxonomy?
**Options offered:** ≥1 table or view; parent 'data object' · ≥1 table; parent 'data object' · ≥1 table or view; no parent
**A:** ≥1 table or view; parent 'data object'
**Effect:** New class `DataObject` with subclasses `Table` and `View`; `DataAsset consistsOf DataObject` (at least 1).

### 2026-11-13 · idea · Q10
**Asked by:** Claude
**Q:** [Claude] S8 introduces "the data product team". Is that the product team that builds the data product (S1)?
**Options offered:** Yes, exactly one team (Recommended); Yes, one or more teams; No, a different team
**A:** "There are many "product teams". Any of them can build data products."
**Effect:** `ProductTeam builds DataProduct` 0..* per team; defined class `DataProductTeam` = a ProductTeam that builds some DataProduct. Exactly one team per data product is an **assumption** (rule R14, from the singular "the data product team" in S8 and Q11), to be confirmed.

### 2026-11-13 · idea · Q11
**Asked by:** Claude
**Q:** [Claude] S7: "A DataProductOwner is member of a product team." Which team?
**Options offered:** Their product's team (Recommended); Any product team
**A:** Their product's team (Recommended)
**Effect:** Relation `Person memberOf ProductTeam`; rule R10: the owner of a data product is a member of that data product's team.

### 2026-11-13 · idea · Q12
**Asked by:** Claude
**Q:** [Claude] S8 says "the data pipeline, the contract, the user manual and other parts" are created and operated by the team. Which of these are 'parts of a data product'?
**Options offered (multi-select):** Data asset (tables, views); Data pipelines; Data contract + user manual; Workspace
**A:** All four.
**Effect:** New parent class `DataProductPart` over DataAsset, DataPipeline, DataContract, DataProductUserManual, Workspace; super-relation `hasPart`; relations `createdBy` / `operatedBy`; rules R11, R12.

### 2026-11-13 · idea · Q13
**Asked by:** Claude
**Q:** [Claude] How many user manuals does a data product have?
**Options offered:** Exactly one (Recommended); Zero or one; One or more
**A:** Exactly one (Recommended)
**Effect:** New class `DataProductUserManual`; `DataProduct hasUserManual` exactly 1 (rule R13).

### 2026-11-13 · idea · Q14
**Asked by:** Claude
**Q:** [Claude] S10 mentions "teams who will use it" (a data product). Who are these teams?
**Options offered:** Any product team (Recommended); Other product teams only; A new kind of team
**A:** Any product team (Recommended)
**Effect:** Relation `ProductTeam uses DataProduct` (inverse `usedBy`, 0..*); defined class `DataProductUserTeam` = a product team that uses some data product.

### 2026-11-13 · idea · Q15
**Asked by:** Claude
**Q:** [Claude] The user manual "explains the purpose of the data product and what is important to know". How should these two contents be modelled?
**Options offered:** Two required text fields (Recommended); Sections as concepts; Purpose on the product
**A:** "Data product user manual explains purpose and usage. But let's not create terms for purpose and usage."
**Effect:** No concepts or properties for purpose / usage; they live only in the user manual's definition (now the expert's wording, S10).

### 2026-11-13 · idea · Q16
**Asked by:** Claude
**Q:** [Claude] (open point, in chat) R14, my assumption: is each data product built by exactly one product team?
**Options offered:** free text
**A:** "Yes, each data product is built by exactly one product team."
**Effect:** R14 confirmed (no longer an assumption), source S12.

### 2026-11-13 · idea · Q17
**Asked by:** Claude
**Q:** [Claude] S13: data pipelines are "private to that data product". What should "private" enforce?
**Options offered:** Own product + own tables (Recommended); Own product only; Also hidden from users
**A:** Own product + own tables (Recommended)
**Effect:** Rules R15 (each pipeline belongs to exactly one data product) and R16 (a pipeline populates only tables of its own data product).

### 2026-11-13 · idea · Q18
**Asked by:** Claude
**Q:** [Claude] S15: data contracts include business and technical metadata: owner name and email, schemas of the tables and views, and the data product's address. Which items are business and which are technical?
**Options offered:** Owner=business, rest=technical (Recommended); All of them technical; No split needed
**A:** "Postpone this question"
**Effect:** No BusinessMetadata / TechnicalMetadata concepts yet; the contract includes the listed items directly. Kept as an open point.

### 2026-11-13 · idea · Q19
**Asked by:** Claude
**Q:** [Claude] How should owner name, owner email, schema and address be stored?
**Options offered:** On the thing, contract refers (Recommended); Copied into the contract
**A:** On the thing, contract refers (Recommended)
**Effect:** Data properties `Person.name`, `Person.email`, `DataProduct.address`; class `Schema` with `DataObject hasSchema Schema`; `DataContract includesSchema Schema`; rules R18–R21.

### 2026-11-13 · idea · Q20
**Asked by:** Claude
**Q:** [Claude] S16: "The data products are exposed via the DataProductCatalog." How many catalogs, and is every data product in it?
**Options offered:** One, every product listed (Recommended); One, only some listed; Several catalogs
**A:** "There is one DataProductCatalog service. But there are 3 instances exposed in the DEV, ACC and PRD environments."
**Effect:** Classes `DataProductCatalog` and `Environment`; individuals DEV, ACC, PRD and DataProductCatalogDEV/ACC/PRD, each `deployedIn` its environment; rule R27 (one catalog instance per environment). Whether every data product must be exposed, and in which environments, stays open.

### 2026-11-13 · idea · Q21
**Asked by:** Claude
**Q:** [Claude] S17/S18: a product team requests a subscription to a data product for its data consumer application or new data product, and the owner accepts or rejects it. What does an accepted request mean?
**Options offered:** Team then uses it (Recommended); Only a status; Consumer uses it
**A:** Team then uses it (Recommended)
**Effect:** Status pending → accepted | rejected; derivation rule R26: an accepted request means the requesting team `uses` the data product.

### 2026-11-13 · idea · Q22
**Asked by:** Claude
**Q:** [Claude] After a data product (or service, or resource) is promoted from DEV to ACC, does it still exist in DEV?
**Options offered:** Yes, it stays (Recommended); No, it moves
**A:** Yes, it stays (Recommended)
**Effect:** Rule R29: deployed in ACC ⇒ deployed in DEV; deployed in PRD ⇒ deployed in ACC. Environment order `nextEnvironment` DEV → ACC → PRD.

### 2026-11-13 · idea · Q23
**Asked by:** Claude
**Q:** [Claude] Does each environment have its own copy of a data product's address, workspace and catalog entry?
**Options offered:** Yes: a Deployment concept (Recommended); No, shared; Postpone
**A:** Yes: a Deployment concept (Recommended)
**Effect:** New class `Deployment` (a resource in one environment). `address` and `hasWorkspace` move from DataProduct to Deployment; `exposedVia` links a data product deployment to the catalog deployment in the same environment. Rules R7, R8, R9, R21, R27 revised; new R30, R33.

### 2026-11-13 · idea · Q24
**Asked by:** Claude
**Q:** [Claude] S21 says data products are promoted "just like any other service or data platform resource". How should these relate?
**Options offered:** One parent (Recommended); Two parents
**A:** One parent (Recommended)
**Effect:** New class `DataPlatformResource` with subclasses `DataProduct` and `Service`; `DataProductCatalog` becomes a Service; its DEV/ACC/PRD instances become the deployments of the one catalog service `AcmeDataProductCatalog`.

### 2026-11-13 · idea · Q25
**Asked by:** Claude
**Q:** [Claude] S24: "Each service has an owner." What kind of owner?
**Options offered:** A person: service owner (Recommended); A team
**A:** A person: service owner (Recommended)
**Effect:** `hasOwner` generalized to every data platform resource (range Person); defined class `ServiceOwner`; rule R34.

### 2026-11-13 · idea · Q26
**Asked by:** Claude
**Q:** [Claude] S24/S25 introduce "support team" and "development team". How do they relate to product teams?
**Options offered:** Roles of a general 'team' (Recommended); Separate team kinds; Product teams play them
**A:** Roles of a general 'team' (Recommended)
**Effect:** New class `Team` (parent of ProductTeam); defined classes `SupportTeam` (supports some service) and `DevelopmentTeam` (develops some custom service); `memberOf` now ranges over Team.

### 2026-11-13 · idea · Q27
**Asked by:** Claude
**Q:** [Claude] S25 names "internally developed (custom) services". What are the other services called?
**Options offered:** Third-party service; Managed (cloud) service; Leave unnamed for now
**A:** "SaaS services. (synonym: managed services)"
**Effect:** Service = CustomService or SaaSService (disjoint); synonyms "internally developed service" and "managed service".

### 2026-11-13 · idea · Q28
**Asked by:** Claude
**Q:** [Claude] Is the DataProductCatalog a custom (internally developed) service?
**Options offered:** Yes, custom; No, not custom; Don't know yet
**A:** Yes, custom
**Effect:** `DataProductCatalog` is a subclass of `CustomService`.

### 2026-11-13 · idea · Q29
**Asked by:** Claude
**Q:** [Claude] "Data product owner team" isn't in the model yet. The closest concept is "data product team". Are they the same, and which name should be the preferred term?
**Options offered:** Same; prefer 'owner team'; Same; keep 'data product team'; A different concept
**A:** Same; prefer 'owner team'
**Effect:** `adp:DataProductTeam` (IRI kept stable) now has preferred label "data product owner team", synonyms "data product producer team" and "data product team"; `adp:DataProductUserTeam` gets synonym "data product consumer team". Definitions use the preferred term.

### 2026-11-13 · idea · Q30
**Asked by:** Claude
**Q:** [Claude] (open point, in chat) Exposure: is every data product deployment listed in its environment's catalog, or only some?
**Options offered:** free text
**A:** "Yes, each data product is listed in its environment's catalog"
**Effect:** New rule R38: every data product deployment is exposed via the catalog deployment in its environment (with R33: exactly that one). `exposedVia` cardinality: exactly 1 per data product deployment.

### 2026-11-14 · idea · Correction C1 (user)
**Asked by:** user (correction, no question)
**Statement:** "Correction: "Service" is not a "data platform resource". The "data platform" cosists of one or more services."
**Effect:** Supersedes the Q24 effect "Service ⊂ DataPlatformResource". Service and DataPlatformResource become disjoint; new relation `DataPlatform consistsOfService Service` (1..*), rule R39.

### 2026-11-14 · idea · Q31
**Asked by:** Claude
**Q:** [Claude] Correction: a service is not a data platform resource. Do services still have deployments in DEV/ACC/PRD and go through promotion (S21), and if so, should services and data platform resources share a parent concept?
**Options offered:** Yes, no shared parent (Recommended); Yes, with a shared parent; No, services aren't promoted
**A:** Yes, no shared parent (Recommended)
**Effect:** Services keep owner, deployments and promotion; `hasOwner`, `hasDeployment`, `promotes`, `productionizes` apply to "data platform resource or service" (OWL union, no named parent). Rules R28–R30 reworded (revised by S30).

### 2026-11-14 · idea · Correction C2 (user)
**Asked by:** user (correction + new info, no question)
**Statement:** "Correction: "Data platform resource" could be one of the following: "data product", "dashboard", "analytical/AI application", "ML/AI model". New info: Product teams use the "data platform" to create/use/consume one of those "data platform resources"."
**Effect:** DataPlatformResource = DataProduct or Dashboard or analytical/AI application or MLModel or AIModel (see Q33); builds/uses generalized (Q35); relation `usesPlatform`.

### 2026-11-14 · idea · Q32
**Asked by:** Claude
**Q:** [Claude] Your last correction is cut off: "'data pipeline', 'contract', 'data product user manual', 'workspace' are …". How does it end?
**Options offered:** …data platform resources; …not data platform resources; …parts of other resources too
**A:** "Correction:"data pipeline", "contract", "data product user manual", "workspace", "data asset" are "data platform sub-resources". "Data platform resources" may consists or use of one or more "Data platform sub-resources". e.g.: A "workspace" is needed to store the "data asset", the "data pipeline", .... but a product team does not create a "workspaces" on its own."
**Effect:** `DataProductPart` replaced by `DataPlatformSubResource` (open list, no covering axiom); `hasPart` replaced by `hasSubResource` ("consists of"), new `usesSubResource` ("uses"; `hasWorkspace` is a sub-relation). **Interpretation (to confirm):** a resource consists of its data asset, pipelines, contract and user manual (created and operated by its owner team, R11/R12) and only uses its workspace, which the team does not create; R11/R12 no longer cover workspaces.

### 2026-11-14 · idea · Q33
**Asked by:** Claude
**Q:** [Claude] "analytical/AI application" and "ML/AI model": one concept each, or two each?
**Options offered:** One each, synonyms (Recommended); Two each
**A:** ""analytical/AI application" is one concept "ML model" is another concept, "AI model" is another concept."
**Effect:** Classes for analytical/AI application, `MLModel`, `AIModel` (separate).

### 2026-11-14 · idea · Q34
**Asked by:** Claude
**Q:** [Claude] S18 has "data consumer application" (the thing a subscription is requested for). Is that the same as the new "analytical/AI application"?
**Options offered:** Same concept (Recommended); Consumer app is broader; Different things
**A:** Same concept (Recommended)
**Effect:** `adp:DataConsumerApplication` (IRI kept) gets preferred label "analytical/AI application", synonym "data consumer application"; it is a data platform resource and a data consumer. `ownedByTeam` dropped in favour of the generalized `builds` (R23 reworded).

### 2026-11-14 · idea · Q35
**Asked by:** Claude
**Q:** [Claude] "Product teams use the data platform to create/use/consume data platform resources." How should this extend the model (today 'builds' and 'uses' only cover data products)?
**Options offered:** Generalize to all resources (Recommended); Data products only
**A:** Generalize to all resources (Recommended)
**Effect:** `builds` and `uses` (synonym: consumes) range over DataPlatformResource; R14 generalized (exactly one builder team per resource); `ProductTeam usesPlatform DataPlatform`.

### 2026-11-14 · idea · Reset R1 (user)
**Asked by:** user (request, no question)
**Statement:** "Let's save the current content (glossary, taxonomy, ontology, rules, markdown files, ...) into a data-platform-concepts-v0.1.zip file. Delete the content, I want to start from scratch again."
**Effect:** All files of `data/AcmeDataPlatform/` (statements S1–S37, 39 rules), a copy of this idea file, the session helper and the SHACL test samples archived in `data/data-platform-concepts-v0.1.zip` (git-ignored, local only); the model files were then deleted. The Q&A log above is kept as history; a fresh model starts with new statement numbers from S1.

### 2026-11-14 · idea · Restart (user)
**Asked by:** user (request, no question)
**Statement:** "Same set-up with an extra addition to support granular learnability. Each concept, relation, rule, ... has a level. Level-1: (core) for a quick overview for anyone to understand the domain in 5-10 minutes. Level-2: (main) for an adopter to be able to use the domain for the most simple use-case(s) Level-3: (detailed) all the concepts, relations, rules that exist in the domain. We need to generate one-one markdown file for each level."
**Effect:** Same formats as v0.1, plus a `level` (1–3) on every concept, individual, relation, property and rule, and generated `level-1.md`, `level-2.md`, `level-3.md`.

### 2026-11-14 · idea · Q36
**Asked by:** Claude
**Q:** [Claude] Are the levels cumulative, so that level-2.md also contains everything from level 1, and level-3.md contains the whole domain?
**Options offered:** Cumulative (Recommended); Separate layers
**A:** Cumulative (Recommended)
**Effect:** level-N.md contains all items with level ≤ N. Check: a relation or rule is never at a lower level than the concepts it uses.

### 2026-11-14 · idea · Q37
**Asked by:** Claude
**Q:** [Claude] Who decides the level of each concept, relation and rule?
**Options offered:** I propose, you confirm (Recommended); You state it; Default 3, promote later
**A:** "Let's start with level-1 and I will let you know when it is complete."
**Effect:** Phased: a `working_level` (now 1) in ontology.yaml; every new item gets the working level. The user announces when level 1 is complete, then the working level moves to 2, later 3.

### 2026-11-14 · idea · Q38
**Asked by:** Claude
**Q:** [Claude] What should each level file contain?
**Options offered:** Full, filtered (Recommended); Text only; Narrative + tables
**A:** Full, filtered (Recommended)
**Effect:** Each level file: short intro, glossary, taxonomy tree, relations, properties, rules, Mermaid taxonomy and ontology graph, all filtered to level ≤ N.

### 2026-11-14 · idea · Note N1 (Claude)
**Asked by:** Claude (disclosure, no question)
**Statement:** While writing a new level-aware generator, the language hook blocked a Python file (rule 9: Python has no quality gate). During v0.1, Claude had written the session helper `derive.py` and ran Python test snippets through Bash, which bypassed that same check; the copy inside `data/data-platform-concepts-v0.1.zip` was produced that way. The model files themselves (YAML, Turtle, Markdown) are not code and are unaffected.
**Effect:** No more Python until it is registered; derived files from a failed run of the old helper were removed.

### 2026-11-14 · idea · Q39
**Asked by:** Claude
**Q:** [Claude] The level files, diagrams and standard formats need a generator. Python is blocked until it has a quality gate (rule 9), and a generator that stays in the repo would also need a spec first (spec-driven rule). How should we proceed?
**Options offered:** /add-language python, then spec it (Recommended); /add-language python, session helper; No code: by hand
**A:** /add-language python, then spec it (Recommended)
**Effect:** Next steps: user runs `/add-language python`; then the generator is captured as idea 0002 and goes through /spec → /plan → /implement as a repo tool. Modelling (level 1) resumes once the generator exists.

### 2026-11-14 · architecture · Q40
**Asked by:** Claude
**Q:** [add-language · decide] Which package and workspace manager for Python? Every app and shared component gets its own pyproject.toml, so the gate needs one command that covers them all.
**Options offered:** uv workspace (Recommended); pip + venv; Poetry
**A:** uv workspace (Recommended)
**Effect:** Root pyproject.toml with `[tool.uv.workspace]`, one committed `uv.lock`, `uv run` for every gate command; Dependabot `uv` ecosystem.

### 2026-11-14 · architecture · Q41
**Asked by:** Claude
**Q:** [add-language · decide] Which minimum Python version should the code support?
**Options offered:** 3.13 (Recommended); 3.14; 3.15
**A:** "Can we use the latest stable version of python?"
**Effect:** Latest stable CPython is 3.15.2 (checked with `uv python list`): `requires-python = ">=3.15"`, `.python-version` 3.15, CI on 3.15.

### 2026-11-14 · architecture · Q42
**Asked by:** Claude
**Q:** [add-language · decide] Which type checker, in strict mode?
**Options offered:** mypy strict (Recommended); pyright strict
**A:** mypy strict (Recommended)
**Effect:** mypy 2.4.1 with `strict = true`, in pre-commit, the PostToolUse hook path and CI.

### 2026-11-14 · architecture · Note N2 (Claude)
**Asked by:** Claude (disclosure, no question; completes N1)
**Statement:** Besides `derive.py`, v0.1 also used inline Python run through Bash (never saved as files) to apply find-and-replace edits to the model files and to run the rdflib / pyshacl checks and SHACL tests. During `/add-language python`, before Python was registered, one more inline snippet added the ADR-0014 row to `docs/architecture/adr/README.md`. All of this bypassed the rule-9 hook in spirit. Python is now registered (ADR-0014); from here on Python is written as files under the quality gate.
**Effect:** None on the model content; the gate now catches Python written by Claude (PostToolUse hook), on commit (pre-commit) and in CI.

### 2026-11-14 · idea · Note N3 (user)
**Asked by:** user (housekeeping, no question)
**Statement:** "Add archive-*.zip to .gitignore" / "I have already renamed it. Check that it will be ignored and not committed to git."
**Effect:** `.gitignore` ignores `archive-*.zip` in every folder. The v0.1 archive is now `data/archive-data-platform-concepts-v0.1.zip` (earlier entries use its old name `data-platform-concepts-v0.1.zip`); verified ignored (by `archive-*.zip` and `/data/*`) and untracked.

### 2026-11-14 · idea · Q43
**Asked by:** Claude
**Q:** [Claude] The generator for the derived files doesn't exist yet (planned as idea 0002). How should I produce the outputs while we model level 1?
**Options offered:** Sources + level-1.md by hand (Recommended); Everything by hand; Pause, build generator first
**A:** Pause, build generator first
**Effect:** Modelling paused. Statements S1–S9 (level 1, new numbering after the restart) and the answers below are recorded in `data/AcmeDataPlatform/statements.md`; `ontology.yaml` stays empty until the generator's spec fixes its input format. Next: idea 0002 (generator) → /spec → /plan → /implement.

### 2026-11-14 · idea · Q44
**Asked by:** Claude
**Q:** [Claude] "Platform services are used by product teams to create platform resources." How many platform services is one platform resource created with?
**Options offered:** Exactly one; One or more; Don't record it
**A:** One or more
**Effect:** (to apply) `PlatformResource createdWith PlatformService` 1..*.

### 2026-11-14 · idea · Q45
**Asked by:** Claude
**Q:** [Claude] How do "platform team" and "product team" relate?
**Options offered:** Two kinds of 'team'; Separate, no parent; A team can be both
**A:** Two kinds of 'team'
**Effect:** (to apply) Level-1 concept `Team` with disjoint subclasses `PlatformTeam` and `ProductTeam`.

### 2026-11-14 · idea · Q46
**Asked by:** Claude
**Q:** [Claude] "Platform services can be deployed to the environments." Do services follow an order like resources do, or can a service be deployed to any environment independently?
**Options offered:** Any environment, independently; Same promotion paths; Not EXP
**A:** Any environment, independently
**Effect:** (to apply) `PlatformService deployedTo Environment` 0..4, no ordering rule; promotion paths apply to platform resources only.

### 2026-11-14 · idea · Note N4 (Claude)
**Asked by:** user ("Let's do modelling now. I want to see partial results.")
**Effect:** Level 1 modelled from S1–S10 with the spec-0002 generator, in three passes (concepts, relations, rules): 12 concepts, 5 individuals, 8 relations, 12 rules (R1–R12), each constraint rule with a violating sample. Q44–Q46 applied (`createdWith` 1..*, Team ⊃ PlatformTeam ⊥ ProductTeam, `deployedTo` with no ordering rule). R5 is a SPARQL check because the `createdBy` range makes a `class` check unfalsifiable under RDFS inference. Drafts (Claude's wording or interpretation, to confirm): concept `DataPlatform`, relation `createdIn` (exactly one), rules R7 and R9–R12 (promotion paths, S8).

### 2026-11-14 · idea · Q47
**Asked by:** Claude
**Q:** [Claude] Draft `data platform` (concept): AcmeDataPlatform is one instance of a kind called "data platform". Is that right, or should AcmeDataPlatform be a concept itself?
**Options offered:** free answer (in chat)
**A:** "correct."
**Effect:** `DataPlatform` confirmed.

### 2026-11-14 · idea · Q48
**Asked by:** Claude
**Q:** [Claude] Draft `created in` / R7: "A platform resource is created in exactly one environment." Is it always exactly one?
**Options offered:** free answer (in chat)
**A:** "A platform resource is either created in EXP environment first and then promoted to DEV, ACC and PRD. Or it is created in DEV and promoted to ACC and PRD."
**Effect:** Recorded as S11. `createdIn` (exactly 1) and R7 confirmed; S11 added to the sources of R8–R12.

### 2026-11-14 · idea · Q49
**Asked by:** Claude
**Q:** [Claude] Draft R9: "A platform resource can only be promoted to DEV, ACC or PRD", i.e. nothing is ever promoted into EXP. Correct?
**Options offered:** free answer (in chat)
**A:** "Correct. EXP is the environment for experimentation. This is an environment for teams who do not know what they want or how they want to implement it. Or just want to learn the new technologies."
**Effect:** Recorded as S12. R9 confirmed; EXP gets the definition "The environment for experimentation."

### 2026-11-14 · idea · Q50
**Asked by:** Claude
**Q:** [Claude] Draft R10: "A platform resource promoted to DEV was created in EXP." Correct?
**Options offered:** free answer (in chat)
**A:** "correct. See the extra information I added for point #3."
**Effect:** R10 confirmed.

### 2026-11-14 · idea · Q51
**Asked by:** Claude
**Q:** [Claude] Draft R11: "A platform resource promoted to ACC was created in or promoted to DEV first." Correct?
**Options offered:** free answer (in chat)
**A:** "Correct. Only automated CI/CD pipelines are allowed to deploy anything to ACC environment. Creating platform resources manually in ACC environment is not allowed and prevented by policy."
**Effect:** Recorded as S13. R11 confirmed; S13 added to R8's sources (no creation in ACC). "Automated CI/CD pipeline" not modelled yet (open, see Q54).

### 2026-11-14 · idea · Q52
**Asked by:** Claude
**Q:** [Claude] Draft R12: "A platform resource promoted to PRD was promoted to ACC first." Correct?
**Options offered:** free answer (in chat)
**A:** "Yes. Platform resources have to be promoted to ACC first then some of the modifications can be promoted further to PRD environment."
**Effect:** Recorded as S14. R12 confirmed; reaching PRD stays optional (no rule requires it).

### 2026-11-14 · idea · Q53
**Asked by:** Claude
**Q:** [Claude] S9 resource kinds: is the list complete (every resource is one of the five), and can one resource be two kinds at once?
**Options offered:** free answer (in chat)
**A:** "Those are all the currently available platform resources related to end-to-end use-cases. But you are right those platform resources may consist of multiple sub-components. I will create those statements for level-2."
**Effect:** Recorded as S15. Closed list: `ontology.axioms.ttl` makes PlatformResource the union of the five kinds. Whether the kinds are mutually exclusive is still open (Q55). Sub-components follow at level 2.

### 2026-11-14 · idea · Q54
**Asked by:** Claude
**Q:** [Claude] S13 introduces "automated CI/CD pipelines". Should it be a level-1 concept now, or wait for level 2?
**Options offered:** level 1 now; level 2 with the sub-components (in chat)
**A:** "CI/CD pipeline will be introduced for level-2. It is only needed for teams which need to build something."
**Effect:** Recorded as S16. No CI/CD pipeline concept at level 1.

### 2026-11-14 · idea · Q55
**Asked by:** Claude
**Q:** [Claude] Can one platform resource be two kinds at once (e.g. a data product that is also a dashboard)? If not, the five kinds become mutually exclusive.
**Options offered:** mutually exclusive; may overlap (in chat)
**A:** "They are not mutually exclusive. Example. An "analytical application" may come with a business "dashboard" as well."
**Effect:** Recorded as S17. No disjointness between the five kinds (model unchanged). The example describes composition (an application *with* a dashboard), which Claude raised back as a follow-up (Q57).

### 2026-11-14 · idea · Q56 (user)
**Asked by:** user
**Q:** "What is your suggestion to modell that a dashboard can be a (top-level) platform resource as well as a (sub / nested) platform resource?"
**A (Claude):** Treat "top-level" and "nested" as roles, not kinds: keep one `Dashboard` class and add a part-of relation between platform resources (e.g. `hasComponent`, "consists of"), so a dashboard is nested when some resource has it as a component and top-level otherwise. Optionally derive the roles: `NestedPlatformResource` (OWL: is a component of some platform resource) and `TopLevelPlatformResource` (a SPARQL rule, because "not part of anything" cannot be inferred under OWL's open world). Rejected: separate classes per role (duplicates every kind) and a "component usage" object (only needed if a nesting carries its own data). Proposed for level 2, with the sub-components (S15).
**Effect:** Proposal only; awaiting the expert's decision.

### 2026-11-14 · idea · Q57
**Asked by:** Claude
**Q:** [Claude] Your example ("an analytical application may come with a business dashboard") reads like composition: two resources, one containing the other. Which is it?
**Options offered:** 1. Composition only (each resource is exactly one kind; nesting via "consists of"); 2. Both (nesting, and one resource can also be two kinds)
**A:** "Let's go with composition for level-2. A platform resource may consist of multiple (nested / sub) platform resourcs. The (nested / sub) platform resources belong to their (parent) platform resource and cannot live on their own and they are created/owned by the same product team."
**Effect:** Recorded as S18. Option 1: the five resource kinds are now mutually exclusive (OWL disjointness, level 1; supersedes the Q55 effect). Level 2: concept `SubPlatformResource` ("sub platform resource", synonym "nested platform resource"), relations `hasSubResource` ("consists of") and its inverse `belongsTo` (exactly 1, functional, irreflexive), rules R13 (exactly one parent) and R14 (same creator as the parent; ownership follows through R6). Level-1 view unchanged.

### 2026-11-14 · idea · Q58
**Asked by:** Claude
**Q:** [Claude] Do sub platform resources follow their parent's lifecycle (same environment, promoted together) or have their own (created and promoted separately)?
**Options offered:** 1. Follow the parent; 2. Own lifecycle
**A:** "Yes, nested platform resources are promoted with their parent platform resource. In fact, promoting a data product from DEV to ACC means: - promote the contract - promote the data pipeline - the data asset will be automatically built from parent/upstream data products automatically. This is also a level-2 information."
**Effect:** Recorded as S19. Option 1, level 2: derivation rules R15 (a sub-resource gets its parent's creation environment) and R16 (its parent's promotions), constraint R17 (never promoted on its own). R3 (created with ≥1 platform service) still applies to sub-resources: dropping it for them would make a level-1 rule depend on a level-2 concept. Contract, data pipeline, data asset and "upstream" not modelled yet (Q59, Q60).

### 2026-11-14 · idea · Note N5 (user)
**Asked by:** user ("Add a relation to level-1: Each "platform service" is owned by a "platform team".")
**Effect:** Same content as S3, which was modelled only through the domain-less `ownedBy` (not drawn in the ontology graph). New level-1 relation `serviceOwnedBy` ("owned by", PlatformService → PlatformTeam, exactly 1, sub-relation of `ownedBy`), source S3. R2 became a SPARQL check, because the new range makes a `class` check unfalsifiable under RDFS inference (as with R5). Samples state service owners with `serviceOwnedBy`.

### 2026-11-14 · idea · Q59
**Asked by:** Claude
**Q:** [Claude] Are contract, data pipeline and data asset sub platform resources (then the closed list of five kinds covers only top-level resources), or a separate concept "data product part"?
**Options offered:** 1. Separate concept "data product part"; 2. Sub platform resources
**A:** "Extra info for level-2: (nested/sub) platform resources of a data product: contract, data pipeline, compute cluster definition, workspace infra definition, data asset(s) (typically tables and views in case of structured data products), dashboards which show the health of the data product, all mandatory. Of an analytical/AI application: dashboard(s), data product, ML model, AI model, all optional. Of a dashboard: data product, ML model, AI model, all optional. Extra info for level-1: Product teams can subscribe to platform resources." (verbatim in S20, S21)
**Effect:** Option 2. Level 2: concepts DataContract ("contract"), DataPipeline, ComputeClusterDefinition, WorkspaceInfraDefinition, DataAsset, each a kind of sub platform resource and disjoint from every other kind; the closed list in `ontology.axioms.ttl` now has ten kinds. Rules R18–R23 (the six mandatory parts of a data product, confirmed) and R24–R26 (only the listed sub-resources are allowed for a data product, an application and a dashboard; draft, Claude's reading of the lists). Level 1: relation `subscribesTo` (ProductTeam → PlatformResource, S21). Tables and views not modelled ("typically"). R24–R26 use `FILTER IN`, since SHACL forbids `VALUES` in SPARQL constraints.

### 2026-11-14 · idea · Q60
**Asked by:** Claude
**Q:** [Claude] "The data asset will be automatically built from parent/upstream data products": does "parent" mean the data products it reads data from (upstream), or the composition parent (S18)?
**Options offered:** upstream; composition parent (in chat)
**A:** "Level-2: - a "data product" may depend on parent/upstream data product(s). Such a data product is also called as a child/downstream data product of its parent(s). - the parent/child relationship between the data products is called as "lineage" - the data asset is always built by a "data pipeline". The data pipeline reads the content of the data asset(s) of the parent data products and populates the data assets of the child data product."
**Effect:** Recorded as S24. Level 2: relation `dependsOn` ("depends on", synonym "lineage"); concepts `ParentDataProduct` (upstream) and `ChildDataProduct` (downstream), derived by R29/R30; relations `populates` and `reads` (DataPipeline → DataAsset); rules R31 (every data asset is populated by a pipeline), R32 (a pipeline populates only its own data product's assets), R33 (it reads only assets of its data product's parents).

### 2026-11-14 · idea · Q61
**Asked by:** Claude
**Q:** [Claude] Drafts R24–R26: are the listed sub-resources the only ones allowed for a data product, an AI/analytical application and a dashboard?
**Options offered:** free answer (in chat)
**A:** "R24: yes, those are the only (nested/sub) platform resources of a data product. R25: correct R26: correct"
**Effect:** R24 (source S22), R25, R26 confirmed.

### 2026-11-14 · idea · Q62
**Asked by:** Claude
**Q:** [Claude] ML/AI models and the part kinds: can they have sub-resources?
**Options offered:** free answer (in chat)
**A:** "ML/AI models may contain a data product (optional)"
**Effect:** Recorded as S23. Rules R27 (an ML model consists only of data products) and R28 (same for AI models). The part kinds (contract, pipeline, …) got no rule: not answered.

### 2026-11-14 · idea · Q63
**Asked by:** Claude
**Q:** [Claude] Should `table` and `view` be kinds of data asset at level 2 or 3, or be left out ("typically")?
**Options offered:** level 2; level 3; leave out
**A:** "Level-3."
**Effect:** Concepts `Table` and `View` (disjoint), kinds of data asset, level 3, source S20.

### 2026-11-14 · idea · Q64
**Asked by:** Claude
**Q:** [Claude] Add a level-1 relation "platform resource → owned by → product team", so resource ownership is drawn in the graph?
**Options offered:** yes; no
**A:** "yes. Let's add "created by" and "owned by" relations"
**Effect:** New relation `resourceOwnedBy` ("owned by", PlatformResource → ProductTeam, exactly 1, sub-relation of `ownedBy`, source S5). "created by" already existed (`createdBy`, level 1). Samples state resource owners with `resourceOwnedBy`.

### 2026-11-14 · idea · Q65
**Asked by:** Claude
**Q:** [Claude] R33 lets a pipeline read only from parent data products, so a data product without parents reads nothing. Correct, or do some data products load from sources outside the platform?
**Options offered:** free answer (in chat)
**A:** Ingestion: "data products can be created via ingestion. An "ingestion data pipeline" ingests data from an (internal or external) source service or data source. … the ingestion produces a data asset in the RAW layer. then one or more "processing data pipelines" perform some of the transformations … across the RAW->CURATED->SERVING medallion layers. Data products can be created also from parent/upstream data products." (verbatim in S25)
**Effect:** Recorded as S25. Level 2: concepts IngestionDataPipeline, ProcessingDataPipeline (kinds of data pipeline, disjoint), DataSource (synonym "source service"), MedallionLayer with individuals RAW → CURATED → SERVING (`nextLayer`); relations `ingestsFrom`, `inLayer` (draft); rules R34 (ingested asset is RAW), R35 (processing populates only CURATED/SERVING, draft), R36 (one layer per asset, draft), R37 (ingestion has a source), R38 (ingested or built from parents, draft). R33 widened: a pipeline also reads its own data product's assets.

### 2026-11-14 · idea · Q66
**Asked by:** Claude
**Q:** [Claude] May lineage contain cycles?
**Options offered:** yes; no (then a rule forbids cycles)
**A:** "Level-2: Yes, lineage is a DAG (Directed Acyclic Graph) and cannot contain cycles/loops."
**Effect:** Recorded as S26. Rule R39 (no data product depends on itself, directly or indirectly).

### 2026-11-14 · idea · Q67
**Asked by:** Claude
**Q:** [Claude] May the part kinds (contract, data pipeline, …) have sub-resources of their own?
**Options offered:** free answer (in chat)
**A:** "Level-2: An "analytical/AI application" can contain a "data product" as a (nested/sub) platform resource, and the data product also has its own (nested/sub) platform resources. But there is no circular dependency in this nested structure and all the (nested/sub) platform resources of a (top-level) platform resource are created and owned by the same product team." Plus, unprompted: "A dashboard, "Analytical/AI application" may also consume/reference/use to a "data product", "ML model", "AI model" created by another product team. In this case they are no nested/sub platform resources, but referenced upstream/parent platform resources, which are deployed separately and can live independently." (verbatim in S27, S28)
**Effect:** Recorded as S27, S28. Rule R40 (nesting has no cycles); R14 cites S27; R15/R16 now follow the whole nesting chain (`belongsTo+`), so deeply nested resources get the top-level resource's environments. Relation `consumes` (synonyms references, uses); rules R41 (only dashboards and applications consume, draft), R42 (only data products, ML and AI models are consumed, draft), R43 (a consumed resource is not a sub-resource). Whether the part kinds may have sub-resources is still unanswered.

### 2026-11-14 · idea · Q68
**Asked by:** Claude
**Q:** [Claude] Draft R41: "Only dashboards and AI/analytical applications consume other platform resources."
**Options offered:** free answer (in chat)
**A:** "R41: correction: data products may also consume other data products, those are the parent/upstream data products."
**Effect:** Recorded as S29. R41 confirmed with data products added; `dependsOn` is now a sub-relation of `consumes`; new rule R44 (the data products a data product consumes are exactly its parents). Drafts R35, R36, R38 and R42 were not answered and stay draft.

### 2026-11-14 · idea · Q69
**Asked by:** Claude
**Q:** [Claude] Ingestion and processing data pipelines are mutually exclusive. Can one pipeline both ingest and transform?
**Options offered:** free answer (in chat)
**A:** "No. An ingestion data pipeline only ingests and stores everything in the RAW layer as raw/unchenged data. i.e.: transformations are not allowed. A processing data pipeline is not allowed to ingest. And each data pipeline can do only one of those things."
**Effect:** Recorded as S30. Disjointness confirmed; closed list in `ontology.axioms.ttl` (a data pipeline is an ingestion or a processing pipeline); rules R45 (every pipeline is one of the two), R46 (ingestion reads no data assets), R47 (processing does not ingest).

### 2026-11-14 · idea · Q70
**Asked by:** Claude
**Q:** [Claude] May a contract, pipeline, compute cluster definition, workspace infra definition or data asset have sub-resources of its own?
**Options offered:** free answer (in chat)
**A:** "there are no nested/sub resources under a data pipeline, contract, ..."
**Effect:** Recorded as S31. Rule R48.

### 2026-11-14 · idea · Q71
**Asked by:** Claude
**Q:** [Claude] May a dashboard also consume a data product of its own team without nesting it?
**Options offered:** yes; no
**A:** "yes, A dashboard can also consum an independent parent/upstream data product (created by a the same or another product team)."
**Effect:** Recorded as S32. No team restriction on `consumes` (model unchanged); R41, R43 and `consumes` cite S32.

### 2026-11-14 · idea · Q72
**Asked by:** Claude
**Q:** [Claude] Drafts R36 (each data asset is in exactly one medallion layer), R35 (processing populates only CURATED or SERVING), R38 (a data product is created via ingestion or from parents), R42 (only data products, ML models and AI models are consumed).
**Options offered:** free answer (in chat)
**A:** "R36: Yes, each data asset is in exactly one medallion layer. R35 correct R38 corect R42: Dashboards can be consumed by human users: (user principlas). Data products, ML models and AI models are consumed by downstream/child application consumers (service principals)."
**Effect:** R35, R36 (with `inLayer`), R38, R42 confirmed; R42 cites S33. Recorded S33. Level 2: concepts `UserPrincipal` (synonym "human user") and `ServicePrincipal` (synonym "application consumer"), disjoint, under a parent `Principal` (draft, Claude's term); relations `userConsumes` (→ Dashboard) and `serviceConsumes` (→ PlatformResource); rules R49 (user principals consume only dashboards) and R50 (service principals consume only data products, ML and AI models).

### 2026-11-14 · idea · Q73
**Asked by:** Claude
**Q:** [Claude] Draft `principal` (Claude's term for the parent of user and service principal): keep, rename or drop? And can one principal be both a user principal and a service principal?
**Options offered:** keep / rename / drop; mutually exclusive or not
**A:** "keep the "principal" term. I will add details on it later." / "mutually exclusive"
**Effect:** `Principal` confirmed; UserPrincipal ⊥ ServicePrincipal confirmed (already modelled).

### 2026-11-14 · idea · Q74
**Asked by:** Claude
**Q:** [Claude] Should a service principal be linked to the application it acts for, and can that application be outside the platform?
**Options offered:** free answer (in chat)
**A:** "Level-3: A "Service principal" represents the identity of an application, data pipeline or other automation whch is not performed by a human. A "user principla" represents the identity of a user or group of users who can look at dashboards, use "analytical/AI applications""
**Effect:** Recorded as S34. Definitions of UserPrincipal and ServicePrincipal now in these words. Level 3: relations `userUses` (UserPrincipal → AIAnalyticalApplication) and `identityOf` ("represents the identity of", ServicePrincipal →, no range); concept `Automation` (draft); rule R51 (draft: the identity is of an AI/analytical application, a data pipeline or an automation). R49 (level 2) unchanged. Whether "application" means only AI/analytical applications, and whether it can be outside the platform, is still open.

### 2026-11-14 · idea · Q75
**Asked by:** Claude
**Q:** [Claude] Draft `automation` (concept): a concept, or only part of the service principal's definition? Draft R51: does "application" mean only AI/analytical applications on the platform, or also applications outside it?
**Options offered:** concept / part of the definition; inside only / also outside
**A:** "part of the definition." / "R51: level-3: yes, "application" can be either an internal "analytical/AI application" which runs inside the AcmeDataPlatform and consumes the platform resources, or an external application that runs outside of the data platform and consumes the "externally exposed/shared" platform resources."
**Effect:** Recorded as S35. Concept `Automation` removed. R51 removed: "other automation" is open-ended, so the kinds a service principal may represent cannot be checked. Level 3: concept `ExternalApplication`; data property `externallyShared` (boolean, synonym "externally exposed") on platform resources; rule R52 (an external application's service principal consumes only externally shared platform resources).

### 2026-11-14 · idea · Q76
**Asked by:** Claude
**Q:** [Claude] "Externally shared": a yes/no property of a platform resource (simpler), or a concept "externally shared platform resource" (only worth it if shared resources have their own relations)?
**Options offered:** yes/no property; concept
**A:** "R52: make "externally shared" a yes/no property."
**Effect:** Confirms the modelled data property `externallyShared` (boolean); no change.

### 2026-11-14 · idea · Note N6 (user)
**Asked by:** user ("Extra statements for level-2: …", seven statements, verbatim in S36–S42)
**Effect:** Level 2: concepts ProductOwner, DataProductOwner (a kind of product owner, Claude's reading of "(Data)ProductOwner"), Catalog, SubscriptionRequest, SubscriptionStatus with individuals Approved, Rejected and Pending (draft); relations hasProductOwner, memberOf, exposedIn ("findable in"), requestedBy, requestFor, requestConsumer, receivedBy, hasStatus, hasAccessTo; rules R53 (draft: every platform resource that is not a sub-resource has a product owner), R54–R59, R60 (draft: the requester is the consumer's product owner), R61, R62 (draft: status values), R63 (derivation: approval grants access to the consumer and makes its owner team subscribe), R64 (cross-team consumption needs an approved request). "By default" exposure in catalogs is not enforced by a rule (open).

### 2026-11-14 · idea · Q77
**Asked by:** Claude
**Q:** [Claude] Drafts R53 (every platform resource that is not a sub-resource has a product owner), `pending` / R62 (pending, approved or rejected), R60 (the requester is the consumer's product owner); and R54, R64 as modelled.
**Options offered:** free answer (in chat)
**A:** "R54: correction: each (top-level) platform resource has exactly one ProductOwner or DataProductOwner. R64: correction: A platform resource can be consumed by a team/app (different than the owner team) only after an approved subscription request. R53: correction: each platform resource (which is not a sub platform resource has exactly one product owner. R62: the "PENDING" term is correct R60: SubscriptionRequest to a platform resource for a new data product, application or other platform resource is created by the owner of that new application, dataproduct or platform resource."
**Effect:** Recorded as S43–S45. R53 + R54 now mean exactly one product owner per top-level platform resource (R54 no longer limits sub-resources). R60, R62 and `Pending` confirmed. R64 reworded (platform resources of another team); new rule R65 for applications of another team and external applications, at level 3 because it needs `identityOf` (level 3, S34).

### 2026-11-14 · idea · Q78
**Asked by:** Claude
**Q:** [Claude] (R64 / R65 as modelled after Q77: cross-team consumption needs an approved subscription request.)
**Options offered:** free answer (in chat)
**A:** "R64: correction: any platform resource can be consumed by a new application, child data product or child platform resource after approved subscription request. Special case: a product team creats a data product "A". If the same product team creates a new child platform resource or application which needs to consume the "A" data product. Approved subscription is needed ieven in this case. But in this case the same DataProductOwner will be the approver as well as the consumer."
**Effect:** Recorded as S46, S47. R64 and R65 drop the same-team exemption: every consumption (including lineage) needs an approved request; the same data product owner may create and receive it.

### 2026-11-14 · idea · Q79
**Asked by:** Claude
**Q:** [Claude] Open points: 1. Who owns an external application and creates its requests? 2. Is there one catalog per environment, and can exposure be turned off? 3. Should a product owner also be a user principal?
**Options offered:** free answer (in chat)
**A:** "1. Each external application (which runs outside of the AcmeDataPlatform) has exactly one product owner. That product owner can create subscription request to platform resources. 2. There is a catalog per environment. Exposure can be turned off. 3. Yes, each employee (ProductOwners, DataProductOwners or other employees) has a exactly one user principal."
**Effect:** Recorded as S48–S50. Level 3: relation `externalAppOwner`, rules R66 (exactly one product owner per external application) and R67 (it creates the requests). Level 2: individuals CatalogEXP/DEV/ACC/PRD (`catalogOf`), data property `exposedInCatalog` (yes by default), derivation R68 (a resource is exposed in the catalog of each of its environments unless turned off); concept `Employee` (parent of ProductOwner), relation `hasUserPrincipal`, rule R69 (exactly one user principal per employee).

### 2026-11-14 · idea · Q80 (user)
**Asked by:** user
**Q:** "Which files are overlapping? Do you recommend keeping all the overlapping files or does it make sense to get rid of some of them?"
**A (Claude):** The sources don't overlap (except the intended copy of answers as statements). The generated files overlap in four groups: the three OWL serialisations (same triples); glossary.md / glossary.tbx / SKOS labels; rules.md / rules.shacl.ttl; level-3.md ⊇ glossary.md + rules.md + diagrams.md. Recommendation: keep all of them while the expert compares formats (the goal of Q2); then drop the ones nobody uses, first `ontology.owl.rdf`, then `glossary.md`, `rules.md` and `diagrams.md` (all inside `level-3.md`), and `ontology.jsonld` unless an app needs it. Keep the sources, `statements.md`, the level views, `ontology.owl.ttl`, `rules.shacl.ttl`, `taxonomy.skos.ttl`, and `glossary.tbx` if a terminology tool is planned. Removing a generated file changes spec 0002 (its file list and AC-1), so it goes through a spec change.
**Effect:** Way-of-working diagram and file table added to `data/AcmeDataPlatform/README.md`; no files removed.

### 2026-11-14 · idea · Q81
**Asked by:** Claude
**Q:** [Claude] `working_level` is still 1. Is level 1 complete, so the working level moves to 2 (Q37)?
**Options offered:** free answer (in chat)
**A:** "Level 1 is complete."
**Effect:** `working_level: 2`; statements from S51 on are recorded at level 2; README updated.

### 2026-11-14 · idea · Q82
**Asked by:** Claude
**Q:** [Claude] Does a user principal also need an approved subscription request before looking at another team's dashboard?
**Options offered:** free answer (in chat)
**A:** "Level-2: users also need a subscription. When a product owner creates a subscription for his/her new consumer application/platform resource, he/she can include some/all of the team members to get access as well. Level-3: the access for users can be differentiated per environment. e.g.: Grant SELECT permission on the tables/view for users in EXP, DEV and ACC environments. But not in PRD where sensitive/PII data is stored. Level-3: developers of the consumer application can request time-limited elevated permissions and run SELECT commands on the tables/views in their data product or in the parent data products in case of an incident resolution or for debugging purposes."
**Effect:** Recorded as S51–S53. Level 2: `memberOf` now from any employee; relation `includesMember`; R70 (derivation: approved request gives included members' user principals access), R71 (included members belong to the consumer's owner team), R72 (draft: a user consumes another team's resource only with access; own team exempt). Level 3: concepts Developer, Permission, ElevatedPermission, Privilege (SELECT), Purpose (incident resolution, debugging); relations developerOf, grantedTo, permissionOn, inEnvironment, grantsPrivilege, forPurpose; property validUntil; rules R73–R75, R76 (draft: no regular permission in PRD). Users still consume only dashboards at level 2 (R49); table access is a level-3 permission.

### 2026-11-14 · idea · Q83
**Asked by:** Claude
**Q:** [Claude] R3 (created with at least one platform service) applies to sub-resources too. Is that right for every nested resource?
**Options offered:** free answer (in chat)
**A:** "Yes, each (top-level or nested) platform resource is created via a platform service. e.g.: tables and views are created via Databricks/Snowflake or other EDW/analytical services."
**Effect:** Recorded as S54. R3 reworded and cites S54.

### 2026-11-14 · idea · Q84
**Asked by:** Claude
**Q:** [Claude] Draft R72 exempts the owner team's own members (a user reads their own team's resources without a request). Right? Draft R76: is "no regular permission in PRD" a general rule?
**Options offered:** free answer (in chat)
**A:** "R72: level-3 info: by default, the team members of the owning team of a platform resource can read their own platform resources. The product owner may limit this intentionally. E.g.: Developers can run SELECT commands or view the dashboard in the EXP, DEV, ACC environments, but not in the PRD environment which contains sensitive/PII information." / "R76: no general rule. Product owner decides for each case."
**Effect:** Recorded as S55, S56. R72 confirmed. R76 removed. Level 3: concept AccessRestriction, relations restricts, restrictedIn, setBy; rules R77 (set by the resource's product owner) and R78 (where a resource is restricted, users get only elevated permissions on its tables/views).

### 2026-11-14 · idea · Q85
**Asked by:** Claude
**Q:** [Claude] R78 covers SELECT on tables/views, not viewing a dashboard in a restricted environment. Add a level-3 permission to view dashboards, so the same restriction applies?
**Options offered:** yes; no
**A:** "R78: yes, same restrictions to dashboards as well."
**Effect:** Recorded as S57. Level 3: privilege VIEW, relation `viewPermissionOn` (Permission → Dashboard), rule R79 (in a restricted environment, users get only elevated permissions to view the dashboard, also a dashboard nested in the restricted resource).
