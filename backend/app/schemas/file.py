from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from app.models.file import FileType, FileProcessingStatus




class FileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    filename: str
    original_filename: str
    file_path: str
    file_type: FileType
    mime_type: str
    file_size: int
    processing_status: FileProcessingStatus
    extracted_text: Optional[str]
    transcription: Optional[str]
    meta: Dict[str, Any]
    in_library: bool
    thumbnail_path: Optional[str]
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True




class FileUploadResponse(BaseModel):
    file: FileResponse
    message: str = "File uploaded successfully"