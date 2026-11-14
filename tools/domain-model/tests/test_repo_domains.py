"""AC-17: data/AcmeDataPlatform is migrated to sources + generated/ and passes check (plan 0002, T20)."""

from __future__ import annotations

from typing import Any

from dm_fixtures import REPO_ROOT, read_yaml, run_cli
from domain_model.discover import discover

ACME = REPO_ROOT / "data" / "AcmeDataPlatform"

# S1–S10 verbatim, as recorded in the idea-0001 session (previously the hand-written statements.md).
STATEMENTS = {
    "S1": "Core concepts: AcmeDataPlatform; platform service; platform resource; platform team; "
    "product team; environments: EXP, DEV, ACC, PRD",
    "S2": 'AcmeDataPlatform consists of "platform services".',
    "S3": "Each platform service is owned by a platform team.",
    "S4": "Platform services are used by product teams to create platform resources.",
    "S5": "Each platform resource is owned by the product team which created it.",
    "S6": "Platform services can be deployed to the environments.",
    "S7": "Platform resources can be created in the EXP or in the DEV environment.",
    "S8": "Platform resources can be promoted to upper environments in 2 ways: "
    "EXP->DEV->ACC->PRD or DEV->ACC->PRD",
    "S9": 'Platform resource can be one of those: "data product", dashboard, "ML model", "AI model", '
    '"AI/analytical application"',
    "S10": "(answers to Q44-Q46) A platform resource is created with one or more platform services. "
    'Platform team and product team are two kinds of "team". '
    "A platform service can be deployed to any environment, independently.",
}


def test_acme_domain_passes_check(capsys: Any) -> None:
    assert ACME in discover(REPO_ROOT)
    assert run_cli(capsys, "check", str(ACME)) == (0, "")


def test_acme_statements_s1_to_s10() -> None:
    """The migrated S1–S10 stay first and verbatim; later statements may follow (modelling continues)."""
    statements = read_yaml(ACME, "statements.yaml")["statements"][: len(STATEMENTS)]
    assert {s["id"]: s["text"] for s in statements} == STATEMENTS
    assert [s["id"] for s in statements] == list(STATEMENTS)
    assert {(str(s["date"]), s["level"]) for s in statements} == {("2026-11-14", 1)}


def test_no_handwritten_ttl_at_top_level() -> None:
    assert {p.name for p in ACME.glob("*.ttl")} <= {"ontology.axioms.ttl"}
    assert not (ACME / "statements.md").exists()
    assert (ACME / "samples" / "valid.ttl").is_file()
