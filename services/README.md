# Kahaniyaa Microservices Architecture

This directory contains the microservices implementation of the Kahaniyaa multilingual storytelling platform.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │
│   (React)       │◄──►│   (FastAPI)     │
└─────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼─────┐
        │ Auth Service │ │Story Service│ │TTS Service│
        │  (FastAPI)   │ │  (FastAPI)  │ │ (FastAPI) │
        └──────────────┘ └─────────────┘ └───────────┘
                                │
                        ┌───────▼──────┐
                        │Vision Service│
                        │  (FastAPI)   │
                        └──────────────┘
```

## Services

### API Gateway (`api-gateway/`)
- **Purpose**: Single entry point for all client requests
- **Responsibilities**: 
  - Request routing to appropriate services
  - Authentication validation
  - Rate limiting and caching
  - Request/response transformation
- **Port**: 8000

### Auth Service (`auth-service/`)
- **Purpose**: User authentication and authorization
- **Responsibilities**:
  - User registration and login
  - JWT token management
  - User profile management
  - Session handling
- **Port**: 8001

### Story Service (`story-service/`)
- **Purpose**: Core story generation logic
- **Responsibilities**:
  - Story creation from scenarios/images/characters
  - Prompt template management
  - LLM integration (OpenAI/Azure)
  - Story metadata and storage
- **Port**: 8002

### TTS Service (`tts-service/`)
- **Purpose**: Text-to-speech conversion
- **Responsibilities**:
  - Audio generation from text
  - Voice preset management
  - SSML processing
  - Audio file storage and serving
- **Port**: 8003

### Vision Service (`vision-service/`)
- **Purpose**: Image analysis and processing
- **Responsibilities**:
  - Image upload handling
  - Computer vision analysis
  - Image-to-text description
  - Image metadata extraction
- **Port**: 8004

### Shared (`shared/`)
- **Purpose**: Common utilities and models
- **Contents**:
  - Database models
  - Common utilities
  - Shared configurations
  - Inter-service communication helpers

## Communication

- **Synchronous**: HTTP/REST APIs between services
- **Asynchronous**: Redis pub/sub for events
- **Service Discovery**: Environment-based configuration
- **Load Balancing**: Docker Compose with multiple replicas

## Development

```bash
# Start all services
docker-compose up -d

# Start individual service
cd services/story-service
python main.py

# Run tests
cd services/story-service
python -m pytest tests/
```

## Deployment

Each service can be deployed independently:
- Container-based deployment (Docker)
- Kubernetes orchestration
- Cloud-native services (AWS Lambda, Google Cloud Functions)
- Traditional VPS deployment

## Benefits

1. **Scalability**: Scale services independently based on load
2. **Maintainability**: Smaller, focused codebases
3. **Technology Diversity**: Use different tech stacks per service
4. **Fault Isolation**: Service failures don't affect entire system
5. **Team Autonomy**: Different teams can own different services
6. **Deployment Flexibility**: Deploy services independently
