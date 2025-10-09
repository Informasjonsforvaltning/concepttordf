"""Test cases for the alternativformulering module."""

from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from concepttordf import AlternativFormulering


def test_alternativformulering_to_rdf() -> None:
    """Test that AlternativFormulering.to_rdf() returns valid RDF."""
    alt_form = AlternativFormulering()
    alt_form.text = {"nb": "En alternativ formulering"}
    alt_form.remark = {"nb": "En test merknad"}
    alt_form.scope = {"nb": "En test omfang"}
    alt_form.source = {"nb": "En test kilde"}
    alt_form.example = {"nb": "En test eksempel"}

    g1 = Graph()
    g1.parse(data=alt_form.to_rdf(), format="text/turtle")

    src = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .

    [] a skosno:AlternativFormulering ;
        skosno:tekst "En alternativ formulering"@nb ;
        skosno:merknad "En test merknad"@nb ;
        skosno:omfang "En test omfang"@nb ;
        skosno:kilde "En test kilde"@nb ;
        skosno:eksempel "En test eksempel"@nb .
    """

    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
    assert _isomorphic


def test_alternativformulering_to_graph() -> None:
    """Test that AlternativFormulering._to_graph() returns a Graph object."""
    alt_form = AlternativFormulering()
    alt_form.text = {"nb": "En alternativ formulering"}

    g1 = alt_form._to_graph()

    src = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .

    [] a skosno:AlternativFormulering ;
        skosno:tekst "En alternativ formulering"@nb .
    """

    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
    assert _isomorphic


def test_alternativformulering_empty() -> None:
    """Test that AlternativFormulering works with no attributes set."""
    alt_form = AlternativFormulering()

    g1 = Graph()
    g1.parse(data=alt_form.to_rdf(), format="text/turtle")

    src = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .

    [] a skosno:AlternativFormulering .
    """

    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
    assert _isomorphic


def test_alternativformulering_multiple_languages() -> None:
    """Test that AlternativFormulering handles multiple languages."""
    alt_form = AlternativFormulering()
    alt_form.text = {
        "nb": "En alternativ formulering på norsk",
        "en": "An alternative formulation in English",
    }
    alt_form.remark = {"nb": "En merknad på norsk", "en": "A remark in English"}

    g1 = Graph()
    g1.parse(data=alt_form.to_rdf(), format="text/turtle")

    src = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix skosno: <https://data.norge.no/vocabulary/skosno#> .

    [] a skosno:AlternativFormulering ;
        skosno:tekst "En alternativ formulering på norsk"@nb ;
        skosno:tekst "An alternative formulation in English"@en ;
        skosno:merknad "En merknad på norsk"@nb ;
        skosno:merknad "A remark in English"@en .
    """

    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Util for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="text/turtle", base="").splitlines():
        if _l:
            print(_l)
