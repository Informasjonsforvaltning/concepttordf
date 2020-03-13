"""Concept collection to rdf

This library maps a concept collection to skos according to
[SKOS-AP-NO](https://doc.difi.no/data/begrep-skos-ap-no/),
a Norwegian application profile for [SKOS](https://www.w3.org/TR/skos-primer/).

The library wraps [rdflib](https://rdflib.readthedocs.io/en/stable/).
The following serialization formats are available:\n
 - `text/turtle`
 - `application/rdf+xml`
 - `application/ld+json`
 - `application/n-triples`
 - `text/n3`

Typical usage example

    from concepttordf import Collection, Concept, Definition

    # Create collection object
    collection = Collection()
    collection.identifier = "http://example.com/collections/1"
    collection.name = {"en": "A concept collection"}
    collection.name = {"nb": "En begrepssamling"}
    collection.publisher = "https://example.com/publishers/1"

    # Create a concept:
    c = Concept()
    c.identifier = "http://example.com/concepts/1"
    c.term = {"name": {"nb": "inntekt", "en": "income"}}
    definition = Definition()
    definition.text = {"nb": "ting man skulle hatt mer av",
                       "en": "something you want more of"}
    c.definition = definition

    # Add concept to collection:
    collection.members.append(c)

    # get rdf representation in turtle (default)
    rdf = collection.to_rdf()
    print(rdf.decode())
"""
from .alternativformulering import AlternativFormulering
from .associativerelation import AssociativeRelation
from .betydningsbeskrivelse import Betydningsbeskrivelse
from .collection import Collection
from .concept import Concept
from .conceptrelation import ConceptRelation
from .contact import Contact
from .definition import Definition
from .genericrelation import GenericRelation
from .partitiverelation import PartitiveRelation
