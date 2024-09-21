from fastapi import FastAPI
from app.api.endpoints import health, conversation

app = FastAPI()

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
