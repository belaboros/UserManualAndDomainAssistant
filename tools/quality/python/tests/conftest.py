"""Fixtures: build a throwaway monorepo with components.json files and Python packages."""

from __future__ import annotations

import itertools
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

_counter = itertools.count()

RepoBuilder = Callable[..., Path]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.fixture
def unique() -> str:
    """A suffix that keeps package names unique across tests (grimp resolves them via sys.path)."""
    return f"t{next(_counter)}"


@pytest.fixture
def make_repo(tmp_path: Path) -> RepoBuilder:
    def build(
        components: list[dict[str, Any]],
        files: dict[str, str],
        app_components: dict[str, list[dict[str, Any]]] | None = None,
        register: bool = True,
    ) -> Path:
        """``register``: make every app/shared folder with code a workspace member checked by mypy."""
        _write(tmp_path / "docs/architecture/components.json", json.dumps({"components": components}))
        for app, comps in (app_components or {}).items():
            _write(
                tmp_path / f"apps/{app}/docs/architecture/components.json", json.dumps({"components": comps})
            )
        for rel, text in files.items():
            _write(tmp_path / rel, text)
        with_code = {"/".join(Path(rel).parts[:2]) for rel in files if "/src/" in rel}
        members = sorted(with_code) if register else []
        for member in members:
            _write(tmp_path / member / "pyproject.toml", f"[project]\nname = '{member.split('/')[1]}'\n")
        listed = ", ".join(f'"{m}"' for m in members)
        typed = ", ".join(f'"{m}/src"' for m in members)
        root = f"[tool.uv.workspace]\nmembers = [{listed}]\n[tool.mypy]\nfiles = [{typed}]\n"
        _write(tmp_path / "pyproject.toml", root)
        return tmp_path

    return build
