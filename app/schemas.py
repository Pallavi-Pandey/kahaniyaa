from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import StoryInputType, StoryStatus, JobStatus


# Request schemas
class StoryCreateRequest(BaseModel):
    input_type: StoryInputType
    input_payload: Dict[str, Any]
    language: str = Field(..., pattern="^(en|hi|ta)$")
    tone: str = "cheerful"
    target_audience: str = "kids"
    length: int = Field(500, ge=100, le=2000)
    tts_voice_preset: Optional[str] = None


class ScenarioInput(BaseModel):
    scenario: str = Field(..., min_length=10, max_length=1000)


class ImageInput(BaseModel):
    image_url: str
    user_description: Optional[str] = None


class CharactersInput(BaseModel):
    characters: List[Dict[str, str]]  # [{"name": "Asha", "traits": "brave, kind"}]
    setting: Optional[str] = None
    conflict: Optional[str] = None


class TTSRegenerateRequest(BaseModel):
    voice_preset: str
    emotion: Optional[str] = "neutral"


# Response schemas
class DialogueLine(BaseModel):
    character: str
    line: str
    emotion: Optional[str] = "neutral"


class Scene(BaseModel):
    id: int
    title: str
    narration: str
    dialogue: List[DialogueLine] = []


class StoryContent(BaseModel):
    title: str
    scenes: List[Scene]
    metadata: Dict[str, Any] = {}


class StoryResponse(BaseModel):
    id: int
    title: str
    language: str
    input_type: StoryInputType
    status: StoryStatus
    story_content: Optional[StoryContent] = None
    audio_urls: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    id: str
    story_id: int
    job_type: str
    status: JobStatus
    progress: int
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VoicePresetResponse(BaseModel):
    id: int
    name: str
    language: str
    provider: str
    style: Optional[str] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None
    accent: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


# Error schemas
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
