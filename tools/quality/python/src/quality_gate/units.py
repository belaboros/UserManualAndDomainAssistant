"""Read ``components.json`` files and find the Python modules that belong to each unit.

A *unit* is an app or shared component (system level) or a component inside one app (app level).
Python code lives in ``src/<package>/``; a unit owns the packages found under its ``paths``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

SYSTEM_COMPONENTS = Path("docs/architecture/components.json")
SKIP_DIRS = {".venv", "node_modules", "__pycache__", ".git"}


@dataclass(frozen=True)
class Unit:
    name: str
    kind: str  # "app" | "shared" | "component"
    may_depend_on: tuple[str, ...]
    modules: tuple[str, ...]  # top modules owned by the unit (dotted)
    public: tuple[str, ...]  # public modules (dotted); empty = everything is public
    roots: tuple[Path, ...]  # import roots (the ``src`` folders)
    package_dirs: tuple[Path, ...]

    def python_files(self) -> list[Path]:
        return sorted(f for d in self.package_dirs for f in d.rglob("*.py") if not _skipped(f))


@dataclass(frozen=True)
class Level:
    name: str  # "system" or the app name
    components_file: Path
    is_system: bool
    units: tuple[Unit, ...]
    declared: tuple[dict[str, object], ...]  # raw component entries, for declaration checks


def _skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def is_package(directory: Path) -> bool:
    return (directory / "__init__.py").is_file()


def module_of_dir(directory: Path) -> tuple[str, Path]:
    """Dotted module name of a package directory, and its import root."""
    parts: list[str] = []
    current = directory
    while is_package(current):
        parts.insert(0, current.name)
        current = current.parent
    return ".".join(parts), current


def module_of_file(path: Path) -> str:
    if path.name == "__init__.py":
        return module_of_dir(path.parent)[0]
    package, _ = module_of_dir(path.parent)
    return f"{package}.{path.stem}" if package else path.stem


def glob_base(pattern: str, repo: Path) -> Path:
    fixed: list[str] = []
    for part in Path(pattern).parts:
        if any(ch in part for ch in "*?["):
            break
        fixed.append(part)
    return repo.joinpath(*fixed)


def top_package_dirs(base: Path) -> list[Path]:
    """Package directories under ``base`` that are top-level inside a ``src`` import root."""
    if not base.is_dir():
        return []
    if is_package(base):
        return [base]
    found = []
    for init in base.rglob("__init__.py"):
        package = init.parent
        if _skipped(package) or is_package(package.parent):
            continue
        if package.parent.name == "src":
            found.append(package)
    return sorted(found)


def _unit(entry: dict[str, object], kind: str, repo: Path) -> Unit:
    dirs: list[Path] = []
    for pattern in as_strings(entry.get("paths")):
        dirs.extend(top_package_dirs(glob_base(pattern, repo)))
    named = [module_of_dir(d) for d in dirs]
    public = tuple(module_of_file(repo / p) for p in as_strings(entry.get("public")))
    return Unit(
        name=str(entry["name"]),
        kind=kind,
        may_depend_on=tuple(as_strings(entry.get("mayDependOn"))),
        modules=tuple(sorted({m for m, _ in named})),
        public=public,
        roots=tuple(sorted({r for _, r in named})),
        package_dirs=tuple(sorted(set(dirs))),
    )


def as_strings(value: object) -> list[str]:
    """A JSON list as strings; anything else as an empty list."""
    return [str(v) for v in value] if isinstance(value, list) else []


def load_level(components_file: Path, repo: Path) -> Level:
    data = json.loads((repo / components_file).read_text())
    entries = tuple(e for e in data.get("components", []) if isinstance(e, dict))
    is_system = components_file == SYSTEM_COMPONENTS
    units = tuple(_unit(e, str(e.get("kind", "")) if is_system else "component", repo) for e in entries)
    name = "system" if is_system else components_file.parts[1]
    return Level(name, components_file, is_system, units, entries)


def all_levels(repo: Path) -> list[Level]:
    levels = [load_level(SYSTEM_COMPONENTS, repo)]
    for app_file in sorted(repo.glob("apps/*/docs/architecture/components.json")):
        levels.append(load_level(app_file.relative_to(repo), repo))
    return levels


def owner(module: str, units: tuple[Unit, ...]) -> Unit | None:
    """The unit owning ``module`` (longest matching module prefix)."""
    best: Unit | None = None
    best_len = -1
    for unit in units:
        for top in unit.modules:
            if (module == top or module.startswith(top + ".")) and len(top) > best_len:
                best, best_len = unit, len(top)
    return best
