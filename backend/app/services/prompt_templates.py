"""
Prompt templates for different story generation scenarios.
These templates are optimized for multilingual storytelling with proper structure.
"""

from typing import Dict, List


class PromptTemplates:
    
    @staticmethod
    def get_scenario_prompt(
        scenario: str, 
        language: str, 
        tone: str, 
        target_audience: str, 
        length: int
    ) -> Dict[str, str]:
        """Get system and user prompts for scenario-based story generation."""
        
        language_names = {"en": "English", "hi": "Hindi", "ta": "Tamil"}
        lang_name = language_names.get(language, "English")
        
        # Language-specific instructions
        lang_instructions = {
            "en": "Use vivid imagery and engaging dialogue. Include cultural references appropriate for English speakers.",
            "hi": "हिंदी में प्राकृतिक और सुंदर भाषा का प्रयोग करें। भारतीय संस्कृति के तत्वों को शामिल करें।",
            "ta": "தமிழில் இயற்கையான மற்றும் அழகான மொழியைப் பயன்படுத்துங்கள். தமிழ் கலாச்சார கூறுகளை உள்ளடக்குங்கள்।"
        }
        
        system_prompt = f"""You are a master storyteller specializing in {lang_name} stories for {target_audience}. 

Create engaging, {tone} stories that captivate your audience. {lang_instructions.get(language, '')}

IMPORTANT: Output ONLY valid JSON in this exact structure:
{{
  "title": "Story title in {lang_name}",
  "scenes": [
    {{
      "id": 1,
      "title": "Scene title",
      "narration": "Descriptive narrative text",
      "dialogue": [
        {{
          "character": "Character name",
          "line": "What the character says",
          "emotion": "neutral/cheerful/excited/sad/angry/calm"
        }}
      ]
    }}
  ]
}}

Guidelines:
- Create 3-5 scenes for a complete story arc
- Keep total length around {length} words
- Include vivid descriptions and engaging dialogue
- Each character should have distinct personality in their speech
- Use appropriate cultural context for {lang_name}
- Ensure the tone is consistently {tone}
- Make it age-appropriate for {target_audience}"""

        user_prompt = f"Create a {tone} story in {lang_name} for {target_audience} based on this scenario: {scenario}"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
    
    @staticmethod
    def get_image_prompt(
        image_description: str,
        user_description: str,
        language: str,
        tone: str,
        target_audience: str,
        length: int
    ) -> Dict[str, str]:
        """Get prompts for image-based story generation."""
        
        language_names = {"en": "English", "hi": "Hindi", "ta": "Tamil"}
        lang_name = language_names.get(language, "English")
        
        lang_instructions = {
            "en": "Use the image as inspiration but expand creatively beyond what's visible.",
            "hi": "चित्र से प्रेरणा लें लेकिन दिखाई देने वाली चीजों से आगे बढ़कर रचनात्मक कहानी बनाएं।",
            "ta": "படத்திலிருந்து உத்வேகம் பெறுங்கள் ஆனால் காணக்கூடியவற்றைத் தாண்டி ஆக்கபூர்வமாக விரிவுபடுத்துங்கள்।"
        }
        
        context = f"Image analysis: {image_description}"
        if user_description:
            context += f"\nUser's interpretation: {user_description}"
        
        system_prompt = f"""You are a master storyteller who creates {lang_name} stories inspired by images.

{lang_instructions.get(language, '')}

IMPORTANT: Output ONLY valid JSON in this exact structure:
{{
  "title": "Story title in {lang_name}",
  "scenes": [
    {{
      "id": 1,
      "title": "Scene title", 
      "narration": "Descriptive narrative text",
      "dialogue": [
        {{
          "character": "Character name",
          "line": "What the character says",
          "emotion": "neutral/cheerful/excited/sad/angry/calm"
        }}
      ]
    }}
  ]
}}

Guidelines:
- Use the image as a starting point, not a limitation
- Create 3-5 scenes with a complete story arc
- Target approximately {length} words
- Maintain a {tone} tone throughout
- Make it appropriate for {target_audience}
- Include rich sensory details beyond what's in the image
- Develop characters with distinct voices"""

        user_prompt = f"Create a {tone} story in {lang_name} for {target_audience} inspired by: {context}"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
    
    @staticmethod
    def get_characters_prompt(
        characters: List[Dict[str, str]],
        setting: str,
        conflict: str,
        language: str,
        tone: str,
        target_audience: str,
        length: int
    ) -> Dict[str, str]:
        """Get prompts for character-driven story generation."""
        
        language_names = {"en": "English", "hi": "Hindi", "ta": "Tamil"}
        lang_name = language_names.get(language, "English")
        
        # Build character descriptions
        char_descriptions = []
        for char in characters:
            name = char.get("name", "Unknown")
            traits = char.get("traits", "mysterious")
            char_descriptions.append(f"• {name}: {traits}")
        
        context_parts = [f"Characters:\n" + "\n".join(char_descriptions)]
        
        if setting:
            context_parts.append(f"Setting: {setting}")
        if conflict:
            context_parts.append(f"Central conflict: {conflict}")
        
        context = "\n\n".join(context_parts)
        
        lang_instructions = {
            "en": "Focus on character development and meaningful interactions. Each character should have a unique voice.",
            "hi": "चरित्र विकास और अर्थपूर्ण बातचीत पर ध्यान दें। हर पात्र की अपनी अलग आवाज़ होनी चाहिए।",
            "ta": "பாத்திர வளர்ச்சி மற்றும் அர்த்தமுள்ள தொடர்புகளில் கவனம் செலுத்துங்கள். ஒவ்வொரு பாத்திரமும் தனித்துவமான குரலைக் கொண்டிருக்க வேண்டும்।"
        }
        
        system_prompt = f"""You are a master storyteller specializing in character-driven {lang_name} stories for {target_audience}.

{lang_instructions.get(language, '')}

IMPORTANT: Output ONLY valid JSON in this exact structure:
{{
  "title": "Story title in {lang_name}",
  "scenes": [
    {{
      "id": 1,
      "title": "Scene title",
      "narration": "Descriptive narrative text", 
      "dialogue": [
        {{
          "character": "Character name (must match provided characters)",
          "line": "What the character says",
          "emotion": "neutral/cheerful/excited/sad/angry/calm"
        }}
      ]
    }}
  ]
}}

Guidelines:
- Each provided character MUST appear and have meaningful dialogue
- Create 3-5 scenes showing character growth and interaction
- Target approximately {length} words
- Maintain a {tone} tone throughout
- Make it appropriate for {target_audience}
- Show character relationships and development
- Each character should have a distinct speaking style
- Build to a satisfying resolution of the conflict"""

        user_prompt = f"Create a {tone} character-driven story in {lang_name} for {target_audience} with:\n\n{context}"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
    
    @staticmethod
    def get_sample_scenarios() -> Dict[str, List[str]]:
        """Get sample scenarios for testing in different languages."""
        
        return {
            "en": [
                "A young girl discovers a magical paintbrush that brings her drawings to life",
                "Two unlikely animal friends must work together to save their forest home",
                "A shy boy finds confidence when he discovers he can talk to plants",
                "A group of children build a time machine in their backyard shed"
            ],
            "hi": [
                "एक छोटी लड़की को एक जादुई तूलिका मिलती है जो उसके चित्रों को जीवंत बना देती है",
                "दो अलग-अलग जानवर मित्रों को अपने जंगल के घर को बचाने के लिए मिलकर काम करना पड़ता है",
                "एक शर्मीला लड़का आत्मविश्वास पाता है जब उसे पता चलता है कि वह पेड़-पौधों से बात कर सकता है"
            ],
            "ta": [
                "ஒரு சிறுமி தன் ஓவியங்களை உயிர்ப்பிக்கும் மாயக் கூரையைக் கண்டுபிடிக்கிறாள்",
                "இரண்டு வேறுபட்ட விலங்கு நண்பர்கள் தங்கள் காட்டு வீட்டைக் காப்பாற்ற ஒன்றாக வேலை செய்ய வேண்டும்",
                "ஒரு கூச்ச சுபாவமுள்ள பையன் தாவரங்களுடன் பேச முடியும் என்பதை அறிந்தபோது தன்னம்பிக்கை பெறுகிறான்"
            ]
        }
    
    @staticmethod
    def get_sample_characters() -> List[Dict[str, any]]:
        """Get sample character sets for testing."""
        
        return [
            {
                "characters": [
                    {"name": "Maya", "traits": "curious, brave, loves books"},
                    {"name": "Ravi", "traits": "funny, loyal, good at solving puzzles"},
                    {"name": "Whiskers", "traits": "wise old cat, mysterious, magical"}
                ],
                "setting": "An old library with secret passages",
                "conflict": "Ancient books are disappearing one by one"
            },
            {
                "characters": [
                    {"name": "Arjun", "traits": "kind-hearted, determined, loves nature"},
                    {"name": "Priya", "traits": "clever, resourceful, speaks multiple languages"},
                    {"name": "Baloo", "traits": "gentle giant bear, protective, wise"}
                ],
                "setting": "A mountain village during monsoon season", 
                "conflict": "The village's water source is mysteriously drying up"
            },
            {
                "characters": [
                    {"name": "Kavi", "traits": "artistic, dreamer, sees beauty everywhere"},
                    {"name": "Meera", "traits": "practical, leader, cares for others"},
                    {"name": "Surya", "traits": "energetic, optimistic, never gives up"}
                ],
                "setting": "A colorful marketplace in an ancient city",
                "conflict": "The annual festival is in danger of being cancelled"
            }
        ]
