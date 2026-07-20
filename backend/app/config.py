from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_user: str = "assessment"
    db_password: str = "assessment"
    db_name: str = "assessment"
    db_host: str = "db"
    db_port: int = 5432

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Em dev, "*" é aceitável. Em produção, defina no .env como a URL
    # pública exata do frontend (ex: https://assessment.suaempresa.com)
    # — nunca deixe "*" com allow_credentials=True em produção.
    cors_origins: str = "*"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
