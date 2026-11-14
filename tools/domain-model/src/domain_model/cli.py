"""``domain-model`` command line: build, check and validate a domain folder (spec 0002).

Exit code 0 = clean, 1 = findings (one line each on stdout), 2 = usage error.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from domain_model.build import render_all, write_generated
from domain_model.consistency import model_findings
from domain_model.discover import discover
from domain_model.freshness import freshness_findings
from domain_model.load import load_domain
from domain_model.model import Domain, Finding
from domain_model.validate import coverage_findings, validate_findings


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="domain-model", description="Domain-model generator (spec 0002).")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="write <folder>/generated/").add_argument("folder", type=Path)
    sub.add_parser("validate", help="SHACL on the samples").add_argument("folder", type=Path)
    check = sub.add_parser("check", help="model, freshness, sample coverage and validate")
    check.add_argument("folder", type=Path, nargs="?")
    check.add_argument("--all", action="store_true", help="check every domain folder in the repo")
    return parser


def _report(findings: Sequence[Finding], prefix: str = "") -> int:
    for finding in findings:
        print(f"{prefix}{finding}")
    return 1 if findings else 0


def _model(folder: Path) -> tuple[Domain | None, list[Finding]]:
    """The loaded domain, or None with the load/model findings."""
    domain, findings = load_domain(folder)
    if domain is None:
        return None, findings
    findings = model_findings(domain)
    return (None if findings else domain), findings


def build(folder: Path) -> list[Finding]:
    """Write ``generated/``; refuses (and writes nothing) when the model has findings."""
    domain, findings = _model(folder)
    if domain is not None:
        write_generated(folder, render_all(domain))
    return findings


def check_folder(folder: Path) -> list[Finding]:
    """Every ``check`` finding for one domain folder."""
    domain, findings = _model(folder)
    if domain is None:
        return findings
    findings = freshness_findings(folder, render_all(domain))
    return findings + samples(domain)


def samples(domain: Domain) -> list[Finding]:
    """Sample coverage, then (when coverage is clean) the SHACL run on every sample."""
    findings = coverage_findings(domain)
    return findings or validate_findings(domain)


def validate_folder(folder: Path) -> list[Finding]:
    domain, findings = _model(folder)
    return findings if domain is None else samples(domain)


def _check_all(root: Path) -> int:
    """``check`` on every domain folder under ``root``; findings are prefixed with the folder."""
    code = 0
    for folder in discover(root):
        code |= _report(check_folder(folder), prefix=f"{folder.relative_to(root).as_posix()}/")
    return code


def main(argv: list[str] | None = None) -> int:
    """Entry point; returns the exit code."""
    args = _parser().parse_args(argv)
    if args.command == "check" and args.all:
        return _check_all(Path.cwd())
    if args.folder is None:
        print("domain-model: check needs a folder or --all", file=sys.stderr)
        return 2
    if not args.folder.is_dir():
        print(f"domain-model: {args.folder} is not a folder", file=sys.stderr)
        return 2
    if args.command == "build":
        return _report(build(args.folder))
    if args.command == "validate":
        return _report(validate_folder(args.folder))
    return _report(check_folder(args.folder))


if __name__ == "__main__":
    sys.exit(main())
