import React, { useState, useRef, useEffect } from 'react'
import { toast } from 'react-hot-toast'
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  SkipBack, 
  SkipForward,
  Download,
  RotateCcw,
  Clock,
  Headphones
} from 'lucide-react'

const AudioPlayer = ({ audioData, story }) => {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const [playbackRate, setPlaybackRate] = useState(1)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const updateTime = () => setCurrentTime(audio.currentTime)
    const updateDuration = () => setDuration(audio.duration)
    const handleEnded = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', updateTime)
    audio.addEventListener('loadedmetadata', updateDuration)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', updateTime)
      audio.removeEventListener('loadedmetadata', updateDuration)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [audioData])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e) => {
    const audio = audioRef.current
    if (!audio) return

    const rect = e.currentTarget.getBoundingClientRect()
    const percent = (e.clientX - rect.left) / rect.width
    const newTime = percent * duration
    audio.currentTime = newTime
    setCurrentTime(newTime)
  }

  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value)
    setVolume(newVolume)
    if (audioRef.current) {
      audioRef.current.volume = newVolume
    }
    setIsMuted(newVolume === 0)
  }

  const toggleMute = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isMuted) {
      audio.volume = volume
      setIsMuted(false)
    } else {
      audio.volume = 0
      setIsMuted(true)
    }
  }

  const skipTime = (seconds) => {
    const audio = audioRef.current
    if (!audio) return

    audio.currentTime = Math.max(0, Math.min(duration, audio.currentTime + seconds))
  }

  const handlePlaybackRateChange = (rate) => {
    const audio = audioRef.current
    if (!audio) return

    audio.playbackRate = rate
    setPlaybackRate(rate)
  }

  const handleDownload = () => {
    if (!audioData?.audio_url && !audioData?.audio_data) {
      toast.error('No audio data available for download')
      return
    }

    try {
      let downloadUrl
      let filename = `${story?.title || 'story'}_audio.mp3`

      if (audioData.audio_url) {
        downloadUrl = audioData.audio_url
      } else if (audioData.audio_data) {
        // Convert base64 to blob
        const byteCharacters = atob(audioData.audio_data)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: 'audio/mpeg' })
        downloadUrl = URL.createObjectURL(blob)
      }

      const element = document.createElement('a')
      element.href = downloadUrl
      element.download = filename
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)

      if (audioData.audio_data) {
        URL.revokeObjectURL(downloadUrl)
      }

      toast.success('Audio downloaded successfully!')
    } catch (error) {
      console.error('Download failed:', error)
      toast.error('Failed to download audio')
    }
  }

  const formatTime = (time) => {
    if (isNaN(time)) return '0:00'
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  const getAudioSource = () => {
    if (audioData?.audio_url) {
      return audioData.audio_url
    } else if (audioData?.audio_data) {
      return `data:audio/mpeg;base64,${audioData.audio_data}`
    }
    return null
  }

  const audioSource = getAudioSource()

  if (!audioSource) {
    return (
      <div className="card">
        <div className="card-content">
          <div className="text-center py-8 text-gray-500">
            <Headphones className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>No audio available</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-blue-500 rounded-lg flex items-center justify-center">
              <Headphones className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-display font-semibold text-gray-900">
                Audio Player
              </h3>
              <p className="text-sm text-gray-600">
                {story?.title || 'Generated Story Audio'}
              </p>
            </div>
          </div>
          
          <button
            onClick={handleDownload}
            className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
            title="Download audio"
          >
            <Download className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="card-content">
        <audio
          ref={audioRef}
          src={audioSource}
          preload="metadata"
        />

        {/* Main Controls */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => skipTime(-10)}
            className="p-2 text-gray-600 hover:text-gray-900 transition-colors"
            title="Skip back 10s"
          >
            <SkipBack className="w-5 h-5" />
          </button>

          <button
            onClick={togglePlay}
            className="w-12 h-12 bg-primary-600 hover:bg-primary-700 text-white rounded-full flex items-center justify-center transition-colors"
          >
            {isPlaying ? (
              <Pause className="w-6 h-6" />
            ) : (
              <Play className="w-6 h-6 ml-0.5" />
            )}
          </button>

          <button
            onClick={() => skipTime(10)}
            className="p-2 text-gray-600 hover:text-gray-900 transition-colors"
            title="Skip forward 10s"
          >
            <SkipForward className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={toggleMute}
              className="p-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              {isMuted ? (
                <VolumeX className="w-5 h-5" />
              ) : (
                <Volume2 className="w-5 h-5" />
              )}
            </button>
            
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={isMuted ? 0 : volume}
              onChange={handleVolumeChange}
              className="w-20"
            />
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2 mb-4">
          <div
            className="w-full h-2 bg-gray-200 rounded-full cursor-pointer"
            onClick={handleSeek}
          >
            <div
              className="h-full bg-primary-600 rounded-full transition-all"
              style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
            />
          </div>
          
          <div className="flex justify-between text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {formatTime(currentTime)}
            </span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>

        {/* Playback Speed */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <RotateCcw className="w-4 h-4 text-gray-600" />
            <span className="text-sm text-gray-600">Speed:</span>
            <div className="flex gap-1">
              {[0.5, 0.75, 1, 1.25, 1.5, 2].map(rate => (
                <button
                  key={rate}
                  onClick={() => handlePlaybackRateChange(rate)}
                  className={`px-2 py-1 text-xs rounded transition-colors ${
                    playbackRate === rate
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {rate}x
                </button>
              ))}
            </div>
          </div>

          {/* Audio Info */}
          {audioData && (
            <div className="text-sm text-gray-500">
              {audioData.language && (
                <span className="capitalize">{audioData.language}</span>
              )}
              {audioData.voice && audioData.language && ' • '}
              {audioData.voice && (
                <span className="capitalize">{audioData.voice.replace('_', ' ')}</span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AudioPlayer
