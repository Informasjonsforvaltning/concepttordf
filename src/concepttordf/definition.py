"""Module for helper class Definition."""

from rdflib import BNode, Graph, Literal, Namespace, RDF

from .betydningsbeskrivelse import Betydningsbeskrivelse

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")


class Definition(Betydningsbeskrivelse):
    """A class representing a definition."""

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._g: Graph = Graph()

    def _to_graph(self) -> Graph:
        """Transforms the definition to an RDF graph.

        Returns:
            an RDF graph representing the definition.
        """
        self._add_definition_to_graph()
        return self._g

    def _add_definition_to_graph(self) -> None:
        """Adds the definition to the Graph _g."""
        self._g.bind("skosno", SKOSNO)

        definition_node = BNode()
        self._g.add((definition_node, RDF.type, SKOSNO.Definisjon))

        self._add_text_to_graph(definition_node)
        self._add_remark_to_graph(definition_node)
        self._add_scope_to_graph(definition_node)
        self._add_source_to_graph(definition_node)
        self._add_example_to_graph(definition_node)

    def _add_text_to_graph(self, node: BNode) -> None:
        """Add text to graph if available."""
        if hasattr(self, "_text") and self._text:
            for lang, text in self._text.items():
                self._g.add((node, SKOSNO.tekst, Literal(text, lang=lang)))

    def _add_remark_to_graph(self, node: BNode) -> None:
        """Add remark to graph if available."""
        if hasattr(self, "_remark") and self._remark:
            for lang, remark in self._remark.items():
                self._g.add((node, SKOSNO.merknad, Literal(remark, lang=lang)))

    def _add_scope_to_graph(self, node: BNode) -> None:
        """Add scope to graph if available."""
        if hasattr(self, "_scope") and self._scope:
            for lang, scope in self._scope.items():
                self._g.add((node, SKOSNO.omfang, Literal(scope, lang=lang)))

    def _add_source_to_graph(self, node: BNode) -> None:
        """Add source to graph if available."""
        if hasattr(self, "_source") and self._source:
            for lang, source in self._source.items():
                self._g.add((node, SKOSNO.kilde, Literal(source, lang=lang)))

    def _add_example_to_graph(self, node: BNode) -> None:
        """Add example to graph if available."""
        if hasattr(self, "_example") and self._example:
            for lang, example in self._example.items():
                self._g.add((node, SKOSNO.eksempel, Literal(example, lang=lang)))

    def to_rdf(self, format: str = "text/turtle") -> str:
        """Convert the definition to RDF format.

        Args:
            format: a valid serialization format.

        Returns:
            RDF representation as a string
        """
        return self._to_graph().serialize(format=format, base="")
