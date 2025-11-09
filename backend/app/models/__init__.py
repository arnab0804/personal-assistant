from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func




class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)




# Import all models AFTER defining TimestampMixin
from app.models.user import User
from app.models.project import Project
from app.models.session import Session, SessionMode
from app.models.message import Message, MessageRole, MessageAttachment
from app.models.file import File, FileType, FileProcessingStatus
from app.models.vector_store import VectorStore, VectorChunk




__all__ = [
    "TimestampMixin",
    "User",
    "Project",
    "Session",
    "SessionMode",
    "Message",
    "MessageRole",
    "MessageAttachment",
    "File",
    "FileType",
    "FileProcessingStatus",
    "VectorStore",
    "VectorChunk",
]