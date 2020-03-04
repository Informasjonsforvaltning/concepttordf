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
    def contactpoint(self) -> dict:
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self, contact: dict):
        self._contactpoint = contact

    @property
    def members(self) -> list:
        return self._members

    @members.setter
    def members(self, members: list):
        self._members = members

    def to_rdf(self, format='turtle') -> str:
        """Maps the collection to rdf and returns a serialization
           as a string according to format"""

        _g = _add_collection_to_graph(self)

        return _g.serialize(format=format, encoding='utf-8')


def _add_collection_to_graph(collection: Collection) -> Graph:
    """Adds the collection to the Graph g and returns g"""

    g = Graph()

    g.bind('dct', DCT)
    g.bind('skos', SKOS)
    g.bind('skosxl', SKOSXL)
    g.bind('vcard', VCARD)
    g.bind('skosno', SKOSNO)
    g.bind('dcat', DCAT)

    g.add((URIRef(collection.identifier), RDF.type, SKOS.Collection))

    # publisher
    g.add((URIRef(collection.identifier), DCT.publisher,
           URIRef(collection.publisher)))

    # name
    if hasattr(collection, 'name'):
        for key in collection.name:
            g.add((URIRef(collection.identifier), RDFS.label,
                   Literal(collection.name[key], lang=key)))

    # description
    if hasattr(collection, 'description'):
        for key in collection.description:
            g.add((URIRef(collection.identifier), DCT.description,
                   Literal(collection.description[key], lang=key)))

    # contactPoint
    if hasattr(collection, 'contactpoint'):
        contact = Contact(collection.contactpoint)
        contactPoint = BNode()
        for s, p, o in contact.to_graph().triples((None, None, None)):
            g.add((contactPoint, p, o))
        g.add((URIRef(collection.identifier), DCAT.contactPoint,
               contactPoint))

    # members
    if hasattr(collection, 'members'):
        for concept in collection.members:
            g.add((URIRef(collection.identifier), SKOS.member,
                   URIRef(concept.identifier)))
    return g
