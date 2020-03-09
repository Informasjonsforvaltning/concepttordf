# concepttordf

A small Python library for mapping a concept collection to the [skos-ap-no specification](https://doc.difi.no/data/begrep-skos-ap-no/).

## Usage
### Install
```
% pip install -i https://test.pypi.org/simple/ concepttordf-stigbd
```
### Getting started

```
from concepttordf.concept import Concept
from concepttordf.definition import Definition

# create a concept
concept = Concept()
# set identifier
concept.identifier = "http://example.com/concepts/1"
# set term
concept.term = {"name": {"nb": "begrep", "en": "concept"}}
# set definition
definition = Definition()
definition.text = {"nb":
                   ("mental forestilling om et konkret eller abstrakt"
                    "fenomen i den virkelige verden"),
                   "en":
                   ("an abstract or generic idea generalized from"
                    "particular instances")
                   }
concept.definition = definition
# set publisher
concept.publisher = "https://example.com/publishers/1"

# get rdf representation in turtle (default)
rdf = concept.to_rdf()
print(rdf.decode())
```
Will print the concept according to the specification:
```
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix skosno: <http://difi.no/skosno#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
@prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.com/concepts/1> a skos:Concept ;
    skosno:betydningsbeskrivelse [ a skosno:Definisjon ;
            rdfs:label "an abstract or generic idea generalized fromparticular instances"@en,
                "mental forestilling om et konkret eller abstraktfenomen i den virkelige verden"@nb ] ;
    dct:publisher <https://example.com/publishers/1> ;
    skosxl:prefLabel [ a skosxl:Label ;
            skosxl:literalForm "concept"@en,
                "begrep"@nb ] .
```

## Development
### Requirements
- python3
- pipenv

### Install
```
% git clone https://github.com/Informasjonsforvaltning/concepttordf.git
% cd concepttordf
% pipenv install
% pipenv shell
% pipenv shell
% pipenv install --dev -e .
```
### Run all tests
```
% pytest -rA
```
With simple coverage-report in output:
```
% pytest -rA --cov-report term-missing --cov=concepttordf tests/
```
Wit coverage-report to html:
```
% pytest -rA --cov-report html --cov=concepttordf tests/
```
### Debugging
You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:
```
pytest --pdb -rA --cov-report term-missing --cov=concepttordf tests/
```
You can set breakpoints directly in code by using the function `breakpoint()`.
