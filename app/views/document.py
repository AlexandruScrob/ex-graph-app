from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Document

router = APIRouter()


@router.get("/v1/document/{document_id}", name="Get Document", dependencies=[Depends(authorize_request)])
def get_document(document_id: str) -> JSONResponse:
    document = operations.get_document(document_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(document))


@router.post("/v1/document", name="Create Document", dependencies=[Depends(authorize_request)])
def create_document(req_data: Document) -> JSONResponse:
    document = operations.create_document(**req_data.model_dump(by_alias=True))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_entity(document))
