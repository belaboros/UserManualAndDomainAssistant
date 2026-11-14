"""Model checks of FR-12: references, levels, is-a cycles and reachability, axioms and rule syntax.

Each ``check_*`` function returns a list of findings; :func:`model_findings` runs them all.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Any

from rdflib import Graph, URIRef
from rdflib.paths import Path as RdfPath
from rdflib.plugins.sparql import prepareQuery

from domain_model.load import AXIOMS, ONTOLOGY, STATEMENTS, TAXONOMY
from domain_model.model import (
    TYPE_PREDICATE,
    CardinalityPattern,
    Concept,
    Condition,
    DerivePattern,
    Domain,
    EqualPattern,
    Finding,
    ImpliesPattern,
    Individual,
    Item,
    Ontology,
    Pattern,
    Property,
    Relation,
    Rule,
    SparqlPattern,
    TreeNode,
    ValuesPattern,
)
from domain_model.paths import PathSyntaxError, names, parse_path

CONCEPT = "concept"
INDIVIDUAL = "individual"
RELATION = "relation"
PROPERTY = "property"
PREDICATE = (RELATION, PROPERTY)
#: Annotation properties the generator itself defines in the domain namespace.
RESERVED = ("level", "status")


@dataclass(frozen=True)
class Ref:
    """One id an item uses, the field it appears in, and the kinds of item it may name."""

    field: str
    id: str
    kinds: tuple[str, ...]


def kind_index(onto: Ontology) -> dict[str, str]:
    """id → kind for every concept, individual, relation and property."""
    index: dict[str, str] = {}
    sections: list[tuple[str, Iterable[Item]]] = [
        (CONCEPT, onto.concepts),
        (INDIVIDUAL, onto.individuals),
        (RELATION, onto.relations),
        (PROPERTY, onto.properties),
    ]
    for kind, items in sections:
        for entry in items:
            index.setdefault(entry.id, kind)
    return index


# ---------------------------------------------------------------------------- what each item uses
def _concept_refs(c: Concept) -> list[Ref]:
    refs = [Ref("parent", p, (CONCEPT,)) for p in c.parents]
    return refs + [Ref("disjoint_with", d, (CONCEPT,)) for d in c.disjoint_with]


def _individual_refs(i: Individual) -> list[Ref]:
    refs = [Ref("types", t, (CONCEPT,)) for t in i.types]
    for relation, targets in i.facts.items():
        refs.append(Ref("facts", relation, (RELATION,)))
        refs += [Ref(f"facts.{relation}", t, (INDIVIDUAL,)) for t in targets]
    return refs + [Ref("values", p, (PROPERTY,)) for p in i.values]


def _relation_refs(r: Relation) -> list[Ref]:
    fields = [("domain", r.domain, CONCEPT), ("range", r.range, CONCEPT)]
    fields += [("inverse", r.inverse, RELATION), ("parent", r.parent, RELATION)]
    return [Ref(f, v, (k,)) for f, v, k in fields if v]


def _property_refs(p: Property) -> list[Ref]:
    return [Ref("domain", p.domain, (CONCEPT,))] if p.domain else []


def path_refs(field: str, text: str) -> list[Ref]:
    """The relations/properties a path uses; raises :class:`PathSyntaxError`."""
    used = sorted(names(parse_path(text)) - {TYPE_PREDICATE})
    return [Ref(field, n, PREDICATE) for n in used]


def _condition_refs(field: str, cond: Condition) -> list[Ref]:
    refs = path_refs(f"{field}.path", cond.path)
    if isinstance(cond.has_value, str):
        refs.append(Ref(f"{field}.has_value", cond.has_value, (INDIVIDUAL,)))
    refs += [Ref(f"{field}.in", v, (INDIVIDUAL,)) for v in cond.in_ or []]
    if cond.class_:
        refs.append(Ref(f"{field}.class", cond.class_, (CONCEPT,)))
    return refs


def _walk_iris(node: Any) -> Iterator[URIRef]:
    """Every IRI inside a parsed SPARQL algebra tree."""
    if isinstance(node, URIRef):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _walk_iris(value)
    elif isinstance(node, list | tuple | set):
        for value in node:
            yield from _walk_iris(value)
    elif isinstance(node, RdfPath):
        yield from _walk_iris(list(vars(node).values()))


def sparql_iris(onto: Ontology, query: str) -> list[str]:
    """Local names of the domain-namespace IRIs a SPARQL query uses; raises on a parse error."""
    parsed = prepareQuery(query, initNs=onto.sparql_prefixes())
    local = {
        str(i)[len(onto.namespace) :] for i in _walk_iris(parsed.algebra) if i.startswith(onto.namespace)
    }
    return sorted(local)


def _derive_refs(d: DerivePattern, index: dict[str, str]) -> list[Ref]:
    refs = _condition_refs("derive.if", d.if_) if d.if_ else []
    if d.add.predicate != TYPE_PREDICATE:
        refs.append(Ref("derive.add.predicate", d.add.predicate, PREDICATE))
    if index.get(d.add.object) in (CONCEPT, INDIVIDUAL):
        return [*refs, Ref("derive.add.object", d.add.object, (CONCEPT, INDIVIDUAL))]
    return refs + path_refs("derive.add.object", d.add.object)


def _values_refs(key: str, in_: list[str] | None, class_: str | None) -> list[Ref]:
    refs = [Ref(f"{key}.in", v, (INDIVIDUAL,)) for v in in_ or []]
    return refs + ([Ref(f"{key}.class", class_, (CONCEPT,))] if class_ else [])


def _body_refs(p: Pattern, onto: Ontology, index: dict[str, str]) -> list[Ref]:
    match p:
        case CardinalityPattern():
            return path_refs("cardinality.path", p.path) + _values_refs("cardinality", None, p.class_)
        case ValuesPattern():
            return path_refs("values.path", p.path) + _values_refs("values", p.in_, p.class_)
        case ImpliesPattern():
            return _condition_refs("implies.if", p.if_) + _condition_refs("implies.then", p.then)
        case EqualPattern():
            return path_refs("equal.left", p.left) + path_refs("equal.right", p.right)
        case DerivePattern():
            return _derive_refs(p, index)
        case SparqlPattern():
            kinds = (CONCEPT, INDIVIDUAL, RELATION, PROPERTY)
            return [Ref("sparql", n, kinds) for n in sparql_iris(onto, p.query)]


def _pattern_refs(rule: Rule, onto: Ontology, index: dict[str, str]) -> list[Ref]:
    focus = Ref(f"{rule.pattern_key}.focus", rule.pattern.focus, (CONCEPT,))
    return [focus, *_body_refs(rule.pattern, onto, index)]


def rule_refs(rule: Rule, onto: Ontology, index: dict[str, str]) -> tuple[list[Ref], list[str]]:
    """What a rule uses, plus syntax errors (bad path, unparsable SPARQL) that hide part of it."""
    try:
        return _pattern_refs(rule, onto, index), []
    except PathSyntaxError as err:
        return [], [f"path syntax: {err}"]
    except Exception as err:  # rdflib raises pyparsing and assorted errors on bad SPARQL
        return [], [f"SPARQL does not parse: {str(err).splitlines()[0]}"]


def item_refs(entry: Item) -> list[Ref]:
    match entry:
        case Concept():
            return _concept_refs(entry)
        case Individual():
            return _individual_refs(entry)
        case Relation():
            return _relation_refs(entry)
        case Property():
            return _property_refs(entry)
        case _:
            return []


# ---------------------------------------------------------------------------- checks
def check_duplicates(domain: Domain) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[str] = set()
    for s in domain.statements:
        if s.id in seen:
            findings.append(Finding(STATEMENTS, s.id, "duplicate statement id"))
        seen.add(s.id)
    seen = set()
    ids = [i.id for i in domain.ontology.items] + [r.id for r in domain.ontology.rules]
    for item_id in ids:
        if item_id in seen or item_id in RESERVED:
            findings.append(Finding(ONTOLOGY, item_id, "duplicate or reserved id"))
        seen.add(item_id)
    tree_ids = [t.id for t in domain.taxonomy.trees]
    findings += [
        Finding(TAXONOMY, t, "duplicate tree id")
        for t in sorted({t for t in tree_ids if tree_ids.count(t) > 1})
    ]
    return findings


def _all_entries(onto: Ontology) -> list[Item | Rule]:
    return [*onto.items, *onto.rules]


def check_sources_and_levels(domain: Domain) -> list[Finding]:
    statement_ids = {s.id for s in domain.statements}
    findings = [
        Finding(STATEMENTS, s.id, f"level {s.level} is outside 1–3")
        for s in domain.statements
        if not 1 <= s.level <= 3
    ]
    onto = domain.ontology
    if not 1 <= onto.working_level <= 3:
        findings.append(Finding(ONTOLOGY, "working_level", f"level {onto.working_level} is outside 1–3"))
    for entry in _all_entries(onto):
        if not 1 <= entry.level <= 3:
            findings.append(Finding(ONTOLOGY, entry.id, f"level {entry.level} is outside 1–3"))
        findings += [
            Finding(ONTOLOGY, entry.id, f"source cites unknown statement {s}")
            for s in entry.source
            if s not in statement_ids
        ]
    return findings


def _refs_of(entry: Item | Rule, onto: Ontology, index: dict[str, str]) -> tuple[list[Ref], list[str]]:
    return rule_refs(entry, onto, index) if isinstance(entry, Rule) else (item_refs(entry), [])


def check_references_and_level_order(domain: Domain) -> list[Finding]:
    """Undefined references, rule syntax, and items with a lower level than an item they use."""
    onto = domain.ontology
    index = kind_index(onto)
    levels = {i.id: i.level for i in onto.items}
    findings: list[Finding] = []
    for entry in _all_entries(onto):
        refs, errors = _refs_of(entry, onto, index)
        findings += [Finding(ONTOLOGY, entry.id, e) for e in errors]
        for ref in refs:
            if index.get(ref.id) not in ref.kinds:
                wanted = " or ".join(ref.kinds)
                findings.append(
                    Finding(ONTOLOGY, entry.id, f"{ref.field}: {ref.id} is not a defined {wanted}")
                )
            elif levels[ref.id] > entry.level:
                message = (
                    f"level {entry.level} is lower than {ref.id} (level {levels[ref.id]}), which it uses"
                )
                findings.append(Finding(ONTOLOGY, entry.id, message))
    return sorted(set(findings))


def _find_cycle(start: str, parents: dict[str, list[str]]) -> list[str] | None:
    """A parent cycle through ``start``, as a list of ids that starts and ends with ``start``."""
    stack: list[tuple[str, list[str]]] = [(start, [start])]
    visited: set[str] = set()
    while stack:
        node, trail = stack.pop()
        for parent in parents.get(node, []):
            if parent == start:
                return [*trail, start]
            if parent not in visited:
                visited.add(parent)
                stack.append((parent, [*trail, parent]))
    return None


def check_taxonomy(domain: Domain) -> list[Finding]:
    """Parent cycles, and concepts not reachable from a top concept of the is-a taxonomy."""
    concepts = domain.ontology.concepts
    parents = {c.id: c.parents for c in concepts}
    findings: list[Finding] = []
    in_cycle: set[str] = set()
    for c in concepts:
        cycle = _find_cycle(c.id, parents)
        if cycle:
            in_cycle.add(c.id)
            findings.append(Finding(ONTOLOGY, c.id, f"parent cycle: {' → '.join(cycle)}"))
    reached = {c.id for c in concepts if not c.parents}
    changed = True
    while changed:
        new = {c.id for c in concepts if c.id not in reached and any(p in reached for p in c.parents)}
        reached |= new
        changed = bool(new)
    for c in concepts:
        if c.id not in reached and c.id not in in_cycle:
            findings.append(Finding(ONTOLOGY, c.id, "not reachable from a top concept in the is-a taxonomy"))
    return findings


def _tree_ids(nodes: list[TreeNode]) -> Iterator[str]:
    for node in nodes:
        yield node.id
        yield from _tree_ids(node.children)


def check_trees(domain: Domain) -> list[Finding]:
    concepts = {c.id for c in domain.ontology.concepts}
    return [
        Finding(TAXONOMY, tree.id, f"{node} is not a defined concept")
        for tree in domain.taxonomy.trees
        for node in _tree_ids(tree.top)
        if node not in concepts
    ]


def check_axioms(domain: Domain) -> list[Finding]:
    """The hand axioms parse and use only ids that ontology.yaml defines."""
    if domain.axioms is None:
        return []
    try:
        graph = Graph().parse(data=domain.axioms, format="turtle")
    except Exception as err:  # rdflib raises assorted parser errors
        return [Finding(AXIOMS, "", f"does not parse: {str(err).splitlines()[0]}")]
    ns = domain.ontology.namespace
    known = set(kind_index(domain.ontology)) | set(RESERVED)
    used = {
        str(t)[len(ns) :]
        for triple in graph
        for t in triple
        if isinstance(t, URIRef) and str(t).startswith(ns)
    }
    return [Finding(AXIOMS, name, "not defined in ontology.yaml") for name in sorted(used - known)]


def model_findings(domain: Domain) -> list[Finding]:
    """Every model problem of FR-12 (freshness and samples are checked elsewhere)."""
    findings: list[Finding] = []
    for check in (
        check_duplicates,
        check_sources_and_levels,
        check_references_and_level_order,
        check_taxonomy,
        check_trees,
        check_axioms,
    ):
        findings += check(domain)
    return findings
