import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models.message import ChatMessage, ChatSession
from schemas.chat_schema import ( 
    ChatSessionResponse,
    ChatSessionRequest,
    ChatLLMRequest,
    ChatMessageResponse
)

router = APIRouter()


# get all the sessions
@router.get("/v1/session/list/")
def get_message(db: Session = Depends(get_db)) -> List[ChatSessionResponse]:
    return db.query(ChatSession).order_by(ChatSession.created_at).all() 

# create a new session
@router.post("/v1/session/create/")
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


# get chat history
@router.get("/v1/session/{session_id}/")
def get_chathistory(
    session_id: uuid.UUID,
    db: Session = Depends(get_db)
    ) -> List[ChatMessageResponse]:
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()


@router.post("/v1/session/{session_id}/")
def llm_respose(payload: ChatLLMRequest,db: Session = Depends(get_db)) -> List[ChatMessageResponse]:

    chat_session = db.get(ChatSession, payload.session_id)

    if chat_session is None:
        HTTPException(
            status_code=404,
            detail="Session not found"
        )

    user_data = ChatMessage(
        session_id=chat_session.session_id,
        role="user",
        content=payload.message
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return db.query(ChatMessage).filter(ChatMessage.session_id == chat_session.session_id).order_by(ChatMessage.created_at).all()






