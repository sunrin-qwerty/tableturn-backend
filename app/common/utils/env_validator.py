from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

__all__ = ["settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    APP_ENV: Literal["development", "production", "testing"]
    SERVER_PORT: int
    DATABASE_URI: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    JWT_SECRET_KEY: str

    @staticmethod
    @field_validator("SERVER_PORT")
    def check_port_range(value: int):
        if not 0 < value < 65536:
            raise ValueError("SERVER_PORT number must be between 1 and 65535")
        return value


settings = Settings()  # type: ignore
