from azure.search.documents.indexes import SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from config import get_settings


def get_indexer_client():
    settings = get_settings()
    credential = AzureKeyCredential(settings.azure_search_admin_key)
    client = SearchIndexerClient(
        endpoint=settings.azure_search_endpoint, credential=credential
    )
    return client
