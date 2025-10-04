# Kahaniyaa Frontend

A modern React-based frontend for the Kahaniyaa multilingual storytelling platform. Built with Vite, Tailwind CSS, and designed to work seamlessly with the microservices backend.

## 🚀 Features

- **Multi-input Story Creation**: Create stories from text scenarios, image uploads, or character definitions
- **Multilingual Support**: English, Hindi (हिन्दी), and Tamil (தமிழ்) language support
- **Audio Narration**: AI-powered text-to-speech with emotion and accent support
- **Responsive Design**: Modern, mobile-first UI with beautiful animations
- **Real-time Audio Player**: Custom audio player with waveform visualization
- **Docker Ready**: Containerized with Nginx for production deployment

## 🛠️ Tech Stack

- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with custom components
- **Icons**: Lucide React
- **HTTP Client**: Axios with interceptors
- **Build Tool**: Vite with hot reload
- **Linting**: ESLint with React plugins
- **Container**: Docker with Nginx

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.jsx       # App header with branding
│   │   ├── StoryCreator.jsx # Story creation form
│   │   ├── StoryDisplay.jsx # Story viewer with audio
│   │   ├── AudioPlayer.jsx  # Custom audio player
│   │   └── LoadingSpinner.jsx # Loading states
│   ├── services/
│   │   └── api.js           # API service layer
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # React entry point
│   └── index.css            # Global styles and Tailwind
├── public/                  # Static assets
├── dist/                    # Build output
├── package.json             # Dependencies and scripts
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS config
├── postcss.config.js        # PostCSS config
├── eslint.config.js         # ESLint configuration
├── Dockerfile               # Multi-stage Docker build
├── nginx.conf               # Nginx configuration
├── docker-entrypoint.sh     # Docker startup script
└── .dockerignore            # Docker ignore patterns
```

## 🚦 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Docker (for containerized deployment)

### Development Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:5173`

3. **Build for production**:
   ```bash
   npm run build
   ```

4. **Preview production build**:
   ```bash
   npm run preview
   ```

### Environment Variables

The frontend supports runtime environment configuration:

- `API_BASE_URL`: Backend API base URL (default: `/api`)
- `APP_NAME`: Application name (default: `Kahaniyaa`)
- `APP_VERSION`: Application version (default: `1.0.0`)
- `ENVIRONMENT`: Environment name (default: `production`)

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -t kahaniyaa-frontend .

# Run the container
docker run -p 3000:80 \
  -e API_BASE_URL=/api \
  -e ENVIRONMENT=production \
  kahaniyaa-frontend
```

### With Docker Compose

The frontend is included in both docker-compose configurations:

```bash
# Monolithic setup
docker-compose up frontend

# Microservices setup
docker-compose -f docker-compose.microservices.yml up frontend
```

## 🔧 Configuration

### Vite Configuration

- **Proxy**: API requests are proxied to `http://localhost:8000` in development
- **Build**: Optimized production builds with code splitting
- **HMR**: Hot module replacement for fast development

### Tailwind CSS

Custom configuration includes:

- **Custom Colors**: Primary and secondary color schemes
- **Typography**: Inter and Poppins font families
- **Animations**: Custom fade-in and pulse animations
- **Components**: Pre-built button, form, and card styles

### Nginx Configuration

Production-ready Nginx setup:

- **Gzip Compression**: Enabled for all text assets
- **Caching**: Long-term caching for static assets
- **API Proxy**: Routes `/api/*` requests to backend services
- **Security Headers**: XSS protection and content security policy
- **Health Check**: `/health` endpoint for monitoring

## 📱 Components

### StoryCreator
- Multi-input story creation (text, image, characters)
- Language and tone selection
- Real-time form validation
- Loading states and error handling

### StoryDisplay
- Rich story content display
- Audio generation and playback
- Social sharing capabilities
- Story metadata and details

### AudioPlayer
- Custom HTML5 audio player
- Waveform visualization
- Volume and playback controls
- Download functionality

## 🌐 API Integration

The frontend communicates with backend microservices through:

- **Auth Service**: User authentication and authorization
- **Story Service**: Story generation and management
- **TTS Service**: Text-to-speech audio generation
- **Vision Service**: Image analysis and processing

### API Service Layer

Located in `src/services/api.js`:

- **Axios Configuration**: Base URL, timeout, and interceptors
- **Error Handling**: Centralized error processing
- **Mock Mode**: Development fallback when backend unavailable
- **Token Management**: Automatic JWT token handling

## 🎨 Styling Guide

### Design System

- **Colors**: Primary (blue), secondary (purple), accent (yellow)
- **Typography**: Hierarchical text scales with semantic classes
- **Spacing**: Consistent 4px grid system
- **Shadows**: Layered elevation system
- **Animations**: Subtle transitions and micro-interactions

### Component Classes

```css
/* Buttons */
.btn-primary    /* Primary action button */
.btn-secondary  /* Secondary action button */
.btn-outline    /* Outlined button variant */

/* Forms */
.form-group     /* Form field container */
.form-label     /* Field labels */
.input          /* Text inputs */
.textarea       /* Text areas */

/* Cards */
.card           /* Base card container */
.story-card     /* Story-specific card styling */

/* Audio */
.audio-player   /* Audio player container */
.audio-controls /* Player control layout */
.audio-progress /* Progress bar styling */
```

## 🔍 Development

### Code Quality

- **ESLint**: React and JavaScript best practices
- **Prettier**: Consistent code formatting (via ESLint)
- **Git Hooks**: Pre-commit linting (can be added)

### Performance

- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Dead code elimination
- **Asset Optimization**: Image and font optimization
- **Lazy Loading**: Component-level lazy loading

### Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

## 🚀 Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] API endpoints accessible
- [ ] SSL/HTTPS enabled
- [ ] CDN configured (optional)
- [ ] Monitoring and logging setup
- [ ] Error tracking (Sentry, etc.)

### Performance Optimization

- **Nginx Gzip**: Reduces bundle size by ~70%
- **Asset Caching**: Long-term caching for static files
- **Code Splitting**: Reduces initial bundle size
- **Image Optimization**: WebP format support

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Node.js version (18+ required)
   - Clear `node_modules` and reinstall
   - Verify Tailwind CSS configuration

2. **API Connection Issues**:
   - Verify backend services are running
   - Check proxy configuration in `vite.config.js`
   - Confirm API base URL environment variable

3. **Docker Issues**:
   - Ensure Docker daemon is running
   - Check port conflicts (3000, 80)
   - Verify environment variables in container

### Debug Mode

Enable debug logging by setting:
```bash
DEBUG=true npm run dev
```

## 📄 License

This project is part of the Kahaniyaa platform. See the main project README for licensing information.

## 🤝 Contributing

1. Follow the existing code style and conventions
2. Add tests for new components and features
3. Update documentation for API changes
4. Ensure Docker builds pass before submitting PRs

---

For more information about the complete Kahaniyaa platform, see the main project documentation.
