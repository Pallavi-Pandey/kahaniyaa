# Kahaniyaa Environment Setup Guide

## Overview
This guide helps you configure the environment variables required for the Kahaniyaa multilingual storytelling platform microservices.

## Required Environment Variables

### 1. OpenAI Configuration (Story Service)
```bash
OPENAI_API_KEY=your_openai_api_key_here
```
- **Purpose**: Used by the Story Service for AI-powered story generation
- **How to get**: Sign up at [OpenAI Platform](https://platform.openai.com/) and create an API key
- **Cost**: Pay-per-use pricing based on tokens consumed

### 2. Azure Speech Services (TTS Service)
```bash
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
```
- **Purpose**: Used by the TTS Service for multilingual text-to-speech conversion
- **How to get**: 
  1. Create an Azure account at [Azure Portal](https://portal.azure.com/)
  2. Create a "Speech Services" resource
  3. Copy the key and region from the resource overview
- **Supported regions**: eastus, westus2, westeurope, etc.

### 3. Azure Computer Vision (Vision Service)
```bash
AZURE_VISION_KEY=your_azure_vision_key_here
AZURE_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
```
- **Purpose**: Used by the Vision Service for image analysis and description
- **How to get**:
  1. Create an Azure account at [Azure Portal](https://portal.azure.com/)
  2. Create a "Computer Vision" resource
  3. Copy the key and endpoint from the resource overview

### 4. Database Configuration
```bash
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/kahaniyaa
REDIS_URL=redis://redis:6379/0
```
- **Purpose**: Database connections for PostgreSQL and Redis
- **Default**: Pre-configured for Docker Compose setup
- **Modify**: Only if using external database services

### 5. JWT Authentication
```bash
JWT_SECRET_KEY=your_super_secret_jwt_key_here_minimum_32_characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```
- **Purpose**: Used by Auth Service for secure token generation
- **Generate**: Use a strong random string (minimum 32 characters)

## Setup Instructions

### Option 1: Using .env File (Recommended)
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your actual API keys:
   ```bash
   nano .env
   ```

3. Fill in all the required values:
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=sk-your-openai-key-here
   
   # Azure Speech Services
   AZURE_SPEECH_KEY=your-speech-key-here
   AZURE_SPEECH_REGION=eastus
   
   # Azure Computer Vision
   AZURE_VISION_KEY=your-vision-key-here
   AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   
   # JWT Configuration
   JWT_SECRET_KEY=your-super-secret-jwt-key-minimum-32-chars
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   
   # Database URLs (default for Docker)
   DATABASE_URL=postgresql://postgres:postgres@postgres:5432/kahaniyaa
   REDIS_URL=redis://redis:6379/0
   ```

### Option 2: Export Environment Variables
```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
export AZURE_SPEECH_KEY="your-speech-key-here"
export AZURE_SPEECH_REGION="eastus"
export AZURE_VISION_KEY="your-vision-key-here"
export AZURE_VISION_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
export JWT_SECRET_KEY="your-super-secret-jwt-key-minimum-32-chars"
```

## Testing Configuration

### 1. Start the services:
```bash
docker-compose -f docker-compose.microservices.yml up -d
```

### 2. Check service health:
```bash
# API Gateway (should show all services healthy)
curl http://localhost:8000/health

# Individual services
curl http://localhost:8001/health  # Auth Service
curl http://localhost:8002/health  # Story Service  
curl http://localhost:8003/health  # TTS Service
curl http://localhost:8004/health  # Vision Service
```

### 3. Test functionality:
```bash
# Test story generation
curl -X POST http://localhost:8000/v1/stories/ \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "scenario",
    "input_data": {"scenario": "A brave little mouse goes on an adventure"},
    "language": "en",
    "tone": "cheerful"
  }'

# Test TTS generation
curl -X POST http://localhost:8000/v1/tts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of our text-to-speech service!",
    "language": "en",
    "voice_preset": "narrator_calm"
  }'
```

## Troubleshooting

### Missing API Keys
- **Symptoms**: Services start but return "Mock" responses or errors
- **Solution**: Ensure all API keys are properly set in your `.env` file

### Invalid API Keys
- **Symptoms**: HTTP 401/403 errors from external services
- **Solution**: Verify your API keys are correct and have sufficient quota

### Network Issues
- **Symptoms**: Services can't communicate with each other
- **Solution**: Ensure all services are on the same Docker network (`kahaniyaa-network`)

### Port Conflicts
- **Symptoms**: Services fail to start with port binding errors
- **Solution**: Check if ports 8000-8004, 3000, 5434, 6380 are available

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use strong, unique JWT secret keys**
3. **Rotate API keys regularly**
4. **Use environment-specific configurations**
5. **Monitor API usage and costs**

## Cost Optimization

### OpenAI API
- Use GPT-3.5-turbo for cost efficiency
- Implement request caching for repeated queries
- Set reasonable token limits

### Azure Services
- Choose appropriate pricing tiers
- Monitor usage through Azure portal
- Set up billing alerts

## Production Deployment

For production environments:
1. Use managed database services (Azure Database, AWS RDS)
2. Implement proper secrets management (Azure Key Vault, AWS Secrets Manager)
3. Set up monitoring and logging
4. Configure auto-scaling and load balancing
5. Implement proper backup strategies

## Support

If you encounter issues:
1. Check the service logs: `docker-compose logs <service-name>`
2. Verify environment variables are loaded: `docker exec <container> env`
3. Test API endpoints individually
4. Consult the main README.md for additional troubleshooting steps
