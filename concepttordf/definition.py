from .betydningsbeskrivelse import Betydningsbeskrivelse
from rdflib import Namespace

SKOSNO = Namespace('http://difi.no/skosno#')


class Definition(Betydningsbeskrivelse):

    def __init__(self, definition: dict = None):
        self.type = SKOSNO.Definisjon
        super().__init__(definition)
