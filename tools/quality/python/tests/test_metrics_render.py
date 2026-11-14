from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from conftest import RepoBuilder
from quality_gate.metrics import snapshot
from quality_gate.render import BEGIN, END, merge, render
from quality_gate.units import SYSTEM_COMPONENTS, load_level

SNAPSHOT_KEYS = {"date", "commit", "languages", "functions", "components", "dependencies", "cycles"}
SNAPSHOT_KEYS |= {"violations", "result"}

COMPLEX = (
    "def f(x):\n" + "".join(f"    if x == {i}:\n        return {i}\n" for i in range(16)) + "    return -1\n"
)


def _two_apps(make_repo: RepoBuilder, unique: str, body: str) -> Path:
    components = [
        {"name": "a", "kind": "app", "paths": ["apps/a/**"], "mayDependOn": ["lib"]},
        {"name": "lib", "kind": "shared", "paths": ["shared/lib/**"], "mayDependOn": []},
    ]
    return make_repo(
        components,
        {
            f"apps/a/src/a_{unique}/__init__.py": f"import json\nimport lib_{unique}\n{body}",
            f"shared/lib/src/lib_{unique}/__init__.py": "import abc\n\nclass Port(abc.ABC):\n    pass\n",
        },
    )


def test_snapshot_schema_and_coupling(make_repo: RepoBuilder, unique: str) -> None:
    repo = _two_apps(make_repo, unique, "")
    snap = snapshot(load_level(SYSTEM_COMPONENTS, repo), repo)
    assert set(snap) == SNAPSHOT_KEYS
    comps = {c["name"]: c for c in snap["components"]}
    assert (comps["a"]["ce"], comps["a"]["ca"], comps["a"]["instability"]) == (1, 0, 1.0)
    assert comps["lib"]["abstractness"] == 1.0
    assert comps["a"]["externalDeps"] == ["json"]
    assert snap["dependencies"] == [{"from": "a", "to": "lib", "count": 1}]
    assert snap["result"] in {"pass", "warn"}


def test_function_over_15_fails(make_repo: RepoBuilder, unique: str) -> None:
    repo = _two_apps(make_repo, unique, COMPLEX)
    snap = snapshot(load_level(SYSTEM_COMPONENTS, repo), repo)
    assert snap["functions"]["ccMax"] == 17
    assert any(v["kind"] == "cc" for v in snap["violations"])
    assert snap["result"] == "fail"


def _snap(deps: list[tuple[str, str, int]], names: list[str]) -> dict[str, Any]:
    comp = {
        "ca": 0,
        "ce": 0,
        "instability": 0.0,
        "relationalCohesion": 2.0,
        "abstractness": None,
        "distance": None,
    }
    return {
        "date": "2026-11-14",
        "commit": "abcdef0123",
        "languages": ["python"],
        "functions": {"count": 2, "ccAvg": 3.0, "ccMax": 4, "overWarn": []},
        "components": [{"name": n, **comp, "externalDeps": []} for n in names],
        "dependencies": [{"from": a, "to": b, "count": c} for a, b, c in deps],
        "cycles": [],
        "violations": [],
        "result": "pass",
    }


def test_merge_unions_edges_and_detects_cycles() -> None:
    merged = merge([_snap([("a", "b", 2)], ["a", "b"]), _snap([("b", "a", 1), ("a", "b", 1)], ["a", "b"])])
    assert merged["dependencies"] == [
        {"from": "a", "to": "b", "count": 3},
        {"from": "b", "to": "a", "count": 1},
    ]
    assert merged["cycles"] == [["a", "b", "a"]]
    assert merged["result"] == "fail"
    assert merged["functions"]["count"] == 4


def test_render_writes_history_latest_and_diagram(tmp_path: Path) -> None:
    arch = tmp_path / "docs/architecture/architecture.md"
    arch.parent.mkdir(parents=True)
    arch.write_text(f"# A\n\n{BEGIN}\nold\n{END}\n")
    render("system", [_snap([("a", "b", 2)], ["a", "b"])], tmp_path)
    history = json.loads((tmp_path / "docs/architecture/metrics/history/2026-11-14.json").read_text())
    assert history["result"] == "pass"
    assert "**Result: PASS**" in (tmp_path / "docs/architecture/metrics/latest.md").read_text()
    text = arch.read_text()
    assert 'a -- "2" --> b' in text
    assert "old" not in text
