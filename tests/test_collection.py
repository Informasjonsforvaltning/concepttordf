from concepttordf.collection import Collection
from concepttordf.concept import Concept
import json
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff


def test_collection_to_rdf_should_return_skos_collection():
    with open('./tests/collection.json') as json_file:
        data = json.load(json_file)
        _collection = data['collection']
    collection = Collection()
    collection.identifier = _collection['identifier']
    collection.name = _collection['name']
    collection.description = _collection['description']
    collection.publisher = _collection['publisher']
    collection.contactpoint = _collection['contactpoint']
    collection.members = []
    for concept in _collection['members']:
        collection.members.append(Concept(concept))

    g1 = Graph()
    g1.parse(data=collection.to_rdf(), format='turtle')
    _dump_turtle(g1)
    g2 = Graph().parse("tests/collection.ttl",
                       format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Util for displaying debug information

def _dump_diff(g1, g2):
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle_sorted(g):
    for l in sorted(g.serialize(format='turtle').splitlines()):
        if l:
            print(l.decode())


def _dump_turtle(g):
    for l in g.serialize(format='turtle').splitlines():
        if l:
            print(l.decode())
