from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from external.neo4j import operations
from views.helpers import parse_entity

router = APIRouter()


@router.post(
    "/v1/person/{person_id}/company/{company_id}",
    name="Person Works For Company",
    dependencies=[Depends(authorize_request)],
)
def create_person_company_relationship(person_id: str, company_id: str) -> JSONResponse:
    is_connected = operations.create_person_company_relationship(person_id=person_id, company_id=company_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=(
            f"{'SUCCESS' if is_connected else 'FAILED'} Person with id:{person_id}"
            f" WORKS FOR company with id:{company_id}"
        ),
    )


@router.post(
    "/v1/person/{person_id}/claim/{claim_id}",
    name="Person Submits Claim",
    dependencies=[Depends(authorize_request)],
)
def create_person_claim_relationship(person_id: str, claim_id: str) -> JSONResponse:
    is_connected = operations.create_person_claim_relationship(person_id=person_id, claim_id=claim_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=(
            f"{'SUCCESS' if is_connected else 'FAILED'} Person with id:{person_id} SUBMITTED claim with id:{claim_id}"
        ),
    )


@router.post(
    "/v1/person/{person_id}/document/{document_id}",
    name="Person Sends Document",
    dependencies=[Depends(authorize_request)],
)
def create_person_document_relationship(person_id: str, document_id: str) -> JSONResponse:
    is_connected = operations.create_person_document_relationship(person_id=person_id, document_id=document_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=(
            f"{'SUCCESS' if is_connected else 'FAILED'} Person with id:{person_id} SENT document with id:{document_id}"
        ),
    )


@router.post(
    "/v1/claim/{claim_id}/company/{company_id}",
    name="Claim has Claimant to Company",
    dependencies=[Depends(authorize_request)],
)
def create_claim_company_relationship(claim_id: str, company_id: str) -> JSONResponse:
    is_connected = operations.create_claim_company_relationship(claim_id=claim_id, company_id=company_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=(
            f"{'SUCCESS' if is_connected else 'FAILED'} Claim with id:{claim_id} "
            f"HAS CLAIMANT Company with id:{company_id}"
        ),
    )


@router.get(
    "/v1/person/{person_id}/claims",
    name="Get Claims Submitted by Person",
    dependencies=[Depends(authorize_request)],
)
def get_claims_by_person(person_id: str) -> JSONResponse:
    claims = operations.get_claims_by_person(person_id=person_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(claims))


@router.get(
    "/v1/claims/company/{company_id}",
    name="Get Claims associated to a specific Company",
    dependencies=[Depends(authorize_request)],
)
def get_claims_by_company(company_id: str) -> JSONResponse:
    claims = operations.get_claims_by_company(company_id=company_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(claims))


@router.get(
    "/v1/company/person/{person_id}",
    name="Get Company associated to a Person",
    dependencies=[Depends(authorize_request)],
)
def get_company_by_person(person_id: str) -> JSONResponse:
    company = operations.get_company_by_person(person_id=person_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(company))
