from sqlalchemy import Column, String, Text, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base
from app.models import TimestampMixin




class SessionMode(str, enum.Enum):
    CHAT = "chat"
    CODE = "code"
    RESEARCH = "research"
    TRANSLATION = "translation"
    COUNCIL = "council"
    AGENT = "agent"




class Session(Base, TimestampMixin):
    __tablename__ = "sessions"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    
    title = Column(String(500), nullable=False)
    mode = Column(Enum(SessionMode), default=SessionMode.CHAT, nullable=False)
    
    # Session-specific model and prompt overrides - renamed to llm_model
    llm_model = Column(String(100), nullable=True)
    system_prompt = Column(Text, nullable=True)
    
    # Session settings (temperature, max_tokens, etc.)
    settings = Column(JSON, default=dict, nullable=False)
    
    # Context management
    context_summary = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    project = relationship("Project", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan", order_by="Message.created_at")