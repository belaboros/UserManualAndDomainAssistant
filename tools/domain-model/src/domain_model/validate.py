"""Run the generated SHACL on the samples and map results back to rules (FR-13); sample coverage.

Sample files (``samples/``):

- ``valid.ttl`` must conform (required, may be empty);
- ``<RuleId>.violates[-<n>].ttl`` must produce a violation from that rule's shape;
- ``<RuleId>.derives[-<n>].ttl`` + ``<RuleId>.expected[-<n>].ttl``: after the SHACL-AF rules ran,
  every expected triple must be in the data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, URIRef
from rdflib.namespace import SH

from domain_model.model import Domain, Finding, Rule
from domain_model.rdf.owl import owl_graph
from domain_model.rdf.shacl import shacl_graph, shape_iri

SAMPLES = "samples"
VALID = "valid.ttl"
_NAME = re.compile(r"^(?P<rule>[A-Za-z][A-Za-z0-9_]*)\.(?P<kind>violates|derives|expected)(?P<n>-\d+)?\.ttl$")
_WANTED = {"constraint": ("violates",), "derivation": ("derives", "expected")}


@dataclass(frozen=True)
class Sample:
    name: str
    rule: str
    kind: str  # violates | derives | expected
    n: str

    @property
    def file(self) -> str:
        return f"{SAMPLES}/{self.name}"


def _scan(folder: Path) -> tuple[list[Sample], list[Finding]]:
    """The well-named sample files, plus findings for names that break the convention."""
    samples, findings = [], []
    directory = folder / SAMPLES
    names = sorted(p.name for p in directory.iterdir() if p.is_file()) if directory.is_dir() else []
    if VALID not in names:
        findings.append(Finding(f"{SAMPLES}/{VALID}", "", "missing (required; it may be empty)"))
    for name in names:
        match = _NAME.match(name)
        if match:
            samples.append(Sample(name, match["rule"], match["kind"], match["n"] or ""))
        elif name != VALID:
            findings.append(
                Finding(f"{SAMPLES}/{name}", "", "name does not follow <RuleId>.<kind>[-<n>].ttl")
            )
    return samples, findings


def _sample_findings(samples: list[Sample], rules: dict[str, Rule]) -> list[Finding]:
    findings = []
    keys = {(s.rule, s.kind, s.n) for s in samples}
    for s in samples:
        rule = rules.get(s.rule)
        partner = {"derives": "expected", "expected": "derives"}.get(s.kind)
        if rule is None:
            findings.append(Finding(s.file, s.rule, "names an unknown rule"))
        elif s.kind not in _WANTED[rule.kind]:
            findings.append(
                Finding(s.file, s.rule, f"a {rule.kind} rule takes {' / '.join(_WANTED[rule.kind])} samples")
            )
        elif partner and (s.rule, partner, s.n) not in keys:
            findings.append(Finding(s.file, s.rule, f"has no matching {s.rule}.{partner}{s.n}.ttl"))
    return findings


def coverage_findings(domain: Domain) -> list[Finding]:
    """Badly named samples, samples for unknown rules or of the wrong kind, and rules without a sample."""
    samples, findings = _scan(domain.folder)
    rules = {r.id: r for r in domain.ontology.rules}
    findings += _sample_findings(samples, rules)
    proving = {(s.rule, s.kind) for s in samples}
    for rule in domain.ontology.rules:
        kind = _WANTED[rule.kind][0]
        if (rule.id, kind) not in proving:
            findings.append(
                Finding(SAMPLES, rule.id, f"no sample proves this rule; add {rule.id}.{kind}.ttl")
            )
    return findings


class _Runner:
    """pyshacl with RDFS inference and SHACL-AF; shapes and ontology are built once per domain."""

    def __init__(self, domain: Domain) -> None:
        self.folder = domain.folder / SAMPLES
        self.shapes = shacl_graph(domain)
        self.ontology = owl_graph(domain)
        self.rule_of: dict[str, str] = {}
        for rule in domain.ontology.rules:
            shape = str(shape_iri(domain.ontology, rule.id))
            self.rule_of[shape] = self.rule_of[f"{shape}_property"] = rule.id

    def parse(self, name: str) -> Graph:
        return Graph().parse(self.folder / name, format="turtle")

    def run(self, data: Graph) -> set[str]:
        """Apply the rules to ``data`` in place; returns the ids of the rules that reported a violation."""
        _, results, _ = validate(
            data,
            shacl_graph=self.shapes,
            ont_graph=self.ontology,
            inference="rdfs",
            advanced=True,
            inplace=True,
        )
        if not isinstance(results, Graph):
            raise TypeError("pyshacl returned no results graph")
        sources = {str(s) for s in results.objects(None, SH.sourceShape) if isinstance(s, URIRef)}
        return {self.rule_of.get(s, s) for s in sources}


def _check_sample(runner: _Runner, sample: Sample | None) -> list[Finding]:
    name = sample.name if sample else VALID
    file = f"{SAMPLES}/{name}"
    data = runner.parse(name)
    violated = runner.run(data)
    if sample is None:
        return [Finding(file, rule, "valid sample violates this rule") for rule in sorted(violated)]
    if sample.kind == "violates" and sample.rule not in violated:
        return [Finding(file, sample.rule, "produced no violation from this rule's shape")]
    if sample.kind == "derives":
        expected_name = f"{sample.rule}.expected{sample.n}.ttl"
        missing = [t for t in runner.parse(expected_name) if t not in data]
        return [
            Finding(
                f"{SAMPLES}/{expected_name}",
                sample.rule,
                f"expected triple not derived: {s.n3()} {p.n3()} {o.n3()}",
            )
            for s, p, o in sorted(missing)
        ]
    return []


def validate_findings(domain: Domain) -> list[Finding]:
    """Run every well-formed sample; a sample that does not parse is a finding."""
    samples, _ = _scan(domain.folder)
    runner = _Runner(domain)
    findings: list[Finding] = []
    todo: list[Sample | None] = [None] if (runner.folder / VALID).is_file() else []
    todo += [s for s in samples if s.kind in ("violates", "derives")]
    for sample in todo:
        try:
            findings += _check_sample(runner, sample)
        except Exception as err:  # rdflib raises assorted parser errors
            name = sample.name if sample else VALID
            findings.append(Finding(f"{SAMPLES}/{name}", "", f"does not parse: {str(err).splitlines()[0]}"))
    return findings
