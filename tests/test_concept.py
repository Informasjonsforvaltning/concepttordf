from concepttordf.concept import Concept
import json
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff


def test_concept_to_rdf_should_return_skos_concept():
    with open('./tests/concept.json') as json_file:
        data = json.load(json_file)
        _concept = data['concept']
    concept = Concept()
    concept.identifier = _concept['identifier']
    concept.term = _concept['term']
    concept.definition = _concept['definition']
    concept.publisher = _concept['publisher']

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format='turtle')
    g2 = Graph().parse("tests/concept.ttl", format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Util for displaying debug information

def _dump_diff(g1, g2):
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle_sorted(in_both)
    print("\nin first:")
    _dump_turtle_sorted(in_first)
    print("\nin second:")
    _dump_turtle_sorted(in_second)


def _dump_turtle_sorted(g):
    for l in sorted(g.serialize(format='turtle').splitlines()):
        if l:
            print(l.decode())


def _dump_turtle(g):
    for l in g.serialize(format='turtle').splitlines():
        if l:
            print(l.decode())
