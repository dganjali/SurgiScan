import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    return Promise.reject(error);
  }
);

// Procedures API
export const proceduresAPI = {
  getProcedures: () => api.get('/procedures'),
  getProcedureDetails: (procedureName) => api.get(`/procedure/${encodeURIComponent(procedureName)}`),
};

// Detection API
export const detectionAPI = {
  detectInstruments: (imageData) => api.post('/detect', { image: imageData }),
  getStatus: () => api.get('/status'),
};

// Checklist API
export const checklistAPI = {
  getChecklist: () => api.get('/checklist'),
  confirmChecklist: (data) => api.post('/checklist/confirm', data),
  rescan: () => api.post('/rescan'),
};

// Utility functions
export const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { 
    hour12: true, 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  });
};

export const getStatusColor = (status) => {
  switch (status) {
    case 'found':
    case 'complete':
      return 'var(--success-green)';
    case 'missing':
    case 'extra':
      return 'var(--error-red)';
    case 'partial':
    case 'optional':
      return 'var(--warning-yellow)';
    default:
      return 'var(--neutral-gray)';
  }
};

export const getStatusIcon = (status) => {
  switch (status) {
    case 'found':
    case 'complete':
      return '✅';
    case 'missing':
    case 'extra':
      return '❌';
    case 'partial':
    case 'optional':
      return '⚠️';
    default:
      return '🔲';
  }
};

export default api; 