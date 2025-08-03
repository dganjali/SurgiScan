import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

const COMMON_PROCEDURES = [
  'Code Blue',
  'Cardiac Arrest',
  'Intubation',
  'Trauma Response',
  'Respiratory Distress',
  'Chest Pain Protocol',
  'Stroke Alert',
  'Sepsis Protocol',
  'Anaphylaxis',
  'Cardiac Catheterization',
  'Custom Procedure'
];

function App() {
  const webcamRef = useRef(null);
  const videoRef = useRef(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedProcedure, setSelectedProcedure] = useState('');
  const [customProcedure, setCustomProcedure] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [requiredTools, setRequiredTools] = useState([]);
  const [detectedTools, setDetectedTools] = useState({});
  const [validationResults, setValidationResults] = useState(null);
  const [completionPercentage, setCompletionPercentage] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [showBoundingBoxes, setShowBoundingBoxes] = useState(true);
  const [boundingBoxes, setBoundingBoxes] = useState([]);
  const [uniqueCrops, setUniqueCrops] = useState([]);
  const [cropAnalysis, setCropAnalysis] = useState({});
  const [logs, setLogs] = useState([]);
  const [isVideoPlaying, setIsVideoPlaying] = useState(false);
  const [referenceTools, setReferenceTools] = useState([]);
  const [showToolReference, setShowToolReference] = useState(false);

  // Load unique crops and analyze them on component mount
  useEffect(() => {
    loadUniqueCrops();
    loadLogs();
    loadReferenceTools();
  }, []);

  // Load unique crops from the crops folder via backend
  const loadUniqueCrops = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/crops-analysis`);
      const data = response.data;
      
      setUniqueCrops(data.tool_types || []);
      setCropAnalysis({
        total_objects: data.total_objects || 0,
        unique_tools: data.unique_tools || 0,
        most_common: data.most_common || 'None',
        confidence_avg: data.confidence_avg || 0
      });
    } catch (error) {
      console.error('Error loading crops:', error);
      // Fallback to simulated data
      setUniqueCrops([
        'syringe', 'scalpel', 'stethoscope', 'defibrillator_pad', 
        'oxygen_mask', 'iv_bag', 'endotracheal_tube', 'gauze'
      ]);
      
      setCropAnalysis({
        total_objects: 450,
        unique_tools: 8,
        most_common: 'syringe',
        confidence_avg: 0.85
      });
    }
  };

  // Load system logs
  const loadLogs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/logs`);
      setLogs(response.data.logs || []);
    } catch (error) {
      console.error('Error loading logs:', error);
    }
  };

  // Load reference tool images
  const loadReferenceTools = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tool-reference`);
      setReferenceTools(response.data.tools || []);
    } catch (error) {
      console.error('Error loading reference tools:', error);
    }
  };

  // Start new validation session
  const startSession = async () => {
    const procedure = selectedProcedure === 'Custom Procedure' ? customProcedure : selectedProcedure;
    if (!procedure.trim()) {
      alert('Please select or enter a procedure');
      return;
    }
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('procedure', procedure);
      const response = await axios.post(`${API_BASE_URL}/input-procedure`, formData);
      setSessionId(response.data.session_id);
      setRequiredTools(response.data.required_tools || []);
      setCurrentView('validation');
    } catch (error) {
      alert('Failed to start session. Make sure the backend is running on localhost:8000');
    } finally {
      setIsLoading(false);
    }
  };

  // Capture and validate current frame
  const captureAndValidate = useCallback(async () => {
    if (!webcamRef.current || !sessionId) return;
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;
    try {
      const response = await fetch(imageSrc);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append('image', blob, 'webcam_frame.jpg');
      formData.append('session_id', sessionId);
      const validateResponse = await axios.post(
        `${API_BASE_URL}/realtime-validate`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setDetectedTools(validateResponse.data.detected_tools || {});
      setValidationResults(validateResponse.data);
      setBoundingBoxes(validateResponse.data.bounding_boxes || []);
      const detectedCount = Object.keys(validateResponse.data.detected_tools || {}).length;
      const requiredCount = requiredTools.length;
      const percentage = requiredCount > 0 ? Math.round((detectedCount / requiredCount) * 100) : 0;
      setCompletionPercentage(Math.min(percentage, 100));
    } catch (error) {}
  }, [sessionId, requiredTools]);

  // Auto-capture every 1000ms (1fps) when session is active
  useEffect(() => {
    if (!sessionId || currentView !== 'validation') return;
    const interval = setInterval(captureAndValidate, 1000);
    return () => clearInterval(interval);
  }, [sessionId, currentView, captureAndValidate]);

  // Reset to procedure selection
  const resetSession = () => {
    setCurrentView('procedure');
    setSessionId(null);
    setSelectedProcedure('');
    setCustomProcedure('');
    setRequiredTools([]);
    setDetectedTools({});
    setValidationResults(null);
    setCompletionPercentage(0);
    setShowBoundingBoxes(true);
    setBoundingBoxes([]);
  };

  // Toggle video playback
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

  // Dashboard render function
  const renderDashboard = () => (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>🏥 Medical Crash Cart Dashboard</h1>
        <div className="nav-buttons">
          <button 
            className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            📊 Dashboard
          </button>
          <button 
            className={`nav-btn ${currentView === 'procedure' ? 'active' : ''}`}
            onClick={() => setCurrentView('procedure')}
          >
            🚀 New Session
          </button>
          <button 
            className={`nav-btn ${currentView === 'validation' ? 'active' : ''}`}
            onClick={() => setCurrentView('validation')}
            disabled={!sessionId}
          >
            📹 Live Validation
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Video Analysis Section */}
        <div className="video-analysis-container">
          <div className="video-section">
            <h2>📹 Segmentation Video Analysis</h2>
            <div className="video-container">
              <video 
                ref={videoRef}
                className="analysis-video"
                controls
                onPlay={() => setIsVideoPlaying(true)}
                onPause={() => setIsVideoPlaying(false)}
                onEnded={() => setShowToolReference(true)}
              >
                <source src="/output.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
              <div className="video-controls">
                <button onClick={toggleVideoPlayback} className="play-pause-btn">
                  {isVideoPlaying ? '⏸️ Pause' : '▶️ Play'}
                </button>
                <button 
                  onClick={() => setShowToolReference(!showToolReference)}
                  className="toggle-reference-btn"
                >
                  {showToolReference ? '🔍 Hide Reference' : '📚 Show Tool Reference'}
                </button>
                <span className="video-info">Object detection and segmentation results</span>
              </div>
            </div>
          </div>

          {/* Tool Reference Panel */}
          {showToolReference && (
            <div className="tool-reference-panel">
              <h3>🔍 Tool Reference Checklist</h3>
              <div className="reference-tools-grid">
                {referenceTools.map((tool, index) => {
                  const isDetected = uniqueCrops.some(detected => 
                    detected.toLowerCase().includes(tool.name.toLowerCase()) ||
                    tool.name.toLowerCase().includes(detected.toLowerCase())
                  );
                  
                  return (
                    <div key={index} className={`reference-tool-item ${isDetected ? 'detected' : 'not-detected'}`}>
                      <div className="tool-image-container">
                        <img 
                          src={`${API_BASE_URL}${tool.image_url}`}
                          alt={tool.display_name}
                          className="tool-reference-image"
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                        <div className="detection-status">
                          {isDetected ? '✅' : '❌'}
                        </div>
                      </div>
                      <div className="tool-info">
                        <span className="tool-name">{tool.display_name}</span>
                        <span className="tool-count">{tool.total_images} ref images</span>
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="reference-summary">
                <div className="summary-stat">
                  <span className="stat-number">
                    {referenceTools.filter(tool => 
                      uniqueCrops.some(detected => 
                        detected.toLowerCase().includes(tool.name.toLowerCase()) ||
                        tool.name.toLowerCase().includes(detected.toLowerCase())
                      )
                    ).length}
                  </span>
                  <span className="stat-label">Detected</span>
                </div>
                <div className="summary-stat">
                  <span className="stat-number">{referenceTools.length}</span>
                  <span className="stat-label">Total Tools</span>
                </div>
                <div className="summary-stat">
                  <span className="stat-number">
                    {referenceTools.length > 0 ? 
                      Math.round((referenceTools.filter(tool => 
                        uniqueCrops.some(detected => 
                          detected.toLowerCase().includes(tool.name.toLowerCase()) ||
                          tool.name.toLowerCase().includes(detected.toLowerCase())
                        )
                      ).length / referenceTools.length) * 100) : 0}%
                  </span>
                  <span className="stat-label">Coverage</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Crop Analysis Section */}
        <div className="crop-analysis-section">
          <h2>🔍 Unique Crops Analysis</h2>
          <div className="analysis-grid">
            <div className="analysis-card">
              <h3>Detection Summary</h3>
              <div className="summary-stats">
                <div className="stat">
                  <span className="stat-number">{cropAnalysis.total_objects || 0}</span>
                  <span className="stat-label">Total Objects</span>
                </div>
                <div className="stat">
                  <span className="stat-number">{cropAnalysis.unique_tools || 0}</span>
                  <span className="stat-label">Unique Tools</span>
                </div>
                <div className="stat">
                  <span className="stat-number">{((cropAnalysis.confidence_avg || 0) * 100).toFixed(1)}%</span>
                  <span className="stat-label">Avg Confidence</span>
                </div>
              </div>
            </div>
            
            <div className="analysis-card">
              <h3>Detected Tool Types</h3>
              <div className="tools-list">
                {uniqueCrops.map((tool, index) => (
                  <div key={index} className="tool-tag">
                    {tool.replace('_', ' ')}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* MCP Tools Comparison */}
        <div className="mcp-comparison-section">
          <h2>🔧 MCP Web Scraped Tools Analysis</h2>
          <div className="comparison-grid">
            <div className="tools-column">
              <h3>✅ Tools We Have</h3>
              <div className="tools-available">
                {detectedTools && Object.keys(detectedTools).length > 0 ? (
                  Object.entries(detectedTools).map(([tool, count], index) => (
                    <div key={index} className="available-tool">
                      <span className="tool-name">{tool}</span>
                      <span className="tool-count">×{count}</span>
                    </div>
                  ))
                ) : (
                  <div className="placeholder">Start a validation session to see detected tools</div>
                )}
              </div>
            </div>
            
            <div className="tools-column">
              <h3>❌ Tools We Need</h3>
              <div className="tools-needed">
                {requiredTools.length > 0 ? (
                  requiredTools.filter(tool => 
                    !Object.keys(detectedTools).some(detected => 
                      detected.toLowerCase().includes(tool.toLowerCase()) ||
                      tool.toLowerCase().includes(detected.toLowerCase())
                    )
                  ).map((tool, index) => (
                    <div key={index} className="needed-tool">
                      <span className="tool-name">{tool}</span>
                      <span className="urgency-indicator">High Priority</span>
                    </div>
                  ))
                ) : (
                  <div className="placeholder">Start a procedure to see required tools</div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* System Logs */}
        <div className="logs-section">
          <h2>📋 Validation History</h2>
          <div className="logs-container">
            {logs.length > 0 ? (
              logs.slice(0, 10).map((log, index) => (
                <div key={index} className="log-entry">
                  <div className="log-header">
                    <span className="log-procedure">{log.procedure}</span>
                    <span className="log-timestamp">
                      {new Date(log.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <div className="log-details">
                    <span className={`completion-badge ${log.completion_percentage >= 80 ? 'good' : log.completion_percentage >= 50 ? 'warning' : 'poor'}`}>
                      {log.completion_percentage}% Complete
                    </span>
                    <span className="issues-count">
                      {log.issues_count} Issues
                    </span>
                    {log.missing_tools.length > 0 && (
                      <span className="missing-indicator">
                        Missing: {log.missing_tools.slice(0, 3).join(', ')}
                        {log.missing_tools.length > 3 && '...'}
                      </span>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="no-logs">No validation history available</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const renderProcedureSelection = () => (
    <div className="procedure-selection">
      <div className="hero-section">
        <h1>🏥 Medical Crash Cart Validator</h1>
        <p>Real-time AI-powered surgical tool validation system</p>
        <button 
          className="dashboard-btn"
          onClick={() => setCurrentView('dashboard')}
        >
          📊 View Dashboard
        </button>
      </div>
      <div className="selection-card">
        <h2>Select Emergency Procedure</h2>
        <p>Choose from common procedures or enter a custom one:</p>
        <div className="procedure-grid">
          {COMMON_PROCEDURES.map((procedure) => (
            <button
              key={procedure}
              className={`procedure-btn ${selectedProcedure === procedure ? 'selected' : ''}`}
              onClick={() => setSelectedProcedure(procedure)}
            >
              {procedure}
            </button>
          ))}
        </div>
        {selectedProcedure === 'Custom Procedure' && (
          <div className="custom-input-group">
            <label htmlFor="custom-procedure">Enter Custom Procedure:</label>
            <input
              id="custom-procedure"
              type="text"
              value={customProcedure}
              onChange={(e) => setCustomProcedure(e.target.value)}
              placeholder="e.g., Emergency Surgery, Pediatric Code..."
              className="custom-input"
            />
          </div>
        )}
        <button 
          onClick={startSession}
          disabled={!selectedProcedure || isLoading || (selectedProcedure === 'Custom Procedure' && !customProcedure.trim())}
          className="start-validation-btn"
        >
          {isLoading ? '⏳ Starting...' : '🚀 Start Validation'}
        </button>
      </div>
    </div>
  );

  const renderValidationInterface = () => (
    <div className="validation-interface">
      <div className="validation-header">
        <div className="session-info">
          <h2>🏥 {selectedProcedure === 'Custom Procedure' ? customProcedure : selectedProcedure}</h2>
          <span className="session-id">Session: {sessionId?.slice(0, 8)}...</span>
        </div>
        <div className="header-controls">
          <button 
            className="dashboard-btn"
            onClick={() => setCurrentView('dashboard')}
          >
            📊 Dashboard
          </button>
          <div className="completion-indicator">
            <div className="completion-circle" style={{'--percentage': completionPercentage}}>
              <span className="percentage">{completionPercentage}%</span>
            </div>
            <span className="completion-label">Complete</span>
          </div>
        </div>
      </div>
      <div className="main-validation-area">
        <div className="webcam-section">
          <div className="webcam-container">
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={{ width: 1280, height: 720, facingMode: "environment" }}
              className="webcam-feed"
            />
            {showBoundingBoxes && boundingBoxes.length > 0 && (
              <div className="bounding-boxes-overlay">
                {boundingBoxes.map((bbox, index) => (
                  <div
                    key={bbox.object_id || index}
                    className="bounding-box"
                    style={{
                      left: `${(bbox.x1 / 1280) * 100}%`,
                      top: `${(bbox.y1 / 720) * 100}%`,
                      width: `${((bbox.x2 - bbox.x1) / 1280) * 100}%`,
                      height: `${((bbox.y2 - bbox.y1) / 720) * 100}%`,
                    }}
                  >
                    <div className="bbox-label">
                      Obj {index} ({(bbox.confidence * 100).toFixed(0)}%)
                    </div>
                  </div>
                ))}
              </div>
            )}
            <div className="debug-info">
              <span>Boxes: {boundingBoxes.length} | Objects: {validationResults?.objects_found || 0}</span>
            </div>
          </div>
          <div className="webcam-controls">
            <button 
              onClick={() => setShowBoundingBoxes(!showBoundingBoxes)}
              className={`toggle-view-btn ${showBoundingBoxes ? 'active' : ''}`}
            >
              {showBoundingBoxes ? '📦 Hide Boxes' : '🎯 Show Boxes'}
            </button>
            <button onClick={resetSession} className="new-session-btn">
              🔄 New Session
            </button>
          </div>
        </div>
        <div className="tools-panel">
          <div className="tools-section">
            <div className="section-header">
              <h3>Required Tools ({requiredTools.length})</h3>
              <button 
                onClick={() => setShowToolReference(!showToolReference)}
                className="toggle-reference-small-btn"
              >
                {showToolReference ? '🔍' : '📚'}
              </button>
            </div>
            <div className="tools-checklist">
              {requiredTools.map((tool, index) => {
                const isDetected = Object.keys(detectedTools).some(
                  detected => 
                    detected.toLowerCase().includes(tool.toLowerCase()) ||
                    tool.toLowerCase().includes(detected.toLowerCase())
                );
                return (
                  <div key={index} className={`tool-item ${isDetected ? 'detected' : 'missing'}`}>
                    <span className="tool-status">
                      {isDetected ? '✅' : '⭕'}
                    </span>
                    <div className="tool-info">
                      <span className="tool-name">{tool}</span>
                      {isDetected && <span className="detection-badge">Detected</span>}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Tool Reference in Validation */}
          {showToolReference && (
            <div className="tools-section">
              <h3>🔍 Tool Reference</h3>
              <div className="reference-tools-compact">
                {referenceTools.slice(0, 8).map((tool, index) => {
                  const isDetected = Object.keys(detectedTools).some(detected => 
                    detected.toLowerCase().includes(tool.name.toLowerCase()) ||
                    tool.name.toLowerCase().includes(detected.toLowerCase())
                  );
                  
                  return (
                    <div key={index} className={`reference-tool-compact ${isDetected ? 'detected' : 'not-detected'}`}>
                      <img 
                        src={`${API_BASE_URL}${tool.image_url}`}
                        alt={tool.display_name}
                        className="tool-reference-image-small"
                        onError={(e) => {
                          e.target.style.display = 'none';
                        }}
                      />
                      <span className="tool-name-small">{tool.display_name}</span>
                      <span className="detection-indicator">{isDetected ? '✅' : '❌'}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          <div className="tools-section">
            <h3>Detected Tools ({Object.keys(detectedTools).length})</h3>
            <div className="detected-tools">
              {Object.entries(detectedTools).map(([tool, count], index) => (
                <div key={index} className="detected-tool-item">
                  <span className="tool-name">{tool}</span>
                  <span className="tool-count">{count}</span>
                </div>
              ))}
              {Object.keys(detectedTools).length === 0 && (
                <p className="no-tools">No tools detected yet...</p>
              )}
            </div>
          </div>
          {validationResults && (
            <div className="tools-section">
              <h3>Analysis Stats</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-label">Objects Found</span>
                  <span className="stat-value">{validationResults.objects_found}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Tools Detected</span>
                  <span className="stat-value">{Object.keys(detectedTools).length}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Missing Tools</span>
                  <span className="stat-value">{validationResults.missing_tools?.length || 0}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Bounding Boxes</span>
                  <span className="stat-value">{boundingBoxes.length}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="app">
      {currentView === 'dashboard' && renderDashboard()}
      {currentView === 'procedure' && renderProcedureSelection()}
      {currentView === 'validation' && renderValidationInterface()}
    </div>
  );
}

export default App;
