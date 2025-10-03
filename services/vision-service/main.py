#!/usr/bin/env python3
"""
Kahaniyaa Vision Service
Handles image analysis and processing for story generation
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import sys
import logging
from datetime import datetime
import base64
import uuid

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import from existing backend
from backend.app.services.vision_service import VisionService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kahaniyaa Vision Service",
    description="Image Analysis and Processing Microservice",
    version="1.0.0"
)

# Initialize vision service
vision_service = VisionService()

# Pydantic models
class ImageAnalysisRequest(BaseModel):
    image_url: str
    user_description: Optional[str] = None

class ImageAnalysisResponse(BaseModel):
    image_id: str
    description: str
    user_description: Optional[str]
    tags: List[str]
    objects: List[Dict]
    colors: List[str]
    metadata: Dict
    created_at: datetime

class ImageUploadResponse(BaseModel):
    image_id: str
    image_url: str
    description: str
    user_description: Optional[str]
    file_size: int
    metadata: Dict

# In-memory image storage (replace with cloud storage)
images_db = {}

@app.get("/")
async def root():
    """Vision service health check"""
    return {
        "service": "Kahaniyaa Vision Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vision-service"}

@app.post("/v1/vision/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(request: ImageAnalysisRequest):
    """Analyze an image from URL and extract description"""
    try:
        # Analyze image using vision service
        analysis_result = await vision_service.analyze_image(
            request.image_url,
            request.user_description
        )
        
        image_id = str(uuid.uuid4())
        
        # Create response
        response = ImageAnalysisResponse(
            image_id=image_id,
            description=analysis_result.get("description", ""),
            user_description=request.user_description,
            tags=analysis_result.get("tags", []),
            objects=analysis_result.get("objects", []),
            colors=analysis_result.get("colors", []),
            metadata={
                "image_url": request.image_url,
                "confidence": analysis_result.get("confidence", 0.0),
                "analysis_time": analysis_result.get("analysis_time", 0.0)
            },
            created_at=datetime.utcnow()
        )
        
        # Store analysis result
        images_db[image_id] = response
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

@app.post("/v1/stories/upload-image", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    user_description: Optional[str] = Form(None)
):
    """Upload and analyze an image file for story generation"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Generate unique filename
        image_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{image_id}.{file_extension}"
        
        # In production, save to cloud storage (S3, GCS, etc.)
        # For now, we'll simulate by storing base64 data
        image_base64 = base64.b64encode(file_content).decode('utf-8')
        image_url = f"/v1/vision/images/{image_id}"
        
        # Analyze uploaded image
        analysis_result = await vision_service.analyze_image_data(
            file_content,
            user_description
        )
        
        response = ImageUploadResponse(
            image_id=image_id,
            image_url=image_url,
            description=analysis_result.get("description", ""),
            user_description=user_description,
            file_size=file_size,
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "analysis": analysis_result,
                "image_data": image_base64  # In production, store in cloud storage
            }
        )
        
        # Store image data
        images_db[image_id] = response
        
        return response
        
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

@app.get("/v1/vision/images/{image_id}")
async def get_image(image_id: str):
    """Retrieve image data by ID"""
    image_data = images_db.get(image_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return image_data

@app.get("/v1/vision/images/")
async def list_images(skip: int = 0, limit: int = 10):
    """List all uploaded images with pagination"""
    images = list(images_db.values())
    return images[skip:skip + limit]

@app.delete("/v1/vision/images/{image_id}")
async def delete_image(image_id: str):
    """Delete an image and its analysis"""
    if image_id not in images_db:
        raise HTTPException(status_code=404, detail="Image not found")
    
    del images_db[image_id]
    return {"message": "Image deleted successfully"}

@app.post("/v1/vision/batch-analyze")
async def batch_analyze_images(image_urls: List[str]):
    """Analyze multiple images in batch"""
    results = []
    
    for i, image_url in enumerate(image_urls):
        try:
            request = ImageAnalysisRequest(image_url=image_url)
            result = await analyze_image(request)
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

@app.get("/v1/vision/capabilities")
async def get_vision_capabilities():
    """Get vision service capabilities and supported features"""
    return {
        "supported_formats": ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
        "max_file_size": "10MB",
        "features": [
            "object_detection",
            "scene_description",
            "color_analysis",
            "text_extraction",
            "face_detection",
            "landmark_recognition"
        ],
        "languages": ["en", "hi", "ta"],
        "confidence_threshold": 0.5
    }

# Test endpoints
@app.get("/v1/test/sample-images")
async def get_sample_images():
    """Get sample image URLs for testing"""
    return {
        "sample_images": [
            {
                "id": "sample_1",
                "url": "https://example.com/forest.jpg",
                "description": "A magical forest with tall trees and sunlight filtering through",
                "expected_tags": ["forest", "trees", "nature", "sunlight"]
            },
            {
                "id": "sample_2", 
                "url": "https://example.com/castle.jpg",
                "description": "An ancient castle on a hilltop with clouds in the background",
                "expected_tags": ["castle", "architecture", "hill", "clouds"]
            },
            {
                "id": "sample_3",
                "url": "https://example.com/ocean.jpg", 
                "description": "A calm ocean with a small boat sailing towards the horizon",
                "expected_tags": ["ocean", "boat", "water", "horizon"]
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
