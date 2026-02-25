# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Project Overview

Python library that maps concept collections to RDF according to [SKOS-AP-NO](https://doc.difi.no/data/begrep-skos-ap-no/) (Norwegian application profile for SKOS). Wraps rdflib for RDF graph construction and serialization.

## Commands

### Run all default nox sessions (lint, mypy, pytype, tests)

```
nox
```

### Run tests with coverage

```
nox -rs tests
```

### Run a single test file

```
nox -rs tests -- tests/test_concept.py
```

### Run a single test

```
nox -rs tests -- tests/test_concept.py::test_function_name
```

### Format code

```
nox -rs black
```

### Lint

```
nox -rs lint
```

### Type check

```
nox -rs mypy
```

## Architecture

Source code is in `src/concepttordf/`. The library models SKOS concepts as Python objects that serialize to RDF graphs.

### Class Hierarchy

- **Collection** — Top-level container (`skos:Collection`). Holds a list of Concept members. Entry point via `to_rdf(format, includeconcepts)`.
- **Concept** — Main entity (`skos:Concept`). Has terms, definitions, relations, contact info, and metadata. Largest class (~815 lines).
- **Betydningsbeskrivelse** — Abstract base for meaning descriptions.
  - **Definition** (`skosno:Definisjon`) — Formal definition with text, source, scope, remark.
  - **AlternativFormulering** (`skosno:AlternativFormulering`) — Alternative formulation.
- **ConceptRelation** — Abstract base for relations between concepts.
  - **AssociativeRelation** — Links associated concepts.
  - **GenericRelation** — Generalization/specialization hierarchy.
  - **PartitiveRelation** — Part-of/has-part relationships.
- **Contact** — Maps to `vcard:Organization` with name, email, telephone, url.

### Test Approach

Tests in `tests/` load expected RDF from JSON fixture files in `tests/files/`, create objects programmatically, serialize to RDF, and compare graphs using `rdflib.compare.isomorphic()`.

## Code Style

- **Formatter**: Black (max line length 80)
- **Linter**: Flake8 with plugins for annotations, security (bandit), bugbear, docstrings, import order
- **Docstrings**: Google style convention
- **Import order**: Google style
- **Type checking**: mypy (strict=false) and pytype
- **Coverage**: 100% required (`fail_under = 100`)
- **Python**: 3.10, 3.11, 3.12
