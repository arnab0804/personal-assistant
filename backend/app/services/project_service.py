from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from typing import List, Optional
import uuid


from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse




class ProjectService:
    """Service for handling project operations"""
    
    @staticmethod
    async def create_project(
        project_data: ProjectCreate,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> ProjectResponse:
        """Create a new project"""
        new_project = Project(
            user_id=user_id,
            name=project_data.name,
            description=project_data.description,
            tags=project_data.tags,
            default_llm_model=project_data.default_llm_model,
            default_system_prompt=project_data.default_system_prompt,
            settings={}
        )
        
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        
        return ProjectResponse.model_validate(new_project)
    
    @staticmethod
    async def get_user_projects(
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> List[ProjectResponse]:
        """Get all projects for a user"""
        result = await db.execute(
            select(Project)
            .where(Project.user_id == user_id)
            .order_by(Project.updated_at.desc())
        )
        projects = result.scalars().all()
        return [ProjectResponse.model_validate(p) for p in projects]
    
    @staticmethod
    async def get_project_by_id(
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> Optional[Project]:
        """Get a specific project by ID"""
        result = await db.execute(
            select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_project(
        project_id: uuid.UUID,
        project_data: ProjectUpdate,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> ProjectResponse:
        """Update a project"""
        project = await ProjectService.get_project_by_id(project_id, user_id, db)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Update fields
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        await db.commit()
        await db.refresh(project)
        
        return ProjectResponse.model_validate(project)
    
    @staticmethod
    async def delete_project(
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        db: AsyncSession
    ) -> bool:
        """Delete a project"""
        project = await ProjectService.get_project_by_id(project_id, user_id, db)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        await db.delete(project)
        await db.commit()
        
        return True