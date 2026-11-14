"""AC-11: draft items are marked in Markdown and carry their status in RDF and TBX (plan 0002, T13)."""

from __future__ import annotations

import xml.etree.ElementTree as ET  # noqa: S405 - parses our own generated output

import pytest
from dm_fixtures import EXAMPLE_DIR
from domain_model.load import load_domain
from domain_model.model import Domain
from domain_model.rdf.owl import owl_graph
from domain_model.rdf.shacl import shacl_graph
from domain_model.rdf.skos import skos_graph
from domain_model.text.markdown import glossary_md, level_md, rules_md
from domain_model.text.tbx import glossary_tbx
from rdflib import Literal, Namespace

LIB = Namespace("https://example.org/library#")
TBX = "{urn:iso:std:iso:30042:ed-2}"


@pytest.fixture(scope="module")
def domain() -> Domain:
    loaded, _ = load_domain(EXAMPLE_DIR)
    assert loaded is not None
    return loaded


def test_draft_marked_in_markdown(domain: Domain) -> None:
    drafts = [i for i in domain.ontology.items if i.status == "draft"]
    assert drafts
    texts = [glossary_md(domain), level_md(domain, 3)]
    for entry in drafts:
        for text in texts:
            assert f"{entry.label} _(draft)_" in text, entry.id
    confirmed = next(i for i in domain.ontology.items if i.status == "confirmed")
    assert f"{confirmed.label} _(draft)_" not in texts[0]
    draft_rules = [r for r in domain.ontology.rules if r.status == "draft"]
    assert draft_rules
    for rule in draft_rules:
        assert f"### {rule.id} · {rule.statement} _(draft)_" in rules_md(domain)


def test_draft_status_in_rdf_and_tbx(domain: Domain) -> None:
    owl, skos, shacl = owl_graph(domain), skos_graph(domain), shacl_graph(domain)
    for entry in domain.ontology.items:
        assert (LIB[entry.id], LIB.status, Literal(entry.status)) in owl
    for concept in domain.ontology.concepts:
        assert (LIB[concept.id], LIB.status, Literal(concept.status)) in skos
    for rule in domain.ontology.rules:
        assert (LIB[f"{rule.id}_shape"], LIB.status, Literal(rule.status)) in shacl
    root = ET.fromstring(glossary_tbx(domain))  # noqa: S314 - our own output
    statuses = {i.id: i.status for i in domain.ontology.items}
    for element in root.iter(f"{TBX}conceptEntry"):
        assert f"status: {statuses[element.attrib['id']]}" in [n.text for n in element.iter(f"{TBX}note")]
