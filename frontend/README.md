# Kahaniyaa Frontend

A modern React frontend for the Kahaniyaa multilingual storytelling platform with AI-powered story generation and text-to-speech capabilities.

## Features

- **Story Creation Interface**: Multiple input methods (text scenarios, image uploads, character descriptions)
- **Audio Player**: Full-featured HTML5 audio player with playback controls, speed adjustment, and download
- **Language Support**: English, Hindi, and Tamil with native voice synthesis
- **Voice Customization**: Emotion, accent, and voice style selection
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Modern UI**: Beautiful gradients, animations, and intuitive user experience

## Tech Stack

- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with custom design system
- **HTTP Client**: Axios with interceptors
- **File Upload**: React Dropzone
- **Notifications**: React Hot Toast
- **Icons**: Lucide React
- **Audio**: HTML5 Audio API with custom controls

## Quick Start

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. **Development Server**
   ```bash
   npm run dev
   # Access at: http://localhost:3000
   ```

4. **Build for Production**
   ```bash
   npm run build
   ```

## API Integration

Integrates with the Kahaniyaa API Gateway at `http://localhost:8000`:

- **Stories**: `/v1/stories/` - Create, read, update, delete stories
- **TTS**: `/v1/tts/generate` - Generate audio from text
- **Vision**: `/v1/vision/analyze` - Analyze uploaded images
- **Auth**: `/v1/auth/` - User authentication (future)

## Components

- **App.jsx**: Main application component with state management
- **Header.jsx**: Navigation header with branding
- **StoryCreator.jsx**: Story input form with multiple input types
- **StoryDisplay.jsx**: Story content display with metadata
- **AudioPlayer.jsx**: Full-featured audio player with controls

## Docker Deployment

```bash
# Build and run with Docker
docker build -t kahaniyaa-frontend .
docker run -p 3000:3000 kahaniyaa-frontend

# Or use with docker-compose
docker-compose -f docker-compose.microservices.yml up frontend
```

## Development Notes

- Uses Vite proxy for API calls during development
- Implements proper error handling and loading states
- Responsive design works on mobile and desktop
- Accessible with ARIA labels and keyboard navigation
- Production-ready with Nginx configuration
