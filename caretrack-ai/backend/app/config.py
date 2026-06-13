from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://caretrack:caretrack@localhost:5432/caretrack_db"
    app_name: str = "CareTrack AI"
    debug: bool = False
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:80"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
