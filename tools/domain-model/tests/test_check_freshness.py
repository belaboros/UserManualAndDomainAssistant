"""AC-14: check fails, naming the file, on a hand edit, a missing or an extra generated file (T15)."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from dm_fixtures import copy_example, run_cli


def _fails_naming(capsys: Any, folder: Path, name: str) -> list[str]:
    code, out = run_cli(capsys, "check", str(folder))
    assert code == 1
    lines = [line for line in out.splitlines() if line.startswith(f"generated/{name}:")]
    assert lines, out
    return out.splitlines()


def test_hand_edited_file_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    path = folder / "generated" / "glossary.md"
    path.write_text(path.read_text(encoding="utf-8") + "hand edit\n", encoding="utf-8")
    _fails_naming(capsys, folder, "glossary.md")


def test_missing_file_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    (folder / "generated" / "ontology.jsonld").unlink()
    _fails_naming(capsys, folder, "ontology.jsonld")


def test_extra_file_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    (folder / "generated" / "notes.txt").write_text("mine\n", encoding="utf-8")
    _fails_naming(capsys, folder, "notes.txt")


def test_stale_after_source_change_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    path = folder / "statements.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("lends items", "lends things"), encoding="utf-8")
    _fails_naming(capsys, folder, "statements.md")


def test_missing_generated_folder_reports_every_file(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    shutil.rmtree(folder / "generated")
    lines = _fails_naming(capsys, folder, "level-1.md")
    assert len([line for line in lines if line.startswith("generated/")]) == 13
