import logging
import pytest
import structlog

from fastapi.testclient import TestClient

from core.logging.context import get_temporary_log_context
from core.settings import get_settings

from main import app


@pytest.fixture(scope="module")
def settings():
    yield get_settings().model_copy(deep=True)


@pytest.fixture(scope="module")
def client_with_auth():
    client = TestClient(app)
    client.auth = (
        get_settings().auth_username,
        get_settings().auth_password.get_secret_value(),
    )
    yield client


@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


@pytest.fixture(scope="function")
def mocked_log_context():
    with get_temporary_log_context(create_new_context=True) as log_ctx:
        yield log_ctx


@pytest.fixture(name="log_output")
def fixture_log_output():
    """Configure structlog for testing: https://www.structlog.org/en/stable/testing.html"""
    return structlog.testing.LogCapture()


@pytest.fixture(autouse=True)
def configure_structlog(log_output):
    """
    Configure structlog for testing by adjusting the processors.

    The last configured processor (the rendered) is replaced with a print processor and the LogCapture class to enable
    easy unit testing.

    https://www.structlog.org/en/stable/testing.html
    """
    original_config = structlog.get_config()
    original_processors = original_config.get("processors", [])
    new_processors = [*original_processors[:-1], _print_log_processor, log_output]
    structlog.configure(**{**original_config, "processors": new_processors})


def _print_log_processor(logger, method_name, event_dict):
    """Structlog processor which prints the `event_dict` when the `app_log_level` is `DEBUG`."""
    if get_settings().logging_level == logging.DEBUG:
        print(event_dict)  # noqa:WPS421

    return event_dict
