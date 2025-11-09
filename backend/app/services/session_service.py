from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import List, Optional
import uuid


from app.models.session import Session, SessionMode
from app.models.message import Message
from app.schemas.chat import SessionCreate, SessionUpdate, SessionResponse




class SessionService:
    """Service for handling session operations"""
    
    @staticmethod
    async def create_session(
        session_data: SessionCreate,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> SessionResponse:
        """Create a new chat session"""
        new_session = Session(
            user_id=user_id,
            project_id=session_data.project_id,
            title=session_data.title,
            mode=session_data.mode,
            llm_model=session_data.llm_model,
            system_prompt=session_data.system_prompt,
            settings={}
        )
        
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        
        return SessionResponse.model_validate(new_session)
    
    @staticmethod
    async def get_user_sessions(
        user_id: uuid.UUID,
        project_id: Optional[uuid.UUID],
        db: AsyncSession
    ) -> List[SessionResponse]:
        """Get all sessions for a user, optionally filtered by project"""
        query = select(Session).where(Session.user_id == user_id)
        
        if project_id:
            query = query.where(Session.project_id == project_id)
        
        query = query.order_by(Session.updated_at.desc())
        
        result = await db.execute(query)
        sessions = result.scalars().all()
        return [SessionResponse.model_validate(s) for s in sessions]
    
    @staticmethod
    async def get_session_by_id(
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> Optional[Session]:
        """Get a specific session by ID"""
        result = await db.execute(
            select(Session)
            .options(selectinload(Session.messages))
            .where(
                and_(
                    Session.id == session_id,
                    Session.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_session(
        session_id: uuid.UUID,
        session_data: SessionUpdate,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> SessionResponse:
        """Update a session"""
        session = await SessionService.get_session_by_id(session_id, user_id, db)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Update fields
        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)
        
        await db.commit()
        await db.refresh(session)
        
        return SessionResponse.model_validate(session)
    
    @staticmethod
    async def delete_session(
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> bool:
        """Delete a session"""
        session = await SessionService.get_session_by_id(session_id, user_id, db)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        await db.delete(session)
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_session_messages(
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> List[Message]:
        """Get all messages for a session"""
        session = await SessionService.get_session_by_id(session_id, user_id, db)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.sequence.asc())
        )
        return result.scalars().all()