import logging
from dotenv import find_dotenv
from functools import lru_cache
from typing import cast

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DotEnvSupportSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(".env"), env_file_encoding="utf-8", extra="ignore")


class DB(DotEnvSupportSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")
    prefix: str
    host_name: str
    name: str

    username: str
    password: SecretStr

    @property
    def auth(self) -> tuple[str, str]:
        return self.username, self.password.get_secret_value()


class Settings(DotEnvSupportSettings):
    ###
    # Convenience toggle for development purposes, such as:
    # - logging to terminal
    # - loading .env files outside of pydantic BaseSettings classes
    ###
    dev_mode: bool = False

    ###
    # Structlog renderer to use when developing and running locally
    ###
    dev_renderer: str = "devtools"

    app_log_level: str = "info"

    ###
    # Redaction settings
    # - redacted when logging level is greater than DEBUG
    ###
    # attributes to redact when logging
    attributes_to_redact: set[str] = set()
    # headers to redact when logging
    headers_to_redact: set[str] = set()
    # value to use when redacting info
    redacted_value: str = "***redacted***"

    auth_username: str
    auth_password: SecretStr

    db_settings: DB = DB()

    @property
    def logging_level(self) -> int:
        """Gets the logging level number configured using the app_log_level setting."""
        try:
            return cast(int, getattr(logging, self.app_log_level.upper()))
        except AttributeError:
            return logging.INFO


@lru_cache
def get_settings() -> Settings:
    return Settings()
