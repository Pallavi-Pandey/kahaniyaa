import axios from 'axios'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth tokens (when implemented)
api.interceptors.request.use(
  (config) => {
    // Add auth token when available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || 
                     error.response.data?.message || 
                     `HTTP ${error.response.status}: ${error.response.statusText}`
      throw new Error(message)
    } else if (error.request) {
      // Request made but no response received
      throw new Error('No response from server. Please check your connection.')
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred')
    }
  }
)

// Story API
export const createStory = async (storyData) => {
  try {
    const response = await api.post('/v1/stories/', storyData)
    return response.data
  } catch (error) {
    console.error('Create story error:', error)
    throw error
  }
}

export const getStory = async (storyId) => {
  try {
    const response = await api.get(`/v1/stories/${storyId}`)
    return response.data
  } catch (error) {
    console.error('Get story error:', error)
    throw error
  }
}

export const listStories = async (params = {}) => {
  try {
    const response = await api.get('/v1/stories/', { params })
    return response.data
  } catch (error) {
    console.error('List stories error:', error)
    throw error
  }
}

export const deleteStory = async (storyId) => {
  try {
    const response = await api.delete(`/v1/stories/${storyId}`)
    return response.data
  } catch (error) {
    console.error('Delete story error:', error)
    throw error
  }
}

// TTS API
export const generateAudio = async (audioData) => {
  try {
    const response = await api.post('/v1/tts/generate', audioData)
    return response.data
  } catch (error) {
    console.error('Generate audio error:', error)
    throw error
  }
}

export const getVoicePresets = async () => {
  try {
    const response = await api.get('/v1/voices/presets')
    return response.data
  } catch (error) {
    console.error('Get voice presets error:', error)
    throw error
  }
}

export const getSupportedLanguages = async () => {
  try {
    const response = await api.get('/v1/voices/languages')
    return response.data
  } catch (error) {
    console.error('Get supported languages error:', error)
    throw error
  }
}

export const getSupportedEmotions = async () => {
  try {
    const response = await api.get('/v1/voices/emotions')
    return response.data
  } catch (error) {
    console.error('Get supported emotions error:', error)
    throw error
  }
}

// Vision API
export const analyzeImage = async (imageData) => {
  try {
    const response = await api.post('/v1/vision/analyze', imageData)
    return response.data
  } catch (error) {
    console.error('Analyze image error:', error)
    throw error
  }
}

export const uploadImage = async (formData) => {
  try {
    const response = await api.post('/v1/vision/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    console.error('Upload image error:', error)
    throw error
  }
}

// Test/Sample Data API
export const getSampleScenarios = async () => {
  try {
    const response = await api.get('/v1/test/sample-scenarios')
    return response.data
  } catch (error) {
    console.error('Get sample scenarios error:', error)
    throw error
  }
}

export const getSampleCharacters = async () => {
  try {
    const response = await api.get('/v1/test/sample-characters')
    return response.data
  } catch (error) {
    console.error('Get sample characters error:', error)
    throw error
  }
}

export const getSampleImages = async () => {
  try {
    const response = await api.get('/v1/test/sample-images')
    return response.data
  } catch (error) {
    console.error('Get sample images error:', error)
    throw error
  }
}

// Health Check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check error:', error)
    throw error
  }
}

// Auth API (for future implementation)
export const login = async (credentials) => {
  try {
    const response = await api.post('/v1/auth/login', credentials)
    const { access_token } = response.data
    if (access_token) {
      localStorage.setItem('auth_token', access_token)
    }
    return response.data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

export const register = async (userData) => {
  try {
    const response = await api.post('/v1/auth/register', userData)
    return response.data
  } catch (error) {
    console.error('Register error:', error)
    throw error
  }
}

export const logout = () => {
  localStorage.removeItem('auth_token')
}

export const getCurrentUser = async () => {
  try {
    const response = await api.get('/v1/auth/me')
    return response.data
  } catch (error) {
    console.error('Get current user error:', error)
    throw error
  }
}

// Utility functions
export const isAuthenticated = () => {
  return !!localStorage.getItem('auth_token')
}

export const getAuthToken = () => {
  return localStorage.getItem('auth_token')
}

export default api
