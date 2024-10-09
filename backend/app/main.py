from fastapi import FastAPI
from api.endpoints import health, conversation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
     "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
