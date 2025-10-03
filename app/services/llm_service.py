import json
import openai
from typing import Dict, Any, List
from app.config import settings
from app.schemas import StoryContent, Scene, DialogueLine
from app.services.prompt_templates import PromptTemplates


class LLMService:
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
    
    def generate_story_from_scenario(
        self, 
        scenario: str, 
        language: str, 
        tone: str, 
        target_audience: str, 
        length: int
    ) -> StoryContent:
        """Generate a story from a text scenario."""
        
        prompts = PromptTemplates.get_scenario_prompt(
            scenario, language, tone, target_audience, length
        )
        system_prompt = prompts["system"]
        user_prompt = prompts["user"]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            story_data = json.loads(content)
            
            # Convert to Pydantic models
            scenes = []
            for scene_data in story_data.get("scenes", []):
                dialogue = [
                    DialogueLine(
                        character=d.get("character", "Narrator"),
                        line=d.get("line", ""),
                        emotion=d.get("emotion", "neutral")
                    )
                    for d in scene_data.get("dialogue", [])
                ]
                
                scene = Scene(
                    id=scene_data.get("id", len(scenes) + 1),
                    title=scene_data.get("title", f"Scene {len(scenes) + 1}"),
                    narration=scene_data.get("narration", ""),
                    dialogue=dialogue
                )
                scenes.append(scene)
            
            return StoryContent(
                title=story_data.get("title", "Untitled Story"),
                scenes=scenes,
                metadata={
                    "tone": tone,
                    "target_audience": target_audience,
                    "language": language,
                    "word_count": self._estimate_word_count(scenes)
                }
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate story: {str(e)}")
    
    def generate_story_from_image(
        self, 
        image_description: str, 
        user_description: str,
        language: str, 
        tone: str, 
        target_audience: str, 
        length: int
    ) -> StoryContent:
        """Generate a story from image analysis."""
        
        prompts = PromptTemplates.get_image_prompt(
            image_description, user_description, language, tone, target_audience, length
        )
        system_prompt = prompts["system"]
        user_prompt = prompts["user"]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            story_data = json.loads(content)
            
            # Convert to Pydantic models (same as scenario method)
            scenes = []
            for scene_data in story_data.get("scenes", []):
                dialogue = [
                    DialogueLine(
                        character=d.get("character", "Narrator"),
                        line=d.get("line", ""),
                        emotion=d.get("emotion", "neutral")
                    )
                    for d in scene_data.get("dialogue", [])
                ]
                
                scene = Scene(
                    id=scene_data.get("id", len(scenes) + 1),
                    title=scene_data.get("title", f"Scene {len(scenes) + 1}"),
                    narration=scene_data.get("narration", ""),
                    dialogue=dialogue
                )
                scenes.append(scene)
            
            return StoryContent(
                title=story_data.get("title", "Untitled Story"),
                scenes=scenes,
                metadata={
                    "tone": tone,
                    "target_audience": target_audience,
                    "language": language,
                    "word_count": self._estimate_word_count(scenes),
                    "image_inspired": True
                }
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate story from image: {str(e)}")
    
    def generate_story_from_characters(
        self, 
        characters: List[Dict[str, str]], 
        setting: str,
        conflict: str,
        language: str, 
        tone: str, 
        target_audience: str, 
        length: int
    ) -> StoryContent:
        """Generate a story from character descriptions."""
        
        prompts = PromptTemplates.get_characters_prompt(
            characters, setting, conflict, language, tone, target_audience, length
        )
        system_prompt = prompts["system"]
        user_prompt = prompts["user"]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            story_data = json.loads(content)
            
            # Convert to Pydantic models (same as other methods)
            scenes = []
            for scene_data in story_data.get("scenes", []):
                dialogue = [
                    DialogueLine(
                        character=d.get("character", "Narrator"),
                        line=d.get("line", ""),
                        emotion=d.get("emotion", "neutral")
                    )
                    for d in scene_data.get("dialogue", [])
                ]
                
                scene = Scene(
                    id=scene_data.get("id", len(scenes) + 1),
                    title=scene_data.get("title", f"Scene {len(scenes) + 1}"),
                    narration=scene_data.get("narration", ""),
                    dialogue=dialogue
                )
                scenes.append(scene)
            
            return StoryContent(
                title=story_data.get("title", "Untitled Story"),
                scenes=scenes,
                metadata={
                    "tone": tone,
                    "target_audience": target_audience,
                    "language": language,
                    "word_count": self._estimate_word_count(scenes),
                    "character_driven": True,
                    "characters": [char.get("name") for char in characters]
                }
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate character story: {str(e)}")
    
    def _estimate_word_count(self, scenes: List[Scene]) -> int:
        """Estimate word count from scenes."""
        total_words = 0
        for scene in scenes:
            total_words += len(scene.narration.split())
            for dialogue in scene.dialogue:
                total_words += len(dialogue.line.split())
        return total_words
