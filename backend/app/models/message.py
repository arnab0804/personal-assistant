from sqlalchemy import Column, String, Text, ForeignKey, JSON, Enum, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base
from app.models import TimestampMixin




class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"




class Message(Base, TimestampMixin):
    __tablename__ = "messages"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    
    # For tracking message order
    sequence = Column(Integer, nullable=False)
    
    # Model used for this message - renamed to llm_model
    llm_model = Column(String(100), nullable=True)
    
    # Token usage tracking
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    
    # Metadata (tool calls, function results, etc.) - renamed to 'meta'
    meta = Column(JSON, default=dict, nullable=False)
    
    # For council mode - which agent/model contributed
    agent_name = Column(String(100), nullable=True)
    
    # Flag for messages that are part of context summary
    is_summary = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")




class MessageAttachment(Base, TimestampMixin):
    __tablename__ = "message_attachments"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    message = relationship("Message", back_populates="attachments")
    file = relationship("File", back_populates="message_attachments")