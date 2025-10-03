#!/bin/bash

# Kahaniyaa Development Setup Script
# This script sets up the development environment for the Kahaniyaa storytelling platform

set -e  # Exit on any error

echo "Setting up Kahaniyaa Development Environment"
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

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source .venv/bin/activate
uv pip install -r backend/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configuration"
else
    echo ".env file already exists"
fi

# Create uploads directory in backend
mkdir -p backend/uploads
echo "Created backend/uploads directory"

# Test imports
echo "Testing Python imports..."
cd backend
python -c "
try:
    from app.config import settings
    from app.models import Base
    from app.services.llm_service import LLMService
    from app.services.tts_service import TTSService
    from app.services.vision_service import VisionService
    print('All imports successful')
except ImportError as e:
    print(f'Import error: {e}')
    exit(1)
"
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start the backend development server:"
echo "   source .venv/bin/activate"
echo "   cd backend && python main.py"
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "4. Run tests with: cd backend && python test_api.py"
