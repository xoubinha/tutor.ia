from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from config import get_settings


def get_search_client():
    settings = get_settings()
    credential = AzureKeyCredential(settings.azure_search_admin_key)
    client = SearchIndexClient(
        endpoint=settings.azure_search_endpoint, credential=credential
    )
    return client
