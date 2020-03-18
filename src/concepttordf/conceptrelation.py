"""Concept module for mapping abstract class ConceptRelation to rdf."""
from abc import ABC
from datetime import date

from rdflib import BNode, Graph, Literal, Namespace

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")
DCT = Namespace("http://purl.org/dc/terms/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class ConceptRelation(ABC):
    """An abstract class representing a concept relation.

    Attributes:
        modified: date when relation was last modified
    """

    _modified: date

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._g = Graph()
        self._relation = BNode()
        self._g.bind("skosno", SKOSNO)
        self._g.bind("dct", DCT)
        self._g.bind("xsd", XSD)

    @property
    def modified(self) -> date:
        """Modified attribute."""
        return self._modified

    @modified.setter
    def modified(self, modified: date) -> None:
        """Modified attribute.

        Args:
            modified: e.g. "yyyy-mm-dd"
        """
        self._modified = modified

    # ---
    def _add_relation_to_graph(self) -> None:

        # modified
        if getattr(self, "modified", None):
            self._g.add(
                (
                    self._relation,
                    DCT.modified,
                    Literal(self.modified, datatype=XSD.date),
                )
            )
