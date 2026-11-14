"""AC-4: is-a links in SKOS and Mermaid match parent/also_parents; extra trees reach diagrams.md."""

from __future__ import annotations

import pytest
from dm_fixtures import EXAMPLE_DIR, mermaid_blocks
from domain_model.load import load_domain
from domain_model.model import Domain
from domain_model.rdf.skos import skos_graph
from domain_model.text.mermaid import diagrams_md
from rdflib import RDF, SKOS, Graph, Namespace

LIB = Namespace("https://example.org/library#")


@pytest.fixture(scope="module")
def domain() -> Domain:
    loaded, _ = load_domain(EXAMPLE_DIR)
    assert loaded is not None
    return loaded


def _parent_pairs(domain: Domain) -> set[tuple[str, str]]:
    return {(c.id, p) for c in domain.ontology.concepts for p in c.parents}


def test_skos_broader_matches_parents(domain: Domain) -> None:
    graph = skos_graph(domain)
    broader = {(str(s)[len(LIB) :], str(o)[len(LIB) :]) for s, o in graph.subject_objects(SKOS.broader)}
    narrower = {(str(o)[len(LIB) :], str(s)[len(LIB) :]) for s, o in graph.subject_objects(SKOS.narrower)}
    assert broader == _parent_pairs(domain)
    assert narrower == broader


def test_skos_concepts_and_top_concepts(domain: Domain) -> None:
    graph: Graph = skos_graph(domain)
    concepts = {str(s)[len(LIB) :] for s in graph.subjects(RDF.type, SKOS.Concept)}
    assert concepts == {c.id for c in domain.ontology.concepts}
    tops = {str(s)[len(LIB) :] for s in graph.subjects(SKOS.topConceptOf, None)}
    assert tops == {c.id for c in domain.ontology.concepts if not c.parents}
    assert (LIB.Book, SKOS.prefLabel, None) in graph
    assert (LIB.Member, SKOS.altLabel, None) in graph


def _edges(block: list[str], arrow: str) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for line in block:
        parts = line.split(f" {arrow} ")
        if len(parts) == 2:
            found.add((parts[0], parts[1]))
    return found


def test_mermaid_is_a_edges_match_parents(domain: Domain) -> None:
    is_a = next(b for b in mermaid_blocks(diagrams_md(domain)) if b[0] == "flowchart BT")
    assert _edges(is_a, "-->") == _parent_pairs(domain)


def test_part_of_tree_in_diagrams(domain: Domain) -> None:
    text = diagrams_md(domain)
    assert "Library composition (part-of)" in text
    blocks = [b for b in mermaid_blocks(text) if any('"part of"' in line for line in b)]
    assert len(blocks) == 1
    assert {line for line in blocks[0] if "part of" in line} == {
        'Branch -->|"part of"| Library',
        'Shelf -->|"part of"| Branch',
    }


def test_ontology_graph_has_relations_and_is_a(domain: Domain) -> None:
    graph = next(b for b in mermaid_blocks(diagrams_md(domain)) if b[0] == "flowchart LR")
    assert 'Loan -->|"has item"| Item' in graph
    assert 'Book -.->|"is a"| Item' in graph
