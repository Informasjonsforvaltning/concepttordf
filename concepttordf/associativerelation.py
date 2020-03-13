from .conceptrelation import ConceptRelation
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from typing import List

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')
DCT = Namespace('http://purl.org/dc/terms/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')


class AssociativeRelation(ConceptRelation):

    def __init__(self):
        self._associatedconcepts = list()
        super().__init__()

    @property
    def description(self) -> dict:
        return self._description

    @description.setter
    def description(self, description: dict):
        self._description = description

    @property
    def associatedconcepts(self) -> List:
        return self._associatedconcepts

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
