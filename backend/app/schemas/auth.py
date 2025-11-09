from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid




class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)




class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)




class UserLogin(BaseModel):
    identifier: str = Field(..., description="Email or username")
    password: str




class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True




class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse




class TokenData(BaseModel):
    user_id: Optional[uuid.UUID] = None