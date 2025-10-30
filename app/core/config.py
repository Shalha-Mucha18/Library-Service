from functools import lru_cache
from typing import Optional

from pydantic import Field, FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    PROJECT_NAME: str = "Library Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./library.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_PREFIX: str = "library-cache"
    CACHE_DEFAULT_EXPIRE_SECONDS: int = 300
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None)
    ENVIRONMENT: str = Field(default="development")

    @field_validator("CELERY_RESULT_BACKEND", mode="before")
    @classmethod
    def default_celery_backend(cls, value: Optional[str], info: FieldValidationInfo) -> Optional[str]:
        """Reuse Redis broker for results if explicit backend is absent."""
        if value:
            return value
        return info.data.get("CELERY_BROKER_URL")


@lru_cache
def get_settings() -> Settings:
    """Return memoized settings instance."""
    return Settings()


settings = get_settings()
