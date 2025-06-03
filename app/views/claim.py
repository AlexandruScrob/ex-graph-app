from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Claim

router = APIRouter()


@router.get("/v1/claim/{claim_id}", name="Get Claim", dependencies=[Depends(authorize_request)])
def get_claim(claim_id: str) -> JSONResponse:
    claim = operations.get_claim(claim_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(claim))


@router.post("/v1/claim", name="Create Claim", dependencies=[Depends(authorize_request)])
def create_claim(req_data: Claim) -> JSONResponse:
    claim = operations.create_claim(**req_data.model_dump(by_alias=True))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_entity(claim))
