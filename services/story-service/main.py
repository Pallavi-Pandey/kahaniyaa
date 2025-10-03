#!/usr/bin/env python3
"""
Kahaniyaa Story Service
Handles story generation from scenarios, images, and characters
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import os
import sys
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import from existing backend
from backend.app.services.llm_service import LLMService
from backend.app.services.prompt_templates import PromptTemplates
from backend.app.models import ScenarioInput, ImageInput, CharactersInput

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kahaniyaa Story Service",
    description="Story Generation Microservice",
    version="1.0.0"
)

# Initialize services
llm_service = LLMService()

# Pydantic models
class StoryRequest(BaseModel):
    input_type: str  # "scenario", "image", "characters"
    input_data: Dict[str, Any]
    language: str = "en"
    tone: str = "cheerful"
    target_audience: str = "kids"
    length: int = 500

class Story(BaseModel):
    id: str
    title: str
    content: str
    language: str
    tone: str
    target_audience: str
    input_type: str
    created_at: datetime
    metadata: Dict[str, Any]

# In-memory story storage (replace with database)
stories_db = {}

@app.get("/")
async def root():
    """Story service health check"""
    return {
        "service": "Kahaniyaa Story Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "story-service"}

@app.post("/v1/stories/", response_model=Story)
async def create_story(request: StoryRequest):
    """Generate a new story based on input type"""
    try:
        # Generate prompts based on input type
        if request.input_type == "scenario":
            scenario_input = ScenarioInput(**request.input_data)
            prompts = PromptTemplates.get_scenario_prompt(
                scenario_input.scenario,
                request.language,
                request.tone,
                request.target_audience,
                request.length
            )
        elif request.input_type == "image":
            image_input = ImageInput(**request.input_data)
            prompts = PromptTemplates.get_image_prompt(
                image_input.user_description,  # Use description as image analysis
                image_input.user_description,
                request.language,
                request.tone,
                request.target_audience,
                request.length
            )
        elif request.input_type == "characters":
            characters_input = CharactersInput(**request.input_data)
            prompts = PromptTemplates.get_characters_prompt(
                characters_input.characters,
                characters_input.setting or "",
                characters_input.conflict or "",
                request.language,
                request.tone,
                request.target_audience,
                request.length
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid input_type")

        # Generate story using LLM
        story_content = await llm_service.generate_story(
            prompts["system"],
            prompts["user"]
        )

        # Extract title from content (first line or generate one)
        lines = story_content.strip().split('\n')
        title = lines[0] if lines and len(lines[0]) < 100 else f"Story {len(stories_db) + 1}"
        
        # Create story object
        story_id = f"story_{len(stories_db) + 1}"
        story = Story(
            id=story_id,
            title=title,
            content=story_content,
            language=request.language,
            tone=request.tone,
            target_audience=request.target_audience,
            input_type=request.input_type,
            created_at=datetime.utcnow(),
            metadata={
                "input_data": request.input_data,
                "prompts": prompts,
                "length": len(story_content)
            }
        )

        # Store story
        stories_db[story_id] = story

        return story

    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

@app.get("/v1/stories/{story_id}", response_model=Story)
async def get_story(story_id: str):
    """Retrieve a specific story"""
    story = stories_db.get(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@app.get("/v1/stories/", response_model=List[Story])
async def list_stories(skip: int = 0, limit: int = 10):
    """List all stories with pagination"""
    stories = list(stories_db.values())
    return stories[skip:skip + limit]

@app.delete("/v1/stories/{story_id}")
async def delete_story(story_id: str):
    """Delete a specific story"""
    if story_id not in stories_db:
        raise HTTPException(status_code=404, detail="Story not found")
    
    del stories_db[story_id]
    return {"message": "Story deleted successfully"}

# Test endpoints
@app.get("/v1/test/sample-scenarios")
async def get_sample_scenarios():
    """Get sample scenarios for testing"""
    return {
        "scenarios": [
            {
                "id": "scenario_1",
                "title": "The Brave Little Boat",
                "scenario": "A small boat named Splash dreams of sailing across the vast ocean to find the legendary Rainbow Island.",
                "language": "en",
                "tone": "adventurous"
            },
            {
                "id": "scenario_2", 
                "title": "जादुई किताब",
                "scenario": "एक छोटी लड़की को अपनी दादी के घर में एक जादुई किताब मिलती है जो उसे अतीत में ले जाती है।",
                "language": "hi",
                "tone": "mysterious"
            },
            {
                "id": "scenario_3",
                "title": "மந்திர மரம்",
                "scenario": "ஒரு சிறுவன் தன் வீட்டு தோட்டத்தில் ஒரு மந்திர மரத்தைக் கண்டுபிடிக்கிறான், அது அவனுடைய கனவுகளை நிறைவேற்றும்.",
                "language": "ta",
                "tone": "whimsical"
            }
        ]
    }

@app.get("/v1/test/sample-characters")
async def get_sample_characters():
    """Get sample characters for testing"""
    return {
        "character_sets": [
            {
                "id": "chars_1",
                "characters": [
                    {"name": "Maya", "traits": "curious, brave, loves books"},
                    {"name": "Ravi", "traits": "funny, loyal, good at solving puzzles"}
                ],
                "setting": "An old library with secret passages",
                "conflict": "Ancient books are disappearing one by one"
            },
            {
                "id": "chars_2",
                "characters": [
                    {"name": "अर्जुन", "traits": "बहादुर, दयालु, जानवरों से प्यार करने वाला"},
                    {"name": "प्रिया", "traits": "चतुर, मिलनसार, कलाकार"}
                ],
                "setting": "एक जादुई जंगल जहाँ जानवर बोल सकते हैं",
                "conflict": "जंगल का जादू गायब हो रहा है"
            }
        ]
    }

@app.get("/v1/test/supported-languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"}
        ]
    }

@app.get("/v1/test/supported-tones")
async def get_supported_tones():
    """Get list of supported story tones"""
    return {
        "tones": [
            "cheerful", "adventurous", "mysterious", "whimsical", 
            "educational", "funny", "heartwarming", "exciting"
        ]
    }

@app.get("/v1/test/target-audiences")
async def get_target_audiences():
    """Get list of target audiences"""
    return {
        "audiences": [
            "kids", "teens", "adults", "family", "toddlers", "preschool"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
