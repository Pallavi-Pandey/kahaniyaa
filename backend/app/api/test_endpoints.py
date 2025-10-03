from fastapi import APIRouter, HTTPException
from typing import Dict, List
from app.services.prompt_templates import PromptTemplates
from app.schemas import StoryCreateRequest, ScenarioInput, ImageInput, CharactersInput

router = APIRouter(prefix="/v1/test", tags=["testing"])


@router.get("/sample-scenarios")
async def get_sample_scenarios() -> Dict[str, List[str]]:
    """Get sample scenarios for testing story generation."""
    return PromptTemplates.get_sample_scenarios()


@router.get("/sample-characters")
async def get_sample_characters() -> List[Dict]:
    """Get sample character sets for testing."""
    return PromptTemplates.get_sample_characters()


@router.post("/validate-scenario")
async def validate_scenario_input(request: Dict) -> Dict:
    """Validate scenario input format."""
    try:
        scenario_input = ScenarioInput(**request)
        return {
            "valid": True,
            "scenario": scenario_input.scenario,
            "length": len(scenario_input.scenario)
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


@router.post("/validate-image")
async def validate_image_input(request: Dict) -> Dict:
    """Validate image input format."""
    try:
        image_input = ImageInput(**request)
        return {
            "valid": True,
            "image_url": image_input.image_url,
            "has_description": bool(image_input.user_description)
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


@router.post("/validate-characters")
async def validate_characters_input(request: Dict) -> Dict:
    """Validate characters input format."""
    try:
        characters_input = CharactersInput(**request)
        return {
            "valid": True,
            "character_count": len(characters_input.characters),
            "characters": [char.get("name", "Unnamed") for char in characters_input.characters],
            "has_setting": bool(characters_input.setting),
            "has_conflict": bool(characters_input.conflict)
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


@router.post("/preview-prompt")
async def preview_prompt(request: Dict) -> Dict:
    """Preview the prompt that would be sent to the LLM."""
    
    try:
        input_type = request.get("input_type")
        input_data = request.get("input_data", {})
        language = request.get("language", "en")
        tone = request.get("tone", "cheerful")
        target_audience = request.get("target_audience", "kids")
        length = request.get("length", 500)
        
        if input_type == "scenario":
            scenario_input = ScenarioInput(**input_data)
            prompts = PromptTemplates.get_scenario_prompt(
                scenario_input.scenario, language, tone, target_audience, length
            )
        elif input_type == "image":
            image_input = ImageInput(**input_data)
            # Mock image description for preview
            image_description = "A colorful scene with various elements"
            prompts = PromptTemplates.get_image_prompt(
                image_description, image_input.user_description, 
                language, tone, target_audience, length
            )
        elif input_type == "characters":
            characters_input = CharactersInput(**input_data)
            prompts = PromptTemplates.get_characters_prompt(
                characters_input.characters, characters_input.setting or "",
                characters_input.conflict or "", language, tone, target_audience, length
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid input_type")
        
        return {
            "input_type": input_type,
            "language": language,
            "tone": tone,
            "target_audience": target_audience,
            "length": length,
            "system_prompt": prompts["system"],
            "user_prompt": prompts["user"],
            "system_prompt_length": len(prompts["system"]),
            "user_prompt_length": len(prompts["user"])
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating prompt: {str(e)}")


@router.get("/supported-languages")
async def get_supported_languages() -> List[Dict[str, str]]:
    """Get list of supported languages."""
    return [
        {"code": "en", "name": "English", "native_name": "English"},
        {"code": "hi", "name": "Hindi", "native_name": "हिंदी"},
        {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"}
    ]


@router.get("/supported-tones")
async def get_supported_tones() -> List[Dict[str, str]]:
    """Get list of supported story tones."""
    return [
        {"id": "cheerful", "name": "Cheerful", "description": "Happy and upbeat stories"},
        {"id": "adventurous", "name": "Adventurous", "description": "Exciting journeys and quests"},
        {"id": "whimsical", "name": "Whimsical", "description": "Playful and imaginative tales"},
        {"id": "gentle", "name": "Gentle", "description": "Calm and soothing stories"},
        {"id": "mysterious", "name": "Mysterious", "description": "Intriguing puzzles and secrets"},
        {"id": "funny", "name": "Funny", "description": "Humorous and entertaining stories"},
        {"id": "inspiring", "name": "Inspiring", "description": "Uplifting and motivational tales"}
    ]


@router.get("/target-audiences")
async def get_target_audiences() -> List[Dict[str, str]]:
    """Get list of target audiences."""
    return [
        {"id": "kids", "name": "Children (5-12)", "description": "Simple language, clear morals"},
        {"id": "teens", "name": "Teenagers (13-17)", "description": "Coming-of-age themes, more complex plots"},
        {"id": "adults", "name": "Adults (18+)", "description": "Sophisticated themes and language"},
        {"id": "family", "name": "Family (All ages)", "description": "Stories enjoyable for everyone"}
    ]
