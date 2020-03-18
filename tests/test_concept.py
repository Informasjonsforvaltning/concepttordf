"""Test cases for the concept module."""
import json

import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from rdflib.plugin import PluginException

from concepttordf.concept import (
    AlternativFormulering,
    AssociativeRelation,
    Concept,
    Contact,
    Definition,
    GenericRelation,
    PartitiveRelation,
)


# @pytest.mark.skip(reason="no way of currently testing this")
def test_simple_concept_to_rdf_should_return_skos_concept() -> None:
    """It returns a a simple concept graph isomorphic to spec."""
    with open("./tests/concept.json") as json_file:
        data = json.load(json_file)
        _concept = data["concept"]
    concept = Concept()
    concept.identifier = _concept["identifier"]
    concept.term = _concept["term"]
    # Definition
    definition = Definition()
    definition.text = _concept["definition"]["text"]
    concept.definition = definition
    # AlternativFormulering
    alternativformulering = AlternativFormulering()
    alternativformulering.text = _concept["alternativformulering"]["text"]
    concept.alternativformulering = alternativformulering
    concept.publisher = _concept["publisher"]
    # Contactpoint
    contact = Contact()
    contact.name = _concept["contactpoint"]["name"]
    concept.contactpoint = contact

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format="text/turtle")
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/concept.ttl", format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_concept_to_rdf_should_return_skos_concept() -> None:
    """It returns a concept graph isomorphic to spec."""
    with open("./tests/completeconcept.json") as json_file:
        data = json.load(json_file)
        _concept = data["concept"]
    concept = Concept()
    concept.identifier = _concept["identifier"]
    concept.term = _concept["term"]
    concept.alternativeterm = _concept["alternativeterm"]
    concept.hiddenterm = _concept["hiddenterm"]
    concept.datastrukturterm = _concept["datastrukturterm"]
    # Definisjon
    definition = Definition()
    definition.text = _concept["definition"]["text"]
    definition.remark = _concept["definition"]["remark"]
    definition.scope = _concept["definition"]["scope"]
    definition.relationtosource = _concept["definition"]["relationtosource"]
    definition.source = _concept["definition"]["source"]
    definition.modified = _concept["definition"]["modified"]
    definition.example = _concept["definition"]["example"]

    concept.definition = definition
    # AlternativFormulering
    af = AlternativFormulering()
    af.text = _concept["alternativformulering"]["text"]
    af.remark = _concept["alternativformulering"]["remark"]
    af.scope = _concept["alternativformulering"]["scope"]
    af.relationtosource = _concept["alternativformulering"]["relationtosource"]
    af.source = _concept["alternativformulering"]["source"]
    af.modified = _concept["alternativformulering"]["modified"]

    concept.alternativformulering = af
    concept.publisher = _concept["publisher"]
    # Contact
    contact = Contact()
    contact.name = _concept["contactpoint"]["name"]
    contact.email = _concept["contactpoint"]["email"]
    contact.url = _concept["contactpoint"]["url"]
    contact.telephone = _concept["contactpoint"]["telephone"]
    concept.contactpoint = contact
    #
    concept.subject = _concept["subject"]
    concept.modified = _concept["modified"]
    concept.bruksomrade = _concept["bruksomrade"]
    concept.validinperiod = _concept["validinperiod"]
    concept.modified = _concept["modified"]
    # --
    related = AssociativeRelation()
    related.description = _concept["related"]["description"]
    related.modified = _concept["related"]["modified"]
    concept.related = related
    for ac in _concept["related"]["associatedconcepts"]:
        concept.related.associatedconcepts.append(ac)
    # --
    generic = GenericRelation()
    generic.criterium = _concept["generalizes"]["criterium"]
    generic.modified = _concept["generalizes"]["modified"]
    concept.generalizes = generic
    for gc in _concept["generalizes"]["genericconcepts"]:
        concept.generalizes.genericconcepts.append(gc)
    # --
    part = PartitiveRelation()
    part.criterium = _concept["hasPart"]["criterium"]
    part.modified = _concept["hasPart"]["modified"]
    concept.hasPart = part
    for pc in _concept["hasPart"]["partconcepts"]:
        concept.hasPart.partconcepts.append(pc)
    # --
    for c in _concept["seeAlso"]:
        seeAlsoConcept = Concept()
        seeAlsoConcept.identifier = c
        concept.seeAlso.append(seeAlsoConcept)
    # --
    for c in _concept["replaces"]:
        replacesConcept = Concept()
        replacesConcept.identifier = c
        concept.replaces.append(replacesConcept)
    # --
    for c in _concept["replacedBy"]:
        replacedByConcept = Concept()
        replacedByConcept.identifier = c
        concept.replacedBy.append(replacedByConcept)
    # --

    g1 = Graph()
    g1.parse(data=concept.to_rdf(), format="text/turtle")
    # _dump_turtle(g1)
    g2 = Graph().parse("tests/completeconcept.ttl", format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# @pytest.mark.skip(reason="no way of currently testing this")
def test_noSource_to_rdf_should_return_skos_definition() -> None:
    """It returns a definition graph isomorphic to spec."""
    definition = Definition()
    definition.relationtosource = "noSource"

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
            skosno:forholdTilKilde skosno:egendefinert ] .
    """
    # -
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# @pytest.mark.skip(reason="no way of currently testing this")
def test_quoteFromSource_to_rdf_should_return_skos_definition() -> None:
    """It returns a definition graph isomorphic to spec."""
    with open("./tests/definition.json") as json_file:
        data = json.load(json_file)
        _definition = data["definition"]
    definition = Definition()
    definition.relationtosource = "quoteFromSource"
    definition.source = _definition["source"]

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
            skosno:forholdTilKilde skosno:sitatFraKilde ;
            dct:source [ rdfs:label "Thrustworthy source"@en,
                "Stolbar kilde"@nb,
                "Stolbar kilde"@nn ;
                rdfs:seeAlso <http://www.example.com/trustworthysources/1> ]
                ] .
    """
    # -
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_serialization_formats_that_should_work() -> None:
    """It returns no exception."""
    concept = Concept()
    concept.identifier = "http://example.com/concepts/1"
    TURTLE = "text/turtle"
    XML = "application/rdf+xml"
    JSONLD = "application/ld+json"
    NT = "application/n-triples"
    N3 = "text/n3"

    _g = Graph()
    _g.parse(data=concept.to_rdf(format=TURTLE), format=TURTLE)
    _g.parse(data=concept.to_rdf(format=XML), format=XML)
    _g.parse(data=concept.to_rdf(format=JSONLD), format=JSONLD)
    _g.parse(data=concept.to_rdf(format=NT), format=NT)
    _g.parse(data=concept.to_rdf(format=N3), format=N3)


def test_serialization_format_that_should_fail() -> None:
    """It raises a PluginException."""
    concept = Concept()
    concept.identifier = "http://example.com/concepts/1"

    _g = Graph()
    with pytest.raises(PluginException):
        _g.parse(data=concept.to_rdf(format="should_fail"))


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


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
