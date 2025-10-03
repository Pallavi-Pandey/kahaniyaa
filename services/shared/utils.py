"""
Shared utilities for Kahaniyaa microservices
"""

import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import os
import json

logger = logging.getLogger(__name__)

class ServiceClient:
    """HTTP client for inter-service communication"""
    
    def __init__(self, timeout: float = 30.0):
        self.client = httpx.AsyncClient(timeout=timeout)
        self.services = {
            "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
            "story": os.getenv("STORY_SERVICE_URL", "http://localhost:8002"),
            "tts": os.getenv("TTS_SERVICE_URL", "http://localhost:8003"),
            "vision": os.getenv("VISION_SERVICE_URL", "http://localhost:8004"),
        }
    
    async def call_service(
        self, 
        service_name: str, 
        endpoint: str, 
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to another microservice"""
        
        service_url = self.services.get(service_name)
        if not service_url:
            raise ValueError(f"Unknown service: {service_name}")
        
        url = f"{service_url}{endpoint}"
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                json=data,
                headers=headers or {}
            )
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "response_time": response.elapsed.total_seconds()
            }
            
        except httpx.RequestError as e:
            logger.error(f"Request to {service_name} failed: {str(e)}")
            return {
                "success": False,
                "status_code": 503,
                "error": f"Service {service_name} unavailable",
                "response_time": 0.0
            }
        except Exception as e:
            logger.error(f"Unexpected error calling {service_name}: {str(e)}")
            return {
                "success": False,
                "status_code": 500,
                "error": str(e),
                "response_time": 0.0
            }
    
    async def health_check(self, service_name: str) -> Dict[str, Any]:
        """Check health of a specific service"""
        return await self.call_service(service_name, "/health")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

class ConfigManager:
    """Configuration management for microservices"""
    
    @staticmethod
    def get_database_url() -> str:
        """Get database connection URL"""
        return os.getenv(
            "DATABASE_URL", 
            "postgresql://username:password@localhost:5432/kahaniyaa"
        )
    
    @staticmethod
    def get_redis_url() -> str:
        """Get Redis connection URL"""
        return os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    @staticmethod
    def get_jwt_secret() -> str:
        """Get JWT secret key"""
        return os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    
    @staticmethod
    def get_openai_api_key() -> str:
        """Get OpenAI API key"""
        return os.getenv("OPENAI_API_KEY", "")
    
    @staticmethod
    def get_azure_speech_config() -> Dict[str, str]:
        """Get Azure Speech service configuration"""
        return {
            "key": os.getenv("AZURE_SPEECH_KEY", ""),
            "region": os.getenv("AZURE_SPEECH_REGION", ""),
        }
    
    @staticmethod
    def get_azure_vision_config() -> Dict[str, str]:
        """Get Azure Vision service configuration"""
        return {
            "key": os.getenv("AZURE_VISION_KEY", ""),
            "endpoint": os.getenv("AZURE_VISION_ENDPOINT", ""),
        }

class Logger:
    """Centralized logging configuration"""
    
    @staticmethod
    def setup_logging(service_name: str, level: str = "INFO"):
        """Setup logging for a microservice"""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=f'%(asctime)s - {service_name} - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f"/tmp/{service_name}.log")
            ]
        )

class ResponseFormatter:
    """Standard response formatting for microservices"""
    
    @staticmethod
    def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Format successful response"""
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def error_response(
        error: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format error response"""
        return {
            "success": False,
            "error": error,
            "error_code": error_code,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        }

class ValidationUtils:
    """Common validation utilities"""
    
    @staticmethod
    def validate_language(language: str) -> bool:
        """Validate if language is supported"""
        supported_languages = ["en", "hi", "ta"]
        return language in supported_languages
    
    @staticmethod
    def validate_tone(tone: str) -> bool:
        """Validate if tone is supported"""
        supported_tones = [
            "cheerful", "adventurous", "mysterious", "whimsical",
            "educational", "funny", "heartwarming", "exciting"
        ]
        return tone in supported_tones
    
    @staticmethod
    def validate_target_audience(audience: str) -> bool:
        """Validate if target audience is supported"""
        supported_audiences = [
            "kids", "teens", "adults", "family", "toddlers", "preschool"
        ]
        return audience in supported_audiences
    
    @staticmethod
    def validate_file_type(content_type: str, allowed_types: list) -> bool:
        """Validate file content type"""
        return content_type in allowed_types

class CacheUtils:
    """Caching utilities for microservices"""
    
    @staticmethod
    def generate_cache_key(*args) -> str:
        """Generate cache key from arguments"""
        return ":".join(str(arg) for arg in args)
    
    @staticmethod
    def serialize_for_cache(data: Any) -> str:
        """Serialize data for caching"""
        return json.dumps(data, default=str)
    
    @staticmethod
    def deserialize_from_cache(data: str) -> Any:
        """Deserialize data from cache"""
        return json.loads(data)
