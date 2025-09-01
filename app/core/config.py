from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"

    LOKI_URL: str
    LOKI_TOKEN: str

    SENTRY_DSN: Optional[str] = None

    LOKI_USER_ID: str

    PROJECT_NAME: str
    API_V1_STR: str
    LOG_LEVEL: str
    ALL_CORS_ORIGINS: Optional[List[str]]  # aceita lista de strings

    class Config:
        env_file = ".env"
        case_sensitive = True  # mantém case sensitive


settings = Settings()
