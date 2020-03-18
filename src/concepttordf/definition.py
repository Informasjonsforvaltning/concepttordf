"""Module for helper class Definition."""
from rdflib import Namespace

from .betydningsbeskrivelse import Betydningsbeskrivelse

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")


class Definition(Betydningsbeskrivelse):
    """A class representing a definition."""

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()
