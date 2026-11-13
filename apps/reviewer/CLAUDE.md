# App: reviewer

This file adds to the root `CLAUDE.md`; everything there applies here too. Purpose: _TBD: one sentence; refined by /spec._

## Where things live for this app

| Path | What it holds |
|------|---------------|
| `apps/reviewer/docs/architecture/architecture.md` | This app's internal architecture: its components and runtime flows |
| `apps/reviewer/docs/architecture/components.json` | This app's components and their allowed dependencies (paths are relative to the repo root) |
| `apps/reviewer/docs/architecture/adr/` | Decisions that concern this app only, cited as `reviewer/ADR-NNNN` |
| `apps/reviewer/docs/specs/` | Specs whose scope is this app only. Ideas always live in the root `docs/ideas/` |
| `apps/reviewer/.env.example` | Variables this app adds to, or overrides in, the root `.env.example` |

## Rules specific to working in an app

1. **Never import from another app.** Use shared code from `shared/` (listed in this app's `mayDependOn` in the root `docs/architecture/components.json`) or a shared dataset through its contract.
2. **Shared data goes through contracts.** This app writes only the datasets it owns and reads others only as described in `shared/contracts/<dataset>/`. A new read or write is a change to the root `components.json` (and possibly a root ADR).
3. **Decide where a decision belongs.** If it changes anything another app can see (a contract, shared code, a base env variable, repo tooling), it is a root ADR; otherwise an app ADR here.
4. **Configuration comes from the environment**, loaded by `tools/env/with-env.sh reviewer`. Never read `.env` files from code paths of your own, never hard-code secrets.

## Commands

_Build, test, lint and run commands for this app: added by `/plan` and `/add-language`._
