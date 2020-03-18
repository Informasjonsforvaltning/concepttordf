"""Module for helper class Definition."""
from rdflib import Namespace

from .betydningsbeskrivelse import Betydningsbeskrivelse

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")


class AlternativFormulering(Betydningsbeskrivelse):
    """A class representing a AlternativFormulering."""

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()
