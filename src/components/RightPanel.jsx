import React, { useState } from 'react';
import styled from 'styled-components';
import { 
  FaCheck, 
  FaTimes, 
  FaExclamationTriangle, 
  FaChevronDown, 
  FaChevronUp,
  FaClipboardCheck,
  FaRedo,
  FaLock,
  FaUnlock
} from 'react-icons/fa';

const Panel = styled.div`
  width: 30%;
  background: var(--white);
  display: flex;
  flex-direction: column;
  border-left: 1px solid #e5e7eb;
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

const Content = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
`;

const Section = styled.div`
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h3`
  font-size: 1rem;
  font-weight: 600;
  color: var(--dark-gray);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const ToolGroup = styled.div`
  margin-bottom: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  overflow: hidden;
`;

const GroupHeader = styled.div`
  background: var(--light-gray);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
  
  &:hover {
    background: #e5e7eb;
  }
`;

const GroupTitle = styled.div`
  font-weight: 600;
  color: var(--dark-gray);
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const GroupStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
`;

const StatusIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: ${props => {
    switch (props.status) {
      case 'complete': return 'var(--success-green)';
      case 'partial': return 'var(--warning-yellow)';
      case 'missing': return 'var(--error-red)';
      default: return 'var(--neutral-gray)';
    }
  }};
  color: var(--white);
  font-size: 0.75rem;
`;

const GroupContent = styled.div`
  padding: 1rem;
  display: ${props => props.isExpanded ? 'block' : 'none'};
`;

const ToolItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  background: ${props => {
    switch (props.status) {
      case 'found': return 'rgba(5, 150, 105, 0.1)';
      case 'missing': return 'rgba(220, 38, 38, 0.1)';
      case 'extra': return 'rgba(220, 38, 38, 0.1)';
      case 'optional': return 'rgba(217, 119, 6, 0.1)';
      default: return 'var(--light-gray)';
    }
  }};
  border-left: 4px solid ${props => {
    switch (props.status) {
      case 'found': return 'var(--success-green)';
      case 'missing': return 'var(--error-red)';
      case 'extra': return 'var(--error-red)';
      case 'optional': return 'var(--warning-yellow)';
      default: return 'var(--neutral-gray)';
    }
  }};
`;

const ToolInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`;

const ToolName = styled.div`
  font-weight: 500;
  color: var(--dark-gray);
`;

const ToolCount = styled.div`
  font-size: 0.875rem;
  color: var(--neutral-gray);
`;

const ToolStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: ${props => {
    switch (props.status) {
      case 'found': return 'var(--success-green)';
      case 'missing': return 'var(--error-red)';
      case 'extra': return 'var(--error-red)';
      case 'optional': return 'var(--warning-yellow)';
      default: return 'var(--neutral-gray)';
    }
  }};
`;

const IssuesLog = styled.div`
  background: var(--light-gray);
  border-radius: 0.75rem;
  padding: 1rem;
  max-height: 200px;
  overflow-y: auto;
`;

const LogEntry = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
  font-size: 0.875rem;
  
  &:last-child {
    border-bottom: none;
  }
`;

const LogTimestamp = styled.div`
  color: var(--neutral-gray);
  font-weight: 500;
  min-width: 4rem;
`;

const LogMessage = styled.div`
  color: var(--dark-gray);
  flex: 1;
`;

const LogIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: ${props => {
    switch (props.type) {
      case 'missing': return 'var(--error-red)';
      case 'extra': return 'var(--error-red)';
      case 'corrected': return 'var(--success-green)';
      default: return 'var(--neutral-gray)';
    }
  }};
  color: var(--white);
  font-size: 0.75rem;
`;

const ActionButtons = styled.div`
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 1rem;
`;

const ActionButton = styled.button`
  flex: 1;
  padding: 1rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &.confirm {
    background: var(--success-green);
    color: var(--white);
    
    &:hover {
      background: #047857;
    }
  }
  
  &.rescan {
    background: var(--primary-blue);
    color: var(--white);
    
    &:hover {
      background: var(--secondary-blue);
    }
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const RightPanel = ({ checklistData, setChecklistData, detectionData }) => {
  const [expandedGroups, setExpandedGroups] = useState({
    hemostats: true,
    scalpels: true,
    retractors: false,
    sutures: false
  });

  const toggleGroup = (groupName) => {
    setExpandedGroups(prev => ({
      ...prev,
      [groupName]: !prev[groupName]
    }));
  };

  const confirmSetup = () => {
    setChecklistData(prev => ({ ...prev, confirmed: true }));
  };

  const rescan = () => {
    setChecklistData(prev => ({ ...prev, confirmed: false }));
  };

  const toolGroups = [
    {
      name: 'hemostats',
      title: 'Hemostats',
      required: 5,
      tools: [
        { name: 'Kelly Hemostat', count: 4, required: 5, status: 'partial' },
        { name: 'Mosquito Hemostat', count: 1, required: 1, status: 'found' }
      ],
      status: 'partial'
    },
    {
      name: 'scalpels',
      title: 'Scalpels',
      required: 2,
      tools: [
        { name: '#10 Blade', count: 1, required: 1, status: 'found' },
        { name: '#15 Blade', count: 1, required: 1, status: 'found' }
      ],
      status: 'complete'
    },
    {
      name: 'retractors',
      title: 'Retractors',
      required: 2,
      tools: [
        { name: 'Army-Navy Retractor', count: 0, required: 1, status: 'missing' },
        { name: 'Weitlaner Retractor', count: 1, required: 1, status: 'found' }
      ],
      status: 'partial'
    }
  ];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'complete': return <FaCheck />;
      case 'partial': return <FaExclamationTriangle />;
      case 'missing': return <FaTimes />;
      default: return <FaTimes />;
    }
  };

  const getLogIcon = (type) => {
    switch (type) {
      case 'missing': return <FaTimes />;
      case 'extra': return <FaTimes />;
      case 'corrected': return <FaCheck />;
      default: return <FaExclamationTriangle />;
    }
  };

  return (
    <Panel>
      <Header>
        <Title>Smart Checklist</Title>
      </Header>

      <Content>
        <Section>
          <SectionTitle>
            <FaClipboardCheck />
            Instrument Checklist
          </SectionTitle>
          
          {toolGroups.map(group => (
            <ToolGroup key={group.name}>
              <GroupHeader onClick={() => toggleGroup(group.name)}>
                <GroupTitle>
                  {group.title} ({group.required} required)
                </GroupTitle>
                <GroupStatus>
                  <StatusIcon status={group.status}>
                    {getStatusIcon(group.status)}
                  </StatusIcon>
                  {expandedGroups[group.name] ? <FaChevronUp /> : <FaChevronDown />}
                </GroupStatus>
              </GroupHeader>
              
              <GroupContent isExpanded={expandedGroups[group.name]}>
                {group.tools.map((tool, index) => (
                  <ToolItem key={index} status={tool.status}>
                    <ToolInfo>
                      <ToolName>{tool.name}</ToolName>
                      <ToolCount>{tool.count}/{tool.required}</ToolCount>
                    </ToolInfo>
                    <ToolStatus status={tool.status}>
                      {tool.status === 'found' && <FaCheck />}
                      {tool.status === 'missing' && <FaTimes />}
                      {tool.status === 'partial' && <FaExclamationTriangle />}
                      {tool.status}
                    </ToolStatus>
                  </ToolItem>
                ))}
              </GroupContent>
            </ToolGroup>
          ))}
        </Section>

        <Section>
          <SectionTitle>Issues Log</SectionTitle>
          <IssuesLog>
            {detectionData.issues.map((issue, index) => (
              <LogEntry key={index}>
                <LogIcon type={issue.type}>
                  {getLogIcon(issue.type)}
                </LogIcon>
                <LogTimestamp>[{issue.timestamp}]</LogTimestamp>
                <LogMessage>{issue.message}</LogMessage>
              </LogEntry>
            ))}
          </IssuesLog>
        </Section>
      </Content>

      <ActionButtons>
        <ActionButton 
          className="confirm" 
          onClick={confirmSetup}
          disabled={checklistData.confirmed}
        >
          <FaCheck />
          Confirm Setup
        </ActionButton>
        <ActionButton className="rescan" onClick={rescan}>
          <FaRedo />
          Re-Scan
        </ActionButton>
      </ActionButtons>
    </Panel>
  );
};

export default RightPanel; 