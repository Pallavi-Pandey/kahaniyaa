#!/bin/bash

# Kahaniyaa Development Setup Script
# This script sets up the development environment for the Kahaniyaa storytelling platform

set -e

echo "🎭 Setting up Kahaniyaa Development Environment"
echo "=============================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv found: $(uv --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
uv venv

# Activate virtual environment and install dependencies
echo "📚 Installing dependencies..."
source .venv/bin/activate
uv pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys and database credentials"
else
    echo "✅ .env file already exists"
fi

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads/images uploads/audio

# Test basic imports
echo "🧪 Testing basic imports..."
source .venv/bin/activate
python -c "
try:
    from app.config import settings
    from app.models import Base
    from app.services.prompt_templates import PromptTemplates
    print('✅ All core modules imported successfully')
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - OPENAI_API_KEY (required for story generation)"
echo "   - AZURE_SPEECH_KEY & AZURE_SPEECH_REGION (for TTS)"
echo "   - AZURE_VISION_KEY & AZURE_VISION_ENDPOINT (for image analysis)"
echo "   - DATABASE_URL (for PostgreSQL, optional for testing)"
echo ""
echo "2. Start the development server:"
echo "   source .venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "4. For production deployment, set up PostgreSQL and Redis:"
echo "   - PostgreSQL for data storage"
echo "   - Redis for Celery task queue"
echo ""
echo "Happy storytelling! 📚✨"
