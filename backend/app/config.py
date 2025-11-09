from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional




class Settings(BaseSettings):
    # Application
    APP_NAME: str = "rikuduo"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # LLM Providers - Azure OpenAI
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Azure AI Foundry (for Deepseek & Grok)
    AZURE_AI_FOUNDRY_ENDPOINT: Optional[str] = None
    AZURE_AI_FOUNDRY_API_KEY: Optional[str] = None
    
    # AWS Bedrock (for Claude)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Vector Store
    VECTOR_DIMENSION: int = 1536  # OpenAI embeddings default
    
    # API Settings
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True




@lru_cache()
def get_settings() -> Settings:
    return Settings()




settings = get_settings()