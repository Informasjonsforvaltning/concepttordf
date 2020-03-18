"""Concept module for mapping class associative relation to rdf."""
from __future__ import annotations

from typing import List, TYPE_CHECKING

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from .conceptrelation import ConceptRelation

if TYPE_CHECKING:  # pragma: no cover
    from .concept import Concept

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")
DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class AssociativeRelation(ConceptRelation):
    """A class representing a associative concept relation.

    Attributes:
        description: dictionary where key is language and value describing relation
        associatedconcepts: list of related concepts
    """

    _description: dict
    _associatedconcepts: List[Concept]

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._associatedconcepts = list()
        super().__init__()

    @property
    def description(self) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self, description: dict) -> None:
        """Description attribute.

        Args:
            description: a dictionary with key language code and value text.
        """
        self._description = description

    @property
    def associatedconcepts(self) -> List[Concept]:
        """Associatedconcepts attributes.

        Returns:
            a list of related concepts
        """
        return self._associatedconcepts

    # ---

    def _to_graph(self) -> Graph:

        self._add_relation_to_graph()

        return self._g

    # ---
    def _add_relation_to_graph(self) -> None:

        super(AssociativeRelation, self)._add_relation_to_graph()

        self._g.add((self._relation, RDF.type, SKOSNO.AssosiativRelasjon))

        # description
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        self._relation,
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

        # associatedconcepts
        if getattr(self, "associatedconcepts", None):
            # breakpoint()
            for ac in self.associatedconcepts:
                self._g.add((self._relation, SKOSNO.assosiertBegrep, URIRef(ac)))
