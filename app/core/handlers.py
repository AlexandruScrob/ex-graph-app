from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.logging.logger import get_logger
from core.logging.context import (
    set_request_ctx_error_data_from_exception,
    set_request_ctx_http_data,
    set_request_ctx_log_data,
)
from core.exceptions import AuthorizationErrorException
from core.logging.serializers import ErrorContext
from core.responses import BadRequestResponse, EntityNotFoundResponse, AuthorizationErrorResponse
from external.neo4j.exceptions import EntityNotFoundError


logger = get_logger()


def catch_auth_exception(request: Request, exc: AuthorizationErrorException):
    """
    This is an exception handler which intercepts exceptions of type AuthorizationException and logs the stacktrace
    and actual error.

    Args:
        request => the actual request
        exc => the actual exception
    Return:
        401, UNAUTHORIZED
    """
    error_msg = AuthorizationErrorResponse(response_message=exc.detail)
    error_context = ErrorContext(message=error_msg.response_message, kind=error_msg.response_code)

    set_request_ctx_http_data(status_code=exc.status_code)
    set_request_ctx_log_data(error=error_context)
    logger.warning("Authorization fail.")
    return JSONResponse(status_code=exc.status_code, content=error_msg.model_dump(by_alias=True))


def catch_entity_not_found(request: Request, exc: EntityNotFoundError):
    """
    This is an exception handler which intercepts exceptions of type EntityNotFoundResponse and logs the stacktrace and
    actual error.

    Args:
        request => the actual request
        exc => the actual exception
    Return:
        404, NOT_FOUND
    """

    error_context = set_request_ctx_error_data_from_exception(exc)
    error_msg = EntityNotFoundResponse(response_message=error_context.message)

    set_request_ctx_http_data(status_code=status.HTTP_404_NOT_FOUND)
    set_request_ctx_log_data(error=error_context)
    logger.warning(f"{error_context.kind}. Detail: {error_context.message}")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_msg.model_dump(by_alias=True))


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

    error_msg = BadRequestResponse(response_message=first_error_msg)
    error_context = ErrorContext(stack="None", message=first_error_msg, kind=exc.errors()[0].get("type", "none"))

    set_request_ctx_http_data(status_code=status.HTTP_400_BAD_REQUEST)
    set_request_ctx_log_data(error=error_context)
    logger.error("Request Validation Error")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_msg.model_dump(by_alias=True))
