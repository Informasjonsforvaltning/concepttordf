from .betydningsbeskrivelse import Betydningsbeskrivelse
from rdflib import Namespace

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')


class Definition(Betydningsbeskrivelse):

    def __init__(self):
        super().__init__()
        self.type = SKOSNO.Definisjon
