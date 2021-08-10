"""Example module for use of Collection."""
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
definition.text = {
    "nb": "ting man skulle hatt mer av",
    "en": "something you want more of",
}
c.definition = definition

# Add concept to collection:
collection.members.append(c)

# get rdf representation in turtle (default)
rdf = collection.to_rdf()
print()
