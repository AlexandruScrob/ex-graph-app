import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from core.logging.context import set_request_ctx_http_data, set_request_ctx_log_data
from core.logging.logger import get_logger
from core.logging.serializers import ClaimContext
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Claim

logger = get_logger()
router = APIRouter()


@router.get("/v1/claim/{claim_id}", name="Get Claim", dependencies=[Depends(authorize_request)])
def get_claim(claim_id: str) -> JSONResponse:
    claim = operations.get_claim(claim_id)

    parsed_entity = parse_entity(claim)
    set_request_ctx_log_data(claim=ClaimContext(method="get_claim", claim_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved claim with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)


@router.post("/v1/claim", name="Create Claim", dependencies=[Depends(authorize_request)])
def create_claim(req_data: Claim) -> JSONResponse:
    claim = operations.create_claim(**req_data.model_dump(by_alias=True))

    parsed_entity = parse_entity(claim)
    set_request_ctx_log_data(claim=ClaimContext(method="create_claim", claim_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_201_CREATED, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully created claim with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parsed_entity)
