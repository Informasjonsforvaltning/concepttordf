from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

DCT = Namespace('http://purl.org/dc/terms/')
SKOSXL = Namespace('http://www.w3.org/2008/05/skos-xl#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SKOSNO = Namespace('https://data.norge.no/vocabulary/skosno#')


class Contact:
    """A class representing a contact """

    def __init__(self, contact: dict = None):
        self._g = Graph()
        if contact is not None:
            if 'name' in contact:
                self._name = contact['name']
            if 'email' in contact:
                self._email = contact['email']
            if 'url' in contact:
                self._url = contact['url']
            if 'telephone' in contact:
                self._telephone = contact['telephone']

    @property
    def name(self) -> dict:
        return self._name

    @name.setter
    def name(self, name: dict):
        self._name = name

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def telephone(self) -> str:
        return self._telephone

    @telephone.setter
    def telephone(self, telephone: str):
        self._telephone = telephone

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    def to_graph(self) -> Graph:

        self._add_contact_to_graph()

        return self._g

    def to_rdf(self, format='turtle') -> str:
        """Maps the contact to rdf and returns a serialization
           as a string according to format"""

        return self.to_graph().serialize(format=format, encoding='utf-8')

    # -----

    def _add_contact_to_graph(self):
        """Adds the concept to the Graph _g"""

        self._g.bind('vcard', VCARD)

        if hasattr(self, 'identifier'):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        self._g.add((_self, RDF.type, VCARD.Organization))

        # name
        if hasattr(self, 'name'):
            for key in self.name:
                self._g.add((_self, VCARD.hasOrganizationName,
                            Literal(self.name[key], lang=key)))

        # email
        if hasattr(self, 'email'):
            self._g.add((_self, VCARD.hasEmail,
                        URIRef('mailto:' + self.email)))

        # telephone
        if hasattr(self, 'telephone'):
            self._g.add((_self, VCARD.hasTelephone,
                        URIRef('tel:' + self.telephone)))

        # url
        if hasattr(self, 'url'):
            self._g.add((_self, VCARD.hasURL,
                        URIRef(self.url)))
