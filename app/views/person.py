from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Person

router = APIRouter()


@router.get("/v1/person/{person_id}", name="Get Person", dependencies=[Depends(authorize_request)])
def get_person(person_id: str) -> JSONResponse:
    person = operations.get_person(person_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=parse_entity(person))


@router.post("/v1/person", name="Create Person", dependencies=[Depends(authorize_request)])
def create_person(req_data: Person) -> JSONResponse:
    person = operations.create_person(**req_data.model_dump(by_alias=True))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parse_entity(person))
