import pytest

from fastapi.security import HTTPBasicCredentials

from core.auth import authorize_request
from core.settings import Settings
from core.exceptions import AuthorizationErrorException


@pytest.mark.asyncio
async def test_core_auth_success(settings: Settings):
    await authorize_request(
        credentials=HTTPBasicCredentials(
            username=settings.auth_username,
            password=settings.auth_password.get_secret_value(),
        )
    )


@pytest.mark.asyncio
async def test_check_header_failed():
    with pytest.raises(AuthorizationErrorException):
        await authorize_request(
            credentials=HTTPBasicCredentials(
                username="bad_user",
                password="test_pass",
            )
        )

    with pytest.raises(AuthorizationErrorException):
        await authorize_request(
            credentials=HTTPBasicCredentials(
                username="test_user",
                password="bad_pass",
            )
        )
