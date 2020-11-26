"""Test cases for the collection module."""
import json

from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from concepttordf import Collection, Concept, Contact, Definition


def test_collection_to_rdf_should_return_skos_collection() -> None:
    """It returns a collection graph isomorphic to spec."""
    with open("./tests/collection.json") as json_file:
        data = json.load(json_file)
        _collection = data["collection"]

    # Create the collection:
    collection = Collection()
    collection.identifier = _collection["identifier"]
    collection.name = _collection["name"]
    collection.description = _collection["description"]
    collection.publisher = _collection["publisher"]

    contact = Contact()
    contact.name = _collection["contactpoint"]["name"]
    contact.email = _collection["contactpoint"]["email"]
    contact.telephone = _collection["contactpoint"]["telephone"]
    contact.url = _collection["contactpoint"]["url"]
    collection.contactpoint = contact

    # Add members:
    collection.members = []
    for _concept in _collection["members"]:
        concept = Concept()
        concept.identifier = _concept["identifier"]
        concept.term = _concept["term"]
        concept.publisher = _concept["publisher"]
        definition = Definition()
        definition.text = _concept["definition"]["text"]
        concept.definition = definition
        collection.members.append(concept)

    # Get the collection as rdf:
    data = collection.to_rdf()

    # Test
    g1 = Graph()
    g1.parse(data=data, format="text/turtle")
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/collection.ttl", format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_collection_to_rdf_should_return_skos_collection_with_no_concepts() -> None:
    """It returns a collection graph without concepts isomorphic to spec."""
    with open("./tests/collection.json") as json_file:
        data = json.load(json_file)
        _collection = data["collection"]

    # Create the collection:
    collection = Collection()
    collection.identifier = _collection["identifier"]
    collection.name = _collection["name"]
    collection.description = _collection["description"]
    collection.publisher = _collection["publisher"]
    # Contact
    contact = Contact()
    contact.name = _collection["contactpoint"]["name"]
    contact.email = _collection["contactpoint"]["email"]
    contact.url = _collection["contactpoint"]["url"]
    contact.telephone = _collection["contactpoint"]["telephone"]
    collection.contactpoint = contact

    # Add members:
    collection.members = []
    for _concept in _collection["members"]:
        concept = Concept()
        concept.identifier = _concept["identifier"]
        collection.members.append(concept)

    # Get the collection as rdf:
    data = collection.to_rdf(includeconcepts=False)

    # Test
    g1 = Graph()
    g1.parse(data=data, format="text/turtle")
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/collection_excluding_concepts.ttl", format="text/turtle")

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
    for _l in g.serialize(format="text/turtle").splitlines():
        if _l:
            print(_l.decode())
