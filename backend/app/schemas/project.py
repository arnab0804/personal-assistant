from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid




class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    default_llm_model: Optional[str] = None
    default_system_prompt: Optional[str] = None




class ProjectCreate(ProjectBase):
    pass




class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    default_llm_model: Optional[str] = None
    default_system_prompt: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None




class ProjectRename(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)




class ProjectResponse(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


    model_config = ConfigDict(from_attributes=True)