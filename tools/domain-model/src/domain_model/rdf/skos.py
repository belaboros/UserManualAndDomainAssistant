"""The SKOS is-a scheme, derived from ``parent`` / ``also_parents`` (FR-3).

Concepts reuse the OWL class IRIs (OWL 2 punning). Extra trees from taxonomy.yaml are diagrams only.
"""

from __future__ import annotations

from rdflib import RDF, SKOS, Graph, Literal

from domain_model.model import Domain
from domain_model.rdf.vocab import annotate_status, annotate_terms, namespace, new_graph


def skos_graph(domain: Domain) -> Graph:
    onto = domain.ontology
    ns = namespace(onto)
    graph = new_graph(onto)
    scheme = ns["_isAScheme"]  # ids start with a letter, so this cannot clash with an item
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal(f"{onto.label} concepts (is-a)", lang=onto.language)))
    for c in onto.concepts:
        node = ns[c.id]
        graph.add((node, RDF.type, SKOS.Concept))
        graph.add((node, SKOS.inScheme, scheme))
        annotate_terms(graph, node, onto, c, label=SKOS.prefLabel)
        annotate_status(graph, node, onto, c)
        for parent in c.parents:
            graph.add((node, SKOS.broader, ns[parent]))
            graph.add((ns[parent], SKOS.narrower, node))
        if not c.parents:
            graph.add((node, SKOS.topConceptOf, scheme))
            graph.add((scheme, SKOS.hasTopConcept, node))
    return graph
