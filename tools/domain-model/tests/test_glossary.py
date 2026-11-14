"""AC-8 (and the TBX parts of AC-10, AC-11): glossary.md and glossary.tbx (plan 0002, T10)."""

from __future__ import annotations

import xml.etree.ElementTree as ET  # noqa: S405 - parses our own generated output

import pytest
from dm_fixtures import EXAMPLE_DIR, TOOL_DIR
from domain_model.consistency import kind_index
from domain_model.load import load_domain
from domain_model.model import Domain, Item
from domain_model.text.markdown import glossary_md
from domain_model.text.tbx import glossary_tbx
from lxml import etree

TBX = "{urn:iso:std:iso:30042:ed-2}"
RNG = TOOL_DIR / "tests" / "resources" / "tbx-core-minimal.rng"


@pytest.fixture(scope="module")
def domain() -> Domain:
    loaded, _ = load_domain(EXAMPLE_DIR)
    assert loaded is not None
    return loaded


def _row(markdown: str, entry: Item) -> str:
    rows = [line for line in markdown.splitlines() if f"| `{entry.id}` |" in line]
    assert len(rows) == 1, entry.id
    return rows[0]


def test_glossary_md_has_every_entry(domain: Domain) -> None:
    text = glossary_md(domain)
    kinds = kind_index(domain.ontology)
    for entry in domain.ontology.items:
        row = _row(text, entry)
        assert entry.label.replace("|", "\\|") in row
        assert f"| {kinds[entry.id]} |" in row
        for synonym in entry.synonyms:
            assert synonym in row
        assert entry.definition in row
        assert f"| {entry.level} |" in row
        assert f"| {entry.status} |" in row
        assert ", ".join(entry.source) in row


def _entries(domain: Domain) -> dict[str, ET.Element]:
    root = ET.fromstring(glossary_tbx(domain))  # noqa: S314 - our own output
    return {e.attrib["id"]: e for e in root.iter(f"{TBX}conceptEntry")}


def _notes(entry: ET.Element) -> list[str]:
    return [n.text or "" for n in entry.iter(f"{TBX}note")]


def test_tbx_has_every_entry(domain: Domain) -> None:
    entries = _entries(domain)
    assert set(entries) == {i.id for i in domain.ontology.items}
    for item in domain.ontology.items:
        entry = entries[item.id]
        terms = [t.text for t in entry.iter(f"{TBX}term")]
        assert terms == [item.label, *item.synonyms]
        definitions = [d.text for d in entry.iter(f"{TBX}descrip") if d.attrib["type"] == "definition"]
        assert definitions == ([item.definition] if item.definition else [])
        notes = _notes(entry)
        assert f"level: {item.level}" in notes
        assert f"status: {item.status}" in notes
        assert f"source: {', '.join(item.source)}" in notes


def test_tbx_validates_against_core_structure(domain: Domain) -> None:
    schema = etree.RelaxNG(etree.parse(str(RNG)))
    document = etree.fromstring(glossary_tbx(domain))
    assert schema.validate(document), schema.error_log
