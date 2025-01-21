import uuid

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.test", env_ignore_empty=True, extra="ignore"
    )
    AUTH_SERVICE_URL: str = "http://localhost:80"
    UGC2_SERVICE_URL: str = "http://localhost:82"
    EXAMPLE_FILM_ID: str = str(uuid.uuid4())


settings = Settings()
