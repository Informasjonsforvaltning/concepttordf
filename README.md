![Tests](https://github.com/Informasjonsforvaltning/concepttordf/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/concepttordf/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/concepttordf)
[![PyPI](https://img.shields.io/pypi/v/concepttordf.svg)](https://pypi.org/project/concepttordf/)
[![Read the Docs](https://readthedocs.org/projects/concepttordf/badge/)](https://concepttordf.readthedocs.io/)
# concepttordf

A small Python library for mapping a concept collection to the [skos-ap-no specification](https://doc.difi.no/data/begrep-skos-ap-no/).

## Usage
### Install
```
% pip install -i concepttordf
```
### Getting started
To create a SKOS-AP-NO concept collection:
```
from concepttordf import Collection, Concept, Definition

# Create collection object
collection = Collection()
collection.identifier = "http://example.com/collections/1"
collection.name = {"en": "A concept collection"}
collection.name = {"nb": "En begrepssamling"}
collection.publisher = "https://example.com/publishers/1"

# Create a concept:
c = Concept()
c.identifier = "http://example.com/concepts/1"
c.term = {"name": {"nb": "inntekt", "en": "income"}}
definition = Definition()
definition.text = {"nb": "ting man skulle hatt mer av",
                   "en": "something you want more of"}
c.definition = definition

# Add concept to collection:
collection.members.append(c)

# get rdf representation in turtle (default)
rdf = collection.to_rdf()
print(rdf.decode())
```
Will print the concept according to the specification:
```
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ns1: <https://data.norge.no/vocabulary/skosno#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix skosno: <http://difi.no/skosno> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.com/collections/1> a skos:Collection ;
    rdfs:label "En begrepssamling"@nb ;
    dct:publisher <https://example.com/publishers/1> ;
    skos:member <http://example.com/concepts/1> .

<http://example.com/concepts/1> a skos:Concept ;
    ns1:betydningsbeskrivelse [ a ns1:Definisjon ;
            rdfs:label "something you want more of"@en,
                "ting man skulle hatt mer av"@nb ] ;
    skosxl:prefLabel [ a skosxl:Label ;
            skosxl:literalForm "income"@en,
                "inntekt"@nb ] .

```

## Development
### Requirements
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)

### Install
```
% git clone https://github.com/Informasjonsforvaltning/concepttordf.git
% cd concepttordf
% pyenv install 3.8.2
% pyenv install 3.7.6
% pyenv local 3.8.2 3.7.6
% poetry install
```
### Run all tests
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
### Debugging
You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:
```
nox -rs tests -- --pdb
```
You can set breakpoints directly in code by using the function `breakpoint()`.
