# Shared runtime data

Default location of the shared datasets at runtime (`SHARED_DATA_DIR=data` in the root `.env`). Everything in this folder except this README is git-ignored: datasets can be large, can contain personal data, and are reproduced by their owning app.

Each dataset lives in `data/<dataset>/`, has exactly one owning app (its only writer) and is described by its contract in [shared/contracts/](../shared/contracts/README.md) (ADR-0013). Point `SHARED_DATA_DIR` somewhere else (an absolute path, a mounted volume) to share data between machines or containers.

**Exception: curated domain models** ([ADR-0015](../docs/architecture/adr/0015-curated-domain-models-are-versioned-in-data.md)). A folder that holds a hand-authored domain model is source, not runtime data: it cannot be reproduced by an app, so it is versioned in git. Each one is un-ignored by its own `!/data/<Domain>/` line in `.gitignore`; every other folder here stays ignored. Such a folder holds YAML sources, `samples/` and a `generated/` folder written by the [domain-model tool](../tools/domain-model/README.md) (ADR-0016); `domain-model check --all` (pre-commit and CI) keeps them consistent. It is not a shared dataset and has no contract yet; one is added when an app first reads a domain model.

| Domain model | Idea |
|--------------|------|
| [AcmeDataPlatform/](AcmeDataPlatform/README.md) | [0001](../docs/ideas/0001-acme-data-platform-domain-model.md) |
