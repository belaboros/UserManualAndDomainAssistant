"""Edge cases of the spec: empty domain, multi-parent concept, cycles, unsafe labels, no generated/."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest
from dm_fixtures import EXAMPLE_DIR, copy_example, item, mutate, run_cli
from domain_model.load import load_domain
from domain_model.model import Domain
from domain_model.text.mermaid import diagrams_md, label
from rdflib import Graph


@pytest.fixture(scope="module")
def domain() -> Domain:
    loaded, _ = load_domain(EXAMPLE_DIR)
    assert loaded is not None
    return loaded


def test_mermaid_multi_parent_is_one_node_with_several_edges(domain: Domain) -> None:
    text = diagrams_md(domain)
    is_a = text.split("flowchart BT", 1)[1].split("```", 1)[0]
    assert is_a.count('EBook["') == 1
    assert "EBook --> Book" in is_a
    assert "EBook --> DigitalResource" in is_a


def test_mermaid_unsafe_label_is_escaped(domain: Domain) -> None:
    assert label('audio/visual "AV" item') == '"audio/visual #quot;AV#quot; item"'
    assert label("C# & more") == '"C#35; & more"'
    text = diagrams_md(domain)
    assert 'AudioVisualItem["audio/visual #quot;AV#quot; item"]' in text
    assert '"AV"' not in text


EMPTY_ONTOLOGY = """
namespace: https://example.org/empty#
prefix: emp
label: Empty
"""


def _empty_domain(tmp_path: Path) -> Path:
    folder = tmp_path / "empty"
    (folder / "samples").mkdir(parents=True)
    (folder / "samples" / "valid.ttl").write_text("", encoding="utf-8")
    (folder / "statements.yaml").write_text("statements: []\n", encoding="utf-8")
    (folder / "ontology.yaml").write_text(EMPTY_ONTOLOGY, encoding="utf-8")
    return folder


def test_empty_domain_builds_and_checks(tmp_path: Path, capsys: Any) -> None:
    folder = _empty_domain(tmp_path)
    assert run_cli(capsys, "build", str(folder)) == (0, "")
    assert (folder / "generated" / "level-1.md").is_file()
    for path in (folder / "generated").glob("*.ttl"):
        Graph().parse(path)
    assert run_cli(capsys, "check", str(folder)) == (0, "")


def test_missing_generated_folder_is_created_by_build(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    shutil.rmtree(folder / "generated", ignore_errors=True)
    assert run_cli(capsys, "build", str(folder))[0] == 0
    assert len(list((folder / "generated").iterdir())) == 13


def test_parent_cycle_is_named(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    mutate(folder, "ontology.yaml", lambda d: item(d, "concepts", "Agent").update(parent="Member"))
    code, out = run_cli(capsys, "check", str(folder))
    assert code == 1
    assert "ontology.yaml:Agent: parent cycle: Agent → Member → Agent" in out
