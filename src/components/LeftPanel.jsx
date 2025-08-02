import React from 'react';
import styled from 'styled-components';
import { 
  FaUserMd, 
  FaClock, 
  FaUser, 
  FaTools, 
  FaEye, 
  FaEyeSlash 
} from 'react-icons/fa';

const Panel = styled.div`
  width: 10%;
  background: linear-gradient(180deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  color: var(--white);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
`;

const Section = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const SectionTitle = styled.h3`
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.9;
  margin-bottom: 0.5rem;
`;

const InfoCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const ProcedureName = styled.div`
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 0.5rem;
`;

const Select = styled.select`
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  color: var(--white);
  padding: 0.5rem;
  font-size: 0.875rem;
  width: 100%;
  margin-top: 0.5rem;
  
  option {
    background: var(--dark-gray);
    color: var(--white);
  }
`;

const InfoRow = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const Icon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 0.375rem;
  font-size: 0.75rem;
`;

const Metric = styled.div`
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const MetricValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
`;

const MetricLabel = styled.div`
  font-size: 0.75rem;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const PrivacyToggle = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  color: var(--white);
  padding: 0.5rem;
  font-size: 0.75rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
`;

const LeftPanel = ({ procedureData, setProcedureData }) => {
  const procedures = [
    'Laparoscopic Cholecystectomy',
    'Appendectomy',
    'Hernia Repair',
    'Colon Resection',
    'Gastric Bypass'
  ];

  return (
    <Panel>
      <Section>
        <SectionTitle>Procedure</SectionTitle>
        <InfoCard>
          <ProcedureName>{procedureData.name}</ProcedureName>
          <Select 
            value={procedureData.name}
            onChange={(e) => setProcedureData(prev => ({ ...prev, name: e.target.value }))}
          >
            {procedures.map(proc => (
              <option key={proc} value={proc}>{proc}</option>
            ))}
          </Select>
        </InfoCard>
      </Section>

      <Section>
        <SectionTitle>Session Info</SectionTitle>
        <InfoCard>
          <InfoRow>
            <Icon><FaClock /></Icon>
            <span>Started {procedureData.startTime}</span>
          </InfoRow>
          <InfoRow>
            <Icon><FaUser /></Icon>
            <span>{procedureData.isPrivacyMode ? '***-***-***' : procedureData.patientId}</span>
          </InfoRow>
        </InfoCard>
      </Section>

      <Section>
        <SectionTitle>Expected Tools</SectionTitle>
        <Metric>
          <MetricValue>{procedureData.expectedInstruments}</MetricValue>
          <MetricLabel>Instruments</MetricLabel>
        </Metric>
      </Section>

      <Section>
        <SectionTitle>Privacy</SectionTitle>
        <PrivacyToggle 
          onClick={() => setProcedureData(prev => ({ ...prev, isPrivacyMode: !prev.isPrivacyMode }))}
        >
          {procedureData.isPrivacyMode ? <FaEyeSlash /> : <FaEye />}
          {procedureData.isPrivacyMode ? 'Privacy On' : 'Privacy Off'}
        </PrivacyToggle>
      </Section>
    </Panel>
  );
};

export default LeftPanel; 