from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    ScoringProfile,
    TextWeights,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    HnswParameters,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    BM25SimilarityAlgorithm,
)

from config import get_settings


def get_index_schema() -> SearchIndex:
    settings = get_settings()
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            searchable=False,
            filterable=False,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SimpleField(
            name="subject",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=True,
            retrievable=False,
            sortable=False,
            facetable=False,
        ),
        SimpleField(
            name="type",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=True,
            retrievable=False,
            sortable=False,
            facetable=False,
        ),
        SimpleField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=True,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SimpleField(
            name="chapter",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=True,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SearchableField(
            name="section",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SimpleField(
            name="page",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=True,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=False,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SimpleField(
            name="storage_url",
            type=SearchFieldDataType.String,
            searchable=False,
            filterable=False,
            retrievable=True,
            sortable=False,
            facetable=False,
        ),
        SearchField(
            name="embeddings",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=3072,
            vector_search_profile_name="vector-search",
        ),
    ]

    scoring_profiles = [
        ScoringProfile(
            name="default-profile",
            function_aggregation="average",
            text_weights=TextWeights(weights={"section": 0.3, "content": 1}),
        )
    ]

    semantic_configurations = [
        SemanticConfiguration(
            name="semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="title"),
                content_fields=[SemanticField(field_name="content")],
                keywords_fields=[SemanticField(field_name="section")],
            ),
        )
    ]

    similarity = BM25SimilarityAlgorithm()

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw",
                kind="hnsw",
                hnsw_parameters=HnswParameters(
                    metric="cosine", m=4, ef_construction=400, ef_search=500
                ),
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-search",
                algorithm_configuration_name="hnsw",
                vectorizer_name="vectorizer-query",
            )
        ],
        vectorizers=[
            AzureOpenAIVectorizer(
                vectorizer_name="vectorizer-query",
                kind="azureOpenAI",
                parameters=AzureOpenAIVectorizerParameters(
                    resource_url=settings.openai_resource_uri,
                    api_key=settings.openai_api_key,
                    deployment_name=settings.openai_embeddings_deployment_id,
                    model_name=settings.openai_embeddings_model_name,
                ),
            )
        ],
    )

    index = SearchIndex(
        name=settings.azure_search_index_name,
        fields=fields,
        scoring_profiles=scoring_profiles,
        similarity=similarity,
        semantic_settings=semantic_configurations,
        vector_search=vector_search,
    )
    return index
