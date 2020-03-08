from concepttordf.collection import Collection
from concepttordf.concept import Concept

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

c1 = Concept()
c1.identifier = "http://example.com/concepts/1"
collection.members.append(c1)

c2 = Concept()
c2.identifier = "http://example.com/concepts/2"
collection.members.append(c2)

print(collection.to_rdf().decode())

# prints:
