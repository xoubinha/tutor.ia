import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from fastapi import APIRouter
from openai import AzureOpenAI
from uuid import UUID
from schemas.conversation import ConversationRequest, ConversationResponse

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

conversation_memory = {}

system_prompt = "You are a helpful assistant."


def init_conversation_memory(
    system_prompt: str, conversation_id: UUID, conversation_memory: dict
):
    memory = [{"role": "system", "content": system_prompt}]
    conversation_memory[conversation_id] = memory
    return memory


def get_conversation_memory(conversation_id: UUID, conversation_memory: dict = None):
    if conversation_id in conversation_memory:
        return conversation_memory[conversation_id]
    else:
        return []


def update_conversation_memory(
    conversation_id: UUID, message: dict, conversation_memory: dict
) -> None:
    conversation_memory[conversation_id].append(message)


def reformulate_query(query: str, memory: dict) -> str:
    previous_context = "\n".join(
        [
            f'{message["role"]}: {message["content"]}'
            for message in memory
            if message["role"] == "user"
        ]
    )
    REFORMULATE_PROMPT = """
    You are assisting a user in finding information in Azure AI Search.
    The context from the conversation so far is the following: 

    {previous_context}

    Based on this context, reformulate the following question to optimize it for document search, 
    making it more specific, clearer, and focused on retrieving the most relevant information:

    Original Question: '{query}'
    
    Your reformulated query should capture the most relevant words and be concise to be effective
    as search query for Azure AI Search Index. Avoid using punctuation or special characters.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": REFORMULATE_PROMPT.format(
                    query=query, previous_context=previous_context
                ).strip(),
            }
        ],
    )
    reformulated_query = response.choices[0].message.content
    return reformulated_query


@router.post("", response_model=ConversationResponse)
def handle_conversation(request: ConversationRequest):

    if request.conversation_id not in conversation_memory:
        init_conversation_memory(
            system_prompt, request.conversation_id, conversation_memory
        )
    messages = get_conversation_memory(request.conversation_id, conversation_memory)
    user_message = {"role": "user", "content": request.prompt}
    messages += [user_message]

    reformulated_query = reformulate_query(request.prompt, messages)
    print(f"Reformulated query: {reformulated_query}")

    search_results = search_client.search(search_text=reformulated_query, top=3)

    GROUNDED_PROMPT = """
    You are a teaching assistant that anwers questions using the information provided in the sources.
    Answer the query using only the sources provided below in a friendly and concise manner.
    Answer ONLY with the information listed in the list of sources below.
    If there isn't enough information below, say you don't know.
    Do not generate answers that don't use the sources below.
    Query: {query}
    Sources:\n{sources}

    At the end of each answer, include the storage_url field in markdown format, followed by the page number in the format #page=<page field + 2>. For example:
    [url](storage_url#page=<page field>)
    """
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": GROUNDED_PROMPT.format(
                    query=request.prompt,
                    sources=[result for result in search_results],
                ),
            }
        ],
    )
    completion_text = completion.choices[0].message.content
    print(f"Completion text: {completion_text}")
    return ConversationResponse(response=completion_text)
