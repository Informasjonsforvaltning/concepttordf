# concepttordf

A small Python library to work with an openAPI specification.

At this moment we support all 3.0.x versions of (The OpenAPI specification)[https://github.com/OAI/OpenAPI-Specification]

Roadmap:
- a method for validating the specification  
- properties for most useful attributes of spec such as:
  - content types in responses
  - server urls
  - schema objects

## Usage
TODO


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
