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
  const [currentView, setCurrentView] = useState('procedure');
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

  const renderProcedureSelection = () => (
    <div className="procedure-selection">
      <div className="hero-section">
        <h1>🏥 Medical Crash Cart Validator</h1>
        <p>Real-time AI-powered surgical tool validation system</p>
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
        <div className="completion-indicator">
          <div className="completion-circle" style={{'--percentage': completionPercentage}}>
            <span className="percentage">{completionPercentage}%</span>
          </div>
          <span className="completion-label">Complete</span>
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
            <h3>Required Tools ({requiredTools.length})</h3>
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
      {currentView === 'procedure' ? renderProcedureSelection() : renderValidationInterface()}
    </div>
  );
}

export default App;
