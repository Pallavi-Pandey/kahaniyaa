import azure.cognitiveservices.speech as speechsdk
from typing import List, Dict, Optional
import tempfile
import os
from app.config import settings
from app.schemas import StoryContent, DialogueLine


class TTSService:
    def __init__(self):
        if settings.azure_speech_key and settings.azure_speech_region:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=settings.azure_speech_key,
                region=settings.azure_speech_region
            )
        else:
            self.speech_config = None
    
    def get_voice_for_language(self, language: str, character: str = "narrator", emotion: str = "neutral") -> str:
        """Get appropriate voice ID based on language and character."""
        voice_map = {
            "en": {
                "narrator": "en-US-AriaNeural",
                "child": "en-US-JennyNeural", 
                "adult_male": "en-US-GuyNeural",
                "adult_female": "en-US-AriaNeural",
                "elderly": "en-US-DavisNeural"
            },
            "hi": {
                "narrator": "hi-IN-SwaraNeural",
                "child": "hi-IN-SwaraNeural",
                "adult_male": "hi-IN-MadhurNeural", 
                "adult_female": "hi-IN-SwaraNeural",
                "elderly": "hi-IN-MadhurNeural"
            },
            "ta": {
                "narrator": "ta-IN-PallaviNeural",
                "child": "ta-IN-PallaviNeural",
                "adult_male": "ta-IN-ValluvarNeural",
                "adult_female": "ta-IN-PallaviNeural", 
                "elderly": "ta-IN-ValluvarNeural"
            }
        }
        
        lang_voices = voice_map.get(language, voice_map["en"])
        return lang_voices.get(character.lower(), lang_voices["narrator"])
    
    def create_ssml(self, text: str, voice: str, emotion: str = "neutral", rate: str = "0%", pitch: str = "0%") -> str:
        """Create SSML markup for enhanced speech synthesis."""
        
        # Map emotions to Azure styles
        style_map = {
            "neutral": "chat",
            "cheerful": "cheerful", 
            "excited": "excited",
            "sad": "sad",
            "angry": "angry",
            "calm": "calm",
            "gentle": "gentle"
        }
        
        style = style_map.get(emotion, "chat")
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
               xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="{voice}">
                <mstts:express-as style="{style}">
                    <prosody rate="{rate}" pitch="{pitch}">
                        {text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """
        return ssml.strip()
    
    def generate_audio_for_story(self, story: StoryContent, language: str) -> List[str]:
        """Generate audio files for each scene in the story."""
        if not self.speech_config:
            raise Exception("Azure Speech service not configured")
        
        audio_urls = []
        
        for scene in story.scenes:
            # Generate audio for narration
            if scene.narration:
                narrator_voice = self.get_voice_for_language(language, "narrator")
                narration_ssml = self.create_ssml(scene.narration, narrator_voice, "calm")
                narration_file = self._synthesize_speech(narration_ssml, f"scene_{scene.id}_narration")
                if narration_file:
                    audio_urls.append(narration_file)
            
            # Generate audio for each dialogue line
            for i, dialogue in enumerate(scene.dialogue):
                character_voice = self.get_voice_for_language(
                    language, 
                    self._get_character_type(dialogue.character),
                    dialogue.emotion
                )
                dialogue_ssml = self.create_ssml(
                    dialogue.line, 
                    character_voice, 
                    dialogue.emotion
                )
                dialogue_file = self._synthesize_speech(
                    dialogue_ssml, 
                    f"scene_{scene.id}_dialogue_{i}"
                )
                if dialogue_file:
                    audio_urls.append(dialogue_file)
        
        return audio_urls
    
    def generate_single_audio(self, text: str, language: str, voice_preset: str = None, emotion: str = "neutral") -> Optional[str]:
        """Generate a single audio file from text."""
        if not self.speech_config:
            raise Exception("Azure Speech service not configured")
        
        voice = voice_preset or self.get_voice_for_language(language, "narrator")
        ssml = self.create_ssml(text, voice, emotion)
        
        return self._synthesize_speech(ssml, "single_audio")
    
    def _synthesize_speech(self, ssml: str, filename_prefix: str) -> Optional[str]:
        """Synthesize speech from SSML and save to temporary file."""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_file.close()
            
            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file.name)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Synthesize speech
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # TODO: Upload to S3/Supabase Storage and return public URL
                # For now, return local file path
                return temp_file.name
            else:
                # Clean up failed file
                os.unlink(temp_file.name)
                return None
                
        except Exception as e:
            print(f"TTS synthesis failed: {str(e)}")
            return None
    
    def _get_character_type(self, character_name: str) -> str:
        """Determine character type from name for voice selection."""
        name_lower = character_name.lower()
        
        if any(word in name_lower for word in ["child", "kid", "little", "young"]):
            return "child"
        elif any(word in name_lower for word in ["old", "elder", "grand"]):
            return "elderly"
        elif any(word in name_lower for word in ["man", "boy", "father", "dad", "king", "prince"]):
            return "adult_male"
        elif any(word in name_lower for word in ["woman", "girl", "mother", "mom", "queen", "princess"]):
            return "adult_female"
        else:
            return "narrator"
    
    def get_available_voices(self, language: str = None) -> List[Dict[str, str]]:
        """Get list of available voice presets."""
        voices = [
            # English voices
            {"id": "en-US-AriaNeural", "name": "Aria (English)", "language": "en", "gender": "female", "style": "conversational"},
            {"id": "en-US-GuyNeural", "name": "Guy (English)", "language": "en", "gender": "male", "style": "conversational"},
            {"id": "en-US-JennyNeural", "name": "Jenny (English)", "language": "en", "gender": "female", "style": "cheerful"},
            
            # Hindi voices
            {"id": "hi-IN-SwaraNeural", "name": "Swara (Hindi)", "language": "hi", "gender": "female", "style": "conversational"},
            {"id": "hi-IN-MadhurNeural", "name": "Madhur (Hindi)", "language": "hi", "gender": "male", "style": "conversational"},
            
            # Tamil voices
            {"id": "ta-IN-PallaviNeural", "name": "Pallavi (Tamil)", "language": "ta", "gender": "female", "style": "conversational"},
            {"id": "ta-IN-ValluvarNeural", "name": "Valluvar (Tamil)", "language": "ta", "gender": "male", "style": "conversational"},
        ]
        
        if language:
            voices = [v for v in voices if v["language"] == language]
        
        return voices
