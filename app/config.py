from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    database_url: str = "sqlite:///./data/pocketsmart.db"
    app_name: str = "PocketSmart AI"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
@lru_cache
def get_settings() -> Settings: return Settings()
