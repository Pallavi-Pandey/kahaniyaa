# Kahaniyaa Backend

FastAPI backend for the Kahaniyaa multilingual storytelling platform.

## Features

- **Story Generation**: Create stories from scenarios, images, or characters
- **Multilingual Support**: English, Hindi, Tamil with native prompts
- **Text-to-Speech**: Azure Neural TTS with emotion and voice control
- **Image Analysis**: Azure Computer Vision for image-to-story conversion
- **Async Processing**: Celery + Redis for background job processing
- **RESTful API**: Comprehensive endpoints with OpenAPI documentation

## Quick Start

```bash
# Install dependencies
source ../.venv/bin/activate
uv pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit .env with your API keys

# Start development server
python main.py
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Key Endpoints

- `POST /v1/stories/` - Create new story
- `GET /v1/stories/{id}` - Get story by ID
- `POST /v1/stories/upload-image` - Upload image for story generation
- `GET /v1/voices/presets` - Get available TTS voices
- `GET /v1/test/sample-scenarios` - Get sample scenarios

## Testing

```bash
python test_api.py
```

## Architecture

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Celery**: Async task processing
- **Pydantic**: Data validation and serialization
