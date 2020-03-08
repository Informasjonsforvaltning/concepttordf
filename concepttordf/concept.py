from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from datetime import date
from .contact import Contact
from .definition import Definition
from .betydningsbeskrivelse import RelationToSource

DCT = Namespace('http://purl.org/dc/terms/')
SKOSXL = Namespace('http://www.w3.org/2008/05/skos-xl#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SKOSNO = Namespace('http://difi.no/skosno#')
DCAT = Namespace('http://www.w3.org/ns/dcat#')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
SCHEMA = Namespace('http://schema.org/')


class Concept:
    """A class representing a concept"""

    def __init__(self, c: dict = None):
        self._g = Graph()
        if c is not None:
            if 'identifier' in c:
                self.identifier = c['identifier']
            if 'term' in c:
                self.term = c['term']
            if 'definition' in c:
                self.definition = Definition(c['definition'])
            if 'contactpoint' in c:
                self.contactpoint = Contact(c['contactpoint'])
            if 'alternativeterm' in c:
                self.alternativeterm = c['alternativeterm']
            if 'hiddenterm' in c:
                self.hiddenterm = c['hiddenterm']
            if 'subject' in c:
                self.subject = c['subject']
            if 'modified' in c:
                self.modified = c['modified']
            if 'example' in c:
                self.example = c['example']
            if 'bruksområde' in c:
                self.bruksområde = c['bruksområde']
            if 'validinperiod' in c:
                self.validinperiod = c['validinperiod']
            if 'publisher' in c:
                self.publisher = c['publisher']
        self.seeAlso = []
        self.replaces = []
        self.replacedBy = []

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
    def hiddenterm(self) -> dict:
        return self._hiddenterm

    @hiddenterm.setter
    def hiddenterm(self, hiddenterm: dict):
        self._hiddenterm = hiddenterm

    @property
    def subject(self) -> dict:
        return self._subject

    @subject.setter
    def subject(self, subject: dict):
        self._subject = subject

    @property
    def definition(self) -> Definition:
        return self._definition

    @definition.setter
    def definition(self, definition: Definition):
        self._definition = definition

    @property
    def contactpoint(self) -> Contact:
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self, contact: Contact):
        self._contactpoint = contact

    @property
    def modified(self) -> date:
        return self._modified

    @modified.setter
    def modified(self, modified: date):
        self._modified = modified

    @property
    def example(self) -> dict:
        return self._example

    @example.setter
    def example(self, example: dict):
        self._example = example

    @property
    def bruksområde(self) -> dict:
        return self._bruksområde

    @bruksområde.setter
    def bruksområde(self, bruksområde: dict):
        self._bruksområde = bruksområde

    @property
    def validinperiod(self) -> dict:
        return self._validinperiod

    @validinperiod.setter
    def validinperiod(self, validinperiod: dict):
        self._validinperiod = validinperiod

    @property
    def publisher(self) -> str:
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: str):
        self._publisher = publisher

    @property
    def seeAlso(self) -> list:
        return self._seeAlso

    @seeAlso.setter
    def seeAlso(self, concepts: list):
        self._seeAlso = concepts

    @property
    def replaces(self) -> list:
        return self._replaces

    @replaces.setter
    def replaces(self, concepts: list):
        self._replaces = concepts

    @property
    def replacedBy(self) -> list:
        return self._replacedBy

    @replacedBy.setter
    def replacedBy(self, concepts: list):
        self._replacedBy = concepts
# ----------------------------------------------

    def to_graph(self) -> Graph:
        """Adds the concept to the Graph g and returns g"""

        self._add_concept_to_graph()

        return self._g

    def to_rdf(self, format='turtle') -> str:
        """Maps the concept to rdf and returns a serialization
           as a string according to format"""

        return self.to_graph().serialize(format=format, encoding='utf-8')

# ----------------------------------------------

    def _add_concept_to_graph(self):
        """Adds the concept to the Graph _g"""

        self._g.bind('dct', DCT)
        self._g.bind('skos', SKOS)
        self._g.bind('skosxl', SKOSXL)
        self._g.bind('vcard', VCARD)
        self._g.bind('skosno', SKOSNO)
        self._g.bind('dcat', DCAT)
        self._g.bind('xsd', XSD)
        self._g.bind('schema', SCHEMA)

        self._g.add((URIRef(self.identifier), RDF.type, SKOS.Concept))

        # prefLabel
        if hasattr(self, 'term'):
            label = BNode()
            self._g.add((label, RDF.type, SKOSXL.Label))
            if 'name' in self.term:
                _name = self.term['name']
                for key in _name:
                    self._g.add((label, SKOSXL.literalForm,
                                 Literal(_name[key], lang=key)))
            if 'modified' in self.term:
                self._g.add((label, DCT.modified,
                            Literal(self.term['modified'], datatype=XSD.date)))
            self._g.add((URIRef(self.identifier), SKOSXL.prefLabel, label))

        # altLabel
        if hasattr(self, 'alternativeterm'):
            altLabel = BNode()
            self._g.add((altLabel, RDF.type, SKOSXL.Label))
            if 'name' in self.alternativeterm:
                _name = self.alternativeterm['name']
                for key in _name:
                    for l in _name[key]:
                        self._g.add((altLabel, SKOSXL.literalForm,
                                     Literal(l, lang=key)))
            if 'modified' in self.alternativeterm:
                self._g.add((altLabel, DCT.modified,
                             Literal(self.alternativeterm['modified'],
                                     datatype=XSD.date)))
            self._g.add((URIRef(self.identifier), SKOSXL.altLabel, altLabel))

        # hiddenLabel
        if hasattr(self, 'hiddenterm'):
            hiddenLabel = BNode()
            self._g.add((hiddenLabel, RDF.type, SKOSXL.Label))
            if 'name' in self.hiddenterm:
                _name = self.hiddenterm['name']
                for key in _name:
                    for l in _name[key]:
                        self._g.add((hiddenLabel, SKOSXL.literalForm,
                                     Literal(l, lang=key)))
            if 'modified' in self.hiddenterm:
                self._g.add((hiddenLabel, DCT.modified,
                             Literal(self.hiddenterm['modified'],
                                     datatype=XSD.date)))
            self._g.add((URIRef(self.identifier),
                         SKOSXL.hiddenLabel, hiddenLabel))

        # definition
        self._add_definition_to_concept()

        # publisher
        if hasattr(self, 'publisher'):
            self._g.add((URIRef(self.identifier), DCT.publisher,
                         URIRef(self.publisher)))

        # contactPoint
        if hasattr(self, 'contactpoint'):
            contact = self.contactpoint
            contactPoint = BNode()
            for s, p, o in contact.to_graph().triples((None, None, None)):
                self._g.add((contactPoint, p, o))
            self._g.add((URIRef(self.identifier), DCAT.contactPoint,
                         contactPoint))

        # subject
        if hasattr(self, 'subject'):
            for key in self.subject:
                self._g.add((URIRef(self.identifier), DCT.subject,
                             Literal(self.subject[key], lang=key)))

        # modified
        if hasattr(self, 'modified'):
            self._g.add((URIRef(self.identifier), DCT.modified,
                         Literal(self.modified, datatype=XSD.date)))

        # example
        if hasattr(self, 'example'):
            for key in self.example:
                self._g.add((URIRef(self.identifier), SKOS.example,
                             Literal(self.example[key], lang=key)))

        # bruksområde
        if hasattr(self, 'bruksområde'):
            for key in self.bruksområde:
                for b in self.bruksområde[key]:
                    self._g.add((URIRef(self.identifier), SKOSNO.bruksområde,
                                 Literal(b, lang=key)))

        # PeriodOfTime
        if hasattr(self, 'validinperiod'):
            periodOfTime = BNode()
            self._g.add((periodOfTime, RDF.type, DCT.PeriodOfTime))
            if 'startdate' in self.validinperiod:
                self._g.add((periodOfTime, SCHEMA.startDate,
                            Literal(self.validinperiod['startdate'],
                                    datatype=XSD.date)))
            if 'enddate' in self.validinperiod:
                self._g.add((periodOfTime, SCHEMA.endDate,
                            Literal(self.validinperiod['enddate'],
                                    datatype=XSD.date)))
            self._g.add((URIRef(self.identifier), DCT.temporal, periodOfTime))

        # seeAlso
        if hasattr(self, 'seeAlso'):
            for c in self.seeAlso:
                self._g.add((URIRef(self.identifier), RDFS.seeAlso,
                            URIRef(c.identifier)))

        # replaces
        if hasattr(self, 'replaces'):
            for c in self.replaces:
                self._g.add((URIRef(self.identifier), DCT.replaces,
                             URIRef(c.identifier)))

        # replacedBy
        if hasattr(self, 'replacedBy'):
            for c in self.replacedBy:
                self._g.add((URIRef(self.identifier), DCT.replacedBy,
                             URIRef(c.identifier)))

# ------------
# Helper methods:

    def _add_definition_to_concept(self):
        # ---
        _betydningsbeskrivelse = BNode()

        self._g.add((_betydningsbeskrivelse, RDF.type, self.definition.type))

        # text
        if hasattr(self.definition, 'text'):
            for key in self.definition.text:
                self._g.add((_betydningsbeskrivelse, RDFS.label,
                            Literal(self.definition.text[key], lang=key)))

        # remark
        if hasattr(self.definition, 'remark'):
            for key in self.definition.remark:
                self._g.add((_betydningsbeskrivelse, SKOS.scopeNote,
                            Literal(self.definition.remark[key], lang=key)))
        # scope
        if hasattr(self.definition, 'scope'):
            _scope = BNode()
            if 'url' in self.definition.scope:
                self._g.add((_scope, RDFS.seeAlso,
                            URIRef(self.definition.scope['url'])))
            if 'text' in self.definition.scope:
                _text = self.definition.scope['text']
                for key in _text:
                    self._g.add((_scope, RDFS.label,
                                Literal(_text[key], lang=key)))
            self._g.add((_betydningsbeskrivelse, SKOSNO.omfang, _scope))

        # relationtosource
        if hasattr(self.definition, 'relationtosource'):
            # -
            # sitatFraKilde = "quoteFromSource"
            # basertPåKilde = "basedOnSource"
            # egendefinert = "noSource"
            #
            # -
            if (RelationToSource(self.definition.relationtosource)
               is RelationToSource.sitatFraKilde):
                self._g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                            SKOSNO.sitatFraKilde))
            elif (RelationToSource(self.definition.relationtosource)
                  is RelationToSource.basertPåKilde):
                self._g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                            SKOSNO.basertPåKilde))
            else:
                self._g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                            SKOSNO.egendefinert))

        # source
        if hasattr(self.definition, 'source'):
            _source = BNode()
            if 'url' in self.definition.source:
                self._g.add((_source, RDFS.seeAlso,
                            URIRef(self.definition.source['url'])))
            if 'text' in self.definition.source:
                _text = self.definition.source['text']
                for key in _text:
                    self._g.add((_source, RDFS.label,
                                Literal(_text[key], lang=key)))
            self._g.add((_betydningsbeskrivelse, DCT.source, _source))

        # modified
        if hasattr(self.definition, 'modified'):
            self._g.add((_betydningsbeskrivelse, DCT.modified,
                         Literal(self.definition.modified, datatype=XSD.date)))

        self._g.add((URIRef(self.identifier), SKOSNO.betydningsbeskrivelse,
                    _betydningsbeskrivelse))
        # ---
