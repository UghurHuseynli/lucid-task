from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any, ClassVar



class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    all_cors_origins: list[str] = ['locahost']
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URI: str
    ALGORITHM: str = "HS256"
    MAX_PAYLOAD_SIZE: int = 1 * 1024 * 1024
    CACHE_TTL_SECONDS: int = 300
    POSTS_CACHE: Dict[int, Dict[str, Any]] = {}

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()