# ADR-0014: Introduce Python and its quality gate

- **Status:** accepted
- **Scope:** system
- **Date:** 2026-11-14
- **Related:** [ADR-0005](0005-modularity-metrics.md), [ADR-0006](0006-enforce-modularity-per-language.md), [ADR-0008](0008-security-checks-for-a-public-repository.md), [ADR-0010](0010-monorepo-of-loosely-coupled-applications.md); idea [0001](../../ideas/0001-acme-data-platform-domain-model.md) Q39–Q42

## Context
Python is the first programming language in this repository. It is needed for a domain-model generator (idea 0001, Q39) and is the likely language for the apps. ADR-0006 requires that a language only enters the codebase together with its quality gate: complexity limits, boundary rules derived from `components.json`, a metrics collector that emits the common snapshot schema, and hooks at three layers (Claude, pre-commit, CI), plus the security checks of ADR-0008.

The repository is a monorepo (ADR-0010): every app and shared component may become its own Python package, and one command has to lint, type-check, test and audit all of them. Boundaries exist at two levels: between apps and shared components (root `components.json`) and between the components inside one app (`apps/<app>/docs/architecture/components.json`). A shared component may declare `public` entry points; everything else is internal.

## Decision
We will use, pinned at these versions (latest stable on 2026-11-14):

| Need | Tool | Version | Notes |
|------|------|---------|-------|
| Interpreter | CPython | 3.15 (3.15.2) | `requires-python = ">=3.15"`, `.python-version`; latest stable (Q41) |
| Packages, workspace, lockfile | uv | 0.13.8 | root `pyproject.toml` is a virtual workspace root; every Python package (app, shared component, tool) is a `[tool.uv.workspace]` member; one committed `uv.lock` (Q40) |
| Lint, complexity, static security | ruff | 0.17.5 | `C901` fails above CC 15; `PLR0912` branches, `PLR0913` arguments (max 5), `PLR0915` statements, `PLR1702` nesting depth (max 4); `S` (bandit) rules for security; formatter |
| Types | mypy | 2.4.1 | `strict = true` (Q42) |
| CC report (warn band 11–15) | radon | 6.0.1 | used by the metrics collector |
| Import graph, boundaries, cycles, Ca/Ce | grimp | 3.20 | custom checker `qg-boundaries` in `tools/quality/python/` |
| Tests | pytest | 9.2.0 | |
| Dependency audit | pip-audit | 2.10.1 | audits the synced environment |
| Hook runner | pre-commit | 4.7.0 | already used for the security hooks |

The gate code lives in the workspace member `tools/quality/python` (package `quality_gate`):
- `qg-boundaries` reads the root and every app `components.json` **at run time** (there is no generated config to keep in sync) and fails on: an app importing another app, a dependency not in `mayDependOn`, shared code importing an app, an import of a non-`public` module of another unit, a dependency cycle between units, a declared app-level cycle or unknown component, and a Python package in `apps/` or `shared/` that is not a workspace member.
- `qg-metrics <components.json>` emits the snapshot schema of `docs/architecture/metrics/README.md` (CC from radon; Ca, Ce, I, relational cohesion, abstractness from grimp and `ast`).
- `qg-arch-render` is the shared, language-independent merge/render step used by `/arch-metrics` (ADR-0006 follow-up): it merges the per-language snapshots of one level, writes `history/<date>.json` and `latest.md`, and regenerates the coupling diagram in `architecture.md`.

Conventions: Python code lives in `src/<package>/` inside its app or shared folder; a unit's modules are the packages under its `paths`.

Hooks: a Claude `PostToolUse` hook runs ruff on every edited Python file and blocks with the findings; `pre-commit` runs ruff, ruff-format, mypy, `qg-boundaries`, pytest and pip-audit; a CI job `python` (`.github/workflows/python.yml`) runs the same gate on push and PR with read-only permissions and SHA-pinned actions; Dependabot watches the `uv` ecosystem with the 7-day cooldown.

## Alternatives considered
| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| import-linter contracts generated from `components.json` (playbook default) | Mature, declarative, readable config | Cannot express "only through `public` entry points" without one hand-tuned contract per consumer; needs a generator plus a separate cycle check; a second graph next to the collector's | A grimp-based checker reads `components.json` directly, covers all rules, and shares one graph with the metrics collector |
| pip + venv (+ pip-tools) | No extra tool | No workspace feature; a script must loop over packages; slower | uv is installed, fast and has workspaces (Q40) |
| Poetry | Popular | Not installed; no native multi-package workspace | Q40 |
| Python 3.13 floor | Widest compatibility | Not the latest stable | User asked for the latest stable (Q41) |
| pyright strict | Fast, strict | PyPI package downloads Node.js at runtime | Q42 |
| bandit as a separate tool | Reference security linter | One more tool; ruff `S` rules cover the same checks | Fewer tools, same coverage |
| lizard for CC | Multi-language | radon is the Python standard and lighter | — |

## Consequences
- **Positive:** Python can be written now; every Python file is linted while Claude edits it, again on commit and in CI; boundary rules follow `components.json` automatically; `/arch-metrics` has a collector and a renderer.
- **Negative / trade-offs:** the boundary checker is our own code (about a few hundred lines, tested) instead of a maintained tool; ruff cannot warn at CC 11–15, so the warn band is reported by `qg-metrics` / `/arch-metrics`, not blocked; Python 3.15 is new, so some libraries may lag.
- **Follow-up:** `tools/quality/languages.json` entry; root `pyproject.toml`, `.python-version`, `uv.lock`; `.pre-commit-config.yaml`, `.claude/settings.json`, `.github/workflows/python.yml`, `.github/dependabot.yml`; commands in the root `CLAUDE.md`; a new app or shared component with Python code adds itself to `[tool.uv.workspace].members`; baseline `/arch-metrics` snapshot.
