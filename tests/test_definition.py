from concepttordf.definition import Definition
import json
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff


def test_definition_to_rdf_should_return_skos_definition():

    with open('./tests/definition.json') as json_file:
        data = json.load(json_file)
        _definition = data['definition']
    definition = Definition()
    definition.identifier = _definition['identifier']
    definition.text = _definition['text']
    definition.remark = _definition['remark']
    definition.scope = _definition['scope']
    definition.relationtosource = _definition['relationtosource']
    definition.source = _definition['source']

    g1 = Graph()
    g1.parse(data=definition.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/definition.ttl",
                       format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_quoteFromSource_to_rdf_should_return_skos_definition():

    with open('./tests/definition.json') as json_file:
        data = json.load(json_file)
        _definition = data['definition']
    definition = Definition()
    definition.identifier = _definition['identifier']
    definition.relationtosource = 'quoteFromSource'
    definition.source = _definition['source']

    g1 = Graph()
    g1.parse(data=definition.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    # -
    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix skosno: <http://difi.no/skosno#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    <http://example.com/definitions/1> a skosno:Definisjon ;
    skosno:forholdTilKilde skosno:sitatFraKilde ;
    dct:source [ rdfs:label "Thrustworthy source"@en,
                "Stolbar kilde"@nb,
                "Stolbar kilde"@nn ;
            rdfs:seeAlso <http://www.example.com/trustworthysources/1> ] .
    '''
    # -
    g2 = Graph().parse(data=src, format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_noSource_to_rdf_should_return_skos_definition():

    with open('./tests/definition.json') as json_file:
        data = json.load(json_file)
        _definition = data['definition']
    definition = Definition()
    definition.identifier = _definition['identifier']
    definition.relationtosource = 'noSource'

    g1 = Graph()
    g1.parse(data=definition.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    # -
    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix skosno: <http://difi.no/skosno#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    <http://example.com/definitions/1> a skosno:Definisjon ;
    skosno:forholdTilKilde skosno:egendefinert .
    '''
    # -
    g2 = Graph().parse(data=src, format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_definition_without_identifier_to_rdf_should_return_skos_definition():

    with open('./tests/definition.json') as json_file:
        data = json.load(json_file)
        _definition = data['definition']
    definition = Definition()
    definition.text = _definition['text']
    definition.remark = _definition['remark']
    definition.scope = _definition['scope']
    definition.relationtosource = _definition['relationtosource']
    definition.source = _definition['source']

    g1 = Graph()
    g1.parse(data=definition.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/definition.ttl",
                       format='turtle', encoding='utf-8')

    assert len(g1) == len(g2)

# ---------------------------------------------------------------------- #
# Utils for displaying debug information


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
