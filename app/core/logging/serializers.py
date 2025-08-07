from typing import Any, Callable, Type

import requests
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class HttpContext(BaseModel):
    ident: str | None = None
    method: str | None = None
    query_params: dict[str, Any] | None = None
    request_body: str | None = None
    request_id: int | None = None
    response_body: str | None = None
    status_code: int = status.HTTP_200_OK
    url: str | None = None


class ErrorContext(BaseModel):
    kind: str  # error type
    message: str  # error message from the stack trace
    stack: str | None = None


class LoggerContext(BaseModel):
    name: str = "structlog"
    thread_name: str = "bind_contextvars"


class PersonContext(BaseModel):
    person_id: str | None = None
    method: str = "UNDEFINED"


class CompanyContext(BaseModel):
    company_id: str | None = None
    method: str = "UNDEFINED"


class ClaimContext(BaseModel):
    claim_id: str | None = None
    method: str = "UNDEFINED"


class DocumentContext(BaseModel):
    document_id: str | None = None
    method: str = "UNDEFINED"


class LogContext(BaseModel):
    application_settings: dict[str, Any] = Field(default_factory=dict)
    duration: int = 0
    ext_duration: int = 0
    int_duration: int = 0
    error: ErrorContext | None = None
    http: HttpContext | None = None
    logger: LoggerContext = Field(default_factory=LoggerContext)
    person: PersonContext | None = None
    company: CompanyContext | None = None
    claim: ClaimContext | None = None
    document: DocumentContext | None = None


class RequestContext(BaseModel):
    error_handlers: dict[Type[Exception], Callable[[requests.Request, Exception], JSONResponse]] = Field(
        default_factory=dict
    )
    log: LogContext = Field(default_factory=LogContext)
    request_time_start: int | None = None
    request_body_json_raw: dict[str, Any] | None = None
