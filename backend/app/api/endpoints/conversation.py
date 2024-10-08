import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from fastapi import APIRouter
from openai import AzureOpenAI
from uuid import UUID
from schemas.conversation import ConversationRequest, ConversationResponse
from api.utils.prompts import (
    CONDENSE_SYSTEM_PROMPT,
    CONDENSE_USER_PROMPT,
    ANSWERING_SYSTEM_PROMPT,
    ANSWERING_USER_PROMPT,
)

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
    # Reformulate the question based on the conversation history
    conversation = chat_history.get_conversation(request.conversation_id)
    condense_completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
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

    search_results = search_client.search(search_text=query, top=3)

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
        model="gpt-4o-mini", messages=messages
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
