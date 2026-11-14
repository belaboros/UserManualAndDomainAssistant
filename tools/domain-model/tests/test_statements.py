"""AC-12: statements.md lists every statement verbatim; rules.md describes every rule (plan 0002, T11)."""

from __future__ import annotations

import pytest
from dm_fixtures import EXAMPLE_DIR
from domain_model.load import load_domain
from domain_model.model import Domain
from domain_model.text.markdown import rules_md, statements_md


@pytest.fixture(scope="module")
def domain() -> Domain:
    loaded, _ = load_domain(EXAMPLE_DIR)
    assert loaded is not None
    return loaded


def test_statements_md_lists_every_statement_verbatim(domain: Domain) -> None:
    lines = statements_md(domain).splitlines()
    for s in domain.statements:
        assert f"| {s.id} | {s.date.isoformat()} | {s.level} | {s.text} |" in lines


def test_rules_md_lists_every_rule(domain: Domain) -> None:
    text = rules_md(domain)
    for rule in domain.ontology.rules:
        section = text.split(f"### {rule.id} ·", 1)[1].split("\n### ", 1)[0]
        assert rule.statement in section
        assert f"**Kind:** {rule.kind}" in section
        assert f"**Pattern:** `{rule.pattern_key}`" in section
        assert f"**Level:** {rule.level}" in section
        assert f"**Status:** {rule.status}" in section
        assert f"**Sources:** {', '.join(rule.source)}" in section
