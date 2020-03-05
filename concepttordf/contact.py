from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

DCT = Namespace('http://purl.org/dc/terms/')
SKOSXL = Namespace('http://www.w3.org/2008/05/skos-xl#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SKOSNO = Namespace('http://difi.no/skosno#')


class Contact:
    """A class representing a contact """

    def __init__(self, contact: dict = None):
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

        return _add_contact_to_graph(self)

    def to_rdf(self, format='turtle') -> str:
        """Maps the contact to rdf and returns a serialization
           as a string according to format"""

        _g = self.to_graph()

        return _g.serialize(format=format, encoding='utf-8')


def _add_contact_to_graph(contact: Contact) -> Graph:
    """Adds the concept to the Graph g and returns g"""

    g = Graph()

    g.bind('vcard', VCARD)

    if hasattr(contact, 'identifier'):
        _contact = URIRef(contact.identifier)
    else:
        _contact = BNode()

    g.add((_contact, RDF.type, VCARD.Organization))

    # name
    if hasattr(contact, 'name'):
        for key in contact.name:
            g.add((_contact, VCARD.hasOrganizationName,
                   Literal(contact.name[key], lang=key)))

    # email
    if hasattr(contact, 'email'):
        g.add((_contact, VCARD.hasEmail,
               URIRef('mailto:' + contact.email)))

    # telephone
    if hasattr(contact, 'telephone'):
        g.add((_contact, VCARD.hasTelephone,
               URIRef('tel:' + contact.telephone)))

    # url
    if hasattr(contact, 'url'):
        g.add((_contact, VCARD.hasURL,
               URIRef(contact.url)))

    return g
