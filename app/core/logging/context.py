from contextlib import contextmanager
from contextvars import ContextVar

from core.logging.serializers import RequestContext, ErrorContext, HttpContext
from core.settings import Settings

request_var: ContextVar[RequestContext] = ContextVar("request", default=Ellipsis)  # type: ignore


def get_request_context() -> RequestContext:
    if request_var.get() is Ellipsis:
        request_var.set(RequestContext())

    return request_var.get()


@contextmanager
def get_temporary_log_context(*, create_new_context: bool = False):
    token = None
    if create_new_context or request_var.get() is Ellipsis:
        token = request_var.set(RequestContext())

    yield request_var.get()

    if token:
        request_var.reset(token)


def set_request_ctx_data(**kwargs):
    request_ctx = get_request_context()
    for field, value in kwargs.items():
        setattr(request_ctx, field, value)


def set_request_ctx_log_data(**kwargs):
    request_ctx = get_request_context()
    for field, value in kwargs.items():
        setattr(request_ctx.log, field, value)


def set_request_ctx_http_data(**kwargs):
    request_ctx = get_request_context()
    if request_ctx.log.http is None:
        request_ctx.log.http = HttpContext()
    for field, value in kwargs.items():
        setattr(request_ctx.log.http, field, value)


def set_request_ctx_error_data_from_exception(exc: Exception) -> ErrorContext:
    error_type = exc.__class__.__name__
    error_ctx = ErrorContext(message=str(exc), kind=error_type)

    set_request_ctx_log_data(error=error_ctx)

    return error_ctx


def set_request_ctx_application_settings(settings: Settings):
    request_ctx = get_request_context()
    request_ctx.log.application_settings = settings.dict()
