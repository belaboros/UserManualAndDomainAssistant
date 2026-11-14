"""Build the import graph with grimp and lift it from modules to units."""

from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass, field

import grimp

from quality_gate.units import Level, Unit, owner

Edge = tuple[str, str]


@dataclass
class ImportFacts:
    """Imports between units: module pairs per unit edge, internal references, external packages."""

    edges: dict[Edge, list[Edge]] = field(default_factory=lambda: defaultdict(list))
    internal: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    modules: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    external: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))


def top_packages(units: tuple[Unit, ...]) -> list[str]:
    return sorted({m.split(".")[0] for u in units for m in u.modules})


def build_graph(units: tuple[Unit, ...]) -> grimp.ImportGraph | None:
    tops = top_packages(units)
    if not tops:
        return None
    for root in sorted({str(r) for u in units for r in u.roots}):
        if root not in sys.path:
            sys.path.insert(0, root)
    return grimp.build_graph(*tops, include_external_packages=True, cache_dir=None)


def collect(level: Level) -> ImportFacts:
    facts = ImportFacts()
    graph = build_graph(level.units)
    if graph is None:
        return facts
    tops = set(top_packages(level.units))
    for importer in sorted(graph.modules):
        source = owner(importer, level.units)
        if source is None:
            continue
        facts.modules[source.name].add(importer)
        for imported in graph.find_modules_directly_imported_by(importer):
            _record(facts, source, importer, imported, level.units, tops)
    return facts


def _record(  # noqa: PLR0913 - one call site; the arguments are the edge and its context
    facts: ImportFacts, source: Unit, importer: str, imported: str, units: tuple[Unit, ...], tops: set[str]
) -> None:
    target = owner(imported, units)
    if target is None:
        if imported.split(".")[0] not in tops:
            facts.external[source.name].add(imported.split(".")[0])
        return
    if target.name == source.name:
        facts.internal[source.name] += 1
    else:
        facts.edges[(source.name, target.name)].append((importer, imported))


def cycles(edges: list[Edge]) -> list[list[str]]:
    """Strongly connected components with more than one node, each closed (``[a, b, a]``)."""
    adjacency: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        adjacency[a].append(b)
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    found: list[list[str]] = []

    def visit(node: str) -> None:
        index[node] = low[node] = len(index)
        stack.append(node)
        for nxt in adjacency[node]:
            if nxt not in index:
                visit(nxt)
                low[node] = min(low[node], low[nxt])
            elif nxt in stack:
                low[node] = min(low[node], index[nxt])
        if low[node] == index[node]:
            component = []
            while True:
                member = stack.pop()
                component.append(member)
                if member == node:
                    break
            if len(component) > 1:
                ordered = sorted(component)
                found.append([*ordered, ordered[0]])

    for node in sorted(set(adjacency) | {b for _, b in edges}):
        if node not in index:
            visit(node)
    return sorted(found)
