from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from app.database import Base
from app.models import TimestampMixin




class Project(Base, TimestampMixin):
    __tablename__ = "projects"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Tags/Symbols for organization
    tags = Column(ARRAY(String), default=list, nullable=False)
    
    # Project-level settings
    settings = Column(JSON, default=dict, nullable=False)
    
    # Default model and system prompt for this project - renamed to default_llm_model
    default_llm_model = Column(String(100), nullable=True)
    default_system_prompt = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    sessions = relationship("Session", back_populates="project", cascade="all, delete-orphan")
    vector_stores = relationship("VectorStore", back_populates="project", cascade="all, delete-orphan")