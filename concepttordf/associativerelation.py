from .conceptrelation import ConceptRelation
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

SKOSNO = Namespace('http://difi.no/skosno#')
DCT = Namespace('http://purl.org/dc/terms/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')


class AssociativeRelation(ConceptRelation):

    def __init__(self, ar: dict = None):
        self._g = Graph()
        self._associatedconcepts = []
        if ar is not None:
            if 'description' in ar:
                self.description = ar['description']
            if 'description' in ar:
                self.description = ar['description']
            if 'assoicatedconcepts' in ar:
                self.associatedconcepts = ar['assoicatedconcepts']
        super().__init__(ar)

    @property
    def description(self) -> dict:
        return self._description

    @description.setter
    def description(self, description: dict):
        self._description = description

    @property
    def associatedconcepts(self) -> list:
        return self._associatedconcepts

    @associatedconcepts.setter
    def associatedconcepts(self, acs: list):
        self._associatedconcepts

    def to_graph(self) -> Graph:

        self._add_relation_to_graph()

        return self._g

# ---
    def _add_relation_to_graph(self):

        self._g.bind('skosno', SKOSNO)
        self._g.bind('dct', DCT)
        self._g.bind('xsd', XSD)

        _relation = BNode()

        self._g.add((_relation, RDF.type, SKOSNO.AssosiativRelasjon))

        # description
        if hasattr(self, 'description'):
            for key in self.description:
                self._g.add((_relation, DCT.description,
                            Literal(self.description[key], lang=key)))

        # modified
        if hasattr(self, 'modified'):
            self._g.add((_relation, DCT.modified,
                         Literal(self.modified, datatype=XSD.date)))

        # modified
        if hasattr(self, 'associatedconcepts'):
            # breakpoint()
            for ac in self.associatedconcepts:
                self._g.add((_relation, SKOSNO.assosiertBegrep,
                            URIRef(ac)))
