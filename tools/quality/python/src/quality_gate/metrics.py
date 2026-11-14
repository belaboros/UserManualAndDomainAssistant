"""``qg-metrics <components.json>``: emit the modularity snapshot (docs/architecture/metrics/README.md)."""

from __future__ import annotations

import ast
import datetime
import json
import shutil
import subprocess  # noqa: S404 - only used to read the git commit sha
import sys
from pathlib import Path
from typing import Any

from radon.complexity import cc_visit

from quality_gate.boundaries import cycle_findings, dependency_findings
from quality_gate.graph import ImportFacts, collect, cycles
from quality_gate.units import Level, Unit, load_level

CC_WARN, CC_FAIL = 10, 15
CE_WARN, CE_FAIL = 4, 7
H_RANGE = (1.5, 4.0)
D_WARN = 0.5
ABSTRACT_BASES = {"ABC", "Protocol"}


def function_complexities(files: list[Path], repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in files:
        for block in _blocks(cc_visit(path.read_text())):
            out.append(
                {
                    "file": path.relative_to(repo).as_posix(),
                    "function": block.fullname,
                    "cc": block.complexity,
                }
            )
    return out


def _blocks(results: list[Any]) -> list[Any]:
    blocks: list[Any] = []
    for result in results:
        methods = getattr(result, "methods", None)
        blocks.extend(methods if methods is not None else [result])
    return blocks


def abstractness(files: list[Path]) -> float | None:
    total = abstract = 0
    for path in files:
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ClassDef):
                total += 1
                abstract += _is_abstract(node)
    return round(abstract / total, 3) if total else None


def _is_abstract(node: ast.ClassDef) -> bool:
    names = {b.id if isinstance(b, ast.Name) else getattr(b, "attr", "") for b in node.bases}
    metaclass = any(k.arg == "metaclass" and "ABCMeta" in ast.unparse(k.value) for k in node.keywords)
    return bool(names & ABSTRACT_BASES) or metaclass


def coupling(level: Level, facts: ImportFacts) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for unit in level.units:
        ce = len({b for a, b in facts.edges if a == unit.name})
        ca = len({a for a, b in facts.edges if b == unit.name})
        stats[unit.name] = {"ca": ca, "ce": ce, "instability": round(ce / (ca + ce), 3) if ca + ce else 0.0}
    return stats


def component_entry(unit: Unit, facts: ImportFacts, stats: dict[str, Any]) -> dict[str, Any]:
    modules = len(facts.modules.get(unit.name, set()))
    cohesion = round((facts.internal.get(unit.name, 0) + 1) / modules, 3) if modules else None
    a = abstractness(unit.python_files())
    distance = round(abs(a + stats["instability"] - 1), 3) if a is not None else None
    return {
        "name": unit.name,
        **stats,
        "relationalCohesion": cohesion,
        "abstractness": a,
        "distance": distance,
        "externalDeps": sorted(facts.external.get(unit.name, set())),
    }


def sdp_violations(edges: list[tuple[str, str]], stats: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    found = []
    for a, b in edges:
        i_a, i_b = stats[a]["instability"], stats[b]["instability"]
        if i_b > i_a:
            found.append({"kind": "sdp", "detail": f"{a} (I={i_a}) depends on less stable {b} (I={i_b})"})
    return found


def result_of(snapshot: dict[str, Any]) -> str:
    if _fails(snapshot):
        return "fail"
    return "warn" if _warns(snapshot) else "pass"


def _fails(snapshot: dict[str, Any]) -> bool:
    kinds = {v["kind"] for v in snapshot["violations"]}
    max_ce = max((c["ce"] for c in snapshot["components"]), default=0)
    return bool(kinds & {"boundary", "cycle"}) or snapshot["functions"]["ccMax"] > CC_FAIL or max_ce > CE_FAIL


def _warns(snapshot: dict[str, Any]) -> bool:
    kinds = {v["kind"] for v in snapshot["violations"]}
    max_ce = max((c["ce"] for c in snapshot["components"]), default=0)
    soft = any(soft_warn(c) for c in snapshot["components"])
    return "sdp" in kinds or bool(snapshot["functions"]["overWarn"]) or max_ce > CE_WARN or soft


def soft_warn(component: dict[str, Any]) -> bool:
    h, d = component["relationalCohesion"], component["distance"]
    return (h is not None and not H_RANGE[0] <= h <= H_RANGE[1]) or (d is not None and d > D_WARN)


def git_sha(repo: Path) -> str:
    git = shutil.which("git")
    if git is None:
        return "unknown"
    done = subprocess.run([git, "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=False)  # noqa: S603
    return done.stdout.strip() or "unknown"


def function_summary(funcs: list[dict[str, Any]]) -> dict[str, Any]:
    ccs = [f["cc"] for f in funcs]
    return {
        "count": len(ccs),
        "ccAvg": round(sum(ccs) / len(ccs), 2) if ccs else 0.0,
        "ccMax": max(ccs, default=0),
        "overWarn": [f for f in funcs if f["cc"] > CC_WARN],
    }


def violations_of(level: Level, facts: ImportFacts, funcs: list[dict[str, Any]]) -> list[dict[str, str]]:
    found = [{"kind": "boundary", "detail": f} for f in dependency_findings(level, facts)]
    found += [{"kind": "cycle", "detail": f} for f in cycle_findings(level, facts)]
    too_complex = [f for f in funcs if f["cc"] > CC_FAIL]
    return found + [
        {"kind": "cc", "detail": f"{f['file']}::{f['function']} CC {f['cc']}"} for f in too_complex
    ]


def snapshot(level: Level, repo: Path) -> dict[str, Any]:
    facts = collect(level)
    files = sorted({f for u in level.units for f in u.python_files()})
    funcs = function_complexities(files, repo)
    stats = coupling(level, facts)
    edges = sorted(facts.edges)
    violations = violations_of(level, facts, funcs) + sdp_violations(edges, stats)
    snap: dict[str, Any] = {
        "date": datetime.date.today().isoformat(),
        "commit": git_sha(repo),
        "languages": ["python"],
        "functions": function_summary(funcs),
        "components": [component_entry(u, facts, stats[u.name]) for u in level.units],
        "dependencies": [{"from": a, "to": b, "count": len(facts.edges[(a, b)])} for a, b in edges],
        "cycles": cycles(edges),
        "violations": violations,
    }
    snap["result"] = result_of(snap)
    return snap


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: qg-metrics <components.json> [repo]", file=sys.stderr)
        return 64
    repo = (Path(args[1]) if len(args) > 1 else Path.cwd()).resolve()
    components = Path(args[0])
    if components.is_absolute():
        components = components.resolve().relative_to(repo)
    level = load_level(components, repo)
    print(json.dumps(snapshot(level, repo), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
