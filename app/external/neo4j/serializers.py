from neomodel import (
    StructuredNode,
    StringProperty,
    DateTimeProperty,
    FloatProperty,
    UniqueIdProperty,
    RelationshipTo,
)


class Company(StructuredNode):
    pid = UniqueIdProperty()
    name = StringProperty(required=True)
    type = StringProperty(required=True)
    registration_number = StringProperty()
    address = StringProperty()


class Claim(StructuredNode):
    pid = UniqueIdProperty()
    claim_number = StringProperty(required=True)
    amount = FloatProperty()
    status = StringProperty(required=True)
    submission_date = DateTimeProperty(format="%Y-%m-%dT%H:%M:%S")
    description = FloatProperty()

    company = RelationshipTo("Company", "HAS_CLAIMANT")


class Document(StructuredNode):
    pid = UniqueIdProperty()
    doc_number = StringProperty(required=True)
    title = StringProperty()
    submission_date = DateTimeProperty(format="%Y-%m-%dT%H:%M:%S")
    content_type = StringProperty()
    file_path = StringProperty()


class Person(StructuredNode):
    pid = UniqueIdProperty()
    name = StringProperty(required=True)
    role = StringProperty()
    email = StringProperty()
    phone = StringProperty()

    company = RelationshipTo("Company", "WORKS_FOR")
    claim = RelationshipTo("Claim", "SUBMITTED")
    document = RelationshipTo("Document", "SENT")
