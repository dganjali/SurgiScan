import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import { 
  FaPlay, 
  FaPause, 
  FaStepForward, 
  FaStepBackward,
  FaCamera,
  FaExpand,
  FaCompress
} from 'react-icons/fa';

const Panel = styled.div`
  width: 60%;
  background: var(--white);
  display: flex;
  flex-direction: column;
  position: relative;
`;

const Header = styled.div`
  background: var(--light-gray);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Title = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--dark-gray);
`;

const Controls = styled.div`
  display: flex;
  gap: 0.5rem;
  align-items: center;
`;

const ControlButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: ${props => props.active ? 'var(--primary-blue)' : 'var(--white)'};
  color: ${props => props.active ? 'var(--white)' : 'var(--dark-gray)'};
  border: 1px solid ${props => props.active ? 'var(--primary-blue)' : '#d1d5db'};
  transition: all 0.2s ease;
  font-size: 0.875rem;
  
  &:hover {
    background: ${props => props.active ? 'var(--secondary-blue)' : 'var(--light-gray)'};
  }
`;

const VideoContainer = styled.div`
  flex: 1;
  background: #000;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
`;

const VideoFrame = styled.div`
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #1a1a1a 25%, transparent 25%), 
              linear-gradient(-45deg, #1a1a1a 25%, transparent 25%), 
              linear-gradient(45deg, transparent 75%, #1a1a1a 75%), 
              linear-gradient(-45deg, transparent 75%, #1a1a1a 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--white);
  font-size: 1.5rem;
  font-weight: 500;
`;

const OverlayBox = styled.div`
  position: absolute;
  border: 3px solid ${props => {
    switch (props.status) {
      case 'found': return 'var(--success-green)';
      case 'missing': return 'var(--error-red)';
      case 'extra': return 'var(--error-red)';
      case 'optional': return 'var(--warning-yellow)';
      default: return 'var(--neutral-gray)';
    }
  }};
  background: ${props => props.status === 'found' ? 'rgba(5, 150, 105, 0.1)' : 'transparent'};
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--white);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  
  &::before {
    content: '${props => {
      switch (props.status) {
        case 'found': return '✅';
        case 'missing': return '❌';
        case 'extra': return '❌';
        case 'optional': return '⚠️';
        default: return '🔲';
      }
    }}';
    position: absolute;
    top: -0.5rem;
    left: -0.5rem;
    background: var(--white);
    border-radius: 50%;
    width: 1rem;
    height: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.5rem;
  }
`;

const StatusIndicator = styled.div`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: ${props => props.isLive ? 'var(--success-green)' : 'var(--warning-yellow)'};
  color: var(--white);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &::before {
    content: '';
    width: 0.5rem;
    height: 0.5rem;
    background: var(--white);
    border-radius: 50%;
    animation: ${props => props.isLive ? 'pulse 2s infinite' : 'none'};
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

const Timeline = styled.div`
  background: var(--light-gray);
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
`;

const TimelineSlider = styled.input`
  width: 100%;
  height: 0.5rem;
  background: #d1d5db;
  border-radius: 0.25rem;
  outline: none;
  -webkit-appearance: none;
  
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 1.5rem;
    height: 1.5rem;
    background: var(--primary-blue);
    border-radius: 50%;
    cursor: pointer;
  }
  
  &::-moz-range-thumb {
    width: 1.5rem;
    height: 1.5rem;
    background: var(--primary-blue);
    border-radius: 50%;
    cursor: pointer;
    border: none;
  }
`;

const TimelineInfo = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: var(--neutral-gray);
`;

const CenterPanel = ({ detectionData, setDetectionData }) => {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const videoRef = useRef(null);

  const toggleLive = () => {
    setDetectionData(prev => ({ ...prev, isLive: !prev.isLive }));
  };

  const togglePause = () => {
    setDetectionData(prev => ({ ...prev, isPaused: !prev.isPaused }));
  };

  const takeSnapshot = () => {
    // Simulate taking a snapshot
    console.log('Snapshot taken');
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  // Simulate detected objects with bounding boxes
  const detectedObjects = [
    { id: 1, name: 'Kelly Hemostat', x: 100, y: 150, width: 80, height: 60, status: 'found' },
    { id: 2, name: 'Mosquito Hemostat', x: 300, y: 200, width: 70, height: 50, status: 'found' },
    { id: 3, name: '#10 Blade', x: 500, y: 100, width: 60, height: 40, status: 'found' },
    { id: 4, name: 'Syringe', x: 200, y: 400, width: 90, height: 30, status: 'extra' },
    { id: 5, name: 'Retractor', x: 600, y: 300, width: 120, height: 80, status: 'missing' }
  ];

  return (
    <Panel>
      <Header>
        <Title>Live Frame Viewer</Title>
        <Controls>
          <ControlButton 
            active={detectionData.isLive}
            onClick={toggleLive}
            title="Toggle Live Mode"
          >
            <FaPlay />
          </ControlButton>
          <ControlButton 
            active={detectionData.isPaused}
            onClick={togglePause}
            title="Pause/Resume"
          >
            <FaPause />
          </ControlButton>
          <ControlButton title="Previous Frame">
            <FaStepBackward />
          </ControlButton>
          <ControlButton title="Next Frame">
            <FaStepForward />
          </ControlButton>
          <ControlButton onClick={takeSnapshot} title="Take Snapshot">
            <FaCamera />
          </ControlButton>
          <ControlButton onClick={toggleFullscreen} title="Toggle Fullscreen">
            {isFullscreen ? <FaCompress /> : <FaExpand />}
          </ControlButton>
        </Controls>
      </Header>

      <VideoContainer ref={videoRef}>
        <VideoFrame>
          {detectionData.isLive ? 'LIVE FEED' : 'PAUSED'}
        </VideoFrame>
        
        {/* Overlay detected objects */}
        {detectedObjects.map(obj => (
          <OverlayBox
            key={obj.id}
            status={obj.status}
            style={{
              left: `${obj.x}px`,
              top: `${obj.y}px`,
              width: `${obj.width}px`,
              height: `${obj.height}px`
            }}
          >
            {obj.name}
          </OverlayBox>
        ))}
        
        <StatusIndicator isLive={detectionData.isLive}>
          {detectionData.isLive ? 'LIVE' : 'PAUSED'}
        </StatusIndicator>
      </VideoContainer>

      <Timeline>
        <TimelineSlider 
          type="range" 
          min="0" 
          max="100" 
          defaultValue="75"
          title="Timeline"
        />
        <TimelineInfo>
          <span>08:24:15</span>
          <span>08:24:30</span>
        </TimelineInfo>
      </Timeline>
    </Panel>
  );
};

export default CenterPanel; 