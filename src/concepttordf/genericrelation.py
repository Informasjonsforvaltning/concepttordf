"""Concept module for mapping class GenericRelation to rdf."""
from __future__ import annotations

from typing import List, TYPE_CHECKING

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from .conceptrelation import ConceptRelation

if TYPE_CHECKING:  # pragma: no cover
    from .concept import Concept

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")
DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class GenericRelation(ConceptRelation):
    """A class representing a generic concept relation.

    Attributes:
        criterium: dictionary where key is language an value describing relation
        genericconcepts: list of related concepts
    """

    _criterium: dict
    _genericconcepts: List[Concept]

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._genericconcepts = list()
        super().__init__()

    @property
    def criterium(self) -> dict:
        """Criterium attribute."""
        return self._criterium

    @criterium.setter
    def criterium(self, criterium: dict) -> None:
        """Criterium attribute.

        Args:
            criterium: a dictionary with key language code and value text.
        """
        self._criterium = criterium

    @property
    def genericconcepts(self) -> List[Concept]:
        """Generic concepts attributes.

        Returns:
            a list of related concepts
        """
        return self._genericconcepts

    # ---

    def _to_graph(self) -> Graph:

        self._add_relation_to_graph()

        return self._g

    # ---
    def _add_relation_to_graph(self) -> None:

        super(GenericRelation, self)._add_relation_to_graph()

        self._g.add((self._relation, RDF.type, SKOSNO.GeneriskRelasjon))

        # criterium
        if getattr(self, "criterium", None):
            for key in self.criterium:
                self._g.add(
                    (
                        self._relation,
                        SKOSNO.inndelingskriterium,
                        Literal(self.criterium[key], lang=key),
                    )
                )

        # genericconcepts
        if getattr(self, "genericconcepts", None):
            # breakpoint()
            for ac in self.genericconcepts:
                self._g.add((self._relation, SKOSNO.overordnetBegrep, URIRef(ac)))
