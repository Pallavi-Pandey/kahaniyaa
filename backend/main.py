from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import stories, voices, test_endpoints
from app.database import engine
from app.models import Base
import os

# Create database tables (only if database is available)
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Warning: Database not available - {e}")
    print("API will run in limited mode without database features")

# Create FastAPI app
app = FastAPI(
    title="Kahaniyaa API",
    description="Multilingual storytelling platform with AI-generated stories and TTS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(stories.router)
app.include_router(voices.router)
app.include_router(test_endpoints.router)

# Serve static files (uploaded images, audio files)
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Kahaniyaa API",
        "description": "Multilingual storytelling platform",
        "version": "1.0.0",
        "docs": "/docs",
        "supported_languages": ["en", "hi", "ta"],
        "features": [
            "Story generation from scenarios",
            "Story generation from images", 
            "Story generation from characters",
            "Text-to-speech with emotions",
            "Multilingual support",
            "Character voices"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "kahaniyaa-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
