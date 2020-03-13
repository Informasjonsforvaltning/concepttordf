from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from datetime import date
from .contact import Contact
from .definition import Definition
from .alternativformulering import AlternativFormulering
from .betydningsbeskrivelse import RelationToSource
from .associativerelation import AssociativeRelation
from .genericrelation import GenericRelation
from .partitiverelation import PartitiveRelation


DCT = Namespace('http://purl.org/dc/terms/')
SKOSXL = Namespace('http://www.w3.org/2008/05/skos-xl#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')
DCAT = Namespace('http://www.w3.org/ns/dcat#')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
SCHEMA = Namespace('http://schema.org/')
XKOS = Namespace('http://rdf-vocabulary.ddialliance.org/xkos#')


class Concept:
    """A class representing a concept"""

    def __init__(self):
        self._g = Graph()

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
    def datastrukturterm(self) -> dict:
        return self._datastrukturterm

    @datastrukturterm.setter
    def datastrukturterm(self, datastrukturterm: dict):
        self._datastrukturterm = datastrukturterm

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
    def alternativformulering(self) -> AlternativFormulering:
        return self._alternativformulering

    @alternativformulering.setter
    def alternativformulering(self,
                              alternativformulering: AlternativFormulering):
        self._alternativformulering = alternativformulering

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

    @property
    def related(self) -> AssociativeRelation:
        return self._related

    @related.setter
    def related(self, ar: AssociativeRelation):
        self._related = ar

    @property
    def generalizes(self) -> GenericRelation:
        return self._generalizes

    @generalizes.setter
    def generalizes(self, gr: GenericRelation):
        self._generalizes = gr

    @property
    def hasPart(self) -> PartitiveRelation:
        return self._hasPart

    @hasPart.setter
    def hasPart(self, gr: PartitiveRelation):
        self._hasPart = gr
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
        self._g.bind('xkos', XKOS)

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

        # datastrukturterm
        if hasattr(self, 'datastrukturterm'):
            datastrukturterm = BNode()
            self._g.add((datastrukturterm, RDF.type, SKOSXL.Label))
            if 'name' in self.datastrukturterm:
                _name = self.datastrukturterm['name']
                for key in _name:
                    for l in _name[key]:
                        self._g.add((datastrukturterm, SKOSXL.literalForm,
                                     Literal(l, lang=key)))
            if 'modified' in self.datastrukturterm:
                self._g.add((datastrukturterm, DCT.modified,
                             Literal(self.datastrukturterm['modified'],
                                     datatype=XSD.date)))
            self._g.add((URIRef(self.identifier),
                         SKOSNO.datastrukturterm, datastrukturterm))
        # definition
        if hasattr(self, 'definition'):
            self._add_betydningsbeskrivelse_to_concept(self.definition)

        # alternativformulering
        if hasattr(self, 'alternativformulering'):
            self._add_betydningsbeskrivelse_to_concept(
                self.alternativformulering)

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

        # related
        if hasattr(self, 'related'):
            _related = self.related
            ar = BNode()
            for s, p, o in _related.to_graph().triples((None, None, None)):
                self._g.add((ar, p, o))
            self._g.add((URIRef(self.identifier), SKOS.related, ar))

        # generalizes
        if hasattr(self, 'generalizes'):
            _generalizes = self.generalizes
            ar = BNode()
            for s, p, o in _generalizes.to_graph().triples((None, None, None)):
                self._g.add((ar, p, o))
            self._g.add((URIRef(self.identifier), XKOS.generalizes, ar))

        # hasPart
        if hasattr(self, 'hasPart'):
            _hasPart = self.hasPart
            ar = BNode()
            for s, p, o in _hasPart.to_graph().triples((None, None, None)):
                self._g.add((ar, p, o))
            self._g.add((URIRef(self.identifier), XKOS.hasPart, ar))

# ------------
# Helper methods:

    def _add_betydningsbeskrivelse_to_concept(self, betydningsbeskrivelse):
        # ---
        _betydningsbeskrivelse = BNode()

        self._g.add((_betydningsbeskrivelse, RDF.type,
                     betydningsbeskrivelse.type))

        # text
        if hasattr(betydningsbeskrivelse, 'text'):
            for key in betydningsbeskrivelse.text:
                self._g.add((_betydningsbeskrivelse, RDFS.label,
                            Literal(betydningsbeskrivelse.text[key],
                                    lang=key)))

        # remark
        if hasattr(betydningsbeskrivelse, 'remark'):
            for key in betydningsbeskrivelse.remark:
                self._g.add((_betydningsbeskrivelse, SKOS.scopeNote,
                            Literal(betydningsbeskrivelse.remark[key],
                                    lang=key)))
        # scope
        if hasattr(betydningsbeskrivelse, 'scope'):
            _scope = BNode()
            if 'url' in betydningsbeskrivelse.scope:
                self._g.add((_scope, RDFS.seeAlso,
                            URIRef(betydningsbeskrivelse.scope['url'])))
            if 'text' in betydningsbeskrivelse.scope:
                _text = betydningsbeskrivelse.scope['text']
                for key in _text:
                    self._g.add((_scope, RDFS.label,
                                Literal(_text[key], lang=key)))
            self._g.add((_betydningsbeskrivelse, SKOSNO.omfang, _scope))

        # relationtosource
        if hasattr(betydningsbeskrivelse, 'relationtosource'):
            # -
            # sitatFraKilde = "quoteFromSource"
            # basertPåKilde = "basedOnSource"
            # egendefinert = "noSource"
            # -
            if (RelationToSource(betydningsbeskrivelse.relationtosource)
               is RelationToSource.sitatFraKilde):
                self._g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                            SKOSNO.sitatFraKilde))
            elif (RelationToSource(betydningsbeskrivelse.relationtosource)
                  is RelationToSource.basertPåKilde):
                self._g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                            SKOSNO.basertPåKilde))
            else:
                self._g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                            SKOSNO.egendefinert))

        # source
        if hasattr(betydningsbeskrivelse, 'source'):
            _source = BNode()
            if 'url' in betydningsbeskrivelse.source:
                self._g.add((_source, RDFS.seeAlso,
                            URIRef(betydningsbeskrivelse.source['url'])))
            if 'text' in betydningsbeskrivelse.source:
                _text = betydningsbeskrivelse.source['text']
                for key in _text:
                    self._g.add((_source, RDFS.label,
                                Literal(_text[key], lang=key)))
            self._g.add((_betydningsbeskrivelse, DCT.source, _source))

        # modified
        if hasattr(betydningsbeskrivelse, 'modified'):
            self._g.add((_betydningsbeskrivelse, DCT.modified,
                         Literal(betydningsbeskrivelse.modified,
                                 datatype=XSD.date)))

        # example
        if hasattr(betydningsbeskrivelse, 'example'):
            for key in betydningsbeskrivelse.example:
                self._g.add((_betydningsbeskrivelse, SKOS.example,
                             Literal(betydningsbeskrivelse.example[key],
                                     lang=key)))

        # Check type, and set correct property
        if isinstance(betydningsbeskrivelse, Definition):
            self._g.add((URIRef(self.identifier), SKOSNO.definisjon,
                        _betydningsbeskrivelse))
        else:
            self._g.add((URIRef(self.identifier), SKOSNO.alternativFormulering,
                        _betydningsbeskrivelse))
        # ---
