from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação, lidas de variáveis de ambiente / `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Aplicação
    env: str = "development"
    debug: bool = True

    # Banco de dados
    database_url: str

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"

    # CORS — chega como string CSV no ambiente e vira list[str].
    # NoDecode evita o parse JSON automático que o pydantic-settings faria
    # em campos do tipo list, deixando o field_validator abaixo cuidar do split.
    allowed_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Retorna a instância única de Settings (lê o `.env` uma só vez)."""
    return Settings()


settings = get_settings()
