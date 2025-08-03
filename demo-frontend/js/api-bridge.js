// SurgiScan API Bridge - Connects frontend with backend MCP server

class SurgiScanAPI {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.isConnected = false;
        this.init();
    }

    async init() {
        try {
            const response = await this.healthCheck();
            this.isConnected = response.status === 'healthy';
            console.log('SurgiScan API connected:', this.isConnected);
        } catch (error) {
            console.error('Failed to connect to SurgiScan API:', error);
            this.isConnected = false;
        }
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`API request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    // Health Check
    async healthCheck() {
        return await this.makeRequest('/health');
    }

    // Surgical Backtable Analysis - Streamlit Enhanced
    async getSurgicalSpecialties() {
        return await this.makeRequest('/surgical/streamlit-specialties');
    }

    async getProceduresBySpecialty(specialty) {
        return await this.makeRequest(`/surgical/streamlit-procedures/${specialty}`);
    }

    async analyzeSurgicalBacktable(procedure, specialty) {
        try {
            console.log('Making API request for:', procedure, specialty);
            
            const response = await fetch(`${this.baseURL}/surgical/analyze-streamlit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    procedure: procedure,
                    specialty: specialty
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Raw API response:', result);
            
            // Transform the API result to match frontend expectations
            const transformedResult = {
                procedure: result.procedure,
                totalInstruments: result.total_instruments,
                validatedInstruments: result.validated_instruments,
                missingInstruments: result.missing_instruments,
                confidenceScore: Math.round((result.confidence_score || 0) * 100),
                categories: result.categories || {},
                detectedItems: result.detected_items || [],
                missingItems: result.missing_items || [],
                sourcesAnalyzed: result.sources_analyzed,
                processingTime: result.processing_time_seconds
            };
            
            console.log('Transformed result:', transformedResult);
            return transformedResult;
            
        } catch (error) {
            console.error('Error analyzing surgical backtable:', error);
            throw new Error('Failed to analyze surgical backtable: ' + error.message);
        }
    }

    // File Upload and Video Playback
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const url = `${this.baseURL}/upload`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        return await response.json();
    }

    async getVideos() {
        return await this.makeRequest('/videos');
    }

    getVideoUrl(filename) {
        return `${this.baseURL}/video/${filename}`;
    }

    getOutputVideoUrl() {
        return `${this.baseURL}/output-video`;
    }

    async processVideo(filename) {
        return await this.makeRequest('/process-video', {
            method: 'POST',
            body: JSON.stringify({ filename: filename })
        });
    }

    // Export Reports
    async exportReport(type, data) {
        return await this.makeRequest('/export-report', {
            method: 'POST',
            body: JSON.stringify({ 
                type: type,
                data: data 
            })
        });
    }
}

// Enhanced Dashboard with API Integration
class SurgiScanDashboardWithAPI extends SurgiScanDashboard {
    constructor() {
        super();
        this.api = new SurgiScanAPI();
        this.setupAPIEventListeners();
    }

    setupAPIEventListeners() {
        // Override the analysis methods to use the API
        this.originalAnalyzeSurgical = this.analyzeSurgical;

        // Replace with API versions
        this.analyzeSurgical = this.analyzeSurgicalWithAPI.bind(this);
        this.handleFileUpload = this.handleFileUploadWithAPI.bind(this);
    }

    async analyzeSurgicalWithAPI() {
        const selectedProcedure = document.getElementById('procedureSelect').value;
        const selectedSpecialty = document.getElementById('specialtySelect').value;
        
        if (!selectedProcedure || !selectedSpecialty) {
            this.showNotification('Please select both specialty and procedure first', 'error');
            return;
        }

        this.showLoadingOverlay();

        try {
            const result = await this.api.analyzeSurgicalBacktable(selectedProcedure, selectedSpecialty);
            this.hideLoadingOverlay();
            
            // Update the display with real API data
            this.displaySurgicalResultsFromAPI(result);
            this.showNotification('Surgical backtable analysis completed', 'success');
            
        } catch (error) {
            this.hideLoadingOverlay();
            this.showNotification(`Analysis failed: ${error.message}`, 'error');
            console.error('Surgical analysis error:', error);
        }
    }

    displaySurgicalResultsFromAPI(apiResult) {
        const resultsContainer = document.getElementById('surgicalResults');
        
        // Update summary stats
        document.getElementById('confidenceScore').textContent = `${apiResult.confidenceScore}%`;
        document.getElementById('validatedItems').textContent = apiResult.validatedInstruments;
        document.getElementById('missingItems').textContent = apiResult.missingInstruments;

        // Display results
        resultsContainer.innerHTML = '';
        
        Object.entries(apiResult.categories).forEach(([category, instruments]) => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'bg-white rounded-lg p-4 border border-gray-200';
            
            const categoryTitle = document.createElement('h4');
            categoryTitle.className = 'text-lg font-semibold text-gray-900 mb-3';
            categoryTitle.textContent = category;
            categoryDiv.appendChild(categoryTitle);
            
            const instrumentsList = document.createElement('div');
            instrumentsList.className = 'space-y-2';
            
            instruments.forEach(instrument => {
                const instrumentDiv = document.createElement('div');
                instrumentDiv.className = 'flex items-center justify-between p-3 bg-gray-50 rounded-md';
                
                const instrumentName = document.createElement('span');
                instrumentName.className = 'text-gray-700 font-medium';
                instrumentName.textContent = instrument.name;
                
                const statusDiv = document.createElement('div');
                statusDiv.className = 'flex items-center space-x-2';
                
                const statusBadge = document.createElement('span');
                statusBadge.className = this.getStatusBadgeClass(instrument.status);
                statusBadge.textContent = this.getStatusText(instrument.status);
                
                const confidenceSpan = document.createElement('span');
                confidenceSpan.className = 'text-xs text-gray-500';
                confidenceSpan.textContent = `${instrument.confidence}%`;
                
                statusDiv.appendChild(statusBadge);
                statusDiv.appendChild(confidenceSpan);
                
                instrumentDiv.appendChild(instrumentName);
                instrumentDiv.appendChild(statusDiv);
                instrumentsList.appendChild(instrumentDiv);
            });
            
            categoryDiv.appendChild(instrumentsList);
            resultsContainer.appendChild(categoryDiv);
        });

        this.updateLabelsTableFromAPI(apiResult);
    }

    updateLabelsTableFromAPI(apiResult) {
        const tableBody = document.getElementById('labelsTable');
        tableBody.innerHTML = '';

        // Flatten all items from all categories
        const allItems = [];
        Object.entries(apiResult.categories).forEach(([category, items]) => {
            items.forEach(item => {
                allItems.push({
                    name: item.name,
                    category: category,
                    status: item.status,
                    confidence: item.confidence,
                    source: item.source || 'Medical Literature Analysis'
                });
            });
        });

        if (allItems.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" class="px-6 py-4 text-center text-gray-500">No items detected yet</td>';
            tableBody.appendChild(row);
            return;
        }

        allItems.forEach(item => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-gray-50';
            
            // Format source for better display
            let sourceDisplay = item.source;
            if (sourceDisplay && sourceDisplay.includes('(') && sourceDisplay.includes(')')) {
                // Extract title and URL from format "Title (URL)"
                const match = sourceDisplay.match(/(.*?)\s*\((.*?)\)/);
                if (match) {
                    const title = match[1].trim();
                    const url = match[2].trim();
                    sourceDisplay = `<span class="font-medium">${title}</span><br><span class="text-xs text-blue-500">${url}</span>`;
                }
            }
            
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.category}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="${this.getStatusBadgeClass(item.status)}">${this.getStatusText(item.status)}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.confidence}%</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${sourceDisplay}</td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Enhanced file upload with API and video playback
    async handleFileUploadWithAPI(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.uploadedFile = file;
        this.showNotification(`File uploaded: ${file.name}`, 'success');
        
        // Upload to backend
        try {
            const uploadResult = await this.api.uploadFile(file);
            this.showNotification('File uploaded to server successfully', 'success');
            
            // If it's a video file, process it and enable playback
            if (file.type.startsWith('video/')) {
                this.processVideoFile(file, uploadResult.file_url);
                
                // Process with backend
                const processResult = await this.api.processVideo(uploadResult.filename);
                this.showNotification(`Video processed: ${processResult.detected_objects.length} objects detected`, 'success');
            }
            
        } catch (error) {
            this.showNotification(`Upload failed: ${error.message}`, 'error');
        }
    }

    processVideoFile(file, videoUrl) {
        // When any video is uploaded, play the output.mp4 file
        const video = document.getElementById('videoStream');
        if (video) {
            // Set the video source to output.mp4
            video.src = '../deployed_modelling/output.mp4';
            video.load();
            
            // Show the video in the livestream page
            const overlay = document.getElementById('streamOverlay');
            if (overlay) {
                overlay.style.display = 'none';
            }
            
            this.showNotification('Video processed - playing output.mp4', 'success');
        }
    }

    // Export functionality with API
    async exportReportWithAPI(type, data) {
        try {
            const result = await this.api.exportReport(type, data);
            this.showNotification('Report exported successfully', 'success');
            
            // Create download link
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${type}_analysis_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            URL.revokeObjectURL(url);
            
        } catch (error) {
            this.showNotification(`Export failed: ${error.message}`, 'error');
        }
    }
}

// Initialize the enhanced dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SurgiScanDashboardWithAPI();
}); 
