"""T1 smoke test: pyshacl with SHACL-AF runs on this interpreter (plan 0002, risks)."""

from __future__ import annotations

from pyshacl import validate
from rdflib import Graph

DATA = """
@prefix ex: <https://example.org/x#> .
ex:a a ex:Thing .
"""

SHAPES = """
@prefix ex: <https://example.org/x#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
ex:S a sh:NodeShape ; sh:targetClass ex:Thing ;
    sh:rule [ a sh:TripleRule ; sh:subject sh:this ; sh:predicate ex:seen ; sh:object ex:yes ] ;
    sh:property [ sh:path ex:name ; sh:minCount 1 ] .
"""


def test_pyshacl_validates_with_advanced_features() -> None:
    data = Graph().parse(data=DATA, format="turtle")
    shapes = Graph().parse(data=SHAPES, format="turtle")
    conforms, _, _ = validate(data, shacl_graph=shapes, advanced=True, inplace=True)
    assert conforms is False
    assert len(list(data.triples((None, None, None)))) == 2
