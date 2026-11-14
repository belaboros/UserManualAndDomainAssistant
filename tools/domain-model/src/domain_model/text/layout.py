"""Packing the is-a diagram towards a 16:9 (width:height) shape.

Mermaid (dagre) puts every separate is-a tree, and every concept without parent or children, side by
side in one row, so a domain with many of them renders very wide and very low. Here the trees are
stacked into columns; ``mermaid.is_a_diagram`` joins the trees of a column with invisible links
(``~~~``). Sizes are estimates in pixels from the label lengths, close to Mermaid's default theme.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from domain_model.model import Concept

TARGET_RATIO = 16 / 9
CHAR_PX = 8.0  # average width of one label character
NODE_PADDING_PX = 30.0  # box padding left and right
NODE_GAP_PX = 50.0  # horizontal space between nodes (dagre nodesep)
RANK_PX = 90.0  # one rank: node height plus vertical space (dagre ranksep)


@dataclass(frozen=True)
class Component:
    """One separate is-a tree: ``ids`` in input order, ``bottom`` a leaf, ``top`` a top concept."""

    ids: tuple[str, ...]
    bottom: str
    top: str
    width: int  # nodes in the widest rank
    height: int  # ranks
    px_width: float
    px_height: float


def _groups(concepts: list[Concept]) -> list[list[Concept]]:
    """Concepts grouped by is-a connectivity (undirected), in input order."""
    root = {c.id: c.id for c in concepts}

    def find(x: str) -> str:
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for c in concepts:
        for p in c.parents:
            if p in root:
                root[find(c.id)] = find(p)
    groups: dict[str, list[Concept]] = {}
    for c in concepts:
        groups.setdefault(find(c.id), []).append(c)
    return list(groups.values())


def _ranks(group: list[Concept]) -> dict[str, int]:
    """Rank as dagre assigns it for ``child --> parent``: leaves 0, a parent one above its highest child."""
    ids = {c.id for c in group}
    children: dict[str, list[str]] = {c.id: [] for c in group}
    for c in group:
        for p in c.parents:
            if p in ids:
                children[p].append(c.id)
    rank: dict[str, int] = {}

    def rank_of(x: str) -> int:
        if x not in rank:
            rank[x] = 1 + max((rank_of(ch) for ch in children[x]), default=-1)
        return rank[x]

    for c in group:
        rank_of(c.id)
    return rank


def _component(group: list[Concept]) -> Component:
    rank = _ranks(group)
    ids = {c.id for c in group}
    per_rank: dict[int, list[Concept]] = {}
    for c in group:
        per_rank.setdefault(rank[c.id], []).append(c)
    px_width = max(
        sum(len(c.label) * CHAR_PX + NODE_PADDING_PX + NODE_GAP_PX for c in row) for row in per_rank.values()
    )
    return Component(
        ids=tuple(c.id for c in group),
        bottom=next(c.id for c in group if rank[c.id] == 0),
        top=next(c.id for c in group if not [p for p in c.parents if p in ids]),
        width=max(len(row) for row in per_rank.values()),
        height=len(per_rank),
        px_width=px_width,
        px_height=len(per_rank) * RANK_PX,
    )


def tree_components(concepts: list[Concept]) -> list[Component]:
    """The separate is-a trees among ``concepts`` (a loose concept is a tree of one)."""
    return [_component(g) for g in _groups(concepts)]


def estimated_ratio(columns: list[list[Component]]) -> float:
    """Estimated width:height of the diagram when each column is drawn as one stack."""
    width = sum(max(c.px_width for c in column) for column in columns)
    height = max(sum(c.px_height for c in column) for column in columns)
    return width / height


def _size(c: Component) -> tuple[int, int, float]:
    """How complex a tree is: concepts, then ranks, then width."""
    return (len(c.ids), c.height, c.px_width)


def _flow(components: list[Component], max_height: float) -> list[list[Component]]:
    """Fill columns top to bottom, left to right; a new column starts when the next tree does not fit."""
    columns: list[list[Component]] = [[]]
    height = 0.0
    for c in components:
        if columns[-1] and height + c.px_height > max_height:
            columns.append([])
            height = 0.0
        columns[-1].append(c)
        height += c.px_height
    return columns


def pack_columns(components: list[Component]) -> list[list[Component]]:
    """Columns (each listed top to bottom, left to right) with the most complex tree first, in the top
    left corner, and smaller trees below it and to the right; the column height is the one whose
    estimated shape is closest to 16:9 (the tallest columns on a tie)."""
    if not components:
        return []
    ordered = sorted(components, key=_size, reverse=True)
    heights = sorted({sum(c.px_height for c in ordered[: i + 1]) for i in range(len(ordered))}, reverse=True)
    candidates = [_flow(ordered, h) for h in heights if h >= max(c.px_height for c in ordered)]
    return min(candidates, key=lambda cols: abs(math.log(estimated_ratio(cols) / TARGET_RATIO)))
