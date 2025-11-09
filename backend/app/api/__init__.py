from fastapi import APIRouter
from app.api import auth, projects, chat, files, search, library


api_router = APIRouter()


# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(files.router, prefix="/files", tags=["Files"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(library.router, prefix="/library", tags=["Library"])