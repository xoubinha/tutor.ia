from fastapi import APIRouter
from app.schemas.conversation import ConversationRequest, ConversationResponse

router = APIRouter()


@router.post("/", response_model=ConversationResponse)
def handle_conversation(request: ConversationRequest):
    response_text = f"Received prompt: {request.prompt} with conversation ID: {request.conversation_id}"
    return ConversationResponse(response=response_text)
