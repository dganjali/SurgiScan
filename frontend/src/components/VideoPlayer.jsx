import React, { useRef, useState } from 'react';

const VideoPlayer = () => {
  const videoRef = useRef(null);
  const [isVideoPlaying, setIsVideoPlaying] = useState(false);

  const toggleVideoPlayback = () => {
    if (videoRef.current) {
      if (isVideoPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsVideoPlaying(!isVideoPlaying);
    }
  };

  return (
    <div className="video-container">
      <h2>📹 Segmentation Video Analysis</h2>
      <video
        ref={videoRef}
        className="analysis-video"
        controls
        onPlay={() => setIsVideoPlaying(true)}
        onPause={() => setIsVideoPlaying(false)}
        onError={(e) => console.error('Video playback error:', e)}
      >
        <source src="http://localhost:8000/video" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <button onClick={toggleVideoPlayback} className="play-pause-btn">
        {isVideoPlaying ? 'Pause' : 'Play'}
      </button>
    </div>
  );
};

export default VideoPlayer;