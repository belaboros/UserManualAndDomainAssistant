"""AC-16 (discovery): ``check --all`` finds every domain folder of the repo (plan 0002, T17)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from dm_fixtures import EXAMPLE_DIR, REPO_ROOT, copy_example, run_cli
from domain_model.discover import discover


def _domain(folder: Path) -> None:
    folder.mkdir(parents=True)
    (folder / "ontology.yaml").write_text("", encoding="utf-8")
    (folder / "statements.yaml").write_text("", encoding="utf-8")


def test_discovery_rules(tmp_path: Path) -> None:
    _domain(tmp_path / "data" / "One")
    _domain(tmp_path / "deep" / "er" / "Two")
    _domain(tmp_path / ".hidden" / "Three")
    _domain(tmp_path / "tools" / "x" / "tests" / "Four")
    (tmp_path / "half").mkdir()
    (tmp_path / "half" / "ontology.yaml").write_text("", encoding="utf-8")
    found = [p.relative_to(tmp_path).as_posix() for p in discover(tmp_path)]
    assert found == ["data/One", "deep/er/Two"]


def test_discovers_domain_folders() -> None:
    found = discover(REPO_ROOT)
    assert EXAMPLE_DIR in found
    assert not any("tests" in p.relative_to(REPO_ROOT).parts for p in found)


def test_check_all_prefixes_findings_with_the_folder(
    tmp_path: Path, capsys: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    folder = copy_example(tmp_path / "repo")
    (folder / "generated" / "extra.txt").write_text("x", encoding="utf-8")
    monkeypatch.chdir(tmp_path / "repo")
    code, out = run_cli(capsys, "check", "--all")
    assert code == 1
    assert out.splitlines() == ["example/generated/extra.txt: not produced by build (extra file); remove it"]


def test_check_all_passes_on_clean_repo(tmp_path: Path, capsys: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    copy_example(tmp_path / "repo")
    monkeypatch.chdir(tmp_path / "repo")
    assert run_cli(capsys, "check", "--all") == (0, "")


def test_usage_errors(tmp_path: Path, capsys: Any) -> None:
    assert run_cli(capsys, "check")[0] == 2
    assert run_cli(capsys, "build", str(tmp_path / "nope"))[0] == 2
