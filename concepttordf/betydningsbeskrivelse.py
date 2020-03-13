from abc import ABC
from enum import Enum


class RelationToSource(Enum):
    sitatFraKilde = "quoteFromSource"
    basertPåKilde = "basedOnSource"
    egendefinert = "noSource"


class Betydningsbeskrivelse(ABC):

    def __init__(self):
        pass

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def text(self) -> dict:
        return self._text

    @text.setter
    def text(self, text: dict):
        self._text = text

    @property
    def remark(self) -> dict:
        return self._remark

    @remark.setter
    def remark(self, remark: dict):
        self._remark = remark

    @property
    def scope(self) -> dict:
        return self._scope

    @scope.setter
    def scope(self, scope: dict):
        self._scope = scope

    @property
    def relationtosource(self) -> str:
        return self._relationtosource

    @relationtosource.setter
    def relationtosource(self, relationtosource: str):
        self._relationtosource = relationtosource

    @property
    def source(self) -> dict:
        return self._source

    @source.setter
    def source(self, source: dict):
        self._source = source

    @property
    def modified(self) -> dict:
        return self._modified

    @modified.setter
    def modified(self, modified: dict):
        self._modified = modified

    @property
    def example(self) -> dict:
        return self._example

    @example.setter
    def example(self, example: dict):
        self._example = example
