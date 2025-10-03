# Kahaniyaa Deployment Guide

This guide covers different deployment options for the Kahaniyaa storytelling platform.

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.8+
- uv package manager
- API keys (OpenAI, Azure Cognitive Services)

### Setup
```bash
# Clone and setup
git clone <repository-url>
cd kahaniyaa
./setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start development server
source .venv/bin/activate
python main.py
```

Visit `http://localhost:8000/docs` for API documentation.

## 🐳 Docker Deployment

### Development with Docker Compose
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

Services:
- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

### Production Docker
```bash
# Build image
docker build -t kahaniyaa:latest .

# Run with external database
docker run -d \
  --name kahaniyaa-api \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e REDIS_URL="redis://host:6379/0" \
  -e OPENAI_API_KEY="your-key" \
  kahaniyaa:latest
```

## ☁️ Cloud Deployment

### Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Render
1. Create new Web Service from GitHub
2. Set build command: `uv pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

### Heroku
```bash
# Install Heroku CLI and login
heroku create kahaniyaa-app

# Set environment variables
heroku config:set OPENAI_API_KEY="your-key"
heroku config:set AZURE_SPEECH_KEY="your-key"
# ... other variables

# Add PostgreSQL and Redis
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini

# Deploy
git push heroku main
```

### AWS/GCP/Azure
Use container services like:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

## 🗄️ Database Setup

### PostgreSQL
```sql
-- Create database and user
CREATE DATABASE kahaniyaa;
CREATE USER kahaniyaa_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE kahaniyaa TO kahaniyaa_user;
```

### Run Migrations
```bash
source .venv/bin/activate
alembic upgrade head
```

## 🔧 Environment Variables

### Required
```bash
# LLM Service
OPENAI_API_KEY=your_openai_api_key

# Database (optional for testing)
DATABASE_URL=postgresql://user:pass@host:5432/kahaniyaa

# Redis (for Celery)
REDIS_URL=redis://host:6379/0
```

### Optional (Enhanced Features)
```bash
# Azure TTS
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_region

# Azure Vision
AZURE_VISION_KEY=your_azure_vision_key
AZURE_VISION_ENDPOINT=https://your-region.api.cognitive.microsoft.com/

# File Storage
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=kahaniyaa-assets

# App Settings
SECRET_KEY=your_secret_key_change_in_production
ENVIRONMENT=production
DEBUG=false
```

## 🔄 Background Jobs (Celery)

### Start Celery Worker
```bash
# Development
source .venv/bin/activate
celery -A app.workers.celery_app worker --loglevel=info

# Production (with supervisor)
celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
```

### Monitor Jobs
```bash
# Flower (Celery monitoring)
pip install flower
celery -A app.workers.celery_app flower
```

## 📊 Monitoring & Logging

### Health Checks
- API Health: `GET /health`
- Database: Check connection in logs
- Redis: Check Celery worker status

### Logging
```python
# Configure logging in production
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔒 Security Considerations

### Production Checklist
- [ ] Change default SECRET_KEY
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Use secure database credentials
- [ ] Enable database connection pooling
- [ ] Set up proper backup strategy

### Rate Limiting
```python
# Add to main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add to endpoints
@limiter.limit("10/minute")
async def create_story(request: Request, ...):
    ...
```

## 🎯 Performance Optimization

### Database
- Use connection pooling
- Add database indexes
- Implement query optimization
- Set up read replicas for scaling

### Caching
```python
# Redis caching for expensive operations
import redis
cache = redis.Redis.from_url(settings.redis_url)

# Cache story generation results
cache.setex(f"story:{hash(prompt)}", 3600, story_json)
```

### File Storage
- Use CDN for static assets
- Implement file compression
- Set up proper caching headers

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Kahaniyaa

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
          
      - name: Install uv
        run: pip install uv
        
      - name: Install dependencies
        run: uv pip install -r requirements.txt
        
      - name: Run tests
        run: pytest
        
      - name: Deploy to production
        run: |
          # Your deployment script here
```

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database status
   pg_isready -h localhost -p 5432
   
   # Verify credentials
   psql -h localhost -U kahaniyaa_user -d kahaniyaa
   ```

2. **Celery Worker Not Starting**
   ```bash
   # Check Redis connection
   redis-cli ping
   
   # Verify Celery configuration
   celery -A app.workers.celery_app inspect active
   ```

3. **API Keys Not Working**
   ```bash
   # Test OpenAI API
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   
   # Test Azure services
   curl -H "Ocp-Apim-Subscription-Key: $AZURE_SPEECH_KEY" \
        "https://$AZURE_SPEECH_REGION.tts.speech.microsoft.com/cognitiveservices/voices/list"
   ```

4. **High Memory Usage**
   - Implement request timeouts
   - Add memory limits to containers
   - Use streaming for large responses

### Logs Location
- Application: stdout/stderr
- Celery: `/var/log/celery/`
- Database: `/var/log/postgresql/`
- Web server: `/var/log/nginx/` or `/var/log/apache2/`

## 📈 Scaling

### Horizontal Scaling
- Multiple API instances behind load balancer
- Separate Celery workers for different task types
- Database read replicas
- Redis clustering

### Vertical Scaling
- Increase CPU/memory for compute-intensive tasks
- SSD storage for database
- Dedicated GPU instances for AI workloads

## 🔄 Backup & Recovery

### Database Backup
```bash
# Automated backup script
pg_dump -h localhost -U kahaniyaa_user kahaniyaa > backup_$(date +%Y%m%d).sql

# Restore
psql -h localhost -U kahaniyaa_user kahaniyaa < backup_20231201.sql
```

### File Storage Backup
```bash
# S3 sync for uploaded files
aws s3 sync ./uploads/ s3://kahaniyaa-backups/uploads/
```

For more detailed deployment assistance, refer to the platform-specific documentation or contact the development team.
