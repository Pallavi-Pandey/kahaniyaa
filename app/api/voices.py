from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import VoicePreset
from app.schemas import VoicePresetResponse
from app.services.tts_service import TTSService

router = APIRouter(prefix="/v1/voices", tags=["voices"])

tts_service = TTSService()


@router.get("/", response_model=List[VoicePresetResponse])
async def get_voices(
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get available voice presets, optionally filtered by language."""
    
    # Get voices from TTS service
    available_voices = tts_service.get_available_voices(language)
    
    # Convert to response format
    voices = []
    for voice in available_voices:
        voices.append(VoicePresetResponse(
            id=hash(voice["id"]) % 1000000,  # Generate numeric ID from string
            name=voice["name"],
            language=voice["language"],
            provider="azure",
            style=voice.get("style"),
            gender=voice.get("gender"),
            age_group="adult",
            accent="native"
        ))
    
    return voices


@router.get("/presets", response_model=List[dict])
async def get_voice_presets():
    """Get predefined voice presets for different character types."""
    
    presets = [
        {
            "id": "narrator_en",
            "name": "English Narrator",
            "language": "en",
            "voice_id": "en-US-AriaNeural",
            "character_type": "narrator",
            "emotion": "calm",
            "description": "Clear, engaging narrator voice"
        },
        {
            "id": "narrator_hi", 
            "name": "Hindi Narrator",
            "language": "hi",
            "voice_id": "hi-IN-SwaraNeural",
            "character_type": "narrator",
            "emotion": "calm",
            "description": "Clear Hindi narrator voice"
        },
        {
            "id": "narrator_ta",
            "name": "Tamil Narrator", 
            "language": "ta",
            "voice_id": "ta-IN-PallaviNeural",
            "character_type": "narrator",
            "emotion": "calm",
            "description": "Clear Tamil narrator voice"
        },
        {
            "id": "child_en",
            "name": "English Child",
            "language": "en", 
            "voice_id": "en-US-JennyNeural",
            "character_type": "child",
            "emotion": "cheerful",
            "description": "Playful child character voice"
        },
        {
            "id": "hero_en",
            "name": "English Hero",
            "language": "en",
            "voice_id": "en-US-GuyNeural", 
            "character_type": "adult_male",
            "emotion": "confident",
            "description": "Strong, heroic character voice"
        },
        {
            "id": "hero_hi",
            "name": "Hindi Hero",
            "language": "hi",
            "voice_id": "hi-IN-MadhurNeural",
            "character_type": "adult_male", 
            "emotion": "confident",
            "description": "Strong Hindi hero voice"
        }
    ]
    
    return presets


@router.get("/emotions")
async def get_supported_emotions():
    """Get list of supported emotions for TTS."""
    
    emotions = [
        {"id": "neutral", "name": "Neutral", "description": "Natural, conversational tone"},
        {"id": "cheerful", "name": "Cheerful", "description": "Happy and upbeat"},
        {"id": "excited", "name": "Excited", "description": "Energetic and enthusiastic"},
        {"id": "calm", "name": "Calm", "description": "Peaceful and soothing"},
        {"id": "sad", "name": "Sad", "description": "Melancholic and gentle"},
        {"id": "angry", "name": "Angry", "description": "Intense and forceful"},
        {"id": "gentle", "name": "Gentle", "description": "Soft and caring"}
    ]
    
    return emotions
