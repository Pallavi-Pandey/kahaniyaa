from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import aiofiles
import os
from app.database import get_db
from app.models import Story, Job, StoryInputType, StoryStatus, JobStatus
from app.schemas import (
    StoryCreateRequest, StoryResponse, JobResponse, TTSRegenerateRequest,
    ScenarioInput, ImageInput, CharactersInput, ErrorResponse
)
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService
from app.services.vision_service import VisionService
from app.workers.story_tasks import generate_story_task, generate_tts_task

router = APIRouter(prefix="/v1/stories", tags=["stories"])

llm_service = LLMService()
tts_service = TTSService()
vision_service = VisionService()


@router.post("/", response_model=StoryResponse)
async def create_story(
    request: StoryCreateRequest,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Get from auth token
):
    """Create a new story from scenario, image, or characters."""
    
    try:
        # Create story record
        story = Story(
            user_id=user_id,
            title="Generating...",
            language=request.language,
            input_type=request.input_type,
            input_payload=request.input_payload,
            tone=request.tone,
            target_audience=request.target_audience,
            length=request.length,
            status=StoryStatus.PROCESSING
        )
        
        db.add(story)
        db.commit()
        db.refresh(story)
        
        # Create job for async processing
        job_id = str(uuid.uuid4())
        job = Job(
            id=job_id,
            story_id=story.id,
            job_type="story_generation",
            status=JobStatus.QUEUED
        )
        
        db.add(job)
        db.commit()
        
        # Queue story generation task
        generate_story_task.delay(
            job_id=job_id,
            story_id=story.id,
            input_type=request.input_type.value,
            input_payload=request.input_payload,
            language=request.language,
            tone=request.tone,
            target_audience=request.target_audience,
            length=request.length
        )
        
        return StoryResponse(
            id=story.id,
            title=story.title,
            language=story.language,
            input_type=story.input_type,
            status=story.status,
            created_at=story.created_at,
            updated_at=story.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")


@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(story_id: int, db: Session = Depends(get_db)):
    """Get story by ID with current status and content."""
    
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    response = StoryResponse(
        id=story.id,
        title=story.title,
        language=story.language,
        input_type=story.input_type,
        status=story.status,
        created_at=story.created_at,
        updated_at=story.updated_at
    )
    
    # Add story content if completed
    if story.status == StoryStatus.COMPLETED and story.story_json:
        response.story_content = story.story_json
        response.audio_urls = story.audio_urls
    
    return response


@router.get("/", response_model=List[StoryResponse])
async def list_stories(
    skip: int = 0,
    limit: int = 20,
    language: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: Get from auth token
):
    """List user's stories with pagination and filtering."""
    
    query = db.query(Story).filter(Story.user_id == user_id)
    
    if language:
        query = query.filter(Story.language == language)
    
    stories = query.offset(skip).limit(limit).all()
    
    return [
        StoryResponse(
            id=story.id,
            title=story.title,
            language=story.language,
            input_type=story.input_type,
            status=story.status,
            created_at=story.created_at,
            updated_at=story.updated_at
        )
        for story in stories
    ]


@router.post("/{story_id}/tts", response_model=JobResponse)
async def regenerate_tts(
    story_id: int,
    request: TTSRegenerateRequest,
    db: Session = Depends(get_db)
):
    """Regenerate TTS audio for a story with different voice settings."""
    
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    if story.status != StoryStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Story must be completed before regenerating TTS")
    
    # Create TTS job
    job_id = str(uuid.uuid4())
    job = Job(
        id=job_id,
        story_id=story.id,
        job_type="tts_generation",
        status=JobStatus.QUEUED
    )
    
    db.add(job)
    db.commit()
    
    # Queue TTS generation task
    generate_tts_task.delay(
        job_id=job_id,
        story_id=story.id,
        voice_preset=request.voice_preset,
        emotion=request.emotion
    )
    
    return JobResponse(
        id=job.id,
        story_id=job.story_id,
        job_type=job.job_type,
        status=job.status,
        progress=job.progress,
        created_at=job.created_at
    )


@router.delete("/{story_id}")
async def delete_story(story_id: int, db: Session = Depends(get_db)):
    """Delete a story and its associated files."""
    
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # TODO: Delete associated audio files from storage
    
    db.delete(story)
    db.commit()
    
    return {"message": "Story deleted successfully"}


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Upload image for story generation."""
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/images"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)
    
    # TODO: Upload to S3/Supabase Storage and return public URL
    # For now, return local file path
    return {"image_url": f"/uploads/images/{unique_filename}"}


@router.get("/{story_id}/jobs", response_model=List[JobResponse])
async def get_story_jobs(story_id: int, db: Session = Depends(get_db)):
    """Get all jobs for a story."""
    
    jobs = db.query(Job).filter(Job.story_id == story_id).all()
    
    return [
        JobResponse(
            id=job.id,
            story_id=job.story_id,
            job_type=job.job_type,
            status=job.status,
            progress=job.progress,
            error_message=job.error_message,
            created_at=job.created_at
        )
        for job in jobs
    ]
