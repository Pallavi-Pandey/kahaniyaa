import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StoryCreator from './components/StoryCreator';
import StoryDisplay from './components/StoryDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorBoundary from './components/ErrorBoundary';
import { storyAPI, apiUtils } from './services/api';
import { AlertCircle, RefreshCw, Plus, BookOpen } from 'lucide-react';

function App() {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreator, setShowCreator] = useState(false);
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    checkHealth();
    loadStories();
  }, []);

  const checkHealth = async () => {
    const response = await apiUtils.checkHealth();
    setHealthStatus(response.data);
  };

  const loadStories = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await storyAPI.getStories();
      setStories(response.data.stories || []);
    } catch (err) {
      // In demo mode, load mock stories instead of showing error
      console.warn('Backend unavailable, loading mock stories');
      const { mockData } = await import('./services/api');
      setStories(mockData.stories);
    } finally {
      setLoading(false);
    }
  };

  const handleStoryCreated = (newStory) => {
    setStories(prev => [newStory, ...prev]);
    setShowCreator(false);
  };

  const handleDeleteStory = async (storyId) => {
    if (!confirm('Are you sure you want to delete this story?')) {
      return;
    }

    try {
      await storyAPI.deleteStory(storyId);
      setStories(prev => prev.filter(story => story.id !== storyId));
    } catch (err) {
      const errorInfo = apiUtils.handleError(err);
      alert(`Failed to delete story: ${errorInfo.message}`);
    }
  };

  const renderHealthStatus = () => {
    if (!healthStatus) return null;

    const statusColors = {
      healthy: 'bg-green-50 border-green-200 text-green-800',
      degraded: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      error: 'bg-red-50 border-red-200 text-red-800'
    };

    return (
      <div className={`mb-6 p-4 border rounded-lg ${statusColors[healthStatus.status] || statusColors.error}`}>
        <div className="flex items-center space-x-2">
          <AlertCircle className="h-5 w-5" />
          <span className="font-medium">
            System Status: {healthStatus.status === 'healthy' ? 'All Services Online' : 
                          healthStatus.status === 'degraded' ? 'Some Services Degraded' : 
                          'Services Unavailable'}
          </span>
          <button
            onClick={checkHealth}
            className="ml-auto p-1 hover:bg-black hover:bg-opacity-10 rounded"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
        {healthStatus.message && (
          <p className="mt-2 text-sm">{healthStatus.message}</p>
        )}
        {healthStatus.services && Object.keys(healthStatus.services).length > 0 && (
          <div className="mt-2 text-sm">
            <details>
              <summary className="cursor-pointer">Service Details</summary>
              <div className="mt-2 space-y-1">
                {Object.entries(healthStatus.services).map(([service, status]) => (
                  <div key={service} className="flex justify-between">
                    <span>{service}:</span>
                    <span className={status === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                      {String(status)}
                    </span>
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}
      </div>
    );
  };

  const renderEmptyState = () => (
    <div className="text-center py-16">
      <BookOpen className="h-24 w-24 text-gray-300 mx-auto mb-6" />
      <h2 className="text-2xl font-semibold text-gray-600 mb-4">No Stories Yet</h2>
      <p className="text-gray-500 mb-8 max-w-md mx-auto">
        Create your first magical story! Choose from text scenarios, image uploads, or character-based stories.
      </p>
      <button
        onClick={() => setShowCreator(true)}
        className="btn btn-primary btn-lg"
      >
        <Plus className="h-5 w-5 mr-2" />
        Create Your First Story
      </button>
    </div>
  );

  const renderErrorState = () => (
    <div className="text-center py-16">
      <AlertCircle className="h-24 w-24 text-red-300 mx-auto mb-6" />
      <h2 className="text-2xl font-semibold text-gray-600 mb-4">Failed to Load Stories</h2>
      <p className="text-gray-500 mb-8">{error}</p>
      <button
        onClick={loadStories}
        className="btn btn-primary"
      >
        <RefreshCw className="h-5 w-5 mr-2" />
        Try Again
      </button>
    </div>
  );

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
        <Header />
        
        <main className="container mx-auto px-4 py-8">
          {renderHealthStatus()}

          {/* Action Bar */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Your Stories</h1>
              <p className="text-gray-600 mt-1">
                {stories.length > 0 ? `${stories.length} ${stories.length === 1 ? 'story' : 'stories'} created` : 'Start creating magical stories'}
              </p>
            </div>
            
            {!showCreator && (
              <button
                onClick={() => setShowCreator(true)}
                className="btn btn-primary"
              >
                <Plus className="h-5 w-5 mr-2" />
                Create New Story
              </button>
            )}
          </div>

          {/* Story Creator */}
          {showCreator && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900">Create New Story</h2>
                <button
                  onClick={() => setShowCreator(false)}
                  className="btn btn-outline"
                >
                  Cancel
                </button>
              </div>
              <ErrorBoundary>
                <StoryCreator onStoryCreated={handleStoryCreated} />
              </ErrorBoundary>
            </div>
          )}

          {/* Content Area */}
          {loading ? (
            <div className="text-center py-16">
              <LoadingSpinner size="xl" text="Loading your stories..." />
            </div>
          ) : error ? (
            renderErrorState()
          ) : stories.length === 0 ? (
            renderEmptyState()
          ) : (
            <div className="space-y-8">
              {stories.map(story => (
                <ErrorBoundary key={story.id}>
                  <StoryDisplay
                    story={story}
                    onDelete={handleDeleteStory}
                  />
                </ErrorBoundary>
              ))}
            </div>
          )}

          {/* Footer */}
          <footer className="mt-16 py-8 border-t border-gray-200 text-center text-gray-500">
            <p>&copy; 2025 Kahaniyaa. Bringing stories to life with AI.</p>
          </footer>
        </main>
      </div>
    </ErrorBoundary>
  );
}

export default App;
