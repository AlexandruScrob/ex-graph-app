from dotenv import find_dotenv
from functools import lru_cache
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
    auth_username: str
    auth_password: SecretStr

    db_settings: DB = DB()


@lru_cache
def get_settings() -> Settings:
    return Settings()
