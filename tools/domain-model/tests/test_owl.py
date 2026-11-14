"""AC-5, AC-10 (OWL), AC-11 (RDF): the OWL graph holds a triple for every YAML field (plan 0002, T6)."""

from __future__ import annotations

import pytest
from dm_fixtures import EXAMPLE_DIR
from domain_model.load import load_domain
from domain_model.model import Domain
from domain_model.rdf.owl import owl_graph
from rdflib import Graph

PREFIXES = """
PREFIX lib: <https://example.org/library#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# One ASK pattern per YAML field (AC-5).
CASES = {
    "ontology": "<https://example.org/library> a owl:Ontology .",
    "class": "lib:Book a owl:Class .",
    "subclass": "lib:Book rdfs:subClassOf lib:Item .",
    "also_parents": "lib:EBook rdfs:subClassOf lib:Book, lib:DigitalResource .",
    "disjointness": "lib:AudioVisualItem owl:disjointWith lib:Book .",
    "label": 'lib:Book rdfs:label "book"@en .',
    "synonym": 'lib:Member skos:altLabel "borrower"@en, "patron"@en .',
    "definition": 'lib:Book skos:definition "A printed item with pages."@en .',
    "source": 'lib:hasItem dct:source "S1", "S2" .',
    "level": "lib:Shelf lib:level 3 .",
    "status": 'lib:Librarian lib:status "draft" .',
    "object_property": "lib:hasItem a owl:ObjectProperty .",
    "domain_range": "lib:hasItem rdfs:domain lib:Loan ; rdfs:range lib:Item .",
    "inverse": "lib:borrowerOf owl:inverseOf lib:hasBorrower .",
    "super_property": "lib:hasBorrower rdfs:subPropertyOf lib:hasParticipant .",
    "characteristics": "lib:hasBorrower a owl:FunctionalProperty ."
    " lib:borrowerOf a owl:InverseFunctionalProperty ."
    " lib:branchOf a owl:AsymmetricProperty, owl:IrreflexiveProperty .",
    "exact_cardinality": "lib:Loan rdfs:subClassOf [ owl:onProperty lib:hasBorrower ;"
    ' owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ; owl:onClass lib:Member ] .',
    "min_cardinality": "lib:Loan rdfs:subClassOf [ owl:onProperty lib:hasItem ;"
    ' owl:minQualifiedCardinality "1"^^xsd:nonNegativeInteger ; owl:onClass lib:Item ] .',
    "max_cardinality": "lib:Loan rdfs:subClassOf [ owl:onProperty lib:issuedBy ;"
    ' owl:maxQualifiedCardinality "1"^^xsd:nonNegativeInteger ; owl:onClass lib:Librarian ] .',
    "range_cardinality": "lib:Branch rdfs:subClassOf [ owl:onProperty lib:hasShelf ;"
    ' owl:minQualifiedCardinality "2"^^xsd:nonNegativeInteger ] , [ owl:onProperty lib:hasShelf ;'
    ' owl:maxQualifiedCardinality "4"^^xsd:nonNegativeInteger ] .',
    "data_property": "lib:dueDate a owl:DatatypeProperty ; rdfs:domain lib:Loan ; rdfs:range xsd:date .",
    "data_cardinality": "lib:Loan rdfs:subClassOf [ owl:onProperty lib:dueDate ;"
    ' owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ; owl:onDataRange xsd:date ] .',
    "individual_type": "lib:CentralBranch a owl:NamedIndividual, lib:Branch .",
    "individual_fact": "lib:CentralBranch lib:branchOf lib:MainLibrary .",
    "individual_values": 'lib:HobbitCopy lib:title "The Hobbit" ; lib:pageCount 310 ;'
    " lib:isReference false .",
    "annotation_properties": "lib:level a owl:AnnotationProperty . lib:status a owl:AnnotationProperty .",
}


@pytest.fixture(scope="module")
def graph() -> Graph:
    domain, _ = load_domain(EXAMPLE_DIR)
    assert isinstance(domain, Domain)
    return owl_graph(domain)


@pytest.mark.parametrize("pattern", CASES.values(), ids=CASES.keys())
def test_owl_triples(graph: Graph, pattern: str) -> None:
    assert graph.query(f"{PREFIXES} ASK {{ {pattern} }}").askAnswer, pattern


def test_cardinality_star_adds_no_restriction(graph: Graph) -> None:
    query = f"{PREFIXES} ASK {{ ?r owl:onProperty lib:servedBy }}"
    assert not graph.query(query).askAnswer


def test_axioms_file_is_merged(graph: Graph) -> None:
    query = f"{PREFIXES} ASK {{ lib:Agent owl:equivalentClass [ owl:unionOf ?list ] }}"
    assert graph.query(query).askAnswer
