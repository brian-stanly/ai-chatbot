from pydantic import BaseModel
import uuid
from datetime import datetime

class ChatSessionResponse(BaseModel):
    session_id: uuid.UUID
    title: str
    created_at: datetime

class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime
    session_id: uuid.UUID

class ChatSessionRequest(BaseModel):
    title: str