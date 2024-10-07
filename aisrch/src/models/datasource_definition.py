from azure.search.documents.indexes.models import (
    SearchIndexerDataSourceConnection,
    SearchIndexerDataContainer,
)
from config import get_settings


def get_datasource() -> SearchIndexerDataSourceConnection:
    settings = get_settings()
    datasource = SearchIndexerDataSourceConnection(
        name=settings.azure_search_datasource_name,
        type="azureblob",
        connection_string=settings.azure_storage_connection_string,
        container=SearchIndexerDataContainer(
            name=settings.azure_storage_container_name,
            query="first-grade/subjects/",
        ),
    )
    return datasource
