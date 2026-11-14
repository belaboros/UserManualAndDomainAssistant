"""AC-7, AC-10 (SHACL): one node shape per rule, for every pattern (plan 0002, T9)."""

from __future__ import annotations

from pathlib import Path

import pytest
from dm_fixtures import EXAMPLE_DIR, copy_example, item, mutate
from domain_model.load import load_domain
from domain_model.model import Domain, Rule
from domain_model.rdf.owl import owl_graph
from domain_model.rdf.shacl import shacl_graph
from pyshacl import validate
from rdflib import DCTERMS, RDF, Graph, Literal, Namespace
from rdflib.namespace import SH

LIB = Namespace("https://example.org/library#")
PREFIXES = """
PREFIX lib: <https://example.org/library#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""


def _load(folder: Path = EXAMPLE_DIR) -> Domain:
    domain, findings = load_domain(folder)
    assert domain is not None, findings
    return domain


@pytest.fixture(scope="module")
def graph() -> Graph:
    return shacl_graph(_load())


@pytest.mark.parametrize("rule", _load().ontology.rules, ids=lambda r: f"{r.id}-{r.pattern_key}")
def test_one_shape_per_rule_with_level(graph: Graph, rule: Rule) -> None:
    shape = LIB[f"{rule.id}_shape"]
    assert (shape, RDF.type, SH.NodeShape) in graph
    assert (shape, SH.targetClass, LIB[rule.pattern.focus]) in graph
    assert [int(v) for v in graph.objects(shape, LIB.level)] == [rule.level]  # type: ignore[call-overload]
    assert (shape, LIB.status, Literal(rule.status)) in graph
    assert {str(s) for s in graph.objects(shape, DCTERMS.source)} == set(rule.source)
    assert graph.value(shape, SH.message) is not None


# One ASK per pattern: the SHACL each pattern must produce (plan 0002, "Rule patterns").
PATTERNS = {
    "cardinality": "lib:R1_shape sh:property [ sh:path lib:hasItem ; sh:minCount 1 ; sh:maxCount 5 ] .",
    "values": "lib:R2_shape sh:property [ sh:path lib:hasStatus ; sh:in ?list ] .",
    "implies": "lib:R3_shape sh:or ( [ sh:not [ sh:path lib:hasStatus ; sh:hasValue lib:Returned ] ]"
    " [ sh:path lib:returnedOn ; sh:minCount 1 ] ) .",
    "equal_paths": "lib:R4_shape sh:sparql [ a sh:SPARQLConstraint ; sh:select ?q ; sh:prefixes ?p ] .",
    "derive_condition": "lib:R5_shape sh:rule [ a sh:TripleRule ; sh:subject sh:this ;"
    " sh:predicate rdf:type ; sh:object lib:OpenLoan ; sh:condition [ sh:path lib:hasStatus ] ] .",
    "derive_path": "lib:R6_shape sh:rule [ a sh:TripleRule ; sh:predicate lib:servedBy ;"
    " sh:object [ sh:path ( lib:hasItem lib:locatedIn ) ] ] .",
    "sparql_select": "lib:R7_shape sh:sparql [ a sh:SPARQLConstraint ; sh:select ?q ; sh:prefixes ?p ] .",
    "sparql_construct": "lib:R8_shape sh:rule [ a sh:SPARQLRule ; sh:construct ?q ; sh:prefixes ?p ] .",
    "prefixes": '?p sh:declare [ sh:prefix "lib" ; sh:namespace ?ns ] .',
}


@pytest.mark.parametrize("pattern", PATTERNS.values(), ids=PATTERNS.keys())
def test_pattern_shacl(graph: Graph, pattern: str) -> None:
    assert graph.query(f"{PREFIXES} ASK {{ {pattern} }}").askAnswer, pattern


def test_equal_single_relations_use_sh_equals(tmp_path: Path) -> None:
    folder = copy_example(tmp_path)
    mutate(folder, "ontology.yaml", lambda d: item(d, "rules", "R4")["equal"].update(right="hasParticipant"))
    graph = shacl_graph(_load(folder))
    shape = "lib:R4_shape sh:property [ sh:path lib:hasBorrower ; sh:equals lib:hasParticipant ]"
    query = f"{PREFIXES} ASK {{ {shape} }}"
    assert graph.query(query).askAnswer


def test_valid_sample_conforms() -> None:
    domain = _load()
    data = Graph().parse(EXAMPLE_DIR / "samples" / "valid.ttl")
    conforms, _, text = validate(
        data, shacl_graph=shacl_graph(domain), ont_graph=owl_graph(domain), inference="rdfs", advanced=True
    )
    assert conforms, text
