import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from core.logging.context import set_request_ctx_http_data, set_request_ctx_log_data
from core.logging.logger import get_logger
from core.logging.serializers import DocumentContext
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Document

logger = get_logger()
router = APIRouter()


@router.get("/v1/document/{document_id}", name="Get Document", dependencies=[Depends(authorize_request)])
def get_document(document_id: str) -> JSONResponse:
    document = operations.get_document(document_id)

    parsed_entity = parse_entity(document)
    set_request_ctx_log_data(document=DocumentContext(method="get_document", document_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved document with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)


@router.post("/v1/document", name="Create Document", dependencies=[Depends(authorize_request)])
def create_document(req_data: Document) -> JSONResponse:
    document = operations.create_document(**req_data.model_dump(by_alias=True))

    parsed_entity = parse_entity(document)
    set_request_ctx_log_data(document=DocumentContext(method="create_document", document_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_201_CREATED, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully created document with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parsed_entity)
