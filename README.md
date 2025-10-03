# Kahaniyaa - Multilingual AI Storytelling Platform

Kahaniyaa is a comprehensive storytelling platform that generates engaging stories in multiple languages (English, Hindi, Tamil) with AI-powered text-to-speech narration. The platform supports three input modes: text scenarios, images, and character descriptions.

## 🌟 Features

- **Multilingual Story Generation**: Create stories in English, Hindi, and Tamil
- **Multiple Input Types**: 
  - Text scenarios
  - Image-based story generation with computer vision
  - Character-driven narratives
- **AI-Powered TTS**: Emotional text-to-speech with character voices and accents
- **SSML Support**: Advanced speech synthesis with emotion and prosody control
- **Async Processing**: Background job processing for heavy operations
- **RESTful API**: Complete API for integration with frontend applications

## 🏗️ Architecture

### Core Services
- **Storytelling Service**: FastAPI backend for story generation
- **LLM Service**: OpenAI/Azure integration for story creation
- **TTS Service**: Azure Cognitive Services for multilingual speech synthesis
- **Vision Service**: Azure Computer Vision for image analysis
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Queue System**: Celery with Redis for async processing

### Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **LLM**: OpenAI GPT-4
- **TTS**: Azure Neural Text-to-Speech
- **Vision**: Azure Computer Vision
- **ORM**: SQLAlchemy with Alembic migrations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- OpenAI API key
- Azure Cognitive Services keys

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd kahaniyaa
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

4. **Initialize database**
```bash
alembic upgrade head
```

5. **Start Redis** (for Celery)
```bash
redis-server
```

6. **Start Celery worker** (in separate terminal)
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

7. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Stories
- `POST /v1/stories/` - Create a new story
- `GET /v1/stories/{id}` - Get story by ID
- `GET /v1/stories/` - List user stories
- `POST /v1/stories/{id}/tts` - Regenerate TTS audio
- `POST /v1/stories/upload-image` - Upload image for story generation

#### Voices
- `GET /v1/voices/` - Get available voice presets
- `GET /v1/voices/presets` - Get character voice presets
- `GET /v1/voices/emotions` - Get supported emotions

#### Testing
- `GET /v1/test/sample-scenarios` - Get sample scenarios
- `GET /v1/test/sample-characters` - Get sample character sets
- `POST /v1/test/preview-prompt` - Preview LLM prompts

## 🎯 Usage Examples

### Create a Story from Scenario

```python
import httpx

# Create story from text scenario
story_request = {
    "input_type": "scenario",
    "input_payload": {
        "scenario": "A young girl discovers a magical paintbrush that brings her drawings to life"
    },
    "language": "en",
    "tone": "whimsical",
    "target_audience": "kids",
    "length": 500
}

response = httpx.post("http://localhost:8000/v1/stories/", json=story_request)
story = response.json()
```

### Create Story from Image

```python
# Upload image first
with open("image.jpg", "rb") as f:
    upload_response = httpx.post(
        "http://localhost:8000/v1/stories/upload-image",
        files={"file": f}
    )
image_url = upload_response.json()["image_url"]

# Create story from image
story_request = {
    "input_type": "image", 
    "input_payload": {
        "image_url": image_url,
        "user_description": "A magical forest scene"
    },
    "language": "hi",
    "tone": "adventurous",
    "target_audience": "kids",
    "length": 600
}

response = httpx.post("http://localhost:8000/v1/stories/", json=story_request)
```

### Create Character-Driven Story

```python
story_request = {
    "input_type": "characters",
    "input_payload": {
        "characters": [
            {"name": "Maya", "traits": "curious, brave, loves books"},
            {"name": "Ravi", "traits": "funny, loyal, good at solving puzzles"}
        ],
        "setting": "An old library with secret passages",
        "conflict": "Ancient books are disappearing one by one"
    },
    "language": "ta",
    "tone": "mysterious",
    "target_audience": "kids",
    "length": 700
}

response = httpx.post("http://localhost:8000/v1/stories/", json=story_request)
```

## 🌍 Multilingual Support

### Supported Languages
- **English (en)**: Full feature support
- **Hindi (hi)**: Native language generation and TTS
- **Tamil (ta)**: Native language generation and TTS

### Voice Presets
Each language includes multiple voice options:
- Narrator voices (calm, engaging)
- Character voices (child, adult male/female, elderly)
- Emotion support (cheerful, excited, sad, calm, etc.)

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/kahaniyaa

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Azure Cognitive Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
AZURE_VISION_KEY=your_azure_vision_key_here
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint_here

# App Settings
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
DEBUG=true
```

## 🧪 Testing

### Run Test Endpoints
```bash
# Get sample scenarios
curl http://localhost:8000/v1/test/sample-scenarios

# Preview prompt generation
curl -X POST http://localhost:8000/v1/test/preview-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "scenario",
    "input_data": {"scenario": "A brave little boat"},
    "language": "en",
    "tone": "cheerful"
  }'
```

## 🚧 Development Roadmap

### MVP (Current)
- ✅ FastAPI backend with story generation
- ✅ LLM integration (OpenAI GPT-4)
- ✅ Basic TTS with Azure Neural Speech
- ✅ Image analysis with Azure Computer Vision
- ✅ Multilingual prompt templates
- ✅ Async job processing with Celery

### V1 (Next Phase)
- [ ] Authentication integration (Supabase/Clerk)
- [ ] React frontend with audio player
- [ ] File storage (S3/Supabase Storage)
- [ ] Advanced SSML voice presets
- [ ] Rate limiting and caching
- [ ] User management and story history

### V2 (Future)
- [ ] Real-time story collaboration
- [ ] Advanced character voice training
- [ ] Story analytics and recommendations
- [ ] Mobile app (React Native)
- [ ] Enterprise features and SSO

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 language model
- Microsoft Azure for Cognitive Services
- FastAPI for the excellent web framework
- The open-source community for various libraries and tools