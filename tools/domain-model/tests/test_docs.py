"""AC-7 (documentation), AC-18: the README documents the format, every pattern, and the example."""

from __future__ import annotations

from dm_fixtures import EXAMPLE_DIR, TOOL_DIR
from domain_model.model import (
    PATTERN_KEYS,
    Concept,
    Condition,
    Individual,
    Ontology,
    Property,
    Relation,
    Rule,
)

README = TOOL_DIR / "README.md"
SECTIONS = ("concepts", "individuals", "relations", "properties", "rules")


def _text() -> str:
    return README.read_text(encoding="utf-8")


def test_readme_documents_every_pattern() -> None:
    rows = [line for line in _text().splitlines() if line.startswith("| `")]
    for key in PATTERN_KEYS:
        assert any(line.startswith(f"| `{key}` |") for line in rows), key


def test_readme_documents_every_field() -> None:
    text = _text()
    for model in (Ontology, Concept, Individual, Relation, Property, Rule, Condition):
        for name, field in model.model_fields.items():
            if name in PATTERN_KEYS or name in SECTIONS:
                continue
            assert f"`{field.alias or name}`" in text, f"{model.__name__}.{name}"


def test_readme_exists_and_references_example() -> None:
    assert "](example/)" in _text()
    assert EXAMPLE_DIR == TOOL_DIR / "example"
    assert (EXAMPLE_DIR / "ontology.yaml").is_file()
