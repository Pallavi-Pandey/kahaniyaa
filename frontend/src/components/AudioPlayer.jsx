import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, RotateCcw, Download } from 'lucide-react';

const AudioPlayer = ({ audioData, audioUrl, title = "Story Audio" }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [loading, setLoading] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);
    const handleLoadStart = () => setLoading(true);
    const handleCanPlay = () => setLoading(false);

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('loadstart', handleLoadStart);
    audio.addEventListener('canplay', handleCanPlay);

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('loadstart', handleLoadStart);
      audio.removeEventListener('canplay', handleCanPlay);
    };
  }, [audioData, audioUrl]);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e) => {
    const audio = audioRef.current;
    if (!audio) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    const newTime = pos * duration;
    audio.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (audioRef.current) {
      audioRef.current.volume = newVolume;
    }
    setIsMuted(newVolume === 0);
  };

  const toggleMute = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isMuted) {
      audio.volume = volume;
      setIsMuted(false);
    } else {
      audio.volume = 0;
      setIsMuted(true);
    }
  };

  const restart = () => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.currentTime = 0;
    setCurrentTime(0);
  };

  const downloadAudio = () => {
    if (audioData) {
      const blob = new Blob([Uint8Array.from(atob(audioData), c => c.charCodeAt(0))], {
        type: 'audio/wav'
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.wav`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const formatTime = (time) => {
    if (isNaN(time)) return '0:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const progressPercentage = duration ? (currentTime / duration) * 100 : 0;

  // Create audio source
  const audioSrc = audioData 
    ? `data:audio/wav;base64,${audioData}`
    : audioUrl;

  if (!audioSrc) {
    return (
      <div className="audio-player">
        <div className="text-center py-8">
          <Volume2 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No audio available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="audio-player">
      <audio ref={audioRef} src={audioSrc} preload="metadata" />
      
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-medium text-gray-900">{title}</h3>
        {audioData && (
          <button
            onClick={downloadAudio}
            className="btn btn-outline btn-sm"
            title="Download Audio"
          >
            <Download className="h-4 w-4" />
          </button>
        )}
      </div>

      <div className="audio-controls">
        {/* Play/Pause Button */}
        <button
          onClick={togglePlayPause}
          disabled={loading}
          className="btn btn-primary p-3 rounded-full"
        >
          {loading ? (
            <div className="spinner h-6 w-6" />
          ) : isPlaying ? (
            <Pause className="h-6 w-6" />
          ) : (
            <Play className="h-6 w-6" />
          )}
        </button>

        {/* Restart Button */}
        <button
          onClick={restart}
          className="btn btn-outline p-2 rounded-full"
          title="Restart"
        >
          <RotateCcw className="h-4 w-4" />
        </button>

        {/* Progress Bar */}
        <div className="audio-progress" onClick={handleSeek}>
          <div 
            className="audio-progress-bar"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>

        {/* Time Display */}
        <div className="text-sm text-gray-600 min-w-[80px]">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>

        {/* Volume Controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={toggleMute}
            className="btn btn-outline p-2 rounded-full"
          >
            {isMuted ? (
              <VolumeX className="h-4 w-4" />
            ) : (
              <Volume2 className="h-4 w-4" />
            )}
          </button>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={isMuted ? 0 : volume}
            onChange={handleVolumeChange}
            className="w-20 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>
      </div>

      {/* Waveform Visualization (Optional Enhancement) */}
      <div className="mt-4">
        <div className="flex items-end justify-center space-x-1 h-12">
          {Array.from({ length: 40 }, (_, i) => (
            <div
              key={i}
              className={`bg-primary-300 rounded-full transition-all duration-150 ${
                i < (progressPercentage / 100) * 40 ? 'bg-primary-500' : ''
              }`}
              style={{
                width: '3px',
                height: `${Math.random() * 80 + 20}%`,
                opacity: isPlaying ? 0.8 : 0.4
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default AudioPlayer;
