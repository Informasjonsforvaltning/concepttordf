from abc import ABC
from rdflib import Graph, BNode, RDF, RDFS, URIRef, Namespace, Literal
from enum import Enum

SKOSNO = Namespace('http://difi.no/skosno#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
DCT = Namespace('http://purl.org/dc/terms/')


class RelationToSource(Enum):
    sitatFraKilde = "quoteFromSource"
    basertPåKilde = "basedOnSource"
    egendefinert = "noSource"


class Betydningsbeskrivelse(ABC):

    def __init__(self, b: dict = None):
        if b is not None:
            if 'identifier' in b:
                self._identifier = b['identifier']
            if 'text' in b:
                self._text = b['text']
            if 'remark' in b:
                self._remark = b['remark']
            if 'scope' in b:
                self._scope = b['scope']
            if 'relationtosource' in b:
                self._relationtosource = b['relationtosource']
            if 'source' in b:
                self._source = b['source']

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        self._identifier = identifier

    @property
    def text(self) -> dict:
        return self._text

    @text.setter
    def text(self, text: dict):
        self._text = text

    @property
    def remark(self) -> dict:
        return self._remark

    @remark.setter
    def remark(self, remark: dict):
        self._remark = remark

    @property
    def scope(self) -> dict:
        return self._scope

    @scope.setter
    def scope(self, scope: dict):
        self._scope = scope

    @property
    def relationtosource(self) -> str:
        return self._relationtosource

    @relationtosource.setter
    def relationtosource(self, relationtosource: str):
        self._relationtosource = relationtosource

    @property
    def source(self) -> dict:
        return self._source

    @source.setter
    def source(self, source: dict):
        self._source = source

# ----
    def to_graph(self) -> Graph:

        return self._add_betydningsbeskrivelse_to_graph()

    def to_rdf(self, format='turtle') -> str:
        """Maps the betydningsbeskrivelse to rdf and returns a serialization
           as a string according to format"""

        _g = self.to_graph()

        return _g.serialize(format=format, encoding='utf-8')

# -------------------------------

    def _add_betydningsbeskrivelse_to_graph(self) -> Graph:
        """Adds the concept to the Graph g and returns g"""

        g = Graph()

        g.bind('skosno', SKOSNO)
        g.bind('skos', SKOS)
        g.bind('dct', DCT)

        # identifier
        if hasattr(self, 'identifier'):
            _betydningsbeskrivelse = URIRef(self.identifier)
        else:
            _betydningsbeskrivelse = BNode()

        g.add((_betydningsbeskrivelse, RDF.type, self.type))

        # text
        if hasattr(self, 'text'):
            for key in self.text:
                g.add((_betydningsbeskrivelse, RDFS.label,
                       Literal(self.text[key], lang=key)))

        # remark
        if hasattr(self, 'remark'):
            for key in self.remark:
                g.add((_betydningsbeskrivelse, SKOS.scopeNote,
                       Literal(self.remark[key], lang=key)))
        # scope
        if hasattr(self, 'scope'):
            _scope = BNode()
            if 'url' in self.scope:
                g.add((_scope, RDFS.seeAlso, URIRef(self.scope['url'])))
            if 'text' in self.scope:
                _text = self.scope['text']
                for key in _text:
                    g.add((_scope, RDFS.label,
                           Literal(_text[key], lang=key)))
            g.add((_betydningsbeskrivelse, SKOSNO.omfang, _scope))

        # relationtosource
        if hasattr(self, 'relationtosource'):
            # -
            # sitatFraKilde = "quoteFromSource"
            # basertPåKilde = "basedOnSource"
            # egendefinert = "noSource"
            #
            # -
            if (RelationToSource(self.relationtosource)
               is RelationToSource.sitatFraKilde):
                g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                       SKOSNO.sitatFraKilde))
            elif (RelationToSource(self.relationtosource)
                  is RelationToSource.basertPåKilde):
                g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                       SKOSNO.basertPåKilde))
            else:
                g.add((_betydningsbeskrivelse, SKOSNO.forholdTilKilde,
                       SKOSNO.egendefinert))

        # source
        if hasattr(self, 'source'):
            _source = BNode()
            if 'url' in self.source:
                g.add((_source, RDFS.seeAlso, URIRef(self.source['url'])))
            if 'text' in self.source:
                _text = self.source['text']
                for key in _text:
                    g.add((_source, RDFS.label,
                           Literal(_text[key], lang=key)))
            g.add((_betydningsbeskrivelse, DCT.source, _source))

        return g
