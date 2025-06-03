from fastapi.testclient import TestClient
import pytest

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
