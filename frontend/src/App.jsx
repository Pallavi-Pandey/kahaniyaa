import React, { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header'
import StoryCreator from './components/StoryCreator'
import StoryDisplay from './components/StoryDisplay'
import AudioPlayer from './components/AudioPlayer'
import { BookOpen, Sparkles, Volume2 } from 'lucide-react'

function App() {
  const [currentStory, setCurrentStory] = useState(null)
  const [currentAudio, setCurrentAudio] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleStoryGenerated = (story) => {
    setCurrentStory(story)
  }

  const handleAudioGenerated = (audioData) => {
    setCurrentAudio(audioData)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Toaster position="top-right" />
      
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <BookOpen className="w-12 h-12 text-primary-600" />
            <Sparkles className="w-8 h-8 text-secondary-500" />
          </div>
          <h1 className="text-4xl md:text-6xl font-display font-bold text-gray-900 mb-4">
            Create Amazing Stories
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Transform your ideas into captivating multilingual stories with AI-powered narration
          </p>
          
          {/* Feature highlights */}
          <div className="flex flex-wrap justify-center gap-6 mb-8">
            <div className="flex items-center gap-2 bg-white rounded-full px-4 py-2 shadow-sm">
              <BookOpen className="w-5 h-5 text-primary-600" />
              <span className="text-sm font-medium">Text to Story</span>
            </div>
            <div className="flex items-center gap-2 bg-white rounded-full px-4 py-2 shadow-sm">
              <Sparkles className="w-5 h-5 text-secondary-500" />
              <span className="text-sm font-medium">Image to Story</span>
            </div>
            <div className="flex items-center gap-2 bg-white rounded-full px-4 py-2 shadow-sm">
              <Volume2 className="w-5 h-5 text-green-600" />
              <span className="text-sm font-medium">AI Narration</span>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Story Creator */}
          <div className="space-y-6">
            <StoryCreator 
              onStoryGenerated={handleStoryGenerated}
              onAudioGenerated={handleAudioGenerated}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          </div>

          {/* Story Display & Audio Player */}
          <div className="space-y-6">
            {currentStory && (
              <StoryDisplay 
                story={currentStory}
                onGenerateAudio={handleAudioGenerated}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
              />
            )}
            
            {currentAudio && (
              <AudioPlayer 
                audioData={currentAudio}
                story={currentStory}
              />
            )}
          </div>
        </div>

        {/* Getting Started Section */}
        {!currentStory && (
          <div className="mt-16 text-center">
            <h2 className="text-2xl font-display font-semibold text-gray-900 mb-6">
              How to Get Started
            </h2>
            <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary-600 font-bold text-xl">1</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Choose Input Type</h3>
                <p className="text-gray-600 text-sm">
                  Start with a scenario, upload an image, or describe characters
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-secondary-600 font-bold text-xl">2</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Generate Story</h3>
                <p className="text-gray-600 text-sm">
                  AI creates a unique story based on your input and preferences
                </p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-green-600 font-bold text-xl">3</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Listen & Enjoy</h3>
                <p className="text-gray-600 text-sm">
                  Convert to speech with emotion and enjoy your personalized story
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
