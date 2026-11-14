"""``qg-boundaries``: fail when imports break the rules declared in ``components.json`` (ADR-0010, -0014).

Checks, at system level and inside every app:
- an app never imports another app; shared code never imports an app;
- a unit only depends on units in its ``mayDependOn``;
- another unit is imported only through its ``public`` entry points (if it declares any);
- no dependency cycles between units, declared or measured;
- every Python package in ``apps/`` or ``shared/`` is a uv workspace member.
"""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

from quality_gate.graph import ImportFacts, collect, cycles
from quality_gate.units import Level, Unit, all_levels, as_strings


def dependency_findings(level: Level, facts: ImportFacts) -> list[str]:
    by_name = {u.name: u for u in level.units}
    findings: list[str] = []
    for (a, b), pairs in sorted(facts.edges.items()):
        rule = _rule_broken(level, by_name[a], by_name[b])
        if rule:
            findings.append(f"[{level.name}] {rule} (e.g. {pairs[0][0]} -> {pairs[0][1]})")
        findings.extend(_internal_imports(level, by_name[a], by_name[b], pairs))
    return findings


def _rule_broken(level: Level, source: Unit, target: Unit) -> str:
    if level.is_system and source.kind == "app" and target.kind == "app":
        return f"app '{source.name}' imports app '{target.name}' (apps never depend on each other)"
    if level.is_system and source.kind == "shared" and target.kind == "app":
        return f"shared '{source.name}' imports app '{target.name}' (shared code never imports an app)"
    if target.name not in source.may_depend_on:
        return f"'{source.name}' depends on '{target.name}', which is not in its mayDependOn"
    return ""


def _internal_imports(level: Level, source: Unit, target: Unit, pairs: list[tuple[str, str]]) -> list[str]:
    if not target.public:
        return []
    return [
        f"[{level.name}] '{source.name}' imports internal module {imported} of '{target.name}' "
        f"(public: {', '.join(target.public)}; from {importer})"
        for importer, imported in sorted(set(pairs))
        if imported not in target.public
    ]


def cycle_findings(level: Level, facts: ImportFacts) -> list[str]:
    measured = [f"[{level.name}] import cycle: {' -> '.join(c)}" for c in cycles(list(facts.edges))]
    declared_edges = [(u.name, d) for u in level.units for d in u.may_depend_on]
    declared = [
        f"[{level.name}] declared cycle in mayDependOn: {' -> '.join(c)}" for c in cycles(declared_edges)
    ]
    return declared + measured


def declaration_findings(level: Level) -> list[str]:
    """App level only (the system level is validated by tools/monorepo/system-map.sh)."""
    if level.is_system:
        return []
    return _name_findings(level) + _path_findings(level)


def _name_findings(level: Level) -> list[str]:
    names = [u.name for u in level.units]
    findings = [f"[{level.name}] component '{n}' is declared twice" for n in set(names) if names.count(n) > 1]
    unknown = [(u.name, d) for u in level.units for d in u.may_depend_on if d not in names]
    return findings + [f"[{level.name}] '{u}' may depend on unknown component '{d}'" for u, d in unknown]


def _path_findings(level: Level) -> list[str]:
    prefix = f"apps/{level.name}/"
    outside = [
        (str(entry.get("name")), pattern)
        for entry in level.declared
        for pattern in as_strings(entry.get("paths"))
        if not pattern.startswith(prefix)
    ]
    return [f"[{level.name}] '{name}' path {pattern} is outside {prefix}" for name, pattern in outside]


UNIT_TOPS = ("apps", "shared")


def workspace_findings(repo: Path) -> list[str]:
    """Every Python package in apps/ or shared/ is a workspace member, and mypy checks every member."""
    return _code_without_project(repo) + _unregistered_projects(repo)


def _code_without_project(repo: Path) -> list[str]:
    inits = [p for top in UNIT_TOPS for p in repo.glob(f"{top}/*/src/*/__init__.py")]
    with_code = sorted({p.relative_to(repo).parts[:2] for p in inits})
    missing = [u for u in with_code if not (repo.joinpath(*u) / "pyproject.toml").is_file()]
    return [f"[workspace] {'/'.join(u)} has Python code but no pyproject.toml" for u in missing]


def _unregistered_projects(repo: Path) -> list[str]:
    tool = tomllib.loads((repo / "pyproject.toml").read_text()).get("tool", {})
    members = set(tool.get("uv", {}).get("workspace", {}).get("members", []))
    typed = set(tool.get("mypy", {}).get("files", []))
    tomls = [p for top in UNIT_TOPS for p in repo.glob(f"{top}/*/pyproject.toml")]
    projects = sorted(p.parent.relative_to(repo).as_posix() for p in tomls)
    unlisted = [
        f"[workspace] {p} is not in [tool.uv.workspace].members" for p in projects if p not in members
    ]
    untyped = [
        f"[workspace] {p}/src is not in [tool.mypy].files" for p in projects if f"{p}/src" not in typed
    ]
    return unlisted + untyped


def check(repo: Path) -> tuple[list[str], int]:
    findings = workspace_findings(repo)
    measured_units = 0
    for level in all_levels(repo):
        facts = collect(level)
        measured_units += sum(1 for u in level.units if u.modules)
        findings += (
            declaration_findings(level) + dependency_findings(level, facts) + cycle_findings(level, facts)
        )
    return findings, measured_units


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    repo = Path(args[0]) if args else Path.cwd()
    findings, measured = check(repo)
    for finding in findings:
        print(finding)
    if findings:
        print(f"qg-boundaries: {len(findings)} violation(s)", file=sys.stderr)
        return 1
    print(f"qg-boundaries: OK ({measured} unit(s) with Python code)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
