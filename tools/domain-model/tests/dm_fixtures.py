"""Helpers for the domain-model tests: copies and mutations of the example domain (plan 0002).

Named ``dm_fixtures`` (not ``conftest``/``fixtures``) so module names stay unique across the
workspace's test folders, which share one pytest and mypy run (plan 0002, T1).
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml
from domain_model.cli import main

TOOL_DIR = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = TOOL_DIR / "example"
REPO_ROOT = TOOL_DIR.parents[1]

Mutation = Callable[[dict[str, Any]], None]


def copy_example(tmp_path: Path, name: str = "example") -> Path:
    """A throwaway copy of the example domain (sources, samples and generated files)."""
    target = tmp_path / name
    shutil.copytree(EXAMPLE_DIR, target)
    return target


def read_yaml(folder: Path, name: str) -> dict[str, Any]:
    data = yaml.safe_load((folder / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def write_yaml(folder: Path, name: str, data: dict[str, Any]) -> None:
    (folder / name).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def mutate(folder: Path, name: str, change: Mutation) -> None:
    """Apply ``change`` to the parsed YAML file ``name`` and write it back."""
    data = read_yaml(folder, name)
    change(data)
    write_yaml(folder, name, data)


def item(data: dict[str, Any], section: str, item_id: str) -> dict[str, Any]:
    """The item with ``item_id`` in ``section`` of a parsed ontology.yaml."""
    found = next(i for i in data[section] if i["id"] == item_id)
    assert isinstance(found, dict)
    return found


def run_cli(capsys: Any, *args: str) -> tuple[int, str]:
    """Run the ``domain-model`` CLI in-process; returns (exit code, stdout)."""
    code = main(list(args))
    return code, capsys.readouterr().out


def mermaid_blocks(text: str) -> list[list[str]]:
    """The stripped lines of every ```mermaid block in a Markdown text."""
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if line.strip() == "```mermaid":
            current = []
        elif line.strip() == "```" and current is not None:
            blocks.append(current)
            current = None
        elif current is not None:
            current.append(line.strip())
    return blocks
