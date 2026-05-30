import uuid
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.llm_service import get_llm_response
from db.database import get_db
from models.message import ChatMessage, ChatSession
from schemas.chat_schema import ( 
    ChatSessionResponse,
    ChatSessionRequest,
    ChatMessageResponse,
    ChatLLMRequest,
    ChatLLMResponse
)

router = APIRouter()

# get all the sessions
@router.get("/session/list/")
def get_message(db: Session = Depends(get_db)) -> List[ChatSessionResponse]:
    return db.query(ChatSession).order_by(ChatSession.created_at).all() 

# create a new session
@router.post("/session/create/")
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
@router.get("/session/{session_id}/")
def get_chathistory(
    session_id: uuid.UUID,
    db: Session = Depends(get_db)
    ) -> List[ChatMessageResponse]:
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()

@router.post("/session/{session_id}/")
def llm_respose(
    session_id: uuid.UUID,
    message: ChatLLMRequest,
    db: Session = Depends(get_db)) -> ChatLLMResponse:

    chat_session = db.get(ChatSession, session_id)

    if chat_session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    user_data = ChatMessage(
        session_id=session_id,
        role="user",
        content=message.message
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    chat_history = db.query(ChatMessage).filter(ChatMessage.session_id == chat_session.session_id).order_by(ChatMessage.created_at).all()

    response = get_llm_response(chat_history)

    ai_data = ChatMessage(
        session_id=chat_session.session_id,
        role="assistant",
        content=response
    )

    db.add(ai_data)
    db.commit()
    db.refresh(ai_data)

    return {"reply": response}

@router.delete("/session/{session_id}/")
def delete_session_chathistory(
    session_id: uuid.UUID,
    db: Session = Depends(get_db)
    ) -> Dict[str, str]:

    session = db.get(ChatSession, session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    db.delete(session)
    db.commit()

    return {"message": "Session deleted successfully"}
