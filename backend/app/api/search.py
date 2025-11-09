from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter()




@router.get("/")
async def search_web(current_user: User = Depends(get_current_user)):
    """Search the web"""
    return {"message": "Web search endpoint - coming soon"}