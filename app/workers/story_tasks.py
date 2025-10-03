from celery import current_task
from sqlalchemy.orm import Session
from app.workers.celery_app import celery_app
from app.database import SessionLocal
from app.models import Story, Job, StoryStatus, JobStatus
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.vision_service import VisionService
from app.schemas import ScenarioInput, ImageInput, CharactersInput
import json


def get_db_session():
    """Get database session for Celery tasks."""
    return SessionLocal()


@celery_app.task(bind=True)
def generate_story_task(
    self,
    job_id: str,
    story_id: int,
    input_type: str,
    input_payload: dict,
    language: str,
    tone: str,
    target_audience: str,
    length: int
):
    """Celery task to generate story content."""
    
    db = get_db_session()
    llm_service = LLMService()
    vision_service = VisionService()
    
    try:
        # Update job status
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = JobStatus.PROCESSING
            job.progress = 10
            db.commit()
        
        # Update task progress
        self.update_state(state='PROGRESS', meta={'progress': 10, 'status': 'Starting story generation'})
        
        story_content = None
        
        if input_type == "scenario":
            scenario_input = ScenarioInput(**input_payload)
            story_content = llm_service.generate_story_from_scenario(
                scenario_input.scenario, language, tone, target_audience, length
            )
            
        elif input_type == "image":
            image_input = ImageInput(**input_payload)
            
            # Analyze image first
            self.update_state(state='PROGRESS', meta={'progress': 30, 'status': 'Analyzing image'})
            image_context = vision_service.generate_story_context(
                image_input.image_url, image_input.user_description
            )
            
            # Generate story from image context
            self.update_state(state='PROGRESS', meta={'progress': 60, 'status': 'Generating story from image'})
            story_content = llm_service.generate_story_from_image(
                image_context, image_input.user_description, language, tone, target_audience, length
            )
            
        elif input_type == "characters":
            characters_input = CharactersInput(**input_payload)
            story_content = llm_service.generate_story_from_characters(
                characters_input.characters,
                characters_input.setting or "",
                characters_input.conflict or "",
                language, tone, target_audience, length
            )
        
        if not story_content:
            raise Exception("Failed to generate story content")
        
        # Update story in database
        self.update_state(state='PROGRESS', meta={'progress': 80, 'status': 'Saving story'})
        
        story = db.query(Story).filter(Story.id == story_id).first()
        if story:
            story.title = story_content.title
            story.story_json = story_content.dict()
            story.status = StoryStatus.COMPLETED
            db.commit()
        
        # Update job status
        if job:
            job.status = JobStatus.COMPLETED
            job.progress = 100
            job.result = {"story_generated": True, "title": story_content.title}
            db.commit()
        
        self.update_state(state='SUCCESS', meta={'progress': 100, 'status': 'Story generated successfully'})
        
        return {
            "status": "completed",
            "story_id": story_id,
            "title": story_content.title
        }
        
    except Exception as e:
        # Update job with error
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            db.commit()
        
        # Update story status
        story = db.query(Story).filter(Story.id == story_id).first()
        if story:
            story.status = StoryStatus.FAILED
            db.commit()
        
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
        
    finally:
        db.close()


@celery_app.task(bind=True)
def generate_tts_task(
    self,
    job_id: str,
    story_id: int,
    voice_preset: str = None,
    emotion: str = "neutral"
):
    """Celery task to generate TTS audio for story."""
    
    db = get_db_session()
    tts_service = TTSService()
    
    try:
        # Update job status
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = JobStatus.PROCESSING
            job.progress = 10
            db.commit()
        
        # Get story
        story = db.query(Story).filter(Story.id == story_id).first()
        if not story or not story.story_json:
            raise Exception("Story not found or not completed")
        
        self.update_state(state='PROGRESS', meta={'progress': 20, 'status': 'Preparing audio generation'})
        
        # Convert story_json back to StoryContent object
        from app.schemas import StoryContent
        story_content = StoryContent(**story.story_json)
        
        # Generate audio
        self.update_state(state='PROGRESS', meta={'progress': 40, 'status': 'Generating audio files'})
        
        audio_urls = tts_service.generate_audio_for_story(
            story_content, story.language
        )
        
        # Update story with audio URLs
        self.update_state(state='PROGRESS', meta={'progress': 80, 'status': 'Saving audio files'})
        
        story.audio_urls = audio_urls
        db.commit()
        
        # Update job status
        if job:
            job.status = JobStatus.COMPLETED
            job.progress = 100
            job.result = {"audio_files_generated": len(audio_urls)}
            db.commit()
        
        self.update_state(state='SUCCESS', meta={'progress': 100, 'status': 'Audio generated successfully'})
        
        return {
            "status": "completed",
            "story_id": story_id,
            "audio_files": len(audio_urls)
        }
        
    except Exception as e:
        # Update job with error
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            db.commit()
        
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
        
    finally:
        db.close()


@celery_app.task
def cleanup_old_jobs():
    """Periodic task to clean up old completed jobs."""
    
    db = get_db_session()
    
    try:
        from datetime import datetime, timedelta
        
        # Delete jobs older than 7 days
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        old_jobs = db.query(Job).filter(
            Job.created_at < cutoff_date,
            Job.status.in_([JobStatus.COMPLETED, JobStatus.FAILED])
        ).all()
        
        for job in old_jobs:
            db.delete(job)
        
        db.commit()
        
        return f"Cleaned up {len(old_jobs)} old jobs"
        
    except Exception as e:
        db.rollback()
        raise
        
    finally:
        db.close()
