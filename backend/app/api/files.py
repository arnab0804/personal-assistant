from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter()




@router.post("/upload")
async def upload_file(current_user: User = Depends(get_current_user)):
    """Upload a file"""
    return {"message": "File upload endpoint - coming soon"}