"""Compare ``render_all()`` with ``generated/``: stale, missing and extra files (FR-12, AC-14)."""

from __future__ import annotations

from pathlib import Path

from domain_model.build import GENERATED
from domain_model.model import Finding


def freshness_findings(folder: Path, expected: dict[str, bytes]) -> list[Finding]:
    target = folder / GENERATED
    actual = (
        {str(p.relative_to(target)): p.read_bytes() for p in sorted(target.rglob("*")) if p.is_file()}
        if target.is_dir()
        else {}
    )
    findings = []
    for name in sorted(set(expected) | set(actual)):
        if name not in actual:
            message = "missing; run `uv run domain-model build <folder>`"
        elif name not in expected:
            message = "not produced by build (extra file); remove it"
        elif actual[name] != expected[name]:
            message = "differs from what build writes (hand edit or stale); edit the sources and rebuild"
        else:
            continue
        findings.append(Finding(f"{GENERATED}/{name}", "", message))
    return findings
