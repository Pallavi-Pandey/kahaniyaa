from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kahaniyaa API Gateway",
    description="Central API Gateway for Kahaniyaa Microservices",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "story": os.getenv("STORY_SERVICE_URL", "http://localhost:8002"),
    "tts": os.getenv("TTS_SERVICE_URL", "http://localhost:8003"),
    "vision": os.getenv("VISION_SERVICE_URL", "http://localhost:8004"),
}

# HTTP client for service communication
client = httpx.AsyncClient(timeout=30.0)

@app.get("/")
async def root():
    """API Gateway health check"""
    return {
        "service": "Kahaniyaa API Gateway",
        "status": "healthy",
        "version": "1.0.0",
        "services": SERVICES
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check for all services"""
    health_status = {"gateway": "healthy", "services": {}}
    
    for service_name, service_url in SERVICES.items():
        try:
            response = await client.get(f"{service_url}/health", timeout=5.0)
            health_status["services"][service_name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "url": service_url
            }
        except Exception as e:
            health_status["services"][service_name] = {
                "status": "unreachable",
                "error": str(e),
                "url": service_url
            }
    
    return health_status

# Auth Service Routes
@app.post("/v1/auth/register")
async def register(request: Request):
    """Proxy to auth service for user registration"""
    return await proxy_request("auth", "/v1/auth/register", request)

@app.post("/v1/auth/login")
async def login(request: Request):
    """Proxy to auth service for user login"""
    return await proxy_request("auth", "/v1/auth/login", request)

@app.get("/v1/auth/me")
async def get_current_user(request: Request):
    """Proxy to auth service for current user info"""
    return await proxy_request("auth", "/v1/auth/me", request)

# Story Service Routes
@app.post("/v1/stories/")
async def create_story(request: Request):
    """Proxy to story service for story creation"""
    return await proxy_request("story", "/v1/stories/", request)

@app.get("/v1/stories/{story_id}")
async def get_story(story_id: str, request: Request):
    """Proxy to story service for story retrieval"""
    return await proxy_request("story", f"/v1/stories/{story_id}", request)

@app.get("/v1/stories/")
async def list_stories(request: Request):
    """Proxy to story service for story listing"""
    return await proxy_request("story", "/v1/stories/", request)

# Frontend-expected story routes
@app.get("/v1/story/stories")
async def get_stories_frontend(request: Request):
    """Proxy to story service for frontend story listing"""
    return await proxy_request("story", "/v1/story/stories", request)

@app.get("/v1/story/languages")
async def get_story_languages(request: Request):
    """Proxy to story service for supported languages"""
    return await proxy_request("story", "/v1/story/languages", request)

@app.get("/v1/story/tones")
async def get_story_tones(request: Request):
    """Proxy to story service for supported tones"""
    return await proxy_request("story", "/v1/story/tones", request)

@app.get("/v1/story/audiences")
async def get_story_audiences(request: Request):
    """Proxy to story service for target audiences"""
    return await proxy_request("story", "/v1/story/audiences", request)

@app.post("/v1/story/generate")
async def generate_story(request: Request):
    """Proxy to story service for story generation"""
    return await proxy_request("story", "/v1/story/generate", request)

@app.post("/v1/story/create")
async def create_story_frontend(request: Request):
    """Proxy to story service for story creation"""
    return await proxy_request("story", "/v1/story/create", request)

# TTS Service Routes
@app.post("/v1/tts/generate")
async def generate_audio(request: Request):
    """Proxy to TTS service for audio generation"""
    return await proxy_request("tts", "/v1/tts/generate", request)

@app.get("/v1/voices/presets")
async def get_voice_presets(request: Request):
    """Proxy to TTS service for voice presets"""
    return await proxy_request("tts", "/v1/voices/presets", request)

# Vision Service Routes
@app.post("/v1/vision/analyze")
async def analyze_image(request: Request):
    """Proxy to vision service for image analysis"""
    return await proxy_request("vision", "/v1/vision/analyze", request)

@app.post("/v1/stories/upload-image")
async def upload_image(request: Request):
    """Proxy to vision service for image upload"""
    return await proxy_request("vision", "/v1/stories/upload-image", request)

# Test Routes (aggregate from multiple services)
@app.get("/v1/test/sample-scenarios")
async def get_sample_scenarios():
    """Get sample scenarios from story service"""
    try:
        response = await client.get(f"{SERVICES['story']}/v1/test/sample-scenarios")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Story service unavailable: {str(e)}")

async def proxy_request(service_name: str, path: str, request: Request):
    """Generic proxy function for forwarding requests to microservices"""
    service_url = SERVICES.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    try:
        # Get request body
        body = await request.body()
        
        # Forward headers (excluding host)
        headers = dict(request.headers)
        headers.pop("host", None)
        
        # Make request to microservice
        response = await client.request(
            method=request.method,
            url=f"{service_url}{path}",
            content=body,
            headers=headers,
            params=dict(request.query_params)
        )
        
        # Return response
        return JSONResponse(
            content=response.json() if response.content else {},
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except httpx.RequestError as e:
        logger.error(f"Request to {service_name} failed: {str(e)}")
        raise HTTPException(
            status_code=503, 
            detail=f"Service {service_name} unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error proxying to {service_name}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error"
        )

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await client.aclose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
