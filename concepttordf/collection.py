from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from .contact import Contact

DCT = Namespace('http://purl.org/dc/terms/')
SKOSXL = Namespace('http://www.w3.org/2008/05/skos-xl#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SKOSNO = Namespace('http://difi.no/skosno')
DCAT = Namespace('http://www.w3.org/ns/dcat#')


class Collection:
    """" A class representing a concept collection"""

    def __init__(self):
        self._g = Graph()
        self._members = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def publisher(self) -> str:
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: str):
        self._publisher = publisher

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def contactpoint(self) -> Contact:
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self, contact: Contact):
        self._contactpoint = contact

    @property
    def members(self) -> list:
        return self._members

    @members.setter
    def members(self, members: list):
        self._members = members

    def to_rdf(self, format='text/turtle', includeconcepts=True) -> str:
        """Maps the collection to rdf and returns a serialization
           as a string according to format"""

        self._add_collection_to_graph()

        if includeconcepts:
            for concept in self.members:
                self._g += concept._to_graph()

        return self._g.serialize(format=format)

    # ---

    def _add_collection_to_graph(self) -> Graph:
        """Adds the collection to the Graph _g"""

        self._g.bind('dct', DCT)
        self._g.bind('skos', SKOS)
        self._g.bind('skosxl', SKOSXL)
        self._g.bind('vcard', VCARD)
        self._g.bind('skosno', SKOSNO)
        self._g.bind('dcat', DCAT)

        self._g.add((URIRef(self.identifier), RDF.type, SKOS.Collection))

        # publisher
        self._g.add((URIRef(self.identifier), DCT.publisher,
                    URIRef(self.publisher)))

        # name
        if hasattr(self, 'name'):
            for key in self.name:
                self._g.add((URIRef(self.identifier), RDFS.label,
                            Literal(self.name[key], lang=key)))

        # description
        if hasattr(self, 'description'):
            for key in self.description:
                self._g.add((URIRef(self.identifier), DCT.description,
                            Literal(self.description[key], lang=key)))

        # contactPoint
        if hasattr(self, 'contactpoint'):
            contact = self.contactpoint
            contactPoint = BNode()
            for s, p, o in contact._to_graph().triples((None, None, None)):
                self._g.add((contactPoint, p, o))
            self._g.add((URIRef(self.identifier), DCAT.contactPoint,
                        contactPoint))

        # members
        if hasattr(self, 'members'):
            for concept in self.members:
                self._g.add((URIRef(self.identifier), SKOS.member,
                             URIRef(concept.identifier)))
