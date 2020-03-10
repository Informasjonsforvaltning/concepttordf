from .conceptrelation import ConceptRelation
from rdflib import Graph, Literal, Namespace, RDF, URIRef

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')
DCT = Namespace('http://purl.org/dc/terms/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')


class AssociativeRelation(ConceptRelation):

    def __init__(self, ar: dict = None):
        self._associatedconcepts = []
        if ar is not None:
            if 'description' in ar:
                self.description = ar['description']
            if 'description' in ar:
                self.description = ar['description']
            if 'associatedconcepts' in ar:
                self.associatedconcepts = ar['associatedconcepts']
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

# ---

    def to_graph(self) -> Graph:

        self._add_relation_to_graph()

        return self._g

# ---
    def _add_relation_to_graph(self):

        super(AssociativeRelation, self)._add_relation_to_graph()

        self._g.add((self._relation, RDF.type, SKOSNO.AssosiativRelasjon))

        # description
        if hasattr(self, 'description'):
            for key in self.description:
                self._g.add((self._relation, DCT.description,
                            Literal(self.description[key], lang=key)))

        # associatedconcepts
        if hasattr(self, 'associatedconcepts'):
            # breakpoint()
            for ac in self.associatedconcepts:
                self._g.add((self._relation, SKOSNO.assosiertBegrep,
                            URIRef(ac)))
