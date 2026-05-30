from pydantic import BaseModel
import uuid
from datetime import datetime

class Session(BaseModel):
    session_id: uuid.UUID
    title: str
    created_at: datetime

class Message(BaseModel):
    role: str
    content: str
    created_at: datetime
    session_id: uuid.UUID