import secrets

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.exceptions import AuthorizationErrorException
from core.settings import get_settings

security = HTTPBasic()
settings = get_settings()


async def authorize_request(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    correct_username = secrets.compare_digest(credentials.username, settings.auth_username)
    correct_password = secrets.compare_digest(credentials.password, settings.auth_password.get_secret_value())

    if not (correct_username and correct_password):
        raise AuthorizationErrorException
