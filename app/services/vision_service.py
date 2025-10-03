from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from typing import Dict, List, Optional
import time
from app.config import settings


class VisionService:
    def __init__(self):
        if settings.azure_vision_key and settings.azure_vision_endpoint:
            self.client = ComputerVisionClient(
                settings.azure_vision_endpoint,
                CognitiveServicesCredentials(settings.azure_vision_key)
            )
        else:
            self.client = None
    
    def analyze_image(self, image_url: str) -> Dict[str, any]:
        """Analyze image and return comprehensive description."""
        if not self.client:
            raise Exception("Azure Computer Vision service not configured")
        
        try:
            # Analyze image for various features
            features = [
                "categories", "description", "faces", "image_type", 
                "color", "adult", "tags", "objects"
            ]
            
            analysis = self.client.analyze_image(image_url, visual_features=features)
            
            # Extract key information
            result = {
                "description": self._get_best_description(analysis.description),
                "tags": [tag.name for tag in analysis.tags if tag.confidence > 0.5],
                "objects": [obj.object_property for obj in analysis.objects] if analysis.objects else [],
                "categories": [cat.name for cat in analysis.categories if cat.score > 0.5],
                "colors": {
                    "dominant_colors": analysis.color.dominant_colors,
                    "accent_color": analysis.color.accent_color,
                    "is_bw": analysis.color.is_bw_img
                },
                "faces": len(analysis.faces) if analysis.faces else 0,
                "confidence": self._calculate_overall_confidence(analysis)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to analyze image: {str(e)}")
    
    def generate_story_context(self, image_url: str, user_description: Optional[str] = None) -> str:
        """Generate rich context for story generation from image analysis."""
        analysis = self.analyze_image(image_url)
        
        # Build narrative context
        context_parts = []
        
        # Main description
        if analysis["description"]:
            context_parts.append(f"Scene: {analysis['description']}")
        
        # Objects and elements
        if analysis["objects"]:
            objects_str = ", ".join(analysis["objects"][:5])  # Limit to top 5
            context_parts.append(f"Key elements: {objects_str}")
        
        # Tags for additional context
        if analysis["tags"]:
            relevant_tags = [tag for tag in analysis["tags"][:8] if tag not in analysis.get("objects", [])]
            if relevant_tags:
                tags_str = ", ".join(relevant_tags)
                context_parts.append(f"Atmosphere: {tags_str}")
        
        # Color mood
        colors = analysis["colors"]
        if colors["dominant_colors"]:
            color_mood = self._interpret_color_mood(colors["dominant_colors"], colors["is_bw"])
            context_parts.append(f"Mood: {color_mood}")
        
        # People context
        if analysis["faces"] > 0:
            people_context = f"{analysis['faces']} person" + ("s" if analysis["faces"] > 1 else "")
            context_parts.append(f"Characters: {people_context} visible")
        
        # User's interpretation
        if user_description:
            context_parts.append(f"User's vision: {user_description}")
        
        return " | ".join(context_parts)
    
    def _get_best_description(self, description_result) -> str:
        """Extract the best description from analysis results."""
        if not description_result or not description_result.captions:
            return "A scene with various elements"
        
        # Get the highest confidence caption
        best_caption = max(description_result.captions, key=lambda x: x.confidence)
        return best_caption.text
    
    def _calculate_overall_confidence(self, analysis) -> float:
        """Calculate overall confidence score from analysis."""
        confidences = []
        
        if analysis.description and analysis.description.captions:
            confidences.extend([cap.confidence for cap in analysis.description.captions])
        
        if analysis.tags:
            confidences.extend([tag.confidence for tag in analysis.tags[:5]])
        
        if analysis.categories:
            confidences.extend([cat.score for cat in analysis.categories[:3]])
        
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    def _interpret_color_mood(self, dominant_colors: List[str], is_bw: bool) -> str:
        """Interpret mood from dominant colors."""
        if is_bw:
            return "monochrome, classic"
        
        color_moods = {
            "Red": "energetic, passionate",
            "Blue": "calm, peaceful", 
            "Green": "natural, serene",
            "Yellow": "bright, cheerful",
            "Orange": "warm, vibrant",
            "Purple": "mysterious, magical",
            "Pink": "gentle, playful",
            "Brown": "earthy, rustic",
            "Black": "dramatic, mysterious",
            "White": "pure, clean",
            "Gray": "neutral, balanced"
        }
        
        moods = []
        for color in dominant_colors[:3]:  # Top 3 colors
            if color in color_moods:
                moods.append(color_moods[color])
        
        return ", ".join(moods) if moods else "colorful, dynamic"
    
    def extract_characters_from_image(self, image_url: str) -> List[Dict[str, str]]:
        """Extract potential character information from image."""
        analysis = self.analyze_image(image_url)
        
        characters = []
        
        # If faces detected, create character placeholders
        if analysis["faces"] > 0:
            for i in range(min(analysis["faces"], 3)):  # Max 3 characters
                character = {
                    "name": f"Character {i+1}",
                    "traits": "mysterious, interesting"
                }
                characters.append(character)
        
        # If no faces but objects suggest characters
        elif any(obj in analysis.get("objects", []) for obj in ["person", "people", "child", "man", "woman"]):
            characters.append({
                "name": "Main Character", 
                "traits": "adventurous, curious"
            })
        
        # If animals present
        animal_objects = [obj for obj in analysis.get("objects", []) if obj in ["dog", "cat", "bird", "horse", "animal"]]
        for animal in animal_objects[:2]:  # Max 2 animal characters
            characters.append({
                "name": f"The {animal.title()}",
                "traits": "loyal, brave"
            })
        
        return characters
