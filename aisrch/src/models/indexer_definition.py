from azure.search.documents.indexes.models import (
    SearchIndexer,
)


def get_indexer_schema():
    indexer = SearchIndexer(
        name="psychology-idxr",
        data_source_name="psychology-ds",
        target_index_name="psychology-idx",
        skillset_name="psychology-skillset",
        parameters={
            "configuration": {
                "indexedFileNameExtensions": ".json",
                "dataToExtract": "contentAndMetadata",
                "parsingMode": "default",
                "imageAction": "generateNormalizedImages",
            }
        },
    )
    return indexer
