import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base

class Converstaion(Base):
    __tablename__ = "converstaions"

    id = Column(String, primary_key=True, index=True) #UUID
    title = Column(String, default="New Converstion")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    messages = relationship("Message", back_populates="converstions", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    converstion_id = Column(String, ForeignKey("converstations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=True) # user or assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    conversation = relationship("Converstaion", back_populates="messages")