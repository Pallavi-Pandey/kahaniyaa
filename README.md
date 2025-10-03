# Kahaniyaa - Multilingual AI Storytelling Platform

A comprehensive storytelling platform that generates engaging stories from scenarios, images, or characters with multilingual support and text-to-speech capabilities.

## Features

- **Multiple Input Types**: Create stories from text scenarios, images, or character descriptions
- **Multilingual Support**: English, Hindi, Tamil with native language prompts
- **AI-Powered Generation**: OpenAI GPT-4 integration for creative storytelling
- **Text-to-Speech**: Azure Neural TTS with emotion and voice control
- **Image Analysis**: Azure Computer Vision for image-to-story conversion
- **Async Processing**: Celery + Redis for background job processing
- **RESTful API**: Comprehensive FastAPI backend with OpenAPI documentation

## Project Structure

```
kahaniyaa/
├── backend/                 # FastAPI backend application
│   ├── app/                # Main application code
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic (LLM, TTS, Vision)
│   │   ├── workers/       # Celery tasks
│   │   └── models.py      # Database models
│   ├── alembic/           # Database migrations
│   ├── uploads/           # File uploads
│   ├── main.py           # FastAPI app entry point
│   ├── requirements.txt  # Python dependencies
│   └── test_api.py       # API tests
├── frontend/              # React frontend (planned)
├── .env.example          # Environment template
├── docker-compose.yml    # Docker services
└── setup.sh             # Development setup script
```

## Architecture

### Core Services
- **Auth Service**: External provider (Supabase Auth recommended)
- **Storytelling Service**: FastAPI backend for story generation
- **TTS Service**: Azure/Google/ElevenLabs for emotion + accent support
- **Vision Service**: Azure Computer Vision for image analysis
- **Assets Service**: S3/Supabase Storage for audio/images
- **Frontend**: React/Next.js with audio player (planned)

### Tech Stack
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Queue**: Redis + Celery for async processing
- **AI Services**: OpenAI GPT-4, Azure Cognitive Services
- **Deployment**: Docker + docker-compose

## Quick Start

### Microservices Architecture (Recommended)

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd kahaniyaa
   chmod +x services/microservices-setup.sh
   ./services/microservices-setup.sh
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run All Microservices**
   ```bash
   docker-compose -f docker-compose.microservices.yml up -d
   ```

4. **Test Services**
   ```bash
   python services/test-microservices.py
   ```

5. **Access Services**
   - API Gateway: http://localhost:8000
   - Auth Service: http://localhost:8001
   - Story Service: http://localhost:8002
   - TTS Service: http://localhost:8003
   - Vision Service: http://localhost:8004

### Monolithic Backend (Legacy)

1. **Setup**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Run with Docker**
   ```bash
   docker-compose up -d
   # Access at: http://localhost:8080
   ```

3. **Or run locally**
   ```bash
   source .venv/bin/activate
   cd backend
   uvicorn app.main:app --reload
   # Access at: http://localhost:8000
   ```

### Using Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

## API Usage

### Create Story from Scenario
```bash
curl -X POST "http://localhost:8000/v1/stories/" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "scenario",
    "input_data": {"scenario": "A brave little boat goes on an adventure"},
    "language": "en",
    "tone": "cheerful",
    "target_audience": "kids"
  }'
```
### Upload Image for Story
```bash
curl -X POST "http://localhost:8000/v1/stories/upload-image" \
  -F "file=@image.jpg" \
  -F "user_description=A magical forest scene"
```

## Multilingual Support

- **English**: Full support with multiple voice options
- **Hindi**: Native prompts with Devanagari script support
- **Tamil**: Native prompts with Tamil script support

## Voice Features

- **Multiple Voices**: 7+ neural voices across languages
- **Emotion Control**: Happy, sad, excited, calm, mysterious
- **SSML Support**: Advanced speech synthesis markup
- **Character Voices**: Different voices for different characters

## Documentation

- **API Docs**: http://localhost:8000/docs
- **Backend**: [backend/README.md](backend/README.md)
- **Frontend**: [frontend/README.md](frontend/README.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

## Testing

```bash
# Test API endpoints
cd backend && python test_api.py

# Run with sample data
curl http://localhost:8000/v1/test/sample-scenarios
```

## Configuration

Key environment variables:

```env
# API Keys
OPENAI_API_KEY=your_openai_key
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_region
AZURE_VISION_KEY=your_vision_key
AZURE_VISION_ENDPOINT=your_endpoint

# Database
DATABASE_URL=postgresql://user:pass@localhost/kahaniyaa

# Redis
REDIS_URL=redis://localhost:6379/0
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Local development
- Docker deployment
- Cloud platforms (AWS, GCP, Azure)
- Environment setup
- Scaling considerations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- Microsoft Azure for Cognitive Services
- FastAPI community
- Contributors and testers

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

## Multilingual Support

### Supported Languages
- **English (en)**: Full feature support
- **Hindi (hi)**: Native language generation and TTS
- **Tamil (ta)**: Native language generation and TTS

### Voice Presets
Each language includes multiple voice options:
- Narrator voices (calm, engaging)
- Character voices (child, adult male/female, elderly)
- Emotion support (cheerful, excited, sad, calm, etc.)

## Configuration

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

## Testing

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

## Development Roadmap

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 language model
- Microsoft Azure for Cognitive Services
- FastAPI for the excellent web framework
- The open-source community for various libraries and tools