"""The property-path mini-language of rules → SHACL path nodes and SPARQL property paths.

Grammar (SPARQL 1.1 property-path precedence)::

    alt     := seq ('|' seq)*
    seq     := elt ('/' elt)*
    elt     := '^'? primary ('*' | '+' | '?')?
    primary := name | '(' alt ')'

``name`` is a relation or property id, or ``a`` for rdf:type.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass

from rdflib import BNode, Graph, Node, URIRef
from rdflib.collection import Collection
from rdflib.namespace import SH


class PathSyntaxError(ValueError):
    """The path text does not follow the grammar."""


@dataclass(frozen=True)
class Name:
    name: str


@dataclass(frozen=True)
class Inverse:
    path: Path


@dataclass(frozen=True)
class Repeat:
    path: Path
    op: str  # '*', '+' or '?'


@dataclass(frozen=True)
class Sequence:
    parts: tuple[Path, ...]


@dataclass(frozen=True)
class Alternative:
    parts: tuple[Path, ...]


Path = Name | Inverse | Repeat | Sequence | Alternative

_TOKEN = re.compile(r"\s*(?:([A-Za-z][A-Za-z0-9_]*)|([/|^*+?()]))")


def _tokenize(text: str) -> list[str]:
    symbols: list[str] = []
    pos = 0
    text = text.rstrip()
    while pos < len(text):
        match = _TOKEN.match(text, pos)
        if match is None:
            raise PathSyntaxError(f"unexpected character at position {pos + 1} in path {text!r}")
        symbols.append(match.group(1) or match.group(2))
        pos = match.end()
    return symbols


class _Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.symbols = _tokenize(text)
        self.pos = 0

    def _peek(self) -> str | None:
        return self.symbols[self.pos] if self.pos < len(self.symbols) else None

    def _next(self) -> str:
        symbol = self._peek()
        if symbol is None:
            raise PathSyntaxError(f"path {self.text!r} ends too early")
        self.pos += 1
        return symbol

    def parse(self) -> Path:
        path = self._alt()
        if self._peek() is not None:
            raise PathSyntaxError(f"unexpected {self._peek()!r} in path {self.text!r}")
        return path

    def _alt(self) -> Path:
        parts = [self._seq()]
        while self._peek() == "|":
            self._next()
            parts.append(self._seq())
        return parts[0] if len(parts) == 1 else Alternative(tuple(parts))

    def _seq(self) -> Path:
        parts = [self._elt()]
        while self._peek() == "/":
            self._next()
            parts.append(self._elt())
        return parts[0] if len(parts) == 1 else Sequence(tuple(parts))

    def _elt(self) -> Path:
        inverse = self._peek() == "^"
        if inverse:
            self._next()
        path = self._primary()
        if self._peek() in ("*", "+", "?"):
            path = Repeat(path, self._next())
        return Inverse(path) if inverse else path

    def _primary(self) -> Path:
        symbol = self._next()
        if symbol == "(":
            path = self._alt()
            if self._next() != ")":
                raise PathSyntaxError(f"missing ')' in path {self.text!r}")
            return path
        if not symbol[0].isalpha():
            raise PathSyntaxError(f"expected a name, got {symbol!r} in path {self.text!r}")
        return Name(symbol)


def parse_path(text: str) -> Path:
    """Parse ``text``; raises :class:`PathSyntaxError` if it does not follow the grammar."""
    return _Parser(text).parse()


def names(path: Path) -> set[str]:
    """Every relation/property name the path uses."""
    match path:
        case Name(name):
            return {name}
        case Inverse(inner) | Repeat(inner, _):
            return names(inner)
        case Sequence(parts) | Alternative(parts):
            return set().union(*(names(p) for p in parts))


def is_single(path: Path) -> bool:
    """True when the path is one plain predicate."""
    return isinstance(path, Name)


_SHACL_REPEAT = {"*": SH.zeroOrMorePath, "+": SH.oneOrMorePath, "?": SH.zeroOrOnePath}


def _shacl_list(graph: Graph, items: list[Node]) -> BNode:
    head = BNode()
    Collection(graph, head, items)
    return head


def to_shacl(graph: Graph, path: Path, resolve: Callable[[str], URIRef]) -> Node:
    """Add the SHACL path for ``path`` to ``graph`` and return its root node."""
    match path:
        case Name(name):
            return resolve(name)
        case Sequence(parts):
            return _shacl_list(graph, [to_shacl(graph, p, resolve) for p in parts])
        case Alternative(parts):
            node = BNode()
            graph.add(
                (node, SH.alternativePath, _shacl_list(graph, [to_shacl(graph, p, resolve) for p in parts]))
            )
            return node
        case Inverse(inner):
            node = BNode()
            graph.add((node, SH.inversePath, to_shacl(graph, inner, resolve)))
            return node
        case Repeat(inner, op):
            node = BNode()
            graph.add((node, _SHACL_REPEAT[op], to_shacl(graph, inner, resolve)))
            return node


def _grouped(path: Path, render: Callable[[str], str]) -> str:
    text = to_sparql(path, render)
    return f"({text})" if isinstance(path, Sequence | Alternative) else text


def _seq_part(path: Path, render: Callable[[str], str]) -> str:
    return _grouped(path, render) if isinstance(path, Alternative) else to_sparql(path, render)


def to_sparql(path: Path, render: Callable[[str], str]) -> str:
    """The SPARQL property path; ``render`` turns a name into a prefixed name or ``<iri>``."""
    match path:
        case Name(name):
            return render(name)
        case Sequence(parts):
            return "/".join(
                _grouped(p, render) if isinstance(p, Alternative) else to_sparql(p, render) for p in parts
            )
        case Alternative(parts):
            return "|".join(to_sparql(p, render) for p in parts)
        case Inverse(inner):
            return "^" + _grouped(inner, render)
        case Repeat(inner, op):
            return _grouped(inner, render) + op
