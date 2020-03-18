"""Concept module for mapping a concept to rdf.

This module contains methods for mapping a concept object to rdf
according to the
`skos-ap-no standard <https://doc.difi.no/data/begrep-skos-ap-no/#_begrep>`__

Example:
    >>> from concepttordf import Collection, Concept, Definition
    >>>
    >>> # Create collection object
    >>> collection = Collection()
    >>> collection.identifier = "http://example.com/collections/1"
    >>> collection.name = {"en": "A concept collection"}
    >>> collection.name = {"nb": "En begrepssamling"}
    >>> collection.publisher = "https://example.com/publishers/1"
    >>>
    >>> # Create a concept:
    >>> c = Concept()
    >>> c.identifier = "http://example.com/concepts/1"
    >>> c.term = {"name": {"nb": "inntekt", "en": "income"}}
    >>> definition = Definition()
    >>> definition.text = {"nb": "ting man skulle hatt mer av",
    >>>                    "en": "something you want more of"}
    >>> c.definition = definition
    >>>
    >>> # Add concept to collection:
    >>> collection.members.append(c)
    >>>
    >>> # get rdf representation in turtle (default)
    >>> bool(collection.to_rdf())
    True
"""
from typing import List

from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, URIRef

from .concept import Concept
from .contact import Contact

DCT = Namespace("http://purl.org/dc/terms/")
SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
SKOSNO = Namespace("http://difi.no/skosno")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Collection:
    """A class representing a concept collection."""

    _identifier: str
    _name: dict
    _publisher: str
    _description: dict
    _contactpoint: Contact
    _members: List[Concept]

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._g = Graph()
        self._members = []

    @property
    def identifier(self) -> str:
        """Identifier attribute.

        Returns:
            a string holding a valid uri
        """
        return self._identifier

    @identifier.setter
    def identifier(self, uri: str) -> None:
        self._identifier = uri

    @property
    def name(self) -> dict:
        """Name attribute."""
        return self._name

    @name.setter
    def name(self, name: dict) -> None:
        self._name = name

    @property
    def publisher(self) -> str:
        """Publisher attribute."""
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: str) -> None:
        self._publisher = publisher

    @property
    def description(self) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self, description: dict) -> None:
        self._description = description

    @property
    def contactpoint(self) -> Contact:
        """Contactpoint attribute."""
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self, contact: Contact) -> None:
        self._contactpoint = contact

    @property
    def members(self) -> List[Concept]:
        """Members attribute."""
        return self._members

    @members.setter
    def members(self, members: List[Concept]) -> None:
        self._members = members

    def to_rdf(self, format: str = "text/turtle", includeconcepts: bool = True) -> str:
        """Maps the collection to rdf.

        Args:
            format: the format of the serialization
            includeconcepts: if true details of concepts are included

        Returns:
            serialization as a string according to format
        """
        self._add_collection_to_graph()

        if includeconcepts:
            for concept in self.members:
                self._g += concept._to_graph()

        return self._g.serialize(format=format)

    # ---

    def _add_collection_to_graph(self) -> None:
        """Adds the collection to the Graph _g."""
        self._g.bind("dct", DCT)
        self._g.bind("skos", SKOS)
        self._g.bind("skosxl", SKOSXL)
        self._g.bind("vcard", VCARD)
        self._g.bind("skosno", SKOSNO)
        self._g.bind("dcat", DCAT)

        self._g.add((URIRef(self.identifier), RDF.type, SKOS.Collection))

        # publisher
        self._g.add((URIRef(self.identifier), DCT.publisher, URIRef(self.publisher)))

        # name
        if getattr(self, "name", None):
            for _key in self.name:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        RDFS.label,
                        Literal(self.name[_key], lang=_key),
                    )
                )

        # description
        if getattr(self, "description", None):
            for _key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[_key], lang=_key),
                    )
                )

        # contactPoint
        if getattr(self, "contactpoint", None):
            contact = self.contactpoint
            contactPoint = BNode()
            for _s, p, o in contact._to_graph().triples((None, None, None)):
                self._g.add((contactPoint, p, o))
            self._g.add((URIRef(self.identifier), DCAT.contactPoint, contactPoint))

        # members
        if getattr(self, "members", None):
            for concept in self.members:
                self._g.add(
                    (URIRef(self.identifier), SKOS.member, URIRef(concept.identifier))
                )
