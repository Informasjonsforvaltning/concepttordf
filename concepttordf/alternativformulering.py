from .betydningsbeskrivelse import Betydningsbeskrivelse
from rdflib import Namespace

SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')


class AlternativFormulering(Betydningsbeskrivelse):

    def __init__(self):
        self.type = SKOSNO.AlternativFormulering
        super().__init__()
