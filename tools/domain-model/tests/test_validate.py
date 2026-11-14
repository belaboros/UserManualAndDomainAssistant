"""AC-15: validate runs the SHACL on the samples (plan 0002, T16)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from dm_fixtures import EXAMPLE_DIR, copy_example, run_cli

PREFIXES = (
    "@prefix lib: <https://example.org/library#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
)


def _write(folder: Path, name: str, body: str) -> None:
    (folder / "samples" / name).write_text(PREFIXES + body, encoding="utf-8")


def _fails(capsys: Any, folder: Path, start: str, command: str = "validate") -> str:
    code, out = run_cli(capsys, command, str(folder))
    assert code == 1
    assert any(line.startswith(start) for line in out.splitlines()), out
    return out


def test_example_samples_pass(capsys: Any) -> None:
    assert run_cli(capsys, "validate", str(EXAMPLE_DIR)) == (0, "")


def test_unflagged_violation_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    _write(folder, "R1.violates.ttl", "lib:loan1 a lib:Loan ; lib:hasItem lib:book1 .")
    _fails(capsys, folder, "samples/R1.violates.ttl:R1:")


def test_flagged_valid_sample_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    _write(folder, "valid.ttl", "lib:loan9 a lib:Loan ; lib:hasStatus lib:Lost .")
    out = _fails(capsys, folder, "samples/valid.ttl:R1:")
    assert "samples/valid.ttl:R2:" in out


def test_missing_derivation_fails(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    _write(folder, "R5.expected.ttl", "lib:loan1 a lib:OpenLoan, lib:LateLoan .")
    _fails(capsys, folder, "samples/R5.expected.ttl:R5:")


def test_check_runs_validate(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    _write(folder, "R1.violates.ttl", "lib:loan1 a lib:Loan ; lib:hasItem lib:book1 .")
    _fails(capsys, folder, "samples/R1.violates.ttl:R1:", command="check")


# Sample-coverage findings (check and validate both report them).
@pytest.mark.parametrize(
    ("name", "body", "start"),
    [
        ("R9.violates.ttl", "", "samples/R9.violates.ttl:R9:"),
        ("R5.violates.ttl", "", "samples/R5.violates.ttl:R5:"),
        ("R1.derives.ttl", "", "samples/R1.derives.ttl:R1:"),
        ("R6.derives-2.ttl", "", "samples/R6.derives-2.ttl:R6:"),
        ("notes.ttl", "", "samples/notes.ttl:"),
        ("R1.violates.ttl", "this is not turtle", "samples/R1.violates.ttl:"),
    ],
    ids=[
        "sample_unknown_rule",
        "sample_wrong_kind",
        "sample_derives_for_constraint",
        "sample_no_expected",
        "sample_bad_name",
        "sample_does_not_parse",
    ],
)
def test_sample_coverage(tmp_path: Path, capsys: Any, name: str, body: str, start: str) -> None:
    folder = copy_example(tmp_path)
    _write(folder, name, body)
    _fails(capsys, folder, start, command="check")


def test_sample_missing_valid(tmp_path: Path, capsys: Any) -> None:
    folder = copy_example(tmp_path)
    (folder / "samples" / "valid.ttl").unlink()
    _fails(capsys, folder, "samples/valid.ttl:", command="check")
