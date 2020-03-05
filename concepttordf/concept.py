from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from .contact import Contact

DCT = Namespace('http://purl.org/dc/terms/')
SKOSXL = Namespace('http://www.w3.org/2008/05/skos-xl#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SKOSNO = Namespace('http://difi.no/skosno#')
DCAT = Namespace('http://www.w3.org/ns/dcat#')


class Concept:
    """A class representing a concept"""

    def __init__(self, concept: dict = None):
        if concept is not None:
            self._identifier = concept['identifier']
            self._term = concept['term']
            self._definition = concept['definition']
            self._contactpoint = concept['contactpoint']

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, uri: str):
        self._identifier = uri

    @property
    def term(self) -> dict:
        return self._term

    @term.setter
    def term(self, term: dict):
        self._term = term

    @property
    def alternativeterm(self) -> dict:
        return self._alternativeterm

    @alternativeterm.setter
    def alternativeterm(self, alternativeterm: dict):
        self._alternativeterm = alternativeterm

    @property
    def subject(self) -> dict:
        return self._subject

    @subject.setter
    def subject(self, subject: dict):
        self._subject = subject

    @property
    def definition(self) -> dict:
        return self._definition

    @definition.setter
    def definition(self, definition: dict):
        self._definition = definition

    @property
    def contactpoint(self) -> Contact:
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self, contact: Contact):
        self._contactpoint = contact

    def to_rdf(self, format='turtle') -> str:
        """Maps the concept to rdf and returns a serialization
           as a string according to format"""

        _g = _add_concept_to_graph(self)

        return _g.serialize(format=format, encoding='utf-8')


def _add_concept_to_graph(concept: Concept) -> Graph:
    """Adds the concept to the Graph g and returns g"""

    g = Graph()

    g.bind('dct', DCT)
    g.bind('skos', SKOS)
    g.bind('skosxl', SKOSXL)
    g.bind('vcard', VCARD)
    g.bind('skosno', SKOSNO)
    g.bind('dcat', DCAT)

    g.add((URIRef(concept.identifier), RDF.type, SKOS.Concept))

    # prefLabel
    label = BNode()
    g.add((label, RDF.type, SKOSXL.Label))
    for key in concept.term:
        g.add((label, SKOSXL.literalForm,
               Literal(concept.term[key], lang=key)))
    g.add((URIRef(concept.identifier), SKOSXL.prefLabel, label))

    # definition
    definition = BNode()
    g.add((definition, RDF.type, SKOSNO.Definisjon))
    for key in concept.definition:
        g.add((definition, RDFS.label,
               Literal(concept.definition[key], lang=key)))
    g.add((URIRef(concept.identifier), SKOSNO.betydningsbeskrivelse,
           definition))

    # publisher
    g.add((URIRef(concept.identifier), DCT.publisher,
           URIRef(concept.publisher)))

    # contactPoint
    if hasattr(concept, 'contactpoint'):
        contact = concept.contactpoint
        contactPoint = BNode()
        for s, p, o in contact.to_graph().triples((None, None, None)):
            g.add((contactPoint, p, o))
        g.add((URIRef(concept.identifier), DCAT.contactPoint,
               contactPoint))

    # altLabel
    if hasattr(concept, 'alternativeterm'):
        altLabel = BNode()
        g.add((altLabel, RDF.type, SKOSXL.Label))
        for key in concept.alternativeterm:
            for l in concept.alternativeterm[key]:
                g.add((altLabel, SKOSXL.literalForm,
                       Literal(l, lang=key)))
        g.add((URIRef(concept.identifier), SKOSXL.altLabel, altLabel))

    # subject
    if hasattr(concept, 'subject'):
        for key in concept.subject:
            g.add((URIRef(concept.identifier), DCT.subject,
                   Literal(concept.subject[key], lang=key)))

    return g
