from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid


from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.message import MessageRole
from app.schemas.chat import (
    SessionCreate,
    SessionUpdate,
    SessionRename,
    SessionResponse,
    MessageResponse,
    ChatRequest,
)
from app.services.session_service import SessionService
from app.services.message_service import MessageService


router = APIRouter()




@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat session"""
    return await SessionService.create_session(session_data, current_user.id, db)




@router.get("/sessions", response_model=List[SessionResponse])
async def list_sessions(
    project_id: Optional[uuid.UUID] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all sessions for the current user, optionally filtered by project"""
    return await SessionService.get_user_sessions(current_user.id, project_id, db)




@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific session"""
    session = await SessionService.get_session_by_id(session_id, current_user.id, db)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return SessionResponse.model_validate(session)




@router.put("/sessions/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: uuid.UUID,
    session_data: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a session"""
    return await SessionService.update_session(session_id, session_data, current_user.id, db)




@router.patch("/sessions/{session_id}/rename", response_model=SessionResponse)
async def rename_session(
    session_id: uuid.UUID,
    rename_data: SessionRename,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Rename a session"""
    update_data = SessionUpdate(title=rename_data.title)
    return await SessionService.update_session(session_id, update_data, current_user.id, db)




@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a session"""
    await SessionService.delete_session(session_id, current_user.id, db)
    return None




@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all messages for a session"""
    messages = await MessageService.get_session_messages(session_id, current_user.id, db)
    return [MessageResponse.model_validate(m) for m in messages]




@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message (basic version - will be enhanced with LLM integration)
    For now, just stores the user message
    """
    if not chat_request.session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id is required"
        )
    
    # Create user message
    user_message = await MessageService.create_message(
        session_id=chat_request.session_id,
        content=chat_request.message,
        role=MessageRole.USER,
        user_id=current_user.id,
        db=db
    )
    
    # TODO: In next step, we'll add LLM integration here
    # For now, create a simple echo response
    assistant_message = await MessageService.create_message(
        session_id=chat_request.session_id,
        content=f"Echo: {chat_request.message}",
        role=MessageRole.ASSISTANT,
        user_id=current_user.id,
        db=db,
        llm_model="echo-bot"
    )
    
    return MessageResponse.model_validate(assistant_message)




@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a message"""
    await MessageService.delete_message(message_id, current_user.id, db)
    return None