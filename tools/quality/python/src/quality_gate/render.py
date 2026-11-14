"""``qg-arch-render <system|app> <snapshot.json>...``: merge per-language snapshots of one level and
write ``history/<date>.json``, ``latest.md`` and the coupling diagram in ``architecture.md``.

Language independent: any collector that emits the snapshot schema can feed it (ADR-0006, ADR-0014).
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from quality_gate.graph import cycles
from quality_gate.metrics import CE_FAIL, CE_WARN, result_of, sdp_violations, soft_warn

BEGIN = "<!-- coupling:begin (generated, do not edit) -->"
END = "<!-- coupling:end -->"


def merge(snaps: list[dict[str, Any]]) -> dict[str, Any]:
    """Sum counts per component, union the edges, recompute I, cycles, SDP and the result."""
    counts = _edge_counts(snaps)
    edges = sorted(counts)
    components = _merge_components(snaps, edges)
    merged: dict[str, Any] = {
        "date": snaps[0]["date"],
        "commit": snaps[0]["commit"],
        "languages": sorted({lang for s in snaps for lang in s["languages"]}),
        "functions": _merge_functions(snaps),
        "components": components,
        "dependencies": [{"from": a, "to": b, "count": counts[(a, b)]} for a, b in edges],
        "cycles": cycles(edges),
    }
    merged["violations"] = _merged_violations(snaps, merged, edges)
    merged["result"] = result_of(merged)
    return merged


def _edge_counts(snaps: list[dict[str, Any]]) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for snap in snaps:
        for dep in snap["dependencies"]:
            counts[(dep["from"], dep["to"])] += dep["count"]
    return counts


def _merged_violations(
    snaps: list[dict[str, Any]], merged: dict[str, Any], edges: list[tuple[str, str]]
) -> list[dict[str, str]]:
    kept = [v for s in snaps for v in s["violations"] if v["kind"] in {"boundary", "cc"}]
    cycle_v = [{"kind": "cycle", "detail": " -> ".join(c)} for c in merged["cycles"]]
    stats = {c["name"]: c for c in merged["components"]}
    return _unique(kept + cycle_v + sdp_violations(edges, stats))


def _unique(items: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: list[dict[str, str]] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def _merge_functions(snaps: list[dict[str, Any]]) -> dict[str, Any]:
    count = sum(s["functions"]["count"] for s in snaps)
    total = sum(s["functions"]["ccAvg"] * s["functions"]["count"] for s in snaps)
    return {
        "count": count,
        "ccAvg": round(total / count, 2) if count else 0.0,
        "ccMax": max(s["functions"]["ccMax"] for s in snaps),
        "overWarn": [f for s in snaps for f in s["functions"]["overWarn"]],
    }


def _merge_components(snaps: list[dict[str, Any]], edges: list[tuple[str, str]]) -> list[dict[str, Any]]:
    by_name: dict[str, dict[str, Any]] = {}
    for snap in snaps:
        for comp in snap["components"]:
            entry = by_name.setdefault(comp["name"], {**comp, "externalDeps": []})
            entry["externalDeps"] = sorted(set(entry["externalDeps"]) | set(comp["externalDeps"]))
    for name, entry in by_name.items():
        entry["ce"] = len({b for a, b in edges if a == name})
        entry["ca"] = len({a for a, b in edges if b == name})
        total = entry["ca"] + entry["ce"]
        entry["instability"] = round(entry["ce"] / total, 3) if total else 0.0
    return [by_name[n] for n in sorted(by_name)]


def level_dirs(level: str, repo: Path) -> tuple[Path, Path]:
    base = repo / "docs/architecture" if level == "system" else repo / f"apps/{level}/docs/architecture"
    return base / "metrics", base / "architecture.md"


def previous_snapshot(history: Path, date: str) -> dict[str, Any] | None:
    older = sorted(p for p in history.glob("*.json") if p.stem < date)
    return json.loads(older[-1].read_text()) if older else None


def _fmt(value: object) -> str:
    return "n/a" if value is None else str(value)


def component_status(component: dict[str, Any]) -> str:
    if component["ce"] > CE_FAIL:
        return "fail"
    return "warn" if component["ce"] > CE_WARN or soft_warn(component) else "pass"


def component_rows(snap: dict[str, Any]) -> list[str]:
    rows = [
        "| Component | Ca | Ce | I | H | A | D | Status | External |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for c in snap["components"]:
        cells = [
            c["ca"],
            c["ce"],
            c["instability"],
            c["relationalCohesion"],
            c["abstractness"],
            c["distance"],
            component_status(c),
        ]
        rows.append(
            f"| **{c['name']}** | "
            + " | ".join(_fmt(x) for x in cells)
            + f" | {', '.join(c['externalDeps']) or '—'} |"
        )
    return rows


def change_lines(snap: dict[str, Any], prev: dict[str, Any] | None) -> list[str]:
    if prev is None:
        return ["_First snapshot: nothing to compare with._"]
    old = {v["detail"] for v in prev["violations"]}
    new = [v for v in snap["violations"] if v["detail"] not in old]
    lines = [f"- Since {prev['date']} ({prev['commit'][:8]}): result {prev['result']} → {snap['result']}"]
    lines.append(f"- CC max {prev['functions']['ccMax']} → {snap['functions']['ccMax']}")
    lines += [f"- New violation: {v['kind']}: {v['detail']}" for v in new] or ["- No new violations"]
    return lines + _ce_changes(snap, prev)


def _ce_changes(snap: dict[str, Any], prev: dict[str, Any]) -> list[str]:
    old_ce = {c["name"]: c["ce"] for c in prev["components"]}
    changed = [(c["name"], old_ce.get(c["name"], 0), c["ce"]) for c in snap["components"]]
    return [f"- {name}: Ce {before} → {after}" for name, before, after in changed if before != after]


def latest_md(level: str, snap: dict[str, Any], prev: dict[str, Any] | None) -> str:
    title = "Latest modularity metrics" if level == "system" else f"{level} · Latest modularity metrics"
    f = snap["functions"]
    out = [
        f"# {title}",
        "",
        f"**Result: {snap['result'].upper()}** · {snap['date']} · commit `{snap['commit'][:8]}` · "
        f"languages: {', '.join(snap['languages'])}",
        "",
        f"Functions: {f['count']} · CC avg {f['ccAvg']} · CC max {f['ccMax']}. Definitions and thresholds: "
        "`docs/architecture/metrics/README.md`.",
        "",
        "## Components",
        "",
        *component_rows(snap),
        "",
        "## Functions over the warn threshold (CC > 10)",
        "",
    ]
    out += [f"- `{x['file']}` {x['function']}: CC {x['cc']}" for x in f["overWarn"]] or ["_None._"]
    out += ["", "## Violations", ""]
    out += [f"- **{v['kind']}**: {v['detail']}" for v in snap["violations"]] or ["_None._"]
    return "\n".join([*out, "", "## Change since the previous snapshot", "", *change_lines(snap, prev), ""])


def coupling_mermaid(snap: dict[str, Any]) -> str:
    if not snap["components"]:
        return "_No components declared yet._"
    ident = {c["name"]: re.sub(r"\W", "_", c["name"]) for c in snap["components"]}
    lines = ["```mermaid", "flowchart LR"]
    for c in snap["components"]:
        lines.append(f'    {ident[c["name"]]}["{c["name"]}<br/>{c["ca"]}·{c["ce"]}·{c["instability"]}"]')
    in_cycle = [set(c) for c in snap["cycles"]]
    bad = _boundary_edges(snap)
    red = []
    for i, dep in enumerate(snap["dependencies"]):
        source, target = ident.get(dep["from"], dep["from"]), ident.get(dep["to"], dep["to"])
        lines.append(f'    {source} -- "{dep["count"]}" --> {target}')
        cyclic = any({dep["from"], dep["to"]} <= members for members in in_cycle)
        if cyclic or (dep["from"], dep["to"]) in bad:
            red.append(str(i))
    if red:
        lines.append(f"    linkStyle {','.join(red)} stroke:#d00,stroke-width:2px")
    return "\n".join(
        [
            *lines,
            "```",
            "",
            "Nodes: `name<br/>Ca·Ce·I`; edges: reference counts; red: boundary violation or cycle.",
        ]
    )


def _boundary_edges(snap: dict[str, Any]) -> set[tuple[str, str]]:
    names = [c["name"] for c in snap["components"]]
    found = set()
    for v in snap["violations"]:
        if v["kind"] != "boundary":
            continue
        mentioned = [n for n in names if f"'{n}'" in v["detail"]]
        if len(mentioned) >= 2:
            found.add((mentioned[0], mentioned[1]))
    return found


def write_coupling(architecture: Path, block: str) -> None:
    text = architecture.read_text()
    start, end = text.index(BEGIN) + len(BEGIN), text.index(END)
    architecture.write_text(text[:start] + "\n" + block + "\n" + text[end:])


def render(level: str, snaps: list[dict[str, Any]], repo: Path) -> dict[str, Any]:
    merged = merge(snaps)
    metrics_dir, architecture = level_dirs(level, repo)
    history = metrics_dir / "history"
    history.mkdir(parents=True, exist_ok=True)
    prev = previous_snapshot(history, merged["date"])
    (history / f"{merged['date']}.json").write_text(json.dumps(merged, indent=2) + "\n")
    (metrics_dir / "latest.md").write_text(latest_md(level, merged, prev))
    write_coupling(architecture, coupling_mermaid(merged))
    return merged


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 2:
        print("usage: qg-arch-render <system|app> <snapshot.json>...", file=sys.stderr)
        return 64
    snaps = [json.loads(Path(p).read_text()) for p in args[1:]]
    merged = render(args[0], snaps, Path.cwd())
    print(f"{args[0]}: {merged['result']}")
    return 1 if merged["result"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
