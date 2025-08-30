from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    LOG_LEVEL: str = "INFO"


settings = Settings()
