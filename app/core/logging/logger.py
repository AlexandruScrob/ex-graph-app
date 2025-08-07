import time
from typing import Any

import structlog
from pydantic.json import pydantic_encoder

from core.logging.context import request_var, set_request_ctx_log_data
from core.logging.serializers import RequestContext
from core.settings import get_settings

settings = get_settings()

if settings.dev_mode:
    from core.logging.renderers import PrettyFormatRenderer


def set_duration(logger, log_method, event_dict):
    request_ctx = request_var.get()

    if request_ctx is not Ellipsis and not request_ctx.log.duration and request_ctx.request_time_start:
        duration = time.time_ns() - request_ctx.request_time_start
        int_duration = duration - request_ctx.log.ext_duration

        set_request_ctx_log_data(duration=duration, int_duration=int_duration)

    return event_dict


def bind_context_from_request_var(logger, log_method, event_dict):
    """Bind the data from the `request.log` context var into the structlog `event_dict`. This enables the use of the
    `pydantic_encoder` JSON encoder in the `JSONRenderer` processor without losing the ability to use the camel case
    aliases.
    """
    request_ctx: RequestContext = request_var.get()

    if request_ctx is Ellipsis:
        return event_dict

    bind_data = request_ctx.log.dict(by_alias=True, exclude_none=True)

    event_dict.update(bind_data)

    return event_dict


def set_elapsed_time(logger, log_method, event_dict):
    time_now = time.time_ns()
    time_start = event_dict.get("start_time")
    if time_start:
        event_dict["response_time_took"] = time_now - time_start
        return event_dict
    return event_dict


# Rename default keys to meet standards
def rename_default_keys(logger, log_method, event_dict):
    event_dict["message"] = event_dict.pop("event", None)
    event_dict.pop("view", None)
    return event_dict


def configure_logger():
    structlog.configure(
        processors=_get_structlog_processors(),
        wrapper_class=structlog.make_filtering_bound_logger(settings.logging_level),  # pylint: disable=no-member
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def _get_structlog_processors() -> list[Any]:
    """Define the processors for structlog.

    NB: the order of the processors matters!
    """
    processors: list[Any] = [
        set_duration,
        bind_context_from_request_var,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        rename_default_keys,
        set_elapsed_time,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.dev_mode:
        ###
        # This section aims to display the logs in a more readable way when running locally by using custom renderers.
        # If no custom renderers are used, it will fall back to the JSONRenderer with indentation and sorted keys.
        ###
        renderer_map = {"devtools": PrettyFormatRenderer()}
        processors.append(
            renderer_map.get(
                settings.dev_renderer,
                structlog.processors.JSONRenderer(default=pydantic_encoder, indent=2, sort_keys=True),
            )
        )
    else:
        processors.append(structlog.processors.JSONRenderer(default=pydantic_encoder))

    return processors


def get_logger() -> structlog.types.FilteringBoundLogger:
    if not structlog.is_configured():
        configure_logger()

    return structlog.get_logger()
