from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter()




@router.get("/")
async def list_library(current_user: User = Depends(get_current_user)):
    """List all files in library"""
    return {"message": "Library endpoint - coming soon"}