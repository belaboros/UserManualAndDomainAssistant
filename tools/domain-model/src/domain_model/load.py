"""Read a domain folder into a typed :class:`Domain`, reporting malformed input as findings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from domain_model.model import Domain, Finding, Ontology, StatementsFile, TaxonomyFile

STATEMENTS = "statements.yaml"
ONTOLOGY = "ontology.yaml"
TAXONOMY = "taxonomy.yaml"
AXIOMS = "ontology.axioms.ttl"


def _read_yaml(folder: Path, name: str, required: bool) -> tuple[Any, list[Finding]]:
    path = folder / name
    if not path.is_file():
        return ({} if not required else None), ([Finding(name, "", "file is missing")] if required else [])
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None)
        where = f"line {mark.line + 1}" if mark is not None else ""
        problem = getattr(err, "problem", None) or str(err)
        return None, [Finding(name, where, f"malformed YAML: {problem}")]
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, [Finding(name, "", "malformed YAML: the top level must be a mapping")]
    return data, []


def _item_id(data: Any, loc: tuple[int | str, ...]) -> str:
    """The id of the list item an error location points into, else a readable location."""
    node = data
    for key in loc:
        try:
            node = node[key]
        except KeyError, IndexError, TypeError:
            break
        if isinstance(key, int) and isinstance(node, dict) and "id" in node:
            return str(node["id"])
    return ".".join(str(k) for k in loc[:2]) or "-"


def _field_path(loc: tuple[int | str, ...]) -> str:
    """The field path below the list item, e.g. ``label`` or ``cardinality.focus``."""
    tail = [str(k) for k in loc if not isinstance(k, int)]
    return ".".join(tail[1:]) if len(tail) > 1 else ".".join(tail)


def _parse[M: BaseModel](model: type[M], name: str, data: Any) -> tuple[M | None, list[Finding]]:
    try:
        return model.model_validate(data), []
    except ValidationError as err:
        findings = []
        for error in err.errors():
            loc = tuple(error["loc"])
            field = _field_path(loc)
            message = f"{field}: {error['msg']}" if field else str(error["msg"])
            findings.append(Finding(name, _item_id(data, loc), message))
        return None, sorted(set(findings))


def load_domain(folder: Path) -> tuple[Domain | None, list[Finding]]:
    """Load the sources of ``folder``; returns ``(None, findings)`` when any source is malformed."""
    findings: list[Finding] = []
    raw_statements, problems = _read_yaml(folder, STATEMENTS, required=True)
    findings += problems
    raw_ontology, problems = _read_yaml(folder, ONTOLOGY, required=True)
    findings += problems
    raw_taxonomy, problems = _read_yaml(folder, TAXONOMY, required=False)
    findings += problems
    if findings:
        return None, findings
    statements, problems = _parse(StatementsFile, STATEMENTS, raw_statements)
    findings += problems
    ontology, problems = _parse(Ontology, ONTOLOGY, raw_ontology)
    findings += problems
    taxonomy, problems = _parse(TaxonomyFile, TAXONOMY, raw_taxonomy)
    findings += problems
    if statements is None or ontology is None or taxonomy is None:
        return None, findings
    axioms_path = folder / AXIOMS
    axioms = axioms_path.read_text(encoding="utf-8") if axioms_path.is_file() else None
    return Domain(folder, statements.statements, ontology, taxonomy, axioms), []
