from concepttordf import Concept, Definition

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

# get rdf representation in xml
rdf = concept.to_rdf(format='xml')
print(rdf.decode())
