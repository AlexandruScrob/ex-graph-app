from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.auth import AuthorizationErrorException
from core.responses import BadRequestResponse, EntityNotFoundResponse, AuthorizationErrorResponse
from external.neo4j.exceptions import EntityNotFoundError


def catch_auth_exception(request: Request, exc: AuthorizationErrorException):
    """
    This is an exception handler which intercepts exceptions of type AuthorizationErrorException
    """

    return JSONResponse(
        status_code=exc.status_code,
        content=AuthorizationErrorResponse().model_dump(by_alias=True),
    )


def catch_entity_not_found(request: Request, exc: EntityNotFoundError):
    """
    This is an exception handler which intercepts exceptions of type AuthorizationErrorException
    """

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=EntityNotFoundResponse().model_dump(by_alias=True),
    )


def catch_request_validation_exception(request: Request, exc: RequestValidationError):
    """
    This is an exception handler which intercepts exceptions of type RequestValidationError. These errors occur
    when the request body could not be validated against pydantic models to output a general error in all cases

    Args:
        request => the actual request
        exc => the actual exception
    Return:
        400, BAD_REQUEST
    """
    first_error = exc.errors()[0]
    first_error_msg = f"Invalid request ({first_error.get('loc', 'base')}): {first_error.get('msg', 'none')}"

    error_msg = BadRequestResponse(responseMessage=first_error_msg)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_msg.model_dump(by_alias=True),
    )
