from functools import lru_cache

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Quran Oetrat API"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "quran_oetrat"
    POSTGRES_PASSWORD: str = "quran_oetrat"
    POSTGRES_DB: str = "quran_oetrat"
    DATABASE_URL: str | None = None

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str] | str:
        if isinstance(value, str) and value:
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def database_uri(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def is_development(self) -> bool:
        return self.APP_ENV.lower() in {"dev", "development", "local"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()