"""AC-1, AC-2, AC-3: build writes every generated file, only there, per namespace, deterministically."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from dm_fixtures import copy_example, item, mutate, run_cli

SPEC_FILES = {
    "statements.md",
    "glossary.md",
    "glossary.tbx",
    "taxonomy.skos.ttl",
    "ontology.owl.ttl",
    "ontology.owl.rdf",
    "ontology.jsonld",
    "rules.md",
    "rules.shacl.ttl",
    "diagrams.md",
    "level-1.md",
    "level-2.md",
    "level-3.md",
}


def _snapshot(folder: Path, skip: str = "generated") -> dict[str, bytes]:
    return {
        str(p.relative_to(folder)): p.read_bytes()
        for p in sorted(folder.rglob("*"))
        if p.is_file() and p.relative_to(folder).parts[0] != skip
    }


def _generated(folder: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted((folder / "generated").iterdir())}


def test_build_writes_every_generated_file(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    assert run_cli(capsys, "build", str(folder))[0] == 0
    assert set(_generated(folder)) == SPEC_FILES


def test_build_writes_nothing_outside_generated(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    before = _snapshot(folder)
    assert run_cli(capsys, "build", str(folder))[0] == 0
    assert _snapshot(folder) == before
    assert {p.name for p in tmp_path.iterdir()} == {"example"}


def _rename_namespace(folder: Path) -> None:
    for name in ("ontology.yaml", "ontology.axioms.ttl"):
        path = folder / name
        text = path.read_text(encoding="utf-8").replace(
            "https://example.org/library#", "https://example.org/other#"
        )
        text = text.replace("lib:", "oth:").replace("prefix: lib", "prefix: oth")
        path.write_text(text, encoding="utf-8")


def test_each_domain_uses_only_its_own_namespace(tmp_path: Path, capsys: Any) -> None:
    lib = copy_example(tmp_path, "lib")
    oth = copy_example(tmp_path, "oth")
    _rename_namespace(oth)
    for folder in (lib, oth):
        assert run_cli(capsys, "build", str(folder)) == (0, "")
    for name, data in _generated(lib).items():
        text = data.decode()
        assert "example.org/other" not in text and "oth:" not in text, name
    for name, data in _generated(oth).items():
        text = data.decode()
        assert "example.org/library" not in text and "lib:" not in text, name
    assert "example.org/other#" in _generated(oth)["ontology.owl.ttl"].decode()


def test_build_is_byte_identical(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    run_cli(capsys, "build", str(folder))
    first = _generated(folder)
    run_cli(capsys, "build", str(folder))
    assert _generated(folder) == first


def test_build_is_byte_identical_across_processes(tmp_path: Path) -> None:
    outputs = []
    for seed in ("1", "2"):
        folder = copy_example(tmp_path, f"seed{seed}")
        env = {**os.environ, "PYTHONHASHSEED": seed}
        command = [sys.executable, "-m", "domain_model.cli", "build", str(folder)]
        subprocess.run(command, env=env, check=True)  # noqa: S603 - fixed interpreter and module
        outputs.append(_generated(folder))
    assert outputs[0] == outputs[1]


def test_build_refuses_on_model_findings(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    run_cli(capsys, "build", str(folder))
    mutate(folder, "ontology.yaml", lambda d: item(d, "concepts", "Book").update(parent="Thing"))
    before = _generated(folder)
    code, out = run_cli(capsys, "build", str(folder))
    assert code == 1
    assert "ontology.yaml:Book:" in out
    assert _generated(folder) == before
