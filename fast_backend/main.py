from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.v1 import chat

app = FastAPI(title="Production FastAPI App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])