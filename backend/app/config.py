import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/kahaniyaa"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # Azure Cognitive Services
    azure_speech_key: Optional[str] = None
    azure_speech_region: Optional[str] = None
    azure_vision_key: Optional[str] = None
    azure_vision_endpoint: Optional[str] = None
    
    # Supabase
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    
    # AWS S3
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_bucket_name: str = "kahaniyaa-assets"
    
    # App Settings
    secret_key: str = "your-secret-key-change-in-production"
    environment: str = "development"
    debug: bool = True
    
    # API Settings
    max_story_length: int = 2000
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    supported_languages: list = ["en", "hi", "ta"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
