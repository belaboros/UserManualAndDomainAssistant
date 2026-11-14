"""AC-20: build and check a synthetic 200-item domain in under 10 seconds (plan 0002, T21)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from dm_fixtures import run_cli, write_yaml

NS = "https://example.org/perf#"
PREFIX = f"@prefix p: <{NS}> .\n"
LEAVES = range(90, 98)  # concepts without children carry the constraint rules
DERIVED = (98, 99)


def _item(item_id: str, **fields: Any) -> dict[str, Any]:
    return {
        "id": item_id,
        "label": item_id.lower(),
        "level": 1,
        "status": "confirmed",
        "source": ["S1"],
        **fields,
    }


def _ontology() -> dict[str, Any]:
    concepts = [_item("C0")] + [_item(f"C{i}", parent=f"C{i // 2}") for i in range(1, 100)]
    relations = [_item(f"r{i}", domain=f"C{i}", range=f"C{i + 1}", cardinality="0..*") for i in range(50)]
    properties = [_item(f"p{i}", domain=f"C{i}", datatype="string", cardinality="0..1") for i in range(30)]
    individuals = [_item(f"I{i}", types=[f"C{i}"]) for i in range(20)]
    rules = [
        {
            **_item(f"R{i}"),
            "statement": f"Each C{i} has an r{i - 90}.",
            "cardinality": {"focus": f"C{i}", "path": f"r{i - 90}", "min": 1},
        }
        for i in LEAVES
    ]
    for i in DERIVED:
        derive = {"focus": f"C{i}", "add": {"predicate": "r0", "object": "I0"}}
        rules.append({**_item(f"R{i}"), "statement": f"Each C{i} is r0-linked to I0.", "derive": derive})
    for rule in rules:
        del rule["label"]
    return {
        "namespace": NS,
        "prefix": "p",
        "label": "Performance",
        "concepts": concepts,
        "individuals": individuals,
        "relations": relations,
        "properties": properties,
        "rules": rules,
    }


def _synthetic_domain(tmp_path: Path) -> Path:
    folder = tmp_path / "perf"
    samples = folder / "samples"
    samples.mkdir(parents=True)
    write_yaml(
        folder,
        "statements.yaml",
        {"statements": [{"id": "S1", "date": "2026-11-14", "level": 1, "text": "x"}]},
    )
    write_yaml(folder, "ontology.yaml", _ontology())
    valid = "".join(f"p:x{i} a p:C{i} ; p:r{i - 90} p:y{i} .\n" for i in LEAVES)
    (samples / "valid.ttl").write_text(PREFIX + valid, encoding="utf-8")
    for i in LEAVES:
        (samples / f"R{i}.violates.ttl").write_text(PREFIX + f"p:x a p:C{i} .\n", encoding="utf-8")
    for i in DERIVED:
        (samples / f"R{i}.derives.ttl").write_text(PREFIX + f"p:x a p:C{i} .\n", encoding="utf-8")
        (samples / f"R{i}.expected.ttl").write_text(PREFIX + "p:x p:r0 p:I0 .\n", encoding="utf-8")
    return folder


def test_build_and_check_200_items_under_10s(tmp_path: Path, capsys: Any) -> None:
    folder = _synthetic_domain(tmp_path)
    start = time.perf_counter()
    assert run_cli(capsys, "build", str(folder)) == (0, "")
    assert run_cli(capsys, "check", str(folder)) == (0, "")
    elapsed = time.perf_counter() - start
    items = len(list((folder / "generated").iterdir()))
    assert items == 13
    assert elapsed < 10, f"build + check took {elapsed:.1f} s"
