# Kahaniyaa Deployment Guide

Complete guide for running the Kahaniyaa multilingual storytelling platform.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Node.js 18+ (for development mode)
- API keys for OpenAI and Azure services

### 1. Environment Setup

```bash
# Clone and navigate to project
cd kahaniyaa

# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

Required environment variables:
```bash
# OpenAI (for story generation)
OPENAI_API_KEY=your_openai_api_key

# Azure Speech Services (for TTS)
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region

# Azure Computer Vision (for image analysis)
AZURE_VISION_KEY=your_azure_vision_key
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/kahaniyaa

# Redis
REDIS_URL=redis://redis:6379/0

# JWT Secret (generate a strong secret)
JWT_SECRET=your_jwt_secret_key
```

### 2. Production Deployment (Recommended)

**Full microservices stack with all features:**

```bash
# Start all services
docker-compose -f docker-compose.microservices.yml up -d

# Check service health
docker-compose -f docker-compose.microservices.yml ps

# View logs
docker-compose -f docker-compose.microservices.yml logs -f
```

**Access points:**
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Individual Services**: 8001-8004

### 3. Development Mode

**Backend services + Frontend dev server:**

```bash
# Terminal 1: Start backend services
docker-compose -f docker-compose.microservices.yml up -d postgres redis api-gateway auth-service story-service tts-service vision-service

# Terminal 2: Start frontend in development
cd frontend
npm install
npm run dev
```

**Access points:**
- **Frontend Dev**: http://localhost:5173 (with hot reload)
- **Backend Services**: http://localhost:8000-8004

### 4. Monolithic Deployment (Simpler)

**Single backend service + Frontend:**

```bash
# Start monolithic stack
docker-compose up -d

# Access frontend
open http://localhost:3000
```

## 🔧 Service Architecture

### Microservices Stack
```
┌─────────────────┐    ┌──────────────────┐
│   Frontend      │    │   API Gateway    │
│   (React+Nginx) │◄──►│   (Port 8000)    │
│   Port 3000     │    └──────────────────┘
└─────────────────┘              │
                                 ▼
                    ┌─────────────────────────┐
                    │     Microservices       │
                    │                         │
                    │  ┌─────────────────┐    │
                    │  │ Auth Service    │    │
                    │  │ (Port 8001)     │    │
                    │  └─────────────────┘    │
                    │                         │
                    │  ┌─────────────────┐    │
                    │  │ Story Service   │    │
                    │  │ (Port 8002)     │    │
                    │  └─────────────────┘    │
                    │                         │
                    │  ┌─────────────────┐    │
                    │  │ TTS Service     │    │
                    │  │ (Port 8003)     │    │
                    │  └─────────────────┘    │
                    │                         │
                    │  ┌─────────────────┐    │
                    │  │ Vision Service  │    │
                    │  │ (Port 8004)     │    │
                    │  └─────────────────┘    │
                    └─────────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │     Infrastructure      │
                    │                         │
                    │  ┌─────────────────┐    │
                    │  │ PostgreSQL      │    │
                    │  │ (Port 5432)     │    │
                    │  └─────────────────┘    │
                    │                         │
                    │  ┌─────────────────┐    │
                    │  │ Redis           │    │
                    │  │ (Port 6379)     │    │
                    │  └─────────────────┘    │
                    └─────────────────────────┘
```

## 🔍 Verification & Testing

### Health Checks

```bash
# Check all services are running
curl http://localhost:8000/health

# Check individual services
curl http://localhost:8001/health  # Auth
curl http://localhost:8002/health  # Story
curl http://localhost:8003/health  # TTS
curl http://localhost:8004/health  # Vision
```

### Test Story Creation

1. Open http://localhost:3000
2. Click "Create New Story"
3. Enter a story scenario
4. Select language and preferences
5. Click "Create Story"
6. Generate audio narration

### Demo Mode

If backend services aren't available, the frontend automatically runs in demo mode:
- Shows sample stories
- Creates mock stories
- Demonstrates full UI functionality

## 🛠️ Management Commands

### Service Management

```bash
# Start services
docker-compose -f docker-compose.microservices.yml up -d

# Stop services
docker-compose -f docker-compose.microservices.yml down

# Restart specific service
docker-compose -f docker-compose.microservices.yml restart story-service

# View logs
docker-compose -f docker-compose.microservices.yml logs -f story-service

# Scale services
docker-compose -f docker-compose.microservices.yml up -d --scale story-service=2
```

### Database Management

```bash
# Access PostgreSQL
docker exec -it kahaniyaa_postgres psql -U postgres -d kahaniyaa

# Backup database
docker exec kahaniyaa_postgres pg_dump -U postgres kahaniyaa > backup.sql

# Restore database
docker exec -i kahaniyaa_postgres psql -U postgres kahaniyaa < backup.sql
```

### Frontend Management

```bash
# Build frontend
cd frontend
npm run build

# Preview production build
npm run preview

# Lint and fix code
npm run lint
```

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check what's using ports
   lsof -i :3000
   lsof -i :8000
   
   # Kill processes if needed
   kill -9 <PID>
   ```

2. **Docker issues**
   ```bash
   # Clean up Docker
   docker system prune -a
   
   # Rebuild images
   docker-compose -f docker-compose.microservices.yml build --no-cache
   ```

3. **API key issues**
   ```bash
   # Verify environment variables
   docker-compose -f docker-compose.microservices.yml exec story-service env | grep OPENAI
   ```

4. **Database connection issues**
   ```bash
   # Check database logs
   docker-compose -f docker-compose.microservices.yml logs postgres
   
   # Test connection
   docker-compose -f docker-compose.microservices.yml exec postgres psql -U postgres -d kahaniyaa -c "SELECT 1;"
   ```

### Service-Specific Issues

**Story Service:**
- Verify OpenAI API key is valid
- Check API quota and billing
- Review story service logs

**TTS Service:**
- Verify Azure Speech credentials
- Check supported languages/voices
- Monitor audio generation logs

**Vision Service:**
- Verify Azure Computer Vision credentials
- Check image format support
- Review vision processing logs

## 📊 Monitoring

### Service Health

```bash
# Monitor all services
watch -n 5 'docker-compose -f docker-compose.microservices.yml ps'

# Check resource usage
docker stats

# Monitor logs in real-time
docker-compose -f docker-compose.microservices.yml logs -f --tail=100
```

### Performance Metrics

- **Frontend**: Browser dev tools, Lighthouse
- **Backend**: Service logs, response times
- **Database**: Connection pools, query performance
- **Redis**: Memory usage, cache hit rates

## 🔒 Security Considerations

### Production Deployment

1. **Environment Variables**
   - Use secrets management (Azure Key Vault, AWS Secrets Manager)
   - Never commit API keys to version control
   - Rotate keys regularly

2. **Network Security**
   - Use HTTPS in production
   - Configure firewall rules
   - Implement rate limiting

3. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

4. **Container Security**
   - Keep base images updated
   - Scan for vulnerabilities
   - Use non-root users

## 🚀 Production Deployment

### Cloud Deployment Options

1. **Docker Swarm**
2. **Kubernetes**
3. **AWS ECS/Fargate**
4. **Azure Container Instances**
5. **Google Cloud Run**

### Scaling Considerations

- **Horizontal scaling**: Multiple instances of services
- **Load balancing**: Nginx or cloud load balancers
- **Database scaling**: Read replicas, connection pooling
- **Caching**: Redis cluster, CDN for static assets

## 📝 Maintenance

### Regular Tasks

1. **Updates**
   - Update Docker images
   - Update dependencies
   - Security patches

2. **Monitoring**
   - Check service health
   - Monitor resource usage
   - Review error logs

3. **Backups**
   - Database backups
   - Configuration backups
   - User data backups

---

For detailed API documentation, see individual service README files.
For environment setup details, see `ENVIRONMENT_SETUP.md`.
For frontend-specific information, see `frontend/README.md`.
