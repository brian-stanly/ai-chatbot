from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models.message import ChatMessage, ChatSession
from schemas.chat_schema import (
    ChatMessageResponse, 
    ChatSessionResponse,
    ChatSessionRequest
)

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to the Production FastAPI App"}

# retive all the messages
@router.get("v1/session/list")
def get_message(db: Session = Depends(get_db)) -> List[ChatMessageResponse]:
    return db.query(ChatMessage).all()

# api for creating sesssion
@router.post("v1/session/create")
def create_session(
    title: ChatSessionRequest,
    db: Session = Depends(get_db)) -> ChatSessionResponse:

    record = ChatSession(
        title = title.title
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# api for llm response


