"""Property-path mini-language → SHACL paths and SPARQL property paths (plan 0002, T4)."""

from __future__ import annotations

import pytest
from domain_model.paths import PathSyntaxError, names, parse_path, to_shacl, to_sparql
from rdflib import RDF, BNode, Graph, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import SH

EX = Namespace("https://example.org/x#")


def _resolve(name: str) -> URIRef:
    return RDF.type if name == "a" else EX[name]


@pytest.mark.parametrize(
    ("text", "sparql"),
    [
        ("p", "ex:p"),
        ("a", "rdf:type"),
        ("p/q", "ex:p/ex:q"),
        ("^p", "^ex:p"),
        ("p*", "ex:p*"),
        ("p+", "ex:p+"),
        ("p?", "ex:p?"),
        ("p|q", "ex:p|ex:q"),
        ("(p|q)/r", "(ex:p|ex:q)/ex:r"),
        ("^(p/q)*", "^(ex:p/ex:q)*"),
        (" p / ^q ", "ex:p/^ex:q"),
    ],
)
def test_sparql_rendering(text: str, sparql: str) -> None:
    assert to_sparql(parse_path(text), lambda n: "rdf:type" if n == "a" else f"ex:{n}") == sparql


@pytest.mark.parametrize("text", ["", "p/", "/p", "(p", "p)", "p||q", "p**", "1p", "p q", "^"])
def test_syntax_errors(text: str) -> None:
    with pytest.raises(PathSyntaxError):
        parse_path(text)


def test_names_collects_every_identifier() -> None:
    assert names(parse_path("(p|^q)/r*/a")) == {"p", "q", "r", "a"}


def test_shacl_single_predicate_is_the_iri() -> None:
    assert to_shacl(Graph(), parse_path("p"), _resolve) == EX.p


def test_shacl_sequence_is_a_list() -> None:
    g = Graph()
    node = to_shacl(g, parse_path("p/q"), _resolve)
    assert isinstance(node, BNode)
    assert list(Collection(g, node)) == [EX.p, EX.q]


@pytest.mark.parametrize(
    ("text", "predicate"),
    [("^p", SH.inversePath), ("p*", SH.zeroOrMorePath), ("p+", SH.oneOrMorePath), ("p?", SH.zeroOrOnePath)],
)
def test_shacl_unary_paths(text: str, predicate: URIRef) -> None:
    g = Graph()
    node = to_shacl(g, parse_path(text), _resolve)
    assert g.value(node, predicate) == EX.p


def test_shacl_alternative() -> None:
    g = Graph()
    node = to_shacl(g, parse_path("p|q"), _resolve)
    alternatives = g.value(node, SH.alternativePath)
    assert alternatives is not None
    assert list(Collection(g, alternatives)) == [EX.p, EX.q]
