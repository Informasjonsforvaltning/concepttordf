"""Test cases for the definition module."""
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from concepttordf import Concept, Definition


def test_quoteFromSource_to_rdf_should_return_skos_definition() -> None:
    """It returns a definition graph isomorphic to spec."""
    definition = Definition()
    definition.text = {
        "nb": """Denne inndelingen øker kvaliteten på saks- \
        og utgiftsbehandling og reduserer muligheten for misbruk."""
    }

    concept = Concept()
    concept.identifier = "http://example.com/concepts/1"
    concept.definition = definition

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format="text/turtle")
    # _dump_turtle(g1)
    # -
    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/concepts/1> a skos:Concept ;
            skosno:definisjon [ a skosno:Definisjon ;
            rdfs:label
        "Denne inndelingen øker kvaliteten på saks- \
        og utgiftsbehandling og reduserer muligheten for misbruk."@nb
            ] .
    """
    # -
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Util for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for l in g.serialize(format="text/turtle").splitlines():
        if l:
            print(l.decode())
