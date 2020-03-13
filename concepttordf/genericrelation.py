from .conceptrelation import ConceptRelation
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from typing import List

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')
DCT = Namespace('http://purl.org/dc/terms/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')


class GenericRelation(ConceptRelation):

    def __init__(self):
        self._genericconcepts = []
        super().__init__()

    @property
    def criterium(self) -> dict:
        return self._criterium

    @criterium.setter
    def criterium(self, criterium: dict):
        self._criterium = criterium

    @property
    def genericconcepts(self) -> List:
        return self._genericconcepts
# ---

    def to_graph(self) -> Graph:

        self._add_relation_to_graph()

        return self._g

# ---
    def _add_relation_to_graph(self):

        super(GenericRelation, self)._add_relation_to_graph()

        self._g.add((self._relation, RDF.type, SKOSNO.GeneriskRelasjon))

        # criterium
        if hasattr(self, 'criterium'):
            for key in self.criterium:
                self._g.add((self._relation, SKOSNO.inndelingskriterium,
                            Literal(self.criterium[key], lang=key)))

        # genericconcepts
        if hasattr(self, 'genericconcepts'):
            # breakpoint()
            for ac in self.genericconcepts:
                self._g.add((self._relation, SKOSNO.overordnetBegrep,
                            URIRef(ac)))
