from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base
from app.models import TimestampMixin




class FileType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    CODE = "code"
    SPREADSHEET = "spreadsheet"
    OTHER = "other"




class FileProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"




class File(Base, TimestampMixin):
    __tablename__ = "files"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    
    file_type = Column(Enum(FileType), nullable=False)
    mime_type = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    
    # Processing status (for transcription, OCR, etc.)
    processing_status = Column(Enum(FileProcessingStatus), default=FileProcessingStatus.PENDING, nullable=False)
    
    # Extracted/processed content
    extracted_text = Column(Text, nullable=True)
    transcription = Column(Text, nullable=True)
    
    # Metadata - renamed to 'meta'
    meta = Column(JSON, default=dict, nullable=False)
    
    # Whether file is in library (vs just uploaded for a message)
    in_library = Column(Boolean, default=True, nullable=False)
    
    # Thumbnail path for images/videos
    thumbnail_path = Column(String(1000), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="files")
    message_attachments = relationship("MessageAttachment", back_populates="file", cascade="all, delete-orphan")
    vector_chunks = relationship("VectorChunk", back_populates="file", cascade="all, delete-orphan")