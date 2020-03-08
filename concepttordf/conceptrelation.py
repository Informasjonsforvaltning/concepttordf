from abc import ABC
from datetime import date


class ConceptRelation(ABC):

    def __init__(self, cr: dict = None):
        if cr is not None:
            if 'modified' in cr:
                self.modified = cr['modified']

    @property
    def modified(self) -> date:
        return self._modified

    @modified.setter
    def modified(self, modified: date):
        self._modified = modified
