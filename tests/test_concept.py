from concepttordf.concept import Concept
from concepttordf.contact import Contact
from concepttordf.definition import Definition
from concepttordf.alternativformulering import AlternativFormulering
from concepttordf.associativerelation import AssociativeRelation
from concepttordf.genericrelation import GenericRelation
from concepttordf.partitiverelation import PartitiveRelation

import json
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff
import pytest


# @pytest.mark.skip(reason="no way of currently testing this")
def test_simple_concept_to_rdf_should_return_skos_concept():
    with open('./tests/concept.json') as json_file:
        data = json.load(json_file)
        _concept = data['concept']
    concept = Concept()
    concept.identifier = _concept['identifier']
    concept.term = _concept['term']
    concept.definition = Definition(_concept['definition'])
    concept.alternativformulering = AlternativFormulering(
                                    _concept['alternativformulering'])
    concept.publisher = _concept['publisher']
    concept.contactpoint = Contact(_concept['contactpoint'])

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/concept.ttl", format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# @pytest.mark.skip(reason="no way of currently testing this")
def test_concept_constructor_to_rdf_should_return_skos_concept():
    with open('./tests/completeconcept.json') as json_file:
        data = json.load(json_file)
        _concept = data['concept']
    concept = Concept(_concept)
    # --
    concept.related = AssociativeRelation(_concept['related'])
    for ac in _concept['related']['associatedconcepts']:
        concept.related.associatedconcepts.append(ac)
    # --
    concept.generalizes = GenericRelation(_concept['generalizes'])
    for gc in _concept['generalizes']['genericconcepts']:
        concept.generalizes.genericconcepts.append(gc)
    # --
    concept.hasPart = PartitiveRelation(_concept['hasPart'])
    for pc in _concept['hasPart']['partconcepts']:
        concept.hasPart.partconcepts.append(pc)
    # --
    # --
    for c in _concept['seeAlso']:
        seeAlsoConcept = Concept()
        seeAlsoConcept.identifier = c
        concept.seeAlso.append(seeAlsoConcept)
    # --
    for c in _concept['replaces']:
        replacesConcept = Concept()
        replacesConcept.identifier = c
        concept.replaces.append(replacesConcept)
    # --
    for c in _concept['replacedBy']:
        replacedByConcept = Concept()
        replacedByConcept.identifier = c
        concept.replacedBy.append(replacedByConcept)

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/completeconcept.ttl",
                       format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        # _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_concept_to_rdf_should_return_skos_concept():
    with open('./tests/completeconcept.json') as json_file:
        data = json.load(json_file)
        _concept = data['concept']
    concept = Concept()
    concept.identifier = _concept['identifier']
    concept.term = _concept['term']
    concept.alternativeterm = _concept['alternativeterm']
    concept.hiddenterm = _concept['hiddenterm']
    concept.definition = Definition(_concept['definition'])
    concept.alternativformulering = AlternativFormulering(
                                    _concept['alternativformulering'])
    concept.publisher = _concept['publisher']
    concept.contactpoint = Contact(_concept['contactpoint'])
    concept.subject = _concept['subject']
    concept.modified = _concept['modified']
    concept.example = _concept['example']
    concept.bruksområde = _concept['bruksområde']
    concept.validinperiod = _concept['validinperiod']
    concept.modified = _concept['modified']
    # --
    concept.related = AssociativeRelation(_concept['related'])
    for ac in _concept['related']['associatedconcepts']:
        concept.related.associatedconcepts.append(ac)
    # --
    concept.generalizes = GenericRelation(_concept['generalizes'])
    for gc in _concept['generalizes']['genericconcepts']:
        concept.generalizes.genericconcepts.append(gc)
    # --
    concept.hasPart = PartitiveRelation(_concept['hasPart'])
    for pc in _concept['hasPart']['partconcepts']:
        concept.hasPart.partconcepts.append(pc)
    # --
    for c in _concept['seeAlso']:
        seeAlsoConcept = Concept()
        seeAlsoConcept.identifier = c
        concept.seeAlso.append(seeAlsoConcept)
    # --
    for c in _concept['replaces']:
        replacesConcept = Concept()
        replacesConcept.identifier = c
        concept.replaces.append(replacesConcept)
    # --
    for c in _concept['replacedBy']:
        replacedByConcept = Concept()
        replacedByConcept.identifier = c
        concept.replacedBy.append(replacedByConcept)
    # --

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/completeconcept.ttl",
                       format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# @pytest.mark.skip(reason="no way of currently testing this")
def test_noSource_to_rdf_should_return_skos_definition():

    with open('./tests/definition.json') as json_file:
        data = json.load(json_file)
        _definition = data['definition']
    definition = Definition()
    definition.identifier = _definition['identifier']
    definition.relationtosource = 'noSource'

    concept = Concept()
    concept.identifier = 'http://example.com/concepts/1'
    concept.definition = definition

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    # -
    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/concepts/1> a skos:Concept ;
    skosno:betydningsbeskrivelse [ a skosno:Definisjon ;
            skosno:forholdTilKilde skosno:egendefinert ] .
    '''
    # -
    g2 = Graph().parse(data=src, format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# @pytest.mark.skip(reason="no way of currently testing this")
def test_quoteFromSource_to_rdf_should_return_skos_definition():

    with open('./tests/definition.json') as json_file:
        data = json.load(json_file)
        _definition = data['definition']
    definition = Definition()
    definition.identifier = _definition['identifier']
    definition.relationtosource = 'quoteFromSource'
    definition.source = _definition['source']

    concept = Concept()
    concept.identifier = 'http://example.com/concepts/1'
    concept.definition = definition

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format='turtle')
    # _dump_turtle(g1)
    # -
    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/concepts/1> a skos:Concept ;
            skosno:betydningsbeskrivelse [ a skosno:Definisjon ;
            skosno:forholdTilKilde skosno:sitatFraKilde ;
            dct:source [ rdfs:label "Thrustworthy source"@en,
                "Stolbar kilde"@nb,
                "Stolbar kilde"@nn ;
                rdfs:seeAlso <http://www.example.com/trustworthysources/1> ]
                ] .
    '''
    # -
    g2 = Graph().parse(data=src, format='turtle', encoding='utf-8')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic

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
