"""AC-13: every FR-12 model problem makes ``check`` fail naming file and item id (plan 0002, T2/T5)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from dm_fixtures import EXAMPLE_DIR, copy_example, item, mutate, run_cli
from domain_model.load import load_domain

Setup = Callable[[Path], None]


def _malformed_yaml(folder: Path) -> None:
    (folder / "ontology.yaml").write_text("namespace: [unclosed\nprefix: lib\n", encoding="utf-8")


def _missing_field(folder: Path) -> None:
    mutate(folder, "ontology.yaml", lambda d: item(d, "concepts", "Book").pop("label"))


def _wrong_type(folder: Path) -> None:
    mutate(folder, "ontology.yaml", lambda d: item(d, "relations", "hasItem").update(characteristics="x"))


def _unknown_field(folder: Path) -> None:
    mutate(folder, "ontology.yaml", lambda d: item(d, "concepts", "Book").update(colour="red"))


def _missing_statements_file(folder: Path) -> None:
    (folder / "statements.yaml").unlink()


def _set(section: str, item_id: str, **fields: Any) -> Setup:
    """A setup that updates fields of one ontology.yaml item."""
    return lambda folder: mutate(folder, "ontology.yaml", lambda d: item(d, section, item_id).update(fields))


def _duplicate_id(folder: Path) -> None:
    mutate(folder, "ontology.yaml", lambda d: d["concepts"].append(dict(item(d, "concepts", "Book"))))


def _statement_level(folder: Path) -> None:
    mutate(folder, "statements.yaml", lambda d: d["statements"][0].update(level=0))


def _duplicate_statement(folder: Path) -> None:
    mutate(folder, "statements.yaml", lambda d: d["statements"].append(dict(d["statements"][0])))


def _rule_path(rule_id: str, **fields: Any) -> Setup:
    def change(d: dict[str, Any]) -> None:
        rule = item(d, "rules", rule_id)
        pattern = next(
            k for k in ("cardinality", "values", "implies", "equal", "derive", "sparql") if k in rule
        )
        rule[pattern].update(fields)

    return lambda folder: mutate(folder, "ontology.yaml", change)


def _undefined_tree_node(folder: Path) -> None:
    mutate(folder, "taxonomy.yaml", lambda d: d["trees"][0]["top"][0].update(id="Libary"))


def _undefined_axiom_iri(folder: Path) -> None:
    with (folder / "ontology.axioms.ttl").open("a", encoding="utf-8") as f:
        f.write("lib:Ghost a owl:Class .\n")


def _unparsable_axioms(folder: Path) -> None:
    with (folder / "ontology.axioms.ttl").open("a", encoding="utf-8") as f:
        f.write("lib:Agent a \n")


def _rule_without_sample(folder: Path) -> None:
    (folder / "samples" / "R2.violates.ttl").unlink()


# (case id, setup, file named, item id named)
CASES: list[tuple[str, Setup, str, str]] = [
    ("malformed_yaml", _malformed_yaml, "ontology.yaml", "line 2"),
    ("missing_field", _missing_field, "ontology.yaml", "Book"),
    ("missing_field_file", _missing_statements_file, "statements.yaml", ""),
    ("malformed_wrong_type", _wrong_type, "ontology.yaml", "hasItem"),
    ("malformed_unknown_field", _unknown_field, "ontology.yaml", "Book"),
    ("duplicate_id", _duplicate_id, "ontology.yaml", "Book"),
    ("duplicate_statement_id", _duplicate_statement, "statements.yaml", "S1"),
    ("undefined_parent", _set("concepts", "Book", parent="Thing"), "ontology.yaml", "Book"),
    ("undefined_relation_range", _set("relations", "hasItem", range="Thing"), "ontology.yaml", "hasItem"),
    ("undefined_inverse", _set("relations", "borrowerOf", inverse="nope"), "ontology.yaml", "borrowerOf"),
    (
        "undefined_fact",
        _set("individuals", "CentralBranch", facts={"branchOf": ["Nowhere"]}),
        "ontology.yaml",
        "CentralBranch",
    ),
    ("undefined_rule_path", _rule_path("R1", path="hasItems"), "ontology.yaml", "R1"),
    ("undefined_rule_value", _rule_path("R2", **{"in": ["Active", "Lost"]}), "ontology.yaml", "R2"),
    ("undefined_tree_node", _undefined_tree_node, "taxonomy.yaml", "LibraryPartOf"),
    ("unknown_statement", _set("concepts", "Book", source=["S99"]), "ontology.yaml", "Book"),
    ("level_out_of_range", _set("concepts", "Shelf", level=4), "ontology.yaml", "Shelf"),
    ("level_out_of_range_statement", _statement_level, "statements.yaml", "S1"),
    ("lower_level_relation", _set("relations", "hasShelf", level=2), "ontology.yaml", "hasShelf"),
    ("lower_level_property", _set("properties", "title", domain="Shelf"), "ontology.yaml", "title"),
    ("lower_level_rule", _set("rules", "R2", level=1), "ontology.yaml", "R2"),
    (
        "lower_level_individual",
        _set("individuals", "CentralBranch", level=1),
        "ontology.yaml",
        "CentralBranch",
    ),
    ("lower_level_child_concept", _set("concepts", "EBook", level=1), "ontology.yaml", "EBook"),
    ("parent_cycle", _set("concepts", "Agent", parent="Member"), "ontology.yaml", "Agent"),
    ("unreachable_concept", _set("concepts", "Agent", parent="Member"), "ontology.yaml", "Librarian"),
    ("undefined_axiom_iri", _undefined_axiom_iri, "ontology.axioms.ttl", "Ghost"),
    ("unparsable_axioms", _unparsable_axioms, "ontology.axioms.ttl", ""),
    ("unparsable_sparql", _rule_path("R7", select="SELECT $this WHERE {"), "ontology.yaml", "R7"),
    (
        "undefined_sparql_iri",
        _rule_path("R7", select="SELECT $this WHERE { $this lib:nope ?x }"),
        "ontology.yaml",
        "R7",
    ),
    (
        "bad_path_syntax",
        _rule_path("R6", add={"predicate": "servedBy", "object": "hasItem//locatedIn"}),
        "ontology.yaml",
        "R6",
    ),
    ("rule_without_sample", _rule_without_sample, "samples", "R2"),
]


@pytest.mark.parametrize(("setup", "file", "item_id"), [c[1:] for c in CASES], ids=[c[0] for c in CASES])
def test_problem_is_reported(tmp_path: Path, capsys: Any, setup: Setup, file: str, item_id: str) -> None:
    folder = copy_example(tmp_path)
    setup(folder)
    code, out = run_cli(capsys, "check", str(folder))
    assert code == 1
    expected = f"{file}:{item_id}:" if item_id else f"{file}:"
    assert any(line.startswith(expected) for line in out.splitlines()), out


def test_clean_example_passes(capsys: Any) -> None:
    code, out = run_cli(capsys, "check", str(EXAMPLE_DIR))
    assert (code, out) == (0, "")


def test_example_loads() -> None:
    domain, findings = load_domain(EXAMPLE_DIR)
    assert findings == []
    assert domain is not None
    onto = domain.ontology
    assert {r.pattern_key for r in onto.rules} == {
        "cardinality",
        "values",
        "implies",
        "equal",
        "derive",
        "sparql",
    }
    assert {i.level for i in onto.items} == {1, 2, 3}
    assert any(c.also_parents for c in onto.concepts)
    assert any(i.status == "draft" for i in onto.items)
    assert domain.axioms is not None and "owl:unionOf" in domain.axioms
    assert domain.taxonomy.trees
