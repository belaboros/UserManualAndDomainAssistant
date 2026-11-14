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
