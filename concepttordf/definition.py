from .betydningsbeskrivelse import Betydningsbeskrivelse
from rdflib import Namespace

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')


class Definition(Betydningsbeskrivelse):

    def __init__(self, definition: dict = None):
        self.type = SKOSNO.Definisjon
        super().__init__(definition)
