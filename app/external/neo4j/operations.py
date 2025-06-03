from warnings import deprecated
from pydantic import BaseModel

from neo4j import GraphDatabase
from neomodel import StructuredNode, clear_neo4j_database, config, db

from external.neo4j import query as q
from external.neo4j.exceptions import EntityNotFoundError
from external.neo4j.serializers import Claim, Company, Document, Person
from core.settings import get_settings

settings = get_settings()
db_settings = settings.db_settings

db_url = f"{db_settings.prefix}://{db_settings.host_name}"
config.DATABASE_URL = (
    f"{db_settings.prefix}://{db_settings.username}:{db_settings.password.get_secret_value()}@{db_settings.host_name}"
)


def check_db_connection() -> None:
    with GraphDatabase.driver(db_url, auth=db_settings.auth) as driver:
        driver.verify_connectivity()


def clear_db() -> None:
    clear_neo4j_database(db, clear_constraints=False, clear_indexes=False)


def get_person(person_id: str) -> StructuredNode | None:
    return Person.nodes.get_or_none(pid=person_id)


def create_person(**kwargs) -> StructuredNode:
    return Person(**kwargs).save()


def get_company(company_id: str) -> StructuredNode | None:
    return Company.nodes.get_or_none(pid=company_id)


def create_company(**kwargs) -> StructuredNode:
    return Company(**kwargs).save()


def get_claim(claim_id: str) -> StructuredNode | None:
    return Claim.nodes.get_or_none(pid=claim_id)


def create_claim(**kwargs) -> StructuredNode:
    return Claim(**kwargs).save()


def get_document(document_id: str) -> StructuredNode | None:
    return Document.nodes.get_or_none(pid=document_id)


def create_document(**kwargs) -> StructuredNode:
    return Document(**kwargs).save()


###
# Relationship Operations
###


def create_person_company_relationship(person_id: str, company_id: str) -> bool:
    if person := get_person(person_id=person_id):
        if company := get_company(company_id=company_id):
            person.company.connect(company)
            return person.company.is_connected(company)
        raise EntityNotFoundError(f"Company with id:{company_id} not found")
    raise EntityNotFoundError(f"Person with id:{person_id} not found")


def create_person_claim_relationship(person_id: str, claim_id: str) -> bool:
    if person := get_person(person_id=person_id):
        if claim := get_claim(claim_id=claim_id):
            person.claim.connect(claim)
            return person.claim.is_connected(claim)
        raise EntityNotFoundError(f"Claim with id:{claim_id} not found")
    raise EntityNotFoundError(f"Person with id:{person_id} not found")


def create_person_document_relationship(person_id: str, document_id: str) -> bool:
    if person := get_person(person_id=person_id):
        if document := get_document(document_id=document_id):
            person.document.connect(document)
            return person.document.is_connected(document)
        raise EntityNotFoundError(f"Document with id:{document_id} not found")
    raise EntityNotFoundError(f"Person with id:{person_id} not found")


def create_claim_company_relationship(claim_id: str, company_id: str) -> bool:
    if claim := get_claim(claim_id=claim_id):
        if company := get_company(company_id=company_id):
            claim.company.connect(company)
            return claim.company.is_connected(company)
        raise EntityNotFoundError(f"Company with id:{company_id} not found")
    raise EntityNotFoundError(f"Claim with id:{claim_id} not found")


def get_claims_by_person(person_id: str) -> list[StructuredNode]:
    result = q.get_claims_by_person(person_id=person_id)
    if not result:
        raise EntityNotFoundError(f"No claims for person with id:{person_id} found")
    return result


def get_claims_by_company(company_id: str) -> list[StructuredNode]:
    result = q.get_claims_by_company(company_id=company_id)
    if not result:
        raise EntityNotFoundError(f"No claims associated to Company with id:{company_id} found")
    return result


def get_company_by_person(person_id: str) -> StructuredNode:
    result = q.get_company_by_person(person_id=person_id)
    if not result:
        raise EntityNotFoundError(f"Person with id:{person_id} is not assiociated with any Company")
    return result


###
# Deprecated
###


@deprecated("This function has been deprecated")
def get_all_entities(entity_name: str):
    with GraphDatabase.driver(db_url, auth=db_settings.auth) as driver:
        with driver.session(database=db_settings.name) as session:
            return session.execute_read(q.get_all_entities, entity_name=entity_name)


@deprecated("This function has been deprecated")
def get_entity(entity_name: str, entity_id: str):
    with GraphDatabase.driver(db_url, auth=db_settings.auth) as driver:
        with driver.session(database=db_settings.name) as session:
            return session.execute_read(q.get_entity, entity_name=entity_name, entity_id=entity_id)


@deprecated("This function has been deprecated")
def create_entity(req_data: BaseModel):
    with GraphDatabase.driver(db_url, auth=db_settings.auth) as driver:
        with driver.session(database=db_settings.name) as session:
            return session.execute_write(
                q.create_entity_tx,
                entity_name=req_data.__class__.__name__,
                attributes=req_data.model_dump(exclude_none=True, by_alias=True),
            )


@deprecated("This function has been deprecated")
def create_relationship(entity_1_name: str, entity_1_id: str, entity_2_name: str, entity_2_id: str, relationship: str):
    with GraphDatabase.driver(db_url, auth=db_settings.auth) as driver:
        with driver.session(database=db_settings.name) as session:
            return session.execute_write(
                q.create_relationship,
                entity_1_name=entity_1_name,
                entity_1_id=entity_1_id,
                entity_2_name=entity_2_name,
                entity_2_id=entity_2_id,
                relationship=relationship,
            )
