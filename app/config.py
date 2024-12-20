from pydantic_settings import BaseSettings
import os

config = os.getenv

class DatabaseSettings(BaseSettings):
    pass

class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="12345")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432")
    POSTGRES_DB: str = config("POSTGRES_DB", default="postgres")
    POSTGRES_SYNC_PREFIX: str = config("POSTGRES_SYNC_PREFIX", default="postgresql://")
    POSTGRES_ASYNC_PREFIX: str = config("POSTGRES_ASYNC_PREFIX", default="postgresql+asyncpg://")
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_URL: str | None = config("POSTGRES_URL", default=None)

class Settings(
    PostgresSettings, 
):
    pass

settings = Settings()

