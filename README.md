# concepttordf

A small Python library for mapping a concept collection to the [skos-ap-no specification](https://doc.difi.no/data/begrep-skos-ap-no/).

## Usage
### Install

### Getting started

```
from concepttordf.concept import Concept

concept = Concept()
concept.identifier = "http://example.com/concepts/1"
concept.term = {}
concept.term['en'] = "concept"
concept.term['nb'] = "begrep"
concept.definition = {}
concept.definition['en'] = (
    "an abstract or generic idea generalized from particular instances"
    )
concept.definition['nb'] = (
    "mental forestilling om et konkret eller abstrakt"
    "fenomen i den virkelige verden"
    )
concept.publisher = "https://example.com/publishers/1"

print(concept.to_rdf().decode())
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
```
### Run all tests
```
pytest -rA
```
With coverage:
```
pytest -rA --cov-report term-missing --cov=concepttordf tests/
```
