import os
from enum import Enum, auto

from pydantic_settings import BaseSettings, SettingsConfigDict

file_name = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(file_name))


class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class EnvMode(StrEnum):
    PROD = auto()
    TEST = auto()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    PROJECT_NAME: str = "UGC2_Service"
    BASE_DIR: str = base_dir
    ENV: str = EnvMode.PROD
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    MONGO_HOST: str = "mongos1"
    MONGO_PORT: int = 27019
    MONGO_DB: str = "ugc2_movies"
    AUTH_SERVICE_URL: str = ""


settings = Settings()
