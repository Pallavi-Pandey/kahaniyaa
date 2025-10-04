import React, { useState, useEffect } from 'react';
import { Clock, Globe, Palette, Users, Volume2, Share2, Trash2, BookOpen } from 'lucide-react';
import { ttsAPI, apiUtils } from '../services/api';
import AudioPlayer from './AudioPlayer';
import LoadingSpinner from './LoadingSpinner';

const StoryDisplay = ({ story, onDelete }) => {
  const [audioData, setAudioData] = useState(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [audioError, setAudioError] = useState('');
  const [selectedVoice, setSelectedVoice] = useState('narrator_calm');
  const [voicePresets, setVoicePresets] = useState([]);

  useEffect(() => {
    loadVoicePresets();
  }, [story.language]);

  const loadVoicePresets = async () => {
    try {
      if (!apiUtils.mockMode) {
        const response = await ttsAPI.getVoicePresets(story.language);
        setVoicePresets(response.data);
      } else {
        setVoicePresets(mockData.voicePresets);
      }
    } catch (err) {
      console.error('Failed to load voice presets:', err);
    }
  };

  const generateAudio = async () => {
    setAudioLoading(true);
    setAudioError('');

    try {
      const ttsRequest = {
        text: story.content,
        language: story.language,
        voice_preset: selectedVoice,
        emotion: story.tone === 'cheerful' ? 'happy' : 
                story.tone === 'mysterious' ? 'mysterious' : 'neutral',
        speed: 1.0,
        pitch: 1.0
      };

      const response = await ttsAPI.generateAudio(ttsRequest);
      setAudioData(response.data);
    } catch (err) {
      const errorInfo = apiUtils.handleError(err);
      setAudioError(errorInfo.message);
    } finally {
      setAudioLoading(false);
    }
  };

  const shareStory = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: story.title,
          text: story.content.substring(0, 200) + '...',
          url: window.location.href
        });
      } catch (err) {
        console.log('Share cancelled');
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(`${story.title}\n\n${story.content}`);
      alert('Story copied to clipboard!');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getLanguageName = (code) => {
    const langMap = {
      'en': 'English',
      'hi': 'हिन्दी',
      'ta': 'தமிழ்'
    };
    return langMap[code] || code;
  };

  return (
    <div className="story-card animate-fade-in">
      {/* Story Header */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{story.title}</h2>
            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <Clock className="h-4 w-4" />
                <span>{formatDate(story.created_at)}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Globe className="h-4 w-4" />
                <span>{getLanguageName(story.language)}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Palette className="h-4 w-4" />
                <span className="capitalize">{story.tone}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Users className="h-4 w-4" />
                <span className="capitalize">{story.target_audience}</span>
              </div>
              <div className="flex items-center space-x-1">
                <BookOpen className="h-4 w-4" />
                <span>{story.metadata?.length || story.content.length} words</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={shareStory}
              className="btn btn-outline btn-sm"
              title="Share Story"
            >
              <Share2 className="h-4 w-4" />
            </button>
            {onDelete && (
              <button
                onClick={() => onDelete(story.id)}
                className="btn btn-outline btn-sm text-red-600 hover:bg-red-50"
                title="Delete Story"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Story Content */}
      <div className="p-6">
        <div className="story-content">
          <div className="prose prose-gray max-w-none">
            {story.content.split('\n').map((paragraph, index) => (
              <p key={index} className="mb-4 leading-relaxed text-gray-800">
                {paragraph}
              </p>
            ))}
          </div>
        </div>
      </div>

      {/* Audio Section */}
      <div className="p-6 bg-gray-50 border-t border-gray-100">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
              <Volume2 className="h-5 w-5" />
              <span>Audio Narration</span>
            </h3>
            
            {!audioData && (
              <div className="flex items-center space-x-4">
                {voicePresets.length > 0 && (
                  <select
                    value={selectedVoice}
                    onChange={(e) => setSelectedVoice(e.target.value)}
                    className="input text-sm"
                  >
                    {voicePresets.map(preset => (
                      <option key={preset.id} value={preset.id}>
                        {preset.name} ({preset.gender})
                      </option>
                    ))}
                  </select>
                )}
                
                <button
                  onClick={generateAudio}
                  disabled={audioLoading}
                  className="btn btn-primary btn-sm"
                >
                  {audioLoading ? (
                    <LoadingSpinner size="sm" text="" />
                  ) : (
                    <>
                      <Volume2 className="h-4 w-4 mr-2" />
                      Generate Audio
                    </>
                  )}
                </button>
              </div>
            )}
          </div>

          {audioError && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{audioError}</p>
            </div>
          )}

          {audioLoading && (
            <div className="text-center py-8">
              <LoadingSpinner size="lg" text="Generating audio narration..." />
            </div>
          )}

          {audioData && (
            <AudioPlayer
              audioData={audioData.audio_data}
              audioUrl={audioData.audio_url}
              title={story.title}
            />
          )}

          {!audioData && !audioLoading && !audioError && (
            <div className="text-center py-8 text-gray-500">
              <Volume2 className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Click "Generate Audio" to create an audio narration of this story</p>
            </div>
          )}
        </div>
      </div>

      {/* Story Metadata */}
      {story.metadata && (
        <div className="p-6 bg-gray-50 border-t border-gray-100">
          <details className="group">
            <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
              Story Details
            </summary>
            <div className="mt-3 text-sm text-gray-600 space-y-2">
              <div><strong>Input Type:</strong> {story.input_type}</div>
              <div><strong>Target Length:</strong> {story.length} words</div>
              {story.metadata.input_data && (
                <div>
                  <strong>Original Input:</strong>
                  <pre className="mt-1 p-2 bg-gray-100 rounded text-xs overflow-auto">
                    {JSON.stringify(story.metadata.input_data, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </details>
        </div>
      )}
    </div>
  );
};

export default StoryDisplay;
