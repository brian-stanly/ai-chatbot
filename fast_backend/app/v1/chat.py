from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models.message import Message as ChatMessage
from schemas.chat_schema import Message
router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to the Production FastAPI App"}

@router.get("/session")
def get_message(db: Session = Depends(get_db)) -> List[Message]:
    return db.query(ChatMessage).all()
