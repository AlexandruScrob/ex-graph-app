import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.auth import authorize_request
from core.logging.context import set_request_ctx_http_data, set_request_ctx_log_data
from core.logging.logger import get_logger
from core.logging.serializers import PersonContext
from external.neo4j import operations
from views.helpers import parse_entity
from views.serializers import Person

logger = get_logger()
router = APIRouter()


@router.get("/v1/person/{person_id}", name="Get Person", dependencies=[Depends(authorize_request)])
def get_person(person_id: str) -> JSONResponse:
    person = operations.get_person(person_id)

    parsed_entity = parse_entity(person)
    set_request_ctx_log_data(person=PersonContext(method="get_person", person_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_200_OK, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully retrieved person with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_entity)


@router.post("/v1/person", name="Create Person", dependencies=[Depends(authorize_request)])
def create_person(req_data: Person) -> JSONResponse:
    person = operations.create_person(**req_data.model_dump(by_alias=True))

    parsed_entity = parse_entity(person)
    set_request_ctx_log_data(person=PersonContext(method="create_person", person_id=parsed_entity.get("pid")))
    set_request_ctx_http_data(status_code=status.HTTP_201_CREATED, response_body=json.dumps(parsed_entity))

    logger.info(f"Successfully created person with ID: {parsed_entity.get('pid')}")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=parsed_entity)
