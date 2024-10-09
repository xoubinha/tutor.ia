from azure.search.documents.indexes.models import (
    SearchIndexer,
    FieldMapping
)

from config import get_settings

def get_indexer_schema():
    settings = get_settings()
    indexer = SearchIndexer(
        name=settings.azure_search_indexer_name,
        data_source_name=settings.azure_search_datasource_name,
        target_index_name=settings.azure_search_index_name,
        skillset_name=settings.azure_search_skillset_name,
        parameters={
            "configuration": {
                "indexedFileNameExtensions": ".json",
                "dataToExtract": "contentAndMetadata",
                "parsingMode": "json",
                "excluded_file_name_extensions": ".pdf, .docx",
            }
        },
        output_field_mappings=[
            FieldMapping(
                    source_field_name="/document/embeddings",
                    target_field_name="embeddings",
                )
        ]
    )
    return indexer
