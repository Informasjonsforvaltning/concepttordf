"""Concept module for mapping a concept to rdf.

This module contains methods for mapping a concept object to rdf
according to the
`skos-ap-no standard <https://doc.difi.no/data/begrep-skos-ap-no/#_begrep>`__

Example:
    >>> from concepttordf import Concept, Definition
    >>>
    >>> concept = Concept()
    >>> concept.identifier = "http://example.com/concepts/1"
    >>> concept.term = {"name": {"en": "concept"}}
    >>>
    >>> definition = Definition()
    >>> definition.text = {"text": {"en": "abstract or generic idea"}}
    >>> concept.definition = definition
    >>>
    >>> bool(concept.to_rdf())
    True
"""
from __future__ import annotations

from datetime import date
from typing import List

from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, URIRef

from .alternativformulering import AlternativFormulering
from .associativerelation import AssociativeRelation
from .betydningsbeskrivelse import Betydningsbeskrivelse, RelationToSource
from .contact import Contact
from .definition import Definition
from .genericrelation import GenericRelation
from .partitiverelation import PartitiveRelation


DCT = Namespace("http://purl.org/dc/terms/")
SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SCHEMA = Namespace("http://schema.org/")
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")


class Concept:
    """A class representing a concept.

    Attributes:
        identifier: the uri identifying the concept
        term: a dictionary describing the prefLabel
        alternativeterm: a dictionary describing altLabel
        hiddenterm: a dictionary describing the hiddenLabel
    """

    _identifier: str
    _term: dict
    _alternativeterm: dict
    _hiddenterm: dict
    _datastrukturterm: dict
    _subject: dict
    _definition: Definition
    _alternativformulering: AlternativFormulering
    _contactpoint: Contact
    _modified: date
    _bruksomrade: dict
    _validinperiod: dict
    _publisher: str
    _seeAlso: List[Concept]
    _replaces: List[Concept]
    _replacedBy: List[Concept]
    _related: AssociativeRelation
    _generalizes: GenericRelation
    _hasPart: PartitiveRelation

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._g = Graph()

        self.seeAlso = []
        self.replaces = []
        self.replacedBy = []

    @property
    def identifier(self: Concept) -> str:
        """Identifier attribute.

        Returns:
            a string holding a valid uri
        """
        return self._identifier

    @identifier.setter
    def identifier(self, uri: str) -> None:
        self._identifier = uri

    @property
    def term(self: Concept) -> dict:
        """Term attribute."""
        return self._term

    @term.setter
    def term(self: Concept, term: dict) -> None:
        self._term = term

    @property
    def alternativeterm(self: Concept) -> dict:
        """Alternativeterm attribute."""
        return self._alternativeterm

    @alternativeterm.setter
    def alternativeterm(self: Concept, alternativeterm: dict) -> None:
        self._alternativeterm = alternativeterm

    @property
    def hiddenterm(self: Concept) -> dict:
        """Hiddenterm attribute."""
        return self._hiddenterm

    @hiddenterm.setter
    def hiddenterm(self: Concept, hiddenterm: dict) -> None:
        self._hiddenterm = hiddenterm

    @property
    def datastrukturterm(self: Concept) -> dict:
        """Datastrukturterm attribute."""
        return self._datastrukturterm

    @datastrukturterm.setter
    def datastrukturterm(self: Concept, datastrukturterm: dict) -> None:
        self._datastrukturterm = datastrukturterm

    @property
    def subject(self: Concept) -> dict:
        """Subject attribute."""
        return self._subject

    @subject.setter
    def subject(self: Concept, subject: dict) -> None:
        self._subject = subject

    @property
    def definition(self: Concept) -> Definition:
        """Definition attribute."""
        return self._definition

    @definition.setter
    def definition(self: Concept, definition: Definition) -> None:
        self._definition = definition

    @property
    def alternativformulering(self: Concept) -> AlternativFormulering:
        """Alternativformulering attribute."""
        return self._alternativformulering

    @alternativformulering.setter
    def alternativformulering(
        self: Concept, alternativformulering: AlternativFormulering
    ) -> None:
        self._alternativformulering = alternativformulering

    @property
    def contactpoint(self: Concept) -> Contact:
        """Contacpoint attribute."""
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self: Concept, contact: Contact) -> None:
        self._contactpoint = contact

    @property
    def modified(self: Concept) -> date:
        """Modified attribute."""
        return self._modified

    @modified.setter
    def modified(self: Concept, modified: date) -> None:
        self._modified = modified

    @property
    def bruksomrade(self: Concept) -> dict:
        """Bruksomrade attribute."""
        return self._bruksomrade

    @bruksomrade.setter
    def bruksomrade(self: Concept, bruksomrade: dict) -> None:
        self._bruksomrade = bruksomrade

    @property
    def validinperiod(self: Concept) -> dict:
        """Validinperiod attribute."""
        return self._validinperiod

    @validinperiod.setter
    def validinperiod(self: Concept, validinperiod: dict) -> None:
        self._validinperiod = validinperiod

    @property
    def publisher(self: Concept) -> str:
        """Publisher attribute."""
        return self._publisher

    @publisher.setter
    def publisher(self: Concept, publisher: str) -> None:
        self._publisher = publisher

    @property
    def seeAlso(self: Concept) -> List[Concept]:
        """Seealso attribute."""
        return self._seeAlso

    @seeAlso.setter
    def seeAlso(self: Concept, concepts: List[Concept]) -> None:
        self._seeAlso = concepts

    @property
    def replaces(self: Concept) -> List[Concept]:
        """Replaces attribute."""
        return self._replaces

    @replaces.setter
    def replaces(self: Concept, concepts: List[Concept]) -> None:
        self._replaces = concepts

    @property
    def replacedBy(self: Concept) -> List[Concept]:
        """Replacedby attribute."""
        return self._replacedBy

    @replacedBy.setter
    def replacedBy(self: Concept, concepts: List[Concept]) -> None:
        self._replacedBy = concepts

    @property
    def related(self: Concept) -> AssociativeRelation:
        """Related attribute."""
        return self._related

    @related.setter
    def related(self: Concept, ar: AssociativeRelation) -> None:
        self._related = ar

    @property
    def generalizes(self: Concept) -> GenericRelation:
        """Generalizes attribute."""
        return self._generalizes

    @generalizes.setter
    def generalizes(self: Concept, gr: GenericRelation) -> None:
        self._generalizes = gr

    @property
    def hasPart(self: Concept) -> PartitiveRelation:
        """Haspart attribute."""
        return self._hasPart

    @hasPart.setter
    def hasPart(self: Concept, gr: PartitiveRelation) -> None:
        self._hasPart = gr

    # ----------------------------------------------

    def _to_graph(self) -> Graph:
        """Transforms the concept to an rdf graph.

        Returns:
            an RDF graph representing the concept.
        """
        self._add_concept_to_graph()

        return self._g

    def to_rdf(self: Concept, format: str = "text/turtle") -> str:
        """Maps the concept to rdf.

        Args:
            format: a valid serialization format.

        Returns:
            a serialization of the RDF graph
        """
        return self._to_graph().serialize(format=format)

    # ----------------------------------------------

    def _add_concept_to_graph(self: Concept) -> None:
        """Adds the concept to the Graph _g."""
        self._g.bind("dct", DCT)
        self._g.bind("skos", SKOS)
        self._g.bind("skosxl", SKOSXL)
        self._g.bind("vcard", VCARD)
        self._g.bind("skosno", SKOSNO)
        self._g.bind("dcat", DCAT)
        self._g.bind("xsd", XSD)
        self._g.bind("schema", SCHEMA)
        self._g.bind("xkos", XKOS)

        self._g.add((URIRef(self.identifier), RDF.type, SKOS.Concept))

        # prefLabel
        self._term_to_graph()

        # altLabel
        self._add_alternativeterm_to_graph()

        # hiddenLabel
        self._add_hiddenterm_to_graph()

        # datastrukturterm
        self._add_datastrukturterm_to_graph()

        # definition
        if getattr(self, "definition", None):
            self._add_betydningsbeskrivelse_to_concept(self.definition)

        # alternativformulering
        if getattr(self, "alternativformulering", None):
            self._add_betydningsbeskrivelse_to_concept(self.alternativformulering)

        # publisher
        self._add_publisher_to_graph()

        # contactPoint
        self._add_contactpoint_to_graph()

        # subject
        self._add_subject_to_graph()

        # modified
        self._add_modified_to_graph()

        # bruksomrade
        self._add_bruksomrade_to_graph()

        # PeriodOfTime
        self._add_validinperiod_to_graph()

        # seeAlso
        self._add_seeAlso_to_graph()

        # replaces
        self._add_replaces_to_graph()

        # replacedBy
        self._add_replacedBy_to_graph()

        # related
        self._add_related_to_graph()

        # generalizes
        self._add_generalizes_to_graph()

        # hasPart
        self._add_hasPart_to_graph()

    # ------------
    # Helper methods:

    def _term_to_graph(self: Concept) -> None:
        if getattr(self, "term", None):
            label = BNode()
            self._g.add((label, RDF.type, SKOSXL.Label))
            if "name" in self.term:
                _name = self.term["name"]
                for key in _name:
                    self._g.add(
                        (label, SKOSXL.literalForm, Literal(_name[key], lang=key))
                    )
            if "modified" in self.term:
                self._g.add(
                    (
                        label,
                        DCT.modified,
                        Literal(self.term["modified"], datatype=XSD.date),
                    )
                )
            self._g.add((URIRef(self.identifier), SKOSXL.prefLabel, label))

    def _add_alternativeterm_to_graph(self: Concept) -> None:
        if getattr(self, "alternativeterm", None):
            altLabel = BNode()
            self._g.add((altLabel, RDF.type, SKOSXL.Label))
            if "name" in self.alternativeterm:
                _name = self.alternativeterm["name"]
                for key in _name:
                    for l in _name[key]:
                        self._g.add(
                            (altLabel, SKOSXL.literalForm, Literal(l, lang=key))
                        )
            if "modified" in self.alternativeterm:
                self._g.add(
                    (
                        altLabel,
                        DCT.modified,
                        Literal(self.alternativeterm["modified"], datatype=XSD.date),
                    )
                )
            self._g.add((URIRef(self.identifier), SKOSXL.altLabel, altLabel))

    def _add_datastrukturterm_to_graph(self: Concept) -> None:
        if getattr(self, "datastrukturterm", None):
            datastrukturterm = BNode()
            self._g.add((datastrukturterm, RDF.type, SKOSXL.Label))
            if "name" in self.datastrukturterm:
                _name = self.datastrukturterm["name"]
                for key in _name:
                    for l in _name[key]:
                        self._g.add(
                            (datastrukturterm, SKOSXL.literalForm, Literal(l, lang=key))
                        )
            if "modified" in self.datastrukturterm:
                self._g.add(
                    (
                        datastrukturterm,
                        DCT.modified,
                        Literal(self.datastrukturterm["modified"], datatype=XSD.date),
                    )
                )
            self._g.add(
                (URIRef(self.identifier), SKOSNO.datastrukturterm, datastrukturterm)
            )

    def _add_hiddenterm_to_graph(self: Concept) -> None:
        if getattr(self, "hiddenterm", None):
            hiddenLabel = BNode()
            self._g.add((hiddenLabel, RDF.type, SKOSXL.Label))
            if "name" in self.hiddenterm:
                _name = self.hiddenterm["name"]
                for key in _name:
                    for l in _name[key]:
                        self._g.add(
                            (hiddenLabel, SKOSXL.literalForm, Literal(l, lang=key))
                        )
            if "modified" in self.hiddenterm:
                self._g.add(
                    (
                        hiddenLabel,
                        DCT.modified,
                        Literal(self.hiddenterm["modified"], datatype=XSD.date),
                    )
                )
            self._g.add((URIRef(self.identifier), SKOSXL.hiddenLabel, hiddenLabel))

    def _add_contactpoint_to_graph(self: Concept) -> None:
        if getattr(self, "contactpoint", None):
            contact = self.contactpoint
            contactPoint = BNode()
            for _s, p, o in contact._to_graph().triples((None, None, None)):
                self._g.add((contactPoint, p, o))
            self._g.add((URIRef(self.identifier), DCAT.contactPoint, contactPoint))

    def _add_subject_to_graph(self: Concept) -> None:
        if getattr(self, "subject", None):
            for key in self.subject:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.subject,
                        Literal(self.subject[key], lang=key),
                    )
                )

    def _add_bruksomrade_to_graph(self: Concept) -> None:
        if getattr(self, "bruksomrade", None):
            for key in self.bruksomrade:
                for b in self.bruksomrade[key]:
                    self._g.add(
                        (
                            URIRef(self.identifier),
                            SKOSNO.bruksområde,
                            Literal(b, lang=key),
                        )
                    )

    def _add_validinperiod_to_graph(self: Concept) -> None:
        if getattr(self, "validinperiod", None):
            periodOfTime = BNode()
            self._g.add((periodOfTime, RDF.type, DCT.PeriodOfTime))
            if "startdate" in self.validinperiod:
                self._g.add(
                    (
                        periodOfTime,
                        SCHEMA.startDate,
                        Literal(self.validinperiod["startdate"], datatype=XSD.date),
                    )
                )
            if "enddate" in self.validinperiod:
                self._g.add(
                    (
                        periodOfTime,
                        SCHEMA.endDate,
                        Literal(self.validinperiod["enddate"], datatype=XSD.date),
                    )
                )
            self._g.add((URIRef(self.identifier), DCT.temporal, periodOfTime))

    def _add_publisher_to_graph(self: Concept) -> None:
        if getattr(self, "publisher", None):
            self._g.add(
                (URIRef(self.identifier), DCT.publisher, URIRef(self.publisher))
            )

    def _add_modified_to_graph(self: Concept) -> None:
        if getattr(self, "modified", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.modified,
                    Literal(self.modified, datatype=XSD.date),
                )
            )

    def _add_seeAlso_to_graph(self: Concept) -> None:
        if getattr(self, "seeAlso", None):
            for c in self.seeAlso:
                self._g.add(
                    (URIRef(self.identifier), RDFS.seeAlso, URIRef(c.identifier))
                )

    def _add_replaces_to_graph(self: Concept) -> None:
        if getattr(self, "replaces", None):
            for c in self.replaces:
                self._g.add(
                    (URIRef(self.identifier), DCT.replaces, URIRef(c.identifier))
                )

    def _add_replacedBy_to_graph(self: Concept) -> None:
        if getattr(self, "replacedBy", None):
            for c in self.replacedBy:
                self._g.add(
                    (URIRef(self.identifier), DCT.replacedBy, URIRef(c.identifier))
                )

    def _add_related_to_graph(self: Concept) -> None:
        if getattr(self, "related", None):
            _related = self.related
            ar = BNode()
            for _s, p, o in _related._to_graph().triples((None, None, None)):
                self._g.add((ar, p, o))
            self._g.add((URIRef(self.identifier), SKOS.related, ar))

    def _add_generalizes_to_graph(self: Concept) -> None:
        if getattr(self, "generalizes", None):
            _generalizes = self.generalizes
            ar = BNode()
            for _s, p, o in _generalizes._to_graph().triples((None, None, None)):
                self._g.add((ar, p, o))
            self._g.add((URIRef(self.identifier), XKOS.generalizes, ar))

    def _add_hasPart_to_graph(self: Concept) -> None:
        if getattr(self, "hasPart", None):
            _hasPart = self.hasPart
            ar = BNode()
            for _s, p, o in _hasPart._to_graph().triples((None, None, None)):
                self._g.add((ar, p, o))
            self._g.add((URIRef(self.identifier), XKOS.hasPart, ar))

    # -
    def _add_betydningsbeskrivelse_to_concept(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse
    ) -> None:

        _betydningsbeskrivelse = BNode()

        # Check type of sub class, and add corresponding object:
        if isinstance(betydningsbeskrivelse, Definition):
            self._g.add((_betydningsbeskrivelse, RDF.type, SKOSNO.Definisjon))
        else:
            self._g.add(
                (_betydningsbeskrivelse, RDF.type, SKOSNO.AlternativFormulering)
            )

        # text
        self._add_text_to_bs_graph(betydningsbeskrivelse, _betydningsbeskrivelse)

        # remark
        self._add_remark_to_bs_graph(betydningsbeskrivelse, _betydningsbeskrivelse)

        # scope
        self._add_scope_to_bs_graph(betydningsbeskrivelse, _betydningsbeskrivelse)

        # relationtosource
        self._add_relationtosource_bs_to_graph(
            betydningsbeskrivelse, _betydningsbeskrivelse
        )

        # source
        self._add_source_to_bs_graph(betydningsbeskrivelse, _betydningsbeskrivelse)

        # modified
        self._add_modified_to_bs_graph(betydningsbeskrivelse, _betydningsbeskrivelse)

        # example
        self._add_example_to_bs_graph(betydningsbeskrivelse, _betydningsbeskrivelse)

        # Check type, and set correct property
        if isinstance(betydningsbeskrivelse, Definition):
            self._g.add(
                (URIRef(self.identifier), SKOSNO.definisjon, _betydningsbeskrivelse)
            )
        else:
            self._g.add(
                (
                    URIRef(self.identifier),
                    SKOSNO.alternativFormulering,
                    _betydningsbeskrivelse,
                )
            )
        # ---

    def _add_text_to_bs_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "text", None):
            _text = betydningsbeskrivelse.text
            for key in _text:
                self._g.add((bsnode, RDFS.label, Literal(_text[key], lang=key),))

    def _add_remark_to_bs_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "remark", None):
            _remark = betydningsbeskrivelse.remark
            for key in _remark:
                self._g.add(
                    (
                        bsnode,
                        SKOS.scopeNote,
                        Literal(betydningsbeskrivelse.remark[key], lang=key),
                    )
                )

    def _add_scope_to_bs_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "scope", None):
            _scope = BNode()
            if "url" in betydningsbeskrivelse.scope:
                self._g.add(
                    (_scope, RDFS.seeAlso, URIRef(betydningsbeskrivelse.scope["url"]),)
                )
            if "text" in betydningsbeskrivelse.scope:
                _text = betydningsbeskrivelse.scope["text"]
                for key in _text:
                    self._g.add((_scope, RDFS.label, Literal(_text[key], lang=key)))
            self._g.add((bsnode, SKOSNO.omfang, _scope))

    def _add_relationtosource_bs_to_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "relationtosource", None):
            # -
            # sitatFraKilde = "quoteFromSource"
            # basertPaKilde = "basedOnSource"
            # egendefinert = "noSource"
            # -
            if (
                RelationToSource(betydningsbeskrivelse.relationtosource)
                is RelationToSource.sitatFraKilde
            ):
                self._g.add((bsnode, SKOSNO.forholdTilKilde, SKOSNO.sitatFraKilde,))
            elif (
                RelationToSource(betydningsbeskrivelse.relationtosource)
                is RelationToSource.basertPaKilde
            ):
                self._g.add((bsnode, SKOSNO.forholdTilKilde, SKOSNO.basertPåKilde,))
            else:
                self._g.add((bsnode, SKOSNO.forholdTilKilde, SKOSNO.egendefinert,))

    def _add_source_to_bs_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "source", None):
            _source = BNode()
            if "url" in betydningsbeskrivelse.source:
                self._g.add(
                    (
                        _source,
                        RDFS.seeAlso,
                        URIRef(betydningsbeskrivelse.source["url"]),
                    )
                )
            if "text" in betydningsbeskrivelse.source:
                _text = betydningsbeskrivelse.source["text"]
                for key in _text:
                    self._g.add((_source, RDFS.label, Literal(_text[key], lang=key)))
            self._g.add((bsnode, DCT.source, _source))

    def _add_modified_to_bs_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "modified", None):
            self._g.add(
                (
                    bsnode,
                    DCT.modified,
                    Literal(betydningsbeskrivelse.modified, datatype=XSD.date),
                )
            )

    def _add_example_to_bs_graph(
        self: Concept, betydningsbeskrivelse: Betydningsbeskrivelse, bsnode: BNode
    ) -> None:
        if getattr(betydningsbeskrivelse, "example", None):
            _example = betydningsbeskrivelse.example
            for key in _example:
                self._g.add((bsnode, SKOS.example, Literal(_example[key], lang=key),))
