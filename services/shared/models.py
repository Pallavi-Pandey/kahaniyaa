"""
Shared models and schemas for Kahaniyaa microservices
"""

from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

# Common enums
class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNREACHABLE = "unreachable"

class StoryInputType(str, Enum):
    SCENARIO = "scenario"
    IMAGE = "image"
    CHARACTERS = "characters"

class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    TAMIL = "ta"

class Tone(str, Enum):
    CHEERFUL = "cheerful"
    ADVENTUROUS = "adventurous"
    MYSTERIOUS = "mysterious"
    WHIMSICAL = "whimsical"
    EDUCATIONAL = "educational"
    FUNNY = "funny"
    HEARTWARMING = "heartwarming"
    EXCITING = "exciting"

class TargetAudience(str, Enum):
    KIDS = "kids"
    TEENS = "teens"
    ADULTS = "adults"
    FAMILY = "family"
    TODDLERS = "toddlers"
    PRESCHOOL = "preschool"

# Base models
class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class ErrorResponse(BaseResponse):
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# User models
class User(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool = True
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# Story models
class ScenarioInput(BaseModel):
    scenario: str

class ImageInput(BaseModel):
    image_url: str
    user_description: Optional[str] = None

class Character(BaseModel):
    name: str
    traits: str

class CharactersInput(BaseModel):
    characters: List[Character]
    setting: Optional[str] = None
    conflict: Optional[str] = None

class StoryRequest(BaseModel):
    input_type: StoryInputType
    input_data: Dict[str, Any]
    language: Language = Language.ENGLISH
    tone: Tone = Tone.CHEERFUL
    target_audience: TargetAudience = TargetAudience.KIDS
    length: int = 500

class Story(BaseModel):
    id: str
    title: str
    content: str
    language: Language
    tone: Tone
    target_audience: TargetAudience
    input_type: StoryInputType
    created_at: datetime
    metadata: Dict[str, Any]

# TTS models
class TTSRequest(BaseModel):
    text: str
    language: Language = Language.ENGLISH
    voice_preset: str = "narrator_calm"
    emotion: str = "neutral"
    speed: float = 1.0
    pitch: float = 1.0

class TTSResponse(BaseModel):
    audio_url: str
    audio_data: Optional[str] = None
    duration: Optional[float] = None
    metadata: Dict[str, Any]

class VoicePreset(BaseModel):
    id: str
    name: str
    language: Language
    gender: str
    age_group: str
    description: str
    voice_name: str

# Vision models
class ImageAnalysisRequest(BaseModel):
    image_url: str
    user_description: Optional[str] = None

class ImageAnalysisResponse(BaseModel):
    image_id: str
    description: str
    user_description: Optional[str]
    tags: List[str]
    objects: List[Dict[str, Any]]
    colors: List[str]
    metadata: Dict[str, Any]
    created_at: datetime

class ImageUploadResponse(BaseModel):
    image_id: str
    image_url: str
    description: str
    user_description: Optional[str]
    file_size: int
    metadata: Dict[str, Any]

# Service communication models
class ServiceHealthCheck(BaseModel):
    service_name: str
    status: ServiceStatus
    version: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

class InterServiceRequest(BaseModel):
    service_name: str
    endpoint: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None
    timeout: float = 30.0

class InterServiceResponse(BaseModel):
    success: bool
    status_code: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    response_time: float
