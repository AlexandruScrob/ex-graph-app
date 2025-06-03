from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Company

router = APIRouter()


@router.get("/v1/company/{company_id}", name="Get Company", dependencies=[Depends(authorize_request)])
def get_company(company_id: str) -> JSONResponse:
    company = operations.get_company(company_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(company))


@router.post("/v1/company", name="Create Company", dependencies=[Depends(authorize_request)])
def create_company(req_data: Company) -> JSONResponse:
    company = operations.create_company(**req_data.model_dump(by_alias=True))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_entity(company))
