"""Namespaces and the annotations every generated resource carries (plan 0002, "RDF vocabulary used")."""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.namespace import SH

from domain_model.model import TYPE_PREDICATE, Datatype, Item, Ontology, Rule, Scalar


def namespace(onto: Ontology) -> Namespace:
    return Namespace(onto.namespace)


def ontology_iri(onto: Ontology) -> URIRef:
    return URIRef(onto.namespace.rstrip("#/"))


type ResolveFn = Callable[[str], URIRef]


def resolver(onto: Ontology) -> ResolveFn:
    """Name → IRI in the domain namespace (``a`` is rdf:type)."""
    ns = namespace(onto)

    def resolve(name: str) -> URIRef:
        return RDF.type if name == TYPE_PREDICATE else ns[name]

    return resolve


def new_graph(onto: Ontology) -> Graph:
    graph = Graph(bind_namespaces="none")
    graph.bind(onto.prefix, namespace(onto))
    for prefix, ns in (("owl", OWL), ("rdf", RDF), ("rdfs", RDFS), ("xsd", XSD)):
        graph.bind(prefix, ns)
    graph.bind("skos", SKOS)
    graph.bind("dct", DCTERMS)
    graph.bind("sh", SH)
    return graph


def literal(value: Scalar, datatype: Datatype) -> Literal:
    """A typed literal (plain for strings); booleans are written as ``true``/``false``, dates in ISO form."""
    if isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, dt.date | dt.datetime):
        text = value.isoformat()
    else:
        text = str(value)
    return Literal(text) if datatype == "string" else Literal(text, datatype=XSD[datatype])


def annotate_status(graph: Graph, node: URIRef, onto: Ontology, entry: Item | Rule) -> None:
    """Level, status and sources (every generated resource, FR-9, FR-10)."""
    ns = namespace(onto)
    graph.add((node, ns.level, Literal(entry.level, datatype=XSD.integer)))
    graph.add((node, ns.status, Literal(entry.status)))
    for source in entry.source:
        graph.add((node, DCTERMS.source, Literal(source)))


def annotate_terms(
    graph: Graph, node: URIRef, onto: Ontology, entry: Item, label: URIRef = RDFS.label
) -> None:
    """Label, synonyms and definition in the domain language."""
    lang = onto.language
    graph.add((node, label, Literal(entry.label, lang=lang)))
    for synonym in entry.synonyms:
        graph.add((node, SKOS.altLabel, Literal(synonym, lang=lang)))
    if entry.definition:
        graph.add((node, SKOS.definition, Literal(entry.definition, lang=lang)))
