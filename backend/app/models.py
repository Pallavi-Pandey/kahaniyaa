from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class StoryInputType(str, enum.Enum):
    SCENARIO = "scenario"
    IMAGE = "image"
    CHARACTERS = "characters"


class StoryStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    auth_provider_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    stories = relationship("Story", back_populates="user")


class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    language = Column(String, nullable=False)  # en, hi, ta
    input_type = Column(Enum(StoryInputType), nullable=False)
    input_payload = Column(JSON, nullable=False)  # Stores scenario text, image URL, or character data
    story_json = Column(JSON, nullable=True)  # Generated story structure
    audio_urls = Column(JSON, nullable=True)  # List of audio file URLs
    status = Column(Enum(StoryStatus), default=StoryStatus.PENDING)
    tone = Column(String, default="cheerful")  # cheerful, dramatic, whimsical, etc.
    target_audience = Column(String, default="kids")  # kids, adults
    length = Column(Integer, default=500)  # Target word count
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="stories")
    jobs = relationship("Job", back_populates="story")


class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    voice_preset = Column(String)  # Voice ID for TTS
    personality_traits = Column(JSON)  # List of traits
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VoicePreset(Base):
    __tablename__ = "voice_presets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    language = Column(String, nullable=False)  # en, hi, ta
    voice_id = Column(String, nullable=False)  # Provider-specific voice ID
    provider = Column(String, nullable=False)  # azure, google, elevenlabs
    style = Column(String)  # cheerful, calm, excited
    gender = Column(String)  # male, female, neutral
    age_group = Column(String)  # child, adult, elderly
    accent = Column(String)  # indian, british, american
    sample_ssml = Column(Text)  # Example SSML for this preset
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True)  # Celery task ID
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    job_type = Column(String, nullable=False)  # story_generation, tts_generation
    status = Column(Enum(JobStatus), default=JobStatus.QUEUED)
    progress = Column(Integer, default=0)  # 0-100
    error_message = Column(Text)
    result = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    story = relationship("Story", back_populates="jobs")
