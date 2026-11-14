"""AC-16: pre-commit and CI run ``domain-model check --all`` (plan 0002, T18)."""

from __future__ import annotations

import re
from typing import Any

import yaml
from dm_fixtures import REPO_ROOT


def _load(path: str) -> Any:
    return yaml.safe_load((REPO_ROOT / path).read_text(encoding="utf-8"))


def test_precommit_runs_check_all() -> None:
    hooks = [h for repo in _load(".pre-commit-config.yaml")["repos"] for h in repo.get("hooks", [])]
    hook = next(h for h in hooks if h["id"] == "domain-model")
    assert hook["entry"].endswith("domain-model check --all")
    assert hook["pass_filenames"] is False
    pattern = re.compile(hook["files"])
    for path in ("data/AcmeDataPlatform/ontology.yaml", "tools/domain-model/example/generated/level-1.md"):
        assert pattern.search(path), path
    assert not pattern.search("apps/assistant/README.md")


def test_ci_runs_check_all() -> None:
    steps = _load(".github/workflows/python.yml")["jobs"]["gate"]["steps"]
    step = next(s for s in steps if s.get("name") == "Domain models (check)")
    assert "domain-model check --all" in step["run"]
