from concepttordf.collection import Collection
from concepttordf.concept import Concept
from concepttordf.definition import Definition

# Create collection object
collection = Collection()
collection.identifier = "http://example.com/collections/1"
collection.name = {}
collection.name['en'] = "A concept collection"
collection.name['nb'] = "En begrepssamling"
collection.description = {}
collection.description['en'] = (
    "This collection collects a sample of our finest concepts"
    )
collection.description['nb'] = (
    "Denne samlingen inneholder et utvalg av våre beste begreper"
    )
collection.publisher = "https://example.com/publishers/1"

# Add concepts to collection
collection.members = []

# A concept:
c1 = Concept()
c1.identifier = "http://example.com/concepts/1"
c1.term = {"name": {"nb": "inntekt", "en": "income"}}
definition = Definition()
definition.text = {"nb": "ting man skulle hatt mer av",
                   "en": "something you want more of"}
c1.definition = definition
collection.members.append(c1)

# Another concept:
c2 = Concept()
c2.identifier = "http://example.com/concepts/2"
c2.term = {"name": {"nb": "lån", "en": "loan"}}
definition = Definition()
definition.text = {"nb": "ting man skulle hatt mindre av",
                   "en": "something you want less of"}
c2.definition = definition
collection.members.append(c2)

# get rdf representation in turtle (default)
rdf = collection.to_rdf()
print(rdf.decode())
