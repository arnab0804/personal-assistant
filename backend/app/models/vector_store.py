from sqlalchemy import Column, String, Text, ForeignKey, Integer, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import uuid
from app.database import Base
from app.models import TimestampMixin
from app.config import settings




class VectorStore(Base, TimestampMixin):
    __tablename__ = "vector_stores"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Source information
    source_type = Column(String(50), nullable=False)  # 'file', 'url', 'manual'
    source_url = Column(String(1000), nullable=True)
    
    # Embedding model used
    embedding_model = Column(String(100), nullable=False, default="text-embedding-ada-002")
    
    # Metadata for filtering - renamed to 'meta'
    meta = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="vector_stores")
    chunks = relationship("VectorChunk", back_populates="vector_store", cascade="all, delete-orphan")




class VectorChunk(Base, TimestampMixin):
    __tablename__ = "vector_chunks"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vector_store_id = Column(UUID(as_uuid=True), ForeignKey("vector_stores.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    
    # Content
    content = Column(Text, nullable=False)
    
    # Vector embedding
    embedding = Column(Vector(settings.VECTOR_DIMENSION), nullable=False)
    
    # Chunk metadata
    chunk_index = Column(Integer, nullable=False)
    token_count = Column(Integer, nullable=True)
    
    # Metadata for filtering (page number, section, etc.) - renamed to 'meta'
    meta = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    vector_store = relationship("VectorStore", back_populates="chunks")
    file = relationship("File", back_populates="vector_chunks")




# Create index for vector similarity search
Index(
    'idx_vector_chunks_embedding',
    VectorChunk.embedding,
    postgresql_using='ivfflat',
    postgresql_with={'lists': 100},
    postgresql_ops={'embedding': 'vector_cosine_ops'}
)