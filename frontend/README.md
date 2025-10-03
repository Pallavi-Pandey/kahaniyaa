# Kahaniyaa Frontend

This directory will contain the React frontend for the Kahaniyaa multilingual storytelling platform.

## Planned Features

- **Story Creation Interface**: Forms for scenario, image, and character-based story generation
- **Audio Player**: HTML5 audio player with playback controls for generated stories
- **File Upload**: Image upload component for image-to-story generation
- **Multilingual Support**: Language selection for English, Hindi, and Tamil
- **Voice Selection**: Choose from different voice presets and emotions
- **Story Library**: Browse and manage generated stories
- **Real-time Status**: Job progress tracking for story generation

## Tech Stack (Planned)

- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS or Material-UI
- **State Management**: React Context or Zustand
- **HTTP Client**: Axios or Fetch API
- **Audio**: HTML5 Audio API
- **File Upload**: React Dropzone
- **Authentication**: Integration with Supabase Auth

## Getting Started

Frontend development will begin after the backend API is fully tested and deployed.

## API Integration

The frontend will connect to the backend API at:
- Development: `http://localhost:8000`
- Production: TBD

Key endpoints to integrate:
- `POST /v1/stories/` - Create new stories
- `GET /v1/stories/` - List user stories
- `POST /v1/stories/upload-image` - Upload images
- `GET /v1/voices/presets` - Get available voices
- `GET /v1/test/sample-*` - Get sample data
