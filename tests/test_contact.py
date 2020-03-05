from concepttordf.contact import Contact
import json
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff


def test_contact_to_rdf_should_return_skos_contact():
    with open('./tests/contact.json') as json_file:
        data = json.load(json_file)
        _contact = data['contact']
    contact = Contact()
    contact.identifier = _contact['identifier']
    contact.name = _contact['name']
    contact.email = _contact['email']
    contact.url = _contact['url']
    contact.telephone = _contact['telephone']

    g1 = Graph()
    g1.parse(data=contact.to_rdf(), format='turtle')
    g2 = Graph().parse("tests/contact.ttl", format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_contact_without_id_to_rdf_should_return_skos_contact():
    with open('./tests/contact.json') as json_file:
        data = json.load(json_file)
        _contact = data['contact']
    contact = Contact()
    contact.name = _contact['name']
    contact.email = _contact['email']
    contact.url = _contact['url']
    contact.telephone = _contact['telephone']

    g1 = Graph()
    g1.parse(data=contact.to_rdf(), format='turtle')
    g2 = Graph().parse("tests/contact.ttl", format='turtle', encoding='utf-8')

    assert len(g1) == len(g2)


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
