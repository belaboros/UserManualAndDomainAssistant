"""SHACL (and SHACL-AF) shapes, generated entirely from the rules in ``ontology.yaml`` (FR-6).

Every rule becomes the node shape ``<prefix>:<RuleId>_shape``; a property shape it needs is
``<prefix>:<RuleId>_shape_property``. Validation results are mapped back to rules by these IRIs.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from rdflib import OWL, RDF, RDFS, XSD, BNode, Graph, Literal, Node, URIRef
from rdflib.collection import Collection
from rdflib.namespace import SH

from domain_model.model import (
    CardinalityPattern,
    Condition,
    DerivePattern,
    Domain,
    EqualPattern,
    ImpliesPattern,
    Ontology,
    Rule,
    Scalar,
    SparqlPattern,
    ValuesPattern,
)
from domain_model.paths import is_single, parse_path, to_shacl, to_sparql
from domain_model.rdf.vocab import ResolveFn, annotate_status, literal, namespace, new_graph, resolver


def shape_iri(onto: Ontology, rule_id: str) -> URIRef:
    return namespace(onto)[f"{rule_id}_shape"]


@dataclass(frozen=True)
class _Ctx:
    graph: Graph
    onto: Ontology
    resolve: ResolveFn
    shape: URIRef
    message: Literal

    @property
    def prefixes(self) -> URIRef:
        return namespace(self.onto)["_prefixes"]

    def path(self, text: str) -> Node:
        return to_shacl(self.graph, parse_path(text), self.resolve)

    def sparql_path(self, text: str) -> str:
        prefix = self.onto.prefix
        return to_sparql(parse_path(text), lambda n: "rdf:type" if n == "a" else f"{prefix}:{n}")

    def add(self, s: Node, p: Node, o: Node) -> None:
        self.graph.add((s, p, o))

    def rdf_list(self, items: list[Node]) -> BNode:
        head = BNode()
        Collection(self.graph, head, items)
        return head

    def property_shape(self, path: str) -> URIRef:
        node = URIRef(f"{self.shape}_property")
        self.add(self.shape, SH.property, node)
        self.add(node, RDF.type, SH.PropertyShape)
        self.add(node, SH.path, self.path(path))
        self.add(node, SH.message, self.message)
        return node


def _scalar(ctx: _Ctx, value: Scalar) -> Node:
    """A ``has_value``: a string names an individual, anything else is a typed literal."""
    match value:
        case str():
            return ctx.resolve(value)
        case bool():
            return literal(value, "boolean")
        case int():
            return literal(value, "integer")
        case float():
            return literal(value, "decimal")
        case dt.datetime():
            return literal(value, "dateTime")
        case dt.date():
            return literal(value, "date")


def _some(ctx: _Ctx, node: BNode, test: tuple[URIRef, Node]) -> None:
    """At least one value of the path satisfies ``test``."""
    qualifier = BNode()
    ctx.add(qualifier, *test)
    ctx.add(node, SH.qualifiedValueShape, qualifier)
    ctx.add(node, SH.qualifiedMinCount, Literal(1))


def _condition(ctx: _Ctx, cond: Condition) -> BNode:
    """A property shape: the focus node has at least one such value (or at least ``min`` values)."""
    node = BNode()
    ctx.add(node, RDF.type, SH.PropertyShape)  # pyshacl only accepts a declared shape as sh:condition
    ctx.add(node, SH.path, ctx.path(cond.path))
    if cond.has_value is not None:
        ctx.add(node, SH.hasValue, _scalar(ctx, cond.has_value))
    elif cond.in_ is not None:
        _some(ctx, node, (SH["in"], ctx.rdf_list([ctx.resolve(v) for v in cond.in_])))
    elif cond.class_ is not None:
        _some(ctx, node, (SH["class"], ctx.resolve(cond.class_)))
    elif cond.min is not None:
        ctx.add(node, SH.minCount, Literal(cond.min))
    return node


def _cardinality(ctx: _Ctx, p: CardinalityPattern) -> None:
    node = ctx.property_shape(p.path)
    if p.class_ is None:
        bounds = ((SH.minCount, p.min), (SH.maxCount, p.max))
    else:
        qualifier = BNode()
        ctx.add(qualifier, SH["class"], ctx.resolve(p.class_))
        ctx.add(node, SH.qualifiedValueShape, qualifier)
        bounds = ((SH.qualifiedMinCount, p.min), (SH.qualifiedMaxCount, p.max))
    for predicate, value in bounds:
        if value is not None:
            ctx.add(node, predicate, Literal(value))


def _values(ctx: _Ctx, p: ValuesPattern) -> None:
    node = ctx.property_shape(p.path)
    if p.in_ is not None:
        ctx.add(node, SH["in"], ctx.rdf_list([ctx.resolve(v) for v in p.in_]))
    elif p.class_ is not None:
        ctx.add(node, SH["class"], ctx.resolve(p.class_))
    elif p.datatype is not None:
        ctx.add(node, SH.datatype, XSD[p.datatype])


def _implies(ctx: _Ctx, p: ImpliesPattern) -> None:
    negated = BNode()
    ctx.add(negated, SH["not"], _condition(ctx, p.if_))
    ctx.add(ctx.shape, SH["or"], ctx.rdf_list([negated, _condition(ctx, p.then)]))


def _sparql_constraint(ctx: _Ctx, select: str) -> None:
    node = BNode()
    ctx.add(ctx.shape, SH.sparql, node)
    ctx.add(node, RDF.type, SH.SPARQLConstraint)
    ctx.add(node, SH.message, ctx.message)
    ctx.add(node, SH.prefixes, ctx.prefixes)
    ctx.add(node, SH.select, Literal(select))


def _equal(ctx: _Ctx, p: EqualPattern) -> None:
    if is_single(parse_path(p.left)) and is_single(parse_path(p.right)):
        node = ctx.property_shape(p.left)
        ctx.add(node, SH.equals, ctx.path(p.right))
        return
    left, right = ctx.sparql_path(p.left), ctx.sparql_path(p.right)
    select = (
        "SELECT $this ?value WHERE {\n"
        f"  {{ $this {left} ?value . FILTER NOT EXISTS {{ $this {right} ?value }} }}\n"
        f"  UNION {{ $this {right} ?value . FILTER NOT EXISTS {{ $this {left} ?value }} }}\n"
        "}"
    )
    _sparql_constraint(ctx, select)


def _derive_object(ctx: _Ctx, obj: str) -> Node:
    terms = {c.id for c in ctx.onto.concepts} | {i.id for i in ctx.onto.individuals}
    if obj in terms:
        return ctx.resolve(obj)
    node = BNode()
    ctx.add(node, SH.path, ctx.path(obj))
    return node


def _derive(ctx: _Ctx, p: DerivePattern) -> None:
    rule = BNode()
    ctx.add(ctx.shape, SH.rule, rule)
    ctx.add(rule, RDF.type, SH.TripleRule)
    ctx.add(rule, SH.subject, SH.this)
    ctx.add(rule, SH.predicate, ctx.resolve(p.add.predicate))
    ctx.add(rule, SH.object, _derive_object(ctx, p.add.object))
    if p.if_ is not None:
        ctx.add(rule, SH.condition, _condition(ctx, p.if_))


def _sparql(ctx: _Ctx, p: SparqlPattern) -> None:
    if p.select is not None:
        _sparql_constraint(ctx, p.select)
        return
    rule = BNode()
    ctx.add(ctx.shape, SH.rule, rule)
    ctx.add(rule, RDF.type, SH.SPARQLRule)
    ctx.add(rule, SH.prefixes, ctx.prefixes)
    ctx.add(rule, SH.construct, Literal(p.query))


def _rule_shape(graph: Graph, onto: Ontology, rule: Rule) -> None:
    shape = shape_iri(onto, rule.id)
    message = Literal(rule.statement, lang=onto.language)
    ctx = _Ctx(graph, onto, resolver(onto), shape, message)
    graph.add((shape, RDF.type, SH.NodeShape))
    graph.add((shape, SH.targetClass, ctx.resolve(rule.pattern.focus)))
    graph.add((shape, RDFS.label, message))
    graph.add((shape, SH.message, message))
    annotate_status(graph, shape, onto, rule)
    match rule.pattern:
        case CardinalityPattern():
            _cardinality(ctx, rule.pattern)
        case ValuesPattern():
            _values(ctx, rule.pattern)
        case ImpliesPattern():
            _implies(ctx, rule.pattern)
        case EqualPattern():
            _equal(ctx, rule.pattern)
        case DerivePattern():
            _derive(ctx, rule.pattern)
        case SparqlPattern():
            _sparql(ctx, rule.pattern)


def _prefix_declarations(graph: Graph, onto: Ontology) -> None:
    node = namespace(onto)["_prefixes"]
    graph.add((node, RDF.type, OWL.Ontology))
    for prefix, ns in sorted(onto.sparql_prefixes().items()):
        declaration = BNode()
        graph.add((node, SH.declare, declaration))
        graph.add((declaration, SH.prefix, Literal(prefix)))
        graph.add((declaration, SH.namespace, Literal(ns, datatype=XSD.anyURI)))


def shacl_graph(domain: Domain) -> Graph:
    onto = domain.ontology
    graph = new_graph(onto)
    if onto.rules:
        _prefix_declarations(graph, onto)
    for rule in onto.rules:
        _rule_shape(graph, onto, rule)
    return graph
