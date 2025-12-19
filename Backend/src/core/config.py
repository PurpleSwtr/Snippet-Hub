from pathlib import Path
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisDB(BaseModel):
    cache: int = 0

class RedisConfig(BaseModel):
    host: str = Field(default="localhost", validation_alias="REDIS_HOST")
    port: int = Field(default=6379, validation_alias="REDIS_PORT")
    TTL: int = Field(default=120, validation_alias="CACHE_TTL")
    db: RedisDB = RedisDB()

class CacheNamespace(BaseModel):
    icons_list: str = "icons-list"
    options_list: str = "options-list"

class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()

class Settings(BaseSettings):
    app_name: str = "LLM Manager"
    
    BASE_DIR: Path = Path(__file__).resolve().parents[2]

    FRONT_STATIC_DIR: Path = Path(__file__).resolve().parents[3] / "Frontend" / "public" / "icons"


    redis: RedisConfig = Field(default_factory=RedisConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

settings = Settings()