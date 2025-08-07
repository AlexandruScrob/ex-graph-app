import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from core.logging.context import set_request_ctx_http_data, set_request_ctx_log_data
from core.logging.logger import get_logger
from core.logging.serializers import CompanyContext, PersonContext, ClaimContext, DocumentContext
from external.neo4j import operations
from views.helpers import parse_entity

logger = get_logger()
router = APIRouter()


@router.post(
    "/v1/person/{person_id}/company/{company_id}",
    name="Person Works For Company",
    dependencies=[Depends(authorize_request)],
)
def create_person_company_relationship(person_id: str, company_id: str) -> JSONResponse:
    is_connected = operations.create_person_company_relationship(person_id=person_id, company_id=company_id)
    response_body = {"isConnected": is_connected}

    set_request_ctx_log_data(
        company=CompanyContext(method="create_person_company_relationship", company_id=company_id),
        person=PersonContext(method="create_person_company_relationship", person_id=person_id),
    )
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=response_body)

    logger.info(
        (
            f"{'Successfully connected' if is_connected else 'Failed to connect'} "
            f"company with ID: {company_id} with person with ID: {person_id}"
        )
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@router.post(
    "/v1/person/{person_id}/claim/{claim_id}",
    name="Person Submits Claim",
    dependencies=[Depends(authorize_request)],
)
def create_person_claim_relationship(person_id: str, claim_id: str) -> JSONResponse:
    is_connected = operations.create_person_claim_relationship(person_id=person_id, claim_id=claim_id)
    response_body = {"isConnected": is_connected}

    set_request_ctx_log_data(
        claim=ClaimContext(method="create_person_claim_relationship", claim_id=claim_id),
        person=PersonContext(method="create_person_claim_relationship", person_id=person_id),
    )
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=response_body)

    logger.info(
        (
            f"{'Successfully connected' if is_connected else 'Failed to connect'} "
            f"claim with ID: {claim_id} with person with ID: {person_id}"
        )
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@router.post(
    "/v1/person/{person_id}/document/{document_id}",
    name="Person Sends Document",
    dependencies=[Depends(authorize_request)],
)
def create_person_document_relationship(person_id: str, document_id: str) -> JSONResponse:
    is_connected = operations.create_person_document_relationship(person_id=person_id, document_id=document_id)
    response_body = {"isConnected": is_connected}

    set_request_ctx_log_data(
        document=DocumentContext(method="create_person_document_relationship", document_id=document_id),
        person=PersonContext(method="create_person_document_relationship", person_id=person_id),
    )
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=response_body)

    logger.info(
        f"{'Successfully connected' if is_connected else 'Failed to connect'} "
        f"document with ID: {document_id} with person with ID: {person_id}"
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@router.post(
    "/v1/claim/{claim_id}/company/{company_id}",
    name="Claim has Claimant to Company",
    dependencies=[Depends(authorize_request)],
)
def create_claim_company_relationship(claim_id: str, company_id: str) -> JSONResponse:
    is_connected = operations.create_claim_company_relationship(claim_id=claim_id, company_id=company_id)
    response_body = {"isConnected": is_connected}

    set_request_ctx_log_data(
        claim=ClaimContext(method="create_claim_company_relationship", claim_id=claim_id),
        company=CompanyContext(method="create_claim_company_relationship", company_id=company_id),
    )
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=response_body)

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@router.get(
    "/v1/person/{person_id}/claims",
    name="Get Claims Submitted by Person",
    dependencies=[Depends(authorize_request)],
)
def get_claims_by_person(person_id: str) -> JSONResponse:
    claims = operations.get_claims_by_person(person_id=person_id)
    parsed_entity = parse_entity(claims)

    set_request_ctx_log_data(person=PersonContext(method="get_claims_by_person", person_id=person_id))
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved claims by person with ID: {person_id}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)


@router.get(
    "/v1/claims/company/{company_id}",
    name="Get Claims associated to a specific Company",
    dependencies=[Depends(authorize_request)],
)
def get_claims_by_company(company_id: str) -> JSONResponse:
    claims = operations.get_claims_by_company(company_id=company_id)
    parsed_entity = parse_entity(claims)

    set_request_ctx_log_data(company=CompanyContext(method="get_claims_by_company", company_id=company_id))
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved claims by company with ID: {company_id}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)


@router.get(
    "/v1/company/person/{person_id}",
    name="Get Company associated to a Person",
    dependencies=[Depends(authorize_request)],
)
def get_company_by_person(person_id: str) -> JSONResponse:
    company = operations.get_company_by_person(person_id=person_id)
    parsed_entity = parse_entity(company)
    company_id = parsed_entity.get("pid")

    set_request_ctx_log_data(
        company=CompanyContext(method="get_company_by_person", company_id=company_id),
        person=PersonContext(method="get_company_by_person", person_id=person_id),
    )
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved company with ID: {company_id} by person with ID: {person_id}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)
