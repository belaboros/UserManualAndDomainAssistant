"""The OWL 2 ontology graph from ``ontology.yaml``, with ``ontology.axioms.ttl`` merged in (FR-4)."""

from __future__ import annotations

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD, BNode, Graph, Literal, URIRef

from domain_model.model import Concept, Domain, Individual, Ontology, Property, Relation, cardinality_bounds
from domain_model.rdf.vocab import (
    annotate_status,
    annotate_terms,
    literal,
    namespace,
    new_graph,
    ontology_iri,
)

CHARACTERISTICS = {
    "functional": OWL.FunctionalProperty,
    "inverse_functional": OWL.InverseFunctionalProperty,
    "transitive": OWL.TransitiveProperty,
    "symmetric": OWL.SymmetricProperty,
    "asymmetric": OWL.AsymmetricProperty,
    "reflexive": OWL.ReflexiveProperty,
    "irreflexive": OWL.IrreflexiveProperty,
}

# (qualified, unqualified) cardinality predicates
_EXACT = (OWL.qualifiedCardinality, OWL.cardinality)
_MIN = (OWL.minQualifiedCardinality, OWL.minCardinality)
_MAX = (OWL.maxQualifiedCardinality, OWL.maxCardinality)

#: How a restriction is qualified: (owl:onClass | owl:onDataRange, filler), or None (unqualified).
Qualifier = tuple[URIRef, URIRef] | None


def _header(graph: Graph, onto: Ontology) -> None:
    ns = namespace(onto)
    lang = onto.language
    graph.add((ontology_iri(onto), RDF.type, OWL.Ontology))
    graph.add((ontology_iri(onto), RDFS.label, Literal(f"{onto.label} ontology", lang=lang)))
    for prop in (DCTERMS.source, SKOS.definition, SKOS.altLabel):
        graph.add((prop, RDF.type, OWL.AnnotationProperty))
    graph.add((ns.level, RDF.type, OWL.AnnotationProperty))
    graph.add((ns.level, RDFS.label, Literal("learnability level", lang=lang)))
    graph.add((ns.level, RDFS.range, XSD.integer))
    graph.add((ns.status, RDF.type, OWL.AnnotationProperty))
    graph.add((ns.status, RDFS.label, Literal("status (confirmed or draft)", lang=lang)))


def _restriction(
    graph: Graph, on: tuple[URIRef, URIRef], predicates: tuple[URIRef, URIRef], n: int, q: Qualifier
) -> None:
    owner, prop = on
    node = BNode()
    graph.add((owner, RDFS.subClassOf, node))
    graph.add((node, RDF.type, OWL.Restriction))
    graph.add((node, OWL.onProperty, prop))
    graph.add((node, predicates[0] if q else predicates[1], Literal(n, datatype=XSD.nonNegativeInteger)))
    if q:
        graph.add((node, q[0], q[1]))


def _cardinality(graph: Graph, on: tuple[URIRef, URIRef], cardinality: str | None, q: Qualifier) -> None:
    """Qualified cardinality restrictions on the domain class (read from the domain side)."""
    if not cardinality:
        return
    low, high = cardinality_bounds(cardinality)
    if low == high:
        _restriction(graph, on, _EXACT, low, q)
        return
    if low > 0:
        _restriction(graph, on, _MIN, low, q)
    if high is not None:
        _restriction(graph, on, _MAX, high, q)


def _concept(graph: Graph, onto: Ontology, c: Concept) -> None:
    ns = namespace(onto)
    node = ns[c.id]
    graph.add((node, RDF.type, OWL.Class))
    annotate_terms(graph, node, onto, c)
    annotate_status(graph, node, onto, c)
    for parent in c.parents:
        graph.add((node, RDFS.subClassOf, ns[parent]))
    for other in c.disjoint_with:
        graph.add((node, OWL.disjointWith, ns[other]))


def _relation(graph: Graph, onto: Ontology, r: Relation) -> None:
    ns = namespace(onto)
    node = ns[r.id]
    graph.add((node, RDF.type, OWL.ObjectProperty))
    annotate_terms(graph, node, onto, r)
    annotate_status(graph, node, onto, r)
    links = [
        (RDFS.domain, r.domain),
        (RDFS.range, r.range),
        (OWL.inverseOf, r.inverse),
        (RDFS.subPropertyOf, r.parent),
    ]
    for predicate, target in links:
        if target:
            graph.add((node, predicate, ns[target]))
    for characteristic in r.characteristics:
        graph.add((node, RDF.type, CHARACTERISTICS[characteristic]))
    if r.domain:
        qualifier = (OWL.onClass, ns[r.range]) if r.range else None
        _cardinality(graph, (ns[r.domain], node), r.cardinality, qualifier)


def _property(graph: Graph, onto: Ontology, p: Property) -> None:
    ns = namespace(onto)
    node = ns[p.id]
    graph.add((node, RDF.type, OWL.DatatypeProperty))
    annotate_terms(graph, node, onto, p)
    annotate_status(graph, node, onto, p)
    graph.add((node, RDFS.range, XSD[p.datatype]))
    if p.domain:
        graph.add((node, RDFS.domain, ns[p.domain]))
        _cardinality(graph, (ns[p.domain], node), p.cardinality, (OWL.onDataRange, XSD[p.datatype]))


def _individual(graph: Graph, onto: Ontology, i: Individual) -> None:
    ns = namespace(onto)
    node = ns[i.id]
    graph.add((node, RDF.type, OWL.NamedIndividual))
    annotate_terms(graph, node, onto, i)
    annotate_status(graph, node, onto, i)
    for t in i.types:
        graph.add((node, RDF.type, ns[t]))
    for relation, targets in i.facts.items():
        for target in targets:
            graph.add((node, ns[relation], ns[target]))
    datatypes = {p.id: p.datatype for p in onto.properties}
    for prop, value in i.values.items():
        graph.add((node, ns[prop], literal(value, datatypes.get(prop, "string"))))


def owl_graph(domain: Domain) -> Graph:
    """The ontology graph (not yet canonical; see :mod:`domain_model.rdf.serialize`)."""
    onto = domain.ontology
    graph = new_graph(onto)
    _header(graph, onto)
    for c in onto.concepts:
        _concept(graph, onto, c)
    for r in onto.relations:
        _relation(graph, onto, r)
    for p in onto.properties:
        _property(graph, onto, p)
    for i in onto.individuals:
        _individual(graph, onto, i)
    if domain.axioms is not None:
        axioms = Graph().parse(data=domain.axioms, format="turtle")
        for prefix, ns in axioms.namespaces():
            if prefix not in dict(graph.namespaces()):
                graph.bind(prefix, ns)
        graph += axioms
    return graph
