from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter()




@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **username**: Username (3-100 characters)
    - **password**: Password (minimum 8 characters)
    """
    return await AuthService.signup(user_data, db)




@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email/username and password
    
    - **identifier**: Email address or username
    - **password**: User password
    
    Returns JWT access token on successful authentication
    """
    return await AuthService.login(credentials, db)




@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return UserResponse.model_validate(current_user)




@router.post("/logout")
async def logout():
    """
    Logout current user
    
    Note: Since we're using JWT, logout is handled client-side by removing the token.
    This endpoint is provided for consistency but doesn't perform server-side action.
    """
    return {"message": "Successfully logged out"}