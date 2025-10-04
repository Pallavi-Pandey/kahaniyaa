import React, { useState } from 'react'
import { toast } from 'react-hot-toast'
import { 
  BookOpen, 
  Volume2, 
  Copy, 
  Download, 
  Share2, 
  RefreshCw,
  Clock,
  User,
  Globe
} from 'lucide-react'
import { generateAudio } from '../services/api'

const StoryDisplay = ({ story, onGenerateAudio, isLoading, setIsLoading }) => {
  const [audioSettings, setAudioSettings] = useState({
    voice: 'default',
    emotion: 'neutral',
    speed: 'normal'
  })

  const handleCopyStory = () => {
    navigator.clipboard.writeText(story.content)
    toast.success('Story copied to clipboard!')
  }

  const handleDownloadStory = () => {
    const element = document.createElement('a')
    const file = new Blob([story.content], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = `${story.title || 'story'}.txt`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
    toast.success('Story downloaded!')
  }

  const handleGenerateAudio = async () => {
    if (!story.content) {
      toast.error('No story content to convert to audio')
      return
    }

    setIsLoading(true)
    
    try {
      const audioData = await generateAudio({
        text: story.content,
        language: story.language || 'en',
        voice: audioSettings.voice,
        emotion: audioSettings.emotion,
        speed: audioSettings.speed
      })
      
      onGenerateAudio(audioData)
      toast.success('Audio generated successfully!')
    } catch (error) {
      console.error('Audio generation failed:', error)
      toast.error(error.message || 'Failed to generate audio')
    } finally {
      setIsLoading(false)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getLanguageName = (code) => {
    const languages = {
      'en': 'English',
      'hi': 'Hindi', 
      'ta': 'Tamil'
    }
    return languages[code] || code
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-display font-semibold text-gray-900">
                {story.title || 'Your Generated Story'}
              </h3>
              <div className="flex items-center gap-4 text-sm text-gray-500 mt-1">
                {story.created_at && (
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>{formatDate(story.created_at)}</span>
                  </div>
                )}
                {story.language && (
                  <div className="flex items-center gap-1">
                    <Globe className="w-4 h-4" />
                    <span>{getLanguageName(story.language)}</span>
                  </div>
                )}
                {story.target_audience && (
                  <div className="flex items-center gap-1">
                    <User className="w-4 h-4" />
                    <span className="capitalize">{story.target_audience}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyStory}
              className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
              title="Copy story"
            >
              <Copy className="w-4 h-4" />
            </button>
            <button
              onClick={handleDownloadStory}
              className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
              title="Download story"
            >
              <Download className="w-4 h-4" />
            </button>
            <button
              className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
              title="Share story"
            >
              <Share2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <div className="card-content space-y-6">
        {/* Story Metadata */}
        {(story.tone || story.input_type) && (
          <div className="flex flex-wrap gap-2">
            {story.tone && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {story.tone}
              </span>
            )}
            {story.input_type && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                {story.input_type.replace('_', ' ')}
              </span>
            )}
          </div>
        )}

        {/* Story Content */}
        <div className="prose prose-gray max-w-none">
          <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
            <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
              {story.content}
            </div>
          </div>
        </div>

        {/* Audio Generation Section */}
        <div className="border-t border-gray-200 pt-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Volume2 className="w-5 h-5" />
            Generate Audio
          </h4>
          
          {/* Audio Settings */}
          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Voice Style
              </label>
              <select
                className="input"
                value={audioSettings.voice}
                onChange={(e) => setAudioSettings(prev => ({ ...prev, voice: e.target.value }))}
              >
                <option value="default">Default</option>
                <option value="child_friendly">Child Friendly</option>
                <option value="storyteller">Storyteller</option>
                <option value="narrator">Narrator</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Emotion
              </label>
              <select
                className="input"
                value={audioSettings.emotion}
                onChange={(e) => setAudioSettings(prev => ({ ...prev, emotion: e.target.value }))}
              >
                <option value="neutral">Neutral</option>
                <option value="happy">Happy</option>
                <option value="excited">Excited</option>
                <option value="calm">Calm</option>
                <option value="dramatic">Dramatic</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Speed
              </label>
              <select
                className="input"
                value={audioSettings.speed}
                onChange={(e) => setAudioSettings(prev => ({ ...prev, speed: e.target.value }))}
              >
                <option value="slow">Slow</option>
                <option value="normal">Normal</option>
                <option value="fast">Fast</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleGenerateAudio}
            disabled={isLoading}
            className="btn-primary w-full md:w-auto"
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Generating Audio...</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Volume2 className="w-4 h-4" />
                <span>Generate Audio</span>
              </div>
            )}
          </button>
        </div>

        {/* Story Stats */}
        {story.content && (
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {story.content.split(' ').length}
                </div>
                <div className="text-sm text-gray-600">Words</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {story.content.length}
                </div>
                <div className="text-sm text-gray-600">Characters</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {Math.ceil(story.content.split(' ').length / 200)}
                </div>
                <div className="text-sm text-gray-600">Min Read</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {Math.ceil(story.content.split(' ').length / 150)}
                </div>
                <div className="text-sm text-gray-600">Min Listen</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default StoryDisplay
