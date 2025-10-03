#!/usr/bin/env python3
"""
Kahaniyaa TTS Service
Handles text-to-speech conversion with multilingual support
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import sys
import logging
from datetime import datetime
import base64

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import from existing backend
from backend.app.services.tts_service import TTSService
from backend.app.services.voice_presets import VoicePresets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kahaniyaa TTS Service",
    description="Text-to-Speech Microservice",
    version="1.0.0"
)

# Initialize TTS service
tts_service = TTSService()

# Pydantic models
class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice_preset: str = "narrator_calm"
    emotion: str = "neutral"
    speed: float = 1.0
    pitch: float = 1.0

class TTSResponse(BaseModel):
    audio_url: str
    audio_data: Optional[str] = None  # Base64 encoded audio
    duration: Optional[float] = None
    metadata: Dict

class VoicePreset(BaseModel):
    id: str
    name: str
    language: str
    gender: str
    age_group: str
    description: str
    voice_name: str

@app.get("/")
async def root():
    """TTS service health check"""
    return {
        "service": "Kahaniyaa TTS Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "tts-service"}

@app.post("/v1/tts/generate", response_model=TTSResponse)
async def generate_audio(request: TTSRequest):
    """Generate audio from text using specified voice and settings"""
    try:
        # Get voice configuration
        voice_config = VoicePresets.get_voice_config(
            request.voice_preset,
            request.language
        )
        
        if not voice_config:
            raise HTTPException(
                status_code=400,
                detail=f"Voice preset '{request.voice_preset}' not found for language '{request.language}'"
            )

        # Generate SSML with emotion and speed adjustments
        ssml_text = VoicePresets.generate_ssml(
            request.text,
            voice_config,
            request.emotion,
            request.speed,
            request.pitch
        )

        # Generate audio
        audio_data = await tts_service.generate_speech(
            ssml_text,
            voice_config["voice_name"],
            request.language
        )

        # For now, return base64 encoded audio data
        # In production, save to file storage and return URL
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return TTSResponse(
            audio_url=f"/v1/tts/audio/{len(audio_base64)[:8]}",  # Mock URL
            audio_data=audio_base64,
            duration=len(request.text) * 0.1,  # Rough estimate
            metadata={
                "voice_preset": request.voice_preset,
                "language": request.language,
                "emotion": request.emotion,
                "text_length": len(request.text),
                "voice_config": voice_config
            }
        )

    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")

@app.get("/v1/voices/presets", response_model=List[VoicePreset])
async def get_voice_presets(language: Optional[str] = None):
    """Get available voice presets, optionally filtered by language"""
    try:
        presets = VoicePresets.get_all_presets()
        
        if language:
            presets = [p for p in presets if p["language"] == language]
        
        return [VoicePreset(**preset) for preset in presets]
        
    except Exception as e:
        logger.error(f"Error getting voice presets: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get voice presets")

@app.get("/v1/voices/emotions")
async def get_supported_emotions():
    """Get list of supported emotions"""
    return {
        "emotions": [
            "neutral", "happy", "sad", "excited", "calm", 
            "mysterious", "cheerful", "dramatic", "gentle"
        ]
    }

@app.get("/v1/voices/languages")
async def get_supported_languages():
    """Get list of supported TTS languages"""
    return {
        "languages": [
            {"code": "en", "name": "English", "voices": 3},
            {"code": "hi", "name": "Hindi", "voices": 2},
            {"code": "ta", "name": "Tamil", "voices": 2}
        ]
    }

@app.post("/v1/tts/batch")
async def generate_batch_audio(requests: List[TTSRequest]):
    """Generate audio for multiple text inputs"""
    results = []
    
    for i, request in enumerate(requests):
        try:
            result = await generate_audio(request)
            results.append({
                "index": i,
                "success": True,
                "result": result
            })
        except Exception as e:
            results.append({
                "index": i,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results}

@app.get("/v1/tts/preview/{voice_preset}")
async def preview_voice(voice_preset: str, language: str = "en"):
    """Generate a preview audio sample for a voice preset"""
    preview_texts = {
        "en": "Hello! This is a preview of my voice. I can tell wonderful stories in many different tones and emotions.",
        "hi": "नमस्ते! यह मेरी आवाज़ का एक नमूना है। मैं कई अलग-अलग स्वरों और भावनाओं में अद्भुत कहानियाँ सुना सकता हूँ।",
        "ta": "வணக்கம்! இது என் குரலின் ஒரு மாதிரி. நான் பல்வேறு தொனிகளிலும் உணர்வுகளிலும் அற்புதமான கதைகளைச் சொல்ல முடியும்."
    }
    
    preview_text = preview_texts.get(language, preview_texts["en"])
    
    request = TTSRequest(
        text=preview_text,
        language=language,
        voice_preset=voice_preset,
        emotion="cheerful"
    )
    
    return await generate_audio(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
