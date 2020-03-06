from .betydningsbeskrivelse import Betydningsbeskrivelse
from rdflib import Namespace

SKOSNO = Namespace('http://difi.no/skosno#')


class Definition(Betydningsbeskrivelse):

    def __init__(self):
        self.type = SKOSNO.Definisjon
