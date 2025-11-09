from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from app.models.session import SessionMode
from app.models.message import MessageRole




class SessionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    mode: SessionMode = SessionMode.CHAT
    llm_model: Optional[str] = None
    system_prompt: Optional[str] = None




class SessionCreate(SessionBase):
    project_id: Optional[uuid.UUID] = None




class SessionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    llm_model: Optional[str] = None
    system_prompt: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None




class SessionRename(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)




class SessionResponse(SessionBase):
    id: uuid.UUID
    user_id: uuid.UUID
    project_id: Optional[uuid.UUID]
    settings: Dict[str, Any]
    context_summary: Optional[str]
    created_at: datetime
    updated_at: datetime


    model_config = ConfigDict(from_attributes=True)




class MessageBase(BaseModel):
    content: str
    role: MessageRole = MessageRole.USER




class MessageCreate(MessageBase):
    file_ids: List[uuid.UUID] = Field(default_factory=list)




class MessageResponse(MessageBase):
    id: uuid.UUID
    session_id: uuid.UUID
    sequence: int
    llm_model: Optional[str]
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]
    meta: Dict[str, Any]
    agent_name: Optional[str]
    is_summary: bool
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)




class ChatRequest(BaseModel):
    message: str
    session_id: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    mode: SessionMode = SessionMode.CHAT
    llm_model: Optional[str] = None
    stream: bool = True
    file_ids: List[uuid.UUID] = Field(default_factory=list)




class ChatResponse(BaseModel):
    session_id: uuid.UUID
    message: MessageResponse