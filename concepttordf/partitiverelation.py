from .conceptrelation import ConceptRelation
from rdflib import Graph, Literal, Namespace, RDF, URIRef

SKOSNO = Namespace('http://difi.no/skosno#')
DCT = Namespace('http://purl.org/dc/terms/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')


class PartitiveRelation(ConceptRelation):

    def __init__(self, ar: dict = None):
        self._partconcepts = []
        if ar is not None:
            if 'criterium' in ar:
                self.criterium = ar['criterium']
            if 'partconcepts' in ar:
                self.partconcepts = ar['partconcepts']
        super().__init__(ar)

    @property
    def criterium(self) -> dict:
        return self._criterium

    @criterium.setter
    def criterium(self, criterium: dict):
        self._criterium = criterium

    @property
    def partconcepts(self) -> list:
        return self._partconcepts

    @partconcepts.setter
    def partconcepts(self, acs: list):
        self._partconcepts

# ---

    def to_graph(self) -> Graph:

        self._add_relation_to_graph()

        return self._g

# ---
    def _add_relation_to_graph(self):

        super(PartitiveRelation, self)._add_relation_to_graph()

        self._g.add((self._relation, RDF.type, SKOSNO.PartitivRelasjon))

        # criterium
        if hasattr(self, 'criterium'):
            for key in self.criterium:
                self._g.add((self._relation, SKOSNO.inndelingskriterium,
                            Literal(self.criterium[key], lang=key)))

        # partconcepts
        if hasattr(self, 'partconcepts'):
            # breakpoint()
            for ac in self.partconcepts:
                self._g.add((self._relation, SKOSNO.underordnetBegrep,
                            URIRef(ac)))
