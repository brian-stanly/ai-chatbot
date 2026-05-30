from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from db.database import Base

class Message(Base):
    __tablename__ = "chat_message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_session.session_id", ondelete="CASCADE"),
        nullable=False,
    )
    session = relationship(
        "Session",
        back_populates="messages",
    )

class Session(Base):
    __tablename__ = "chat_session"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String, default="New Conversation", nullable=False)
    create_at = Column(DateTime, server_default=func.now(), nullable=False)
    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan"
    )
