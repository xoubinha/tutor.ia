from pydantic import BaseModel
from uuid import UUID


class ConversationRequest(BaseModel):
    conversation_id: UUID
    prompt: str


class ConversationResponse(BaseModel):
    response: str
