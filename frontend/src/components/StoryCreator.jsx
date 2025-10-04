import React, { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'react-hot-toast'
import { 
  FileText, 
  Image, 
  Users, 
  Upload, 
  Wand2, 
  Globe,
  Volume2,
  Heart,
  Smile,
  Frown,
  Zap
} from 'lucide-react'
import { createStory, generateAudio } from '../services/api'

const StoryCreator = ({ onStoryGenerated, onAudioGenerated, isLoading, setIsLoading }) => {
  const [inputType, setInputType] = useState('scenario')
  const [formData, setFormData] = useState({
    scenario: '',
    characters: '',
    language: 'en',
    tone: 'cheerful',
    target_audience: 'kids',
    voice: 'default',
    emotion: 'neutral'
  })
  const [uploadedImage, setUploadedImage] = useState(null)

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
    { code: 'ta', name: 'Tamil', flag: '🇮🇳' }
  ]

  const tones = [
    { value: 'cheerful', label: 'Cheerful', icon: Smile, color: 'text-yellow-500' },
    { value: 'adventurous', label: 'Adventurous', icon: Zap, color: 'text-orange-500' },
    { value: 'calm', label: 'Calm', icon: Heart, color: 'text-blue-500' },
    { value: 'mysterious', label: 'Mysterious', icon: Frown, color: 'text-purple-500' }
  ]

  const audiences = [
    { value: 'kids', label: 'Kids (3-8 years)' },
    { value: 'children', label: 'Children (8-12 years)' },
    { value: 'teens', label: 'Teens (13-17 years)' },
    { value: 'adults', label: 'Adults (18+ years)' }
  ]

  const emotions = [
    { value: 'neutral', label: 'Neutral' },
    { value: 'happy', label: 'Happy' },
    { value: 'excited', label: 'Excited' },
    { value: 'calm', label: 'Calm' },
    { value: 'dramatic', label: 'Dramatic' }
  ]

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = () => {
        setUploadedImage({
          file,
          preview: reader.result,
          name: file.name
        })
      }
      reader.readAsDataURL(file)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  })

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.scenario && !formData.characters && !uploadedImage) {
      toast.error('Please provide some input to generate a story')
      return
    }

    setIsLoading(true)
    
    try {
      let inputData = {}
      
      if (inputType === 'scenario') {
        inputData = { scenario: formData.scenario }
      } else if (inputType === 'characters') {
        inputData = { characters: formData.characters }
      } else if (inputType === 'image' && uploadedImage) {
        // Convert image to base64
        const base64 = uploadedImage.preview.split(',')[1]
        inputData = { 
          image_data: base64,
          image_name: uploadedImage.name
        }
      }

      const storyData = {
        input_type: inputType,
        input_data: inputData,
        language: formData.language,
        tone: formData.tone,
        target_audience: formData.target_audience
      }

      const story = await createStory(storyData)
      onStoryGenerated(story)
      toast.success('Story generated successfully!')

      // Auto-generate audio if story is created
      if (story.content) {
        try {
          const audioData = await generateAudio({
            text: story.content,
            language: formData.language,
            voice: formData.voice,
            emotion: formData.emotion
          })
          onAudioGenerated(audioData)
          toast.success('Audio generated successfully!')
        } catch (audioError) {
          console.error('Audio generation failed:', audioError)
          toast.error('Story created but audio generation failed')
        }
      }

    } catch (error) {
      console.error('Story generation failed:', error)
      toast.error(error.message || 'Failed to generate story')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="text-2xl font-display font-semibold text-gray-900">
          Create Your Story
        </h2>
        <p className="text-gray-600">
          Choose your input method and let AI create a magical story
        </p>
      </div>

      <div className="card-content">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Input Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              How would you like to start?
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { type: 'scenario', icon: FileText, label: 'Text Scenario' },
                { type: 'image', icon: Image, label: 'Upload Image' },
                { type: 'characters', icon: Users, label: 'Characters' }
              ].map(({ type, icon: Icon, label }) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setInputType(type)}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    inputType === type
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300 text-gray-600'
                  }`}
                >
                  <Icon className="w-6 h-6 mx-auto mb-2" />
                  <span className="text-sm font-medium">{label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Input Content */}
          <div>
            {inputType === 'scenario' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Describe your story scenario
                </label>
                <textarea
                  className="textarea"
                  rows={4}
                  placeholder="A brave little mouse goes on an adventure to find the magical cheese..."
                  value={formData.scenario}
                  onChange={(e) => handleInputChange('scenario', e.target.value)}
                />
              </div>
            )}

            {inputType === 'characters' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Describe your characters
                </label>
                <textarea
                  className="textarea"
                  rows={4}
                  placeholder="A curious cat named Whiskers and a wise old owl named Hoot..."
                  value={formData.characters}
                  onChange={(e) => handleInputChange('characters', e.target.value)}
                />
              </div>
            )}

            {inputType === 'image' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload an image
                </label>
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                    isDragActive
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <input {...getInputProps()} />
                  {uploadedImage ? (
                    <div className="space-y-3">
                      <img
                        src={uploadedImage.preview}
                        alt="Preview"
                        className="w-32 h-32 object-cover rounded-lg mx-auto"
                      />
                      <p className="text-sm text-gray-600">{uploadedImage.name}</p>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation()
                          setUploadedImage(null)
                        }}
                        className="text-sm text-red-600 hover:text-red-700"
                      >
                        Remove
                      </button>
                    </div>
                  ) : (
                    <div>
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-gray-600">
                        {isDragActive
                          ? 'Drop the image here...'
                          : 'Drag & drop an image, or click to select'}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        PNG, JPG, GIF up to 10MB
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Settings Grid */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Language Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Globe className="w-4 h-4 inline mr-1" />
                Language
              </label>
              <select
                className="input"
                value={formData.language}
                onChange={(e) => handleInputChange('language', e.target.value)}
              >
                {languages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Target Audience */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience
              </label>
              <select
                className="input"
                value={formData.target_audience}
                onChange={(e) => handleInputChange('target_audience', e.target.value)}
              >
                {audiences.map(audience => (
                  <option key={audience.value} value={audience.value}>
                    {audience.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Tone Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Story Tone
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {tones.map(({ value, label, icon: Icon, color }) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => handleInputChange('tone', value)}
                  className={`p-3 rounded-lg border-2 transition-all ${
                    formData.tone === value
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Icon className={`w-5 h-5 mx-auto mb-1 ${color}`} />
                  <span className="text-sm font-medium">{label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Voice Settings */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Volume2 className="w-4 h-4 inline mr-1" />
                Voice Style
              </label>
              <select
                className="input"
                value={formData.voice}
                onChange={(e) => handleInputChange('voice', e.target.value)}
              >
                <option value="default">Default</option>
                <option value="child_friendly">Child Friendly</option>
                <option value="storyteller">Storyteller</option>
                <option value="narrator">Narrator</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Emotion
              </label>
              <select
                className="input"
                value={formData.emotion}
                onChange={(e) => handleInputChange('emotion', e.target.value)}
              >
                {emotions.map(emotion => (
                  <option key={emotion.value} value={emotion.value}>
                    {emotion.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary w-full h-12 text-base font-medium disabled:opacity-50"
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Creating Story...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-2">
                <Wand2 className="w-5 h-5" />
                <span>Generate Story</span>
              </div>
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default StoryCreator
