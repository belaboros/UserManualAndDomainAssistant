"""AC-9, AC-10: level views are filtered by level; every RDF resource and TBX entry carries its level."""

from __future__ import annotations

import xml.etree.ElementTree as ET  # noqa: S405 - parses our own generated output

import pytest
from dm_fixtures import EXAMPLE_DIR, mermaid_blocks
from domain_model.load import load_domain
from domain_model.model import Domain
from domain_model.rdf.owl import owl_graph
from domain_model.rdf.shacl import shacl_graph
from domain_model.rdf.skos import skos_graph
from domain_model.text.markdown import level_md
from domain_model.text.tbx import glossary_tbx
from rdflib import OWL, RDF, SKOS, Graph, Namespace
from rdflib.namespace import SH

LIB = Namespace("https://example.org/library#")
TBX = "{urn:iso:std:iso:30042:ed-2}"
SECTIONS = ["## Glossary", "## Taxonomy (is-a)", "## Library composition (part-of)", "## Relations"]
SECTIONS += ["## Properties", "## Rules", "## Diagrams"]


@pytest.fixture(scope="module")
def domain() -> Domain:
    loaded, _ = load_domain(EXAMPLE_DIR)
    assert loaded is not None
    return loaded


@pytest.mark.parametrize("level", [1, 2, 3])
def test_level_view_contains_only_items_up_to_level(domain: Domain, level: int) -> None:
    text = level_md(domain, level)
    glossary = text.split("## Glossary", 1)[1].split("\n## ", 1)[0]
    for entry in domain.ontology.items:
        assert (f"| `{entry.id}` |" in glossary) == (entry.level <= level), entry.id
    for rule in domain.ontology.rules:
        assert (f"### {rule.id} ·" in text) == (rule.level <= level), rule.id
    nodes = {line.split("[", 1)[0] for block in mermaid_blocks(text) for line in block if "[" in line}
    for concept in domain.ontology.concepts:
        assert (concept.id in nodes) == (concept.level <= level), concept.id


@pytest.mark.parametrize("level", [1, 2, 3])
def test_level_view_has_all_sections_and_diagrams(domain: Domain, level: int) -> None:
    text = level_md(domain, level)
    for heading in SECTIONS:
        assert f"\n{heading}\n" in text, heading
    kinds = [block[0] for block in mermaid_blocks(text)]
    assert "flowchart BT" in kinds
    assert "flowchart LR" in kinds
    assert domain.ontology.level_info(level).audience in text


@pytest.mark.parametrize("level", [1, 2, 3])
def test_level_view_shows_diagrams_first(domain: Domain, level: int) -> None:
    """Diagrams come right after the intro, before every text section: they are read faster."""
    text = level_md(domain, level)
    diagrams = text.index("\n## Diagrams\n")
    assert all(diagrams < text.index(f"\n{heading}\n") for heading in SECTIONS if heading != "## Diagrams")


def test_level_3_is_the_whole_domain(domain: Domain) -> None:
    text = level_md(domain, 3)
    assert all(f"| `{i.id}` |" in text for i in domain.ontology.items)


def test_multi_parent_concept_listed_under_each_parent(domain: Domain) -> None:
    tree = level_md(domain, 3).split("\n## Taxonomy (is-a)\n", 1)[1].split("\n## ", 1)[0]
    assert tree.count("`EBook`") == 2


def _levels(graph: Graph, node: object) -> list[int]:
    return [int(v) for v in graph.objects(node, LIB.level)]  # type: ignore[arg-type, call-overload]


def test_every_rdf_resource_has_exactly_one_level(domain: Domain) -> None:
    onto = domain.ontology
    owl, skos, shacl = owl_graph(domain), skos_graph(domain), shacl_graph(domain)
    expected = {LIB[i.id]: i.level for i in onto.items}
    typed = set()
    for kind in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.NamedIndividual):
        typed |= {s for s in owl.subjects(RDF.type, kind) if str(s).startswith(str(LIB))}
    assert typed == set(expected)
    for node, level in expected.items():
        assert _levels(owl, node) == [level], node
    for concept in onto.concepts:
        assert _levels(skos, LIB[concept.id]) == [concept.level]
    assert {s for s in skos.subjects(RDF.type, SKOS.Concept)} == {LIB[c.id] for c in onto.concepts}
    shapes = set(shacl.subjects(RDF.type, SH.NodeShape))
    assert shapes == {LIB[f"{r.id}_shape"] for r in onto.rules}
    for rule in onto.rules:
        assert _levels(shacl, LIB[f"{rule.id}_shape"]) == [rule.level]


def test_every_tbx_entry_has_level_note(domain: Domain) -> None:
    root = ET.fromstring(glossary_tbx(domain))  # noqa: S314 - our own output
    levels = {i.id: i.level for i in domain.ontology.items}
    for entry in root.iter(f"{TBX}conceptEntry"):
        notes = [n.text for n in entry.iter(f"{TBX}note") if (n.text or "").startswith("level: ")]
        assert notes == [f"level: {levels[entry.attrib['id']]}"]
