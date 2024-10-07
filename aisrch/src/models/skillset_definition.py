# src/models/skillset_definition.py
from azure.search.documents.indexes.models import (
    SearchIndexerSkillset,
    AzureOpenAIEmbeddingSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
)
from config import get_settings


def get_skillset() -> SearchIndexerSkillset:
    settings = get_settings()

    embedding_skill = AzureOpenAIEmbeddingSkill(
        name="EmbeddingSkill",
        description="Skill to generate embeddings via Azure OpenAI",
        context="/document",
        resource_url=settings.openai_resource_uri,
        deployment_name=settings.openai_embeddings_deployment_id,
        api_key=settings.openai_api_key,
        model_name=settings.openai_embeddings_model_name,
        inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
        outputs=[OutputFieldMappingEntry(name="embedding", target_name="embeddings")],
    )

    skillset = SearchIndexerSkillset(
        name=settings.azure_search_skillset_name,
        description="Document processing",
        skills=[embedding_skill],
    )
    return skillset
