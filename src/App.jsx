import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import LeftPanel from './components/LeftPanel.jsx';
import CenterPanel from './components/CenterPanel.jsx';
import RightPanel from './components/RightPanel.jsx';
import { GlobalStyles } from './styles/GlobalStyles.js';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Inter', sans-serif;
`;

const App = () => {
  const [procedureData, setProcedureData] = useState({
    name: 'Laparoscopic Cholecystectomy',
    startTime: '08:24 AM',
    patientId: 'P-2024-001',
    expectedInstruments: 24,
    isPrivacyMode: false
  });

  const [detectionData, setDetectionData] = useState({
    isLive: true,
    isPaused: false,
    currentFrame: null,
    detectedInstruments: [],
    issues: []
  });

  const [checklistData, setChecklistData] = useState({
    found: [],
    missing: [],
    optional: [],
    confirmed: false
  });

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      if (detectionData.isLive && !detectionData.isPaused) {
        // Simulate new detection data
        setDetectionData(prev => ({
          ...prev,
          detectedInstruments: [
            { id: 1, name: 'Kelly Hemostat', count: 4, status: 'found', required: 5 },
            { id: 2, name: 'Mosquito Hemostat', count: 1, status: 'found', required: 1 },
            { id: 3, name: '#10 Blade', count: 1, status: 'found', required: 1 },
            { id: 4, name: '#15 Blade', count: 1, status: 'found', required: 1 },
            { id: 5, name: 'Syringe', count: 1, status: 'extra', required: 0 }
          ],
          issues: [
            { timestamp: '08:24:18', type: 'missing', message: 'Kelly Hemostat (1)' },
            { timestamp: '08:24:20', type: 'extra', message: 'Syringe (not listed)' },
            { timestamp: '08:24:25', type: 'corrected', message: 'Retractor added' }
          ]
        }));
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [detectionData.isLive, detectionData.isPaused]);

  return (
    <>
      <GlobalStyles />
      <AppContainer>
        <LeftPanel 
          procedureData={procedureData}
          setProcedureData={setProcedureData}
        />
        <CenterPanel 
          detectionData={detectionData}
          setDetectionData={setDetectionData}
        />
        <RightPanel 
          checklistData={checklistData}
          setChecklistData={setChecklistData}
          detectionData={detectionData}
        />
      </AppContainer>
    </>
  );
};

export default App; 