import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from core.logging.context import set_request_ctx_http_data, set_request_ctx_log_data
from core.logging.logger import get_logger
from core.logging.serializers import CompanyContext
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Company

logger = get_logger()
router = APIRouter()


@router.get("/v1/company/{company_id}", name="Get Company", dependencies=[Depends(authorize_request)])
def get_company(company_id: str) -> JSONResponse:
    company = operations.get_company(company_id)

    parsed_entity = parse_entity(company)
    set_request_ctx_log_data(company=CompanyContext(method="get_company", company_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved company with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)


@router.post("/v1/company", name="Create Company", dependencies=[Depends(authorize_request)])
def create_company(req_data: Company) -> JSONResponse:
    company = operations.create_company(**req_data.model_dump(by_alias=True))

    parsed_entity = parse_entity(company)
    set_request_ctx_log_data(company=CompanyContext(method="create_company", company_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_201_CREATED, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully created company with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parsed_entity)
