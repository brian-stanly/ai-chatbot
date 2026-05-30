from fastapi import FastAPI

from app.v1 import chat
from db.database import SessionLocal

app = FastAPI(title="Production FastAPI App")

app.include_router(chat.router, prefix="/api", tags=["Chat"])