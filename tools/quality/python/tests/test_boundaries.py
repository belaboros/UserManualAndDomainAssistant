from __future__ import annotations

from typing import Any

from conftest import RepoBuilder
from quality_gate.boundaries import check
from quality_gate.graph import cycles


def app(name: str, depends: list[str] | None = None) -> dict[str, Any]:
    return {"name": name, "kind": "app", "paths": [f"apps/{name}/**"], "mayDependOn": depends or []}


def shared(name: str, public: list[str] | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "name": name,
        "kind": "shared",
        "paths": [f"shared/{name}/**"],
        "mayDependOn": [],
    }
    if public:
        entry["public"] = public
    return entry


def test_clean_repo_passes(make_repo: RepoBuilder, unique: str) -> None:
    lib = f"lib_{unique}"
    repo = make_repo(
        [app("a", ["lib"]), shared("lib", [f"shared/lib/src/{lib}/__init__.py"])],
        {
            f"apps/a/src/a_{unique}/__init__.py": f"import {lib}\n",
            f"shared/lib/src/{lib}/__init__.py": "from . import core\n",
            f"shared/lib/src/{lib}/core.py": "X = 1\n",
        },
    )
    findings, measured = check(repo)
    assert findings == []
    assert measured == 2


def test_app_importing_another_app_fails(make_repo: RepoBuilder, unique: str) -> None:
    repo = make_repo(
        [app("a"), app("b")],
        {
            f"apps/a/src/a_{unique}/__init__.py": f"import b_{unique}\n",
            f"apps/b/src/b_{unique}/__init__.py": "",
        },
    )
    findings, _ = check(repo)
    assert any("app 'a' imports app 'b'" in f for f in findings)


def test_undeclared_shared_dependency_fails(make_repo: RepoBuilder, unique: str) -> None:
    repo = make_repo(
        [app("a"), shared("lib")],
        {
            f"apps/a/src/a_{unique}/__init__.py": f"import lib_{unique}\n",
            f"shared/lib/src/lib_{unique}/__init__.py": "",
        },
    )
    findings, _ = check(repo)
    assert any("'a' depends on 'lib', which is not in its mayDependOn" in f for f in findings)


def test_internal_module_of_shared_component_fails(make_repo: RepoBuilder, unique: str) -> None:
    lib = f"lib_{unique}"
    repo = make_repo(
        [app("a", ["lib"]), shared("lib", [f"shared/lib/src/{lib}/__init__.py"])],
        {
            f"apps/a/src/a_{unique}/__init__.py": f"from {lib} import core\n",
            f"shared/lib/src/{lib}/__init__.py": "",
            f"shared/lib/src/{lib}/core.py": "",
        },
    )
    findings, _ = check(repo)
    assert any(f"imports internal module {lib}.core of 'lib'" in f for f in findings)


def test_shared_importing_app_fails(make_repo: RepoBuilder, unique: str) -> None:
    repo = make_repo(
        [app("a"), shared("lib")],
        {
            f"apps/a/src/a_{unique}/__init__.py": "",
            f"shared/lib/src/lib_{unique}/__init__.py": f"import a_{unique}\n",
        },
    )
    findings, _ = check(repo)
    assert any("shared 'lib' imports app 'a'" in f for f in findings)


def _app_with_components(unique: str, ui_depends: list[str], core_depends: list[str]) -> dict[str, Any]:
    pkg = f"a_{unique}"
    return {
        "components": [
            {"name": "ui", "paths": [f"apps/a/src/{pkg}/ui/**"], "mayDependOn": ui_depends},
            {"name": "core", "paths": [f"apps/a/src/{pkg}/core/**"], "mayDependOn": core_depends},
        ],
        "files": {
            f"apps/a/src/{pkg}/__init__.py": "",
            f"apps/a/src/{pkg}/ui/__init__.py": f"from {pkg} import core\n",
            f"apps/a/src/{pkg}/core/__init__.py": f"from {pkg} import ui\n",
        },
    }


def test_app_level_boundary_fails(make_repo: RepoBuilder, unique: str) -> None:
    layout = _app_with_components(unique, ["core"], [])
    repo = make_repo([app("a")], layout["files"], {"a": layout["components"]})
    findings, _ = check(repo)
    assert any("[a] 'core' depends on 'ui', which is not in its mayDependOn" in f for f in findings)
    assert any("[a] import cycle: core -> ui -> core" in f for f in findings)


def test_declared_cycle_fails(make_repo: RepoBuilder, unique: str) -> None:
    layout = _app_with_components(unique, ["core"], ["ui"])
    repo = make_repo([app("a")], layout["files"], {"a": layout["components"]})
    findings, _ = check(repo)
    assert any("declared cycle in mayDependOn: core -> ui -> core" in f for f in findings)


def test_package_outside_workspace_fails(make_repo: RepoBuilder) -> None:
    repo = make_repo([app("a")], {"apps/a/pyproject.toml": "[project]\nname = 'a'\n"}, register=False)
    findings, _ = check(repo)
    assert findings == [
        "[workspace] apps/a is not in [tool.uv.workspace].members",
        "[workspace] apps/a/src is not in [tool.mypy].files",
    ]


def test_registered_member_passes(make_repo: RepoBuilder, unique: str) -> None:
    repo = make_repo([app("a")], {f"apps/a/src/a_{unique}/__init__.py": ""})
    findings, _ = check(repo)
    assert findings == []


def test_python_code_without_pyproject_fails(make_repo: RepoBuilder, unique: str) -> None:
    repo = make_repo([app("a")], {f"apps/a/src/a_{unique}/__init__.py": ""}, register=False)
    findings, _ = check(repo)
    assert findings == ["[workspace] apps/a has Python code but no pyproject.toml"]


def test_cycles_finds_strongly_connected_components() -> None:
    assert cycles([("a", "b"), ("b", "c"), ("c", "a"), ("c", "d")]) == [["a", "b", "c", "a"]]
    assert cycles([("a", "b")]) == []
