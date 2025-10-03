#!/bin/bash

# Kahaniyaa Microservices Setup Script
# This script sets up the microservices development environment

set -e  # Exit on any error

echo "Setting up Kahaniyaa Microservices Environment"
echo "=============================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "uv found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies for each service
echo "Installing dependencies for all microservices..."

services=("api-gateway" "auth-service" "story-service" "tts-service" "vision-service")

for service in "${services[@]}"; do
    echo "Installing dependencies for $service..."
    if [ -f "services/$service/requirements.txt" ]; then
        uv pip install -r "services/$service/requirements.txt"
    else
        echo "Warning: requirements.txt not found for $service"
    fi
done

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configuration"
else
    echo ".env file already exists"
fi

# Create necessary directories
mkdir -p services/shared/logs
mkdir -p services/tts-service/audio
mkdir -p services/vision-service/uploads

echo "Created necessary directories"

# Test imports for shared modules
echo "Testing shared module imports..."
cd services
python -c "
try:
    from shared.models import *
    from shared.utils import *
    print('All shared imports successful')
except ImportError as e:
    print(f'Import error: {e}')
    exit(1)
"
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "Microservices Architecture:"
echo "- API Gateway:    http://localhost:8000"
echo "- Auth Service:   http://localhost:8001"
echo "- Story Service:  http://localhost:8002"
echo "- TTS Service:    http://localhost:8003"
echo "- Vision Service: http://localhost:8004"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start all services:"
echo "   docker-compose -f docker-compose.microservices.yml up -d"
echo "3. Or start individual services:"
echo "   cd services/api-gateway && python main.py"
echo "4. Visit http://localhost:8000/docs for API Gateway documentation"
