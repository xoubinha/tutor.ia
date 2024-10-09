import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv
from fastapi import APIRouter
from openai import AzureOpenAI
from schemas.conversation import ConversationRequest, ConversationResponse
from api.utils.prompts import (
    CONDENSE_SYSTEM_PROMPT,
    CONDENSE_USER_PROMPT,
    ANSWERING_SYSTEM_PROMPT,
    ANSWERING_USER_PROMPT,
)
from api.utils import get_subject

router = APIRouter()

load_dotenv("../.env")

openai_client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY")),
)


class ChatHistory:
    def __init__(self):
        self.conversations: dict = {}

    def get_conversation(self, conversation_id: any) -> list:
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]
        else:
            return []

    def delete_conversation(self, conversation_id: any):
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]

    def delete_all_conversations(self):
        self.conversations = {}

    def update_conversation(self, conversation_id: any, messages: list[dict]):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id] += messages


chat_history = ChatHistory()

@router.post("", response_model=ConversationResponse)
def handle_conversation(request: ConversationRequest):
    subject = get_subject(request.prompt)
    conversation = chat_history.get_conversation(request.conversation_id)
    condense_completion = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_MODEL"],
        messages=[
            {"role": "system", "content": CONDENSE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": CONDENSE_USER_PROMPT.format(
                    question=request.prompt,
                    chat_history="\n".join(
                        [
                            f"{message['role']}: {message['content']}"
                            for message in conversation
                        ]
                    ),
                ).strip(),
            },
        ],
    )

    query = condense_completion.choices[0].message.content
    print(f"Reformulated query: {query}")

    query_embedding = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-large",
    )

    search_results = search_client.search(
        search_text=query,
        vector_queries=[
            VectorizedQuery(
                vector=query_embedding.data[0].embedding,
                exhaustive=False,
                k_nearest_neighbors=5,
                fields="embeddings",
            )
        ],
        filter = f"subject eq '{subject}'" if subject else None,
        top=5,
    )
    messages = [
        {
            "role": "system",
            "content": ANSWERING_SYSTEM_PROMPT,
        },
    ]
    for message in chat_history.get_conversation(request.conversation_id):
        messages.append({"role": message["role"], "content": message["content"]})
    messages.append(
        {
            "role": "user",
            "content": ANSWERING_USER_PROMPT.format(
                sources=[source for source in search_results],
                question=request.prompt,
            ),
        }
    )
    answer_completion = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_MODEL"], messages=messages
    )
    answer_text = answer_completion.choices[0].message.content

    chat_history.update_conversation(
        request.conversation_id,
        [
            {"role": "user", "content": request.prompt},
            {"role": "assistant", "content": answer_text},
        ],
    )
    print(f"Answer: {answer_text}")
    return ConversationResponse(response=answer_text)
