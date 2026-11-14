"""Deterministic Turtle, RDF/XML and JSON-LD output (FR-2, FR-5; plan 0002, "Approach" step 4).

1. Blank nodes get content-derived ids (``rdflib.compare.to_canonical_graph``).
2. The graph is rebuilt by inserting its triples in sorted order (the memory store keeps insertion order).
3. JSON-LD is post-sorted: node arrays by ``@id``, value arrays by their JSON text (``@list`` keeps order).

RDF/XML uses the plain ``xml`` writer (``pretty-xml`` duplicated shared lists in v0.1). That writer
visits subjects in hash order, so its top-level ``rdf:Description`` blocks are sorted afterwards; this
is safe because ``<`` inside literals is escaped, so a line starting with ``  <rdf:`` is always markup.
"""

from __future__ import annotations

import json
from typing import Any

from rdflib import Graph, Node
from rdflib.compare import to_canonical_graph

FORMATS = ("turtle", "xml", "json-ld")


def _sort_key(triple: tuple[Node, Node, Node]) -> tuple[str, str, str]:
    s, p, o = triple
    return (s.n3(), p.n3(), o.n3())


def canonical(graph: Graph) -> Graph:
    """A copy of ``graph`` with canonical blank nodes and triples inserted in sorted order."""
    result = Graph(bind_namespaces="none")
    for prefix, ns in sorted(graph.namespaces()):
        result.bind(prefix, ns, override=True)
    for triple in sorted(to_canonical_graph(graph), key=_sort_key):
        result.add(triple)
    return result


def _sorted_json(node: Any, key: str = "") -> Any:
    if isinstance(node, dict):
        return {k: _sorted_json(v, k) for k, v in node.items()}
    if isinstance(node, list):
        items = [_sorted_json(v) for v in node]
        if key == "@list":
            return items
        return sorted(items, key=_json_key)
    return node


def _json_key(value: Any) -> tuple[str, str]:
    node_id = str(value.get("@id", "")) if isinstance(value, dict) else ""
    return node_id, json.dumps(value, sort_keys=True)


def _sorted_rdfxml(text: str) -> str:
    """Sort the top-level ``rdf:Description`` blocks of the plain ``xml`` writer's output."""
    lines = text.splitlines()
    first = next((i for i, line in enumerate(lines) if line.startswith("  <rdf:Description")), None)
    if first is None:
        return text
    last = max(i for i, line in enumerate(lines) if line.startswith("</rdf:RDF>"))
    blocks: list[list[str]] = []
    for line in lines[first:last]:
        if line.startswith("  <rdf:Description"):
            blocks.append([])
        blocks[-1].append(line)
    body = [line for block in sorted(blocks) for line in block]
    return "\n".join([*lines[:first], *body, *lines[last:]]) + "\n"


def _jsonld(graph: Graph) -> str:
    context = {prefix: str(ns) for prefix, ns in sorted(graph.namespaces())}
    data = json.loads(graph.serialize(format="json-ld", context=context, auto_compact=True))
    return json.dumps(_sorted_json(data), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def serialize(graph: Graph, fmt: str, header: str) -> bytes:
    """``graph`` in ``fmt`` (one of :data:`FORMATS`), with ``header`` as a comment where the format allows."""
    stable = canonical(graph)
    if fmt == "turtle":
        text = f"# {header}\n\n" + stable.serialize(format="turtle")
    elif fmt == "xml":
        declaration, _, body = _sorted_rdfxml(stable.serialize(format="xml")).partition("\n")
        text = f"{declaration}\n<!-- {header} -->\n{body}"
    elif fmt == "json-ld":
        text = _jsonld(stable)  # JSON cannot hold a comment
    else:
        raise ValueError(f"unknown format {fmt}")
    return text.encode("utf-8")
