from .conceptrelation import ConceptRelation
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from typing import List

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')
DCT = Namespace('http://purl.org/dc/terms/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')


class PartitiveRelation(ConceptRelation):

    def __init__(self):
        self._partconcepts = []
        super().__init__()

    @property
    def criterium(self) -> dict:
        return self._criterium

    @criterium.setter
    def criterium(self, criterium: dict):
        self._criterium = criterium

    @property
    def partconcepts(self) -> List:
        return self._partconcepts
# ---

    def _to_graph(self) -> Graph:

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
