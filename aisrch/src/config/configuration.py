from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_search_endpoint: str
    azure_search_admin_key: str
    azure_search_index_name: str
    azure_search_indexer_name: str
    azure_search_datasource_name: str
    azure_search_skillset_name: str
    azure_storage_connection_string: str
    azure_storage_container_name: str
    azure_cognitive_services_key: str
    openai_api_key: str
    openai_embeddings_deployment_id: str
    openai_embeddings_model_name: str
    openai_resource_uri: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
