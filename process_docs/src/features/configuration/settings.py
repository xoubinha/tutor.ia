from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    docintelligence_api_endpoint: str
    docintelligence_api_key: str
    storage_account_name: str
    storage_account_container: str
    storage_account_connection_string: str
    model_config = SettingsConfigDict(env_file="../.env")


@lru_cache
def get_app_settings() -> Settings:
    return Settings()
