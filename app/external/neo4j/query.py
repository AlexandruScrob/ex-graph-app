from typing import Any
from warnings import deprecated

from neomodel import db


def get_claims_by_person(person_id: str):
    results = db.cypher_query(
        """
            MATCH (pe:Person)-[r:SUBMITTED]->(cl:Claim)
            WHERE pe.pid = $person_id
            RETURN cl
        """,
        params={"person_id": person_id},
    )
    # only the list of nodes
    try:
        return [claim[0] for claim in results[0]]
    except IndexError:
        return None


def get_claims_by_company(company_id: str):
    results = db.cypher_query(
        """
            MATCH (cl:Claim)-[r:HAS_CLAIMANT]->(co:Company)
            WHERE co.pid = $company_id
            RETURN cl
        """,
        params={"company_id": company_id},
    )
    # only the list of nodes
    try:
        return [claim[0] for claim in results[0]]
    except IndexError:
        return None


def get_company_by_person(person_id: str):
    results = db.cypher_query(
        """
            MATCH (pe:Person)-[r:WORKS_FOR]->(co:Company)
            WHERE pe.pid = $person_id
            RETURN co
        """,
        params={"person_id": person_id},
    )
    # only the first node
    try:
        return results[0][0][0]
    except IndexError:
        return None


###
# Deprecated
###


@deprecated("This function has been deprecated")
def get_all_entities(tx, entity_name: str):
    entity_alias = entity_name.lower()[:2]

    result = tx.run(f"MATCH ({entity_alias}:{entity_name}) RETURN {entity_alias};")
    return result.value()


@deprecated("This function has been deprecated")
def get_entity(tx, entity_name: str, entity_id: str):
    entity_alias = entity_name.lower()[:2]
    result = tx.run(
        f"MATCH ({entity_alias}:{entity_name} {{id: $entity_id}})-[r]-(b) RETURN {entity_alias}, b, type(r)",
        entity_id=entity_id,
    )
    return result.value()


@deprecated("This function has been deprecated")
def create_entity_tx(tx, entity_name: str, attributes: dict[str, Any]):
    entity_alias = entity_name.lower()[:2]

    result = tx.run(
        f"CREATE ({entity_alias}:{entity_name} $attributes) RETURN {entity_alias};",
        {"attributes": attributes},
    )
    return result.single()[0]


def create_relationship(
    tx,
    entity_1_name: str,
    entity_1_id: str,
    entity_2_name: str,
    entity_2_id: str,
    relationship: str,
):
    entity_1_alias = entity_1_name.lower()[:2]
    entity_2_alias = entity_2_name.lower()[:2]
    result = tx.run(
        f"""
            MATCH ({entity_1_alias}:{entity_1_name} {{id: $entity_1_id}})
            MATCH ({entity_2_alias}:{entity_2_name} {{id: $entity_2_id}})
            MERGE ({entity_1_alias})-[r:{{rel: $relationship}}]->({entity_1_alias})
            RETURN {entity_1_alias}, {entity_1_alias}, type(r)
        """,
        entity_1_name=entity_1_name,
        entity_1_id=entity_1_id,
        entity_2_name=entity_2_name,
        entity_2_id=entity_2_id,
        relationship=relationship,
    )
    return result.single()
