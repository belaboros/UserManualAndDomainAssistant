# assistant

_TBD: one sentence; refined by /spec._

| | |
|---|---|
| **Kind** | application in the monorepo ([system architecture](../../docs/architecture/architecture.md)) |
| **Instructions for Claude** | [CLAUDE.md](CLAUDE.md) (adds to the root [CLAUDE.md](../../CLAUDE.md)) |
| **Architecture** | [docs/architecture/architecture.md](docs/architecture/architecture.md) · [ADRs](docs/architecture/adr/README.md) |
| **Specs** | [docs/specs/](docs/specs/README.md) (specs that concern this app only) |
| **Environment** | [.env.example](.env.example), layered over the root [.env.example](../../.env.example) |

## Run

```bash
cp apps/assistant/.env.example apps/assistant/.env    # only if this app needs its own variables
tools/env/with-env.sh assistant --check
tools/env/with-env.sh assistant -- <command>          # the run command is added by /plan
```
