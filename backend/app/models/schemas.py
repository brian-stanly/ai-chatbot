import datetime
from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    reply: str


class ChatInput(BaseModel):
    content: str

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Converstion"

class ConversationTitleUpdate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True