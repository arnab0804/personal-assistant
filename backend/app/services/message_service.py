from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import List
import uuid


from app.models.message import Message, MessageRole
from app.models.session import Session
from app.schemas.chat import MessageCreate, MessageResponse




class MessageService:
    """Service for handling message operations"""
    
    @staticmethod
    async def create_message(
        session_id: uuid.UUID,
        content: str,
        role: MessageRole,
        user_id: uuid.UUID,
        db: AsyncSession,
        llm_model: str = None,
        meta: dict = None
    ) -> Message:
        """Create a new message in a session"""
        # Verify session belongs to user
        result = await db.execute(
            select(Session).where(
                Session.id == session_id,
                Session.user_id == user_id
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get the next sequence number
        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.sequence.desc())
        )
        last_message = result.scalar_one_or_none()
        next_sequence = (last_message.sequence + 1) if last_message else 0
        
        # Create message
        new_message = Message(
            session_id=session_id,
            role=role,
            content=content,
            sequence=next_sequence,
            llm_model=llm_model,
            meta=meta or {}
        )
        
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        
        return new_message
    
    @staticmethod
    async def get_session_messages(
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> List[Message]:
        """Get all messages for a session"""
        # Verify session belongs to user
        result = await db.execute(
            select(Session).where(
                Session.id == session_id,
                Session.user_id == user_id
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get messages
        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.sequence.asc())
        )
        return result.scalars().all()
    
    @staticmethod
    async def delete_message(
        message_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> bool:
        """Delete a message"""
        # Get message and verify ownership through session
        result = await db.execute(
            select(Message)
            .join(Session)
            .where(
                Message.id == message_id,
                Session.user_id == user_id
            )
        )
        message = result.scalar_one_or_none()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        await db.delete(message)
        await db.commit()
        
        return True