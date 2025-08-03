// SurgiScan Professional Dashboard JavaScript

class SurgiScanDashboard {
    constructor() {
        this.currentPage = 'dashboard';
        this.currentTab = 'surgical';
        this.uploadedFile = null;
        this.streamActive = false;
        this.isAnalyzing = false;
        this.init();
    }

    init() {
        this.initializeFeatherIcons();
        this.setupEventListeners();
        this.loadSampleData();
        this.loadSpecialties();
        this.updateCurrentTime();
        setInterval(() => this.updateCurrentTime(), 1000);
    }

    initializeFeatherIcons() {
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    setupEventListeners() {
        // Navigation
        document.getElementById('dashboardTab').addEventListener('click', () => this.switchPage('dashboard'));
        document.getElementById('livestreamTab').addEventListener('click', () => this.switchPage('livestream'));

        // File upload
        document.getElementById('uploadBtn').addEventListener('click', () => document.getElementById('fileInput').click());
        document.getElementById('fileInput').addEventListener('change', (e) => this.handleFileUpload(e));

        // Analysis buttons
        document.getElementById('analyzeSurgical').addEventListener('click', () => this.analyzeSurgical());

        // Specialty selection
        document.getElementById('specialtySelect').addEventListener('change', (e) => this.updateProcedures(e.target.value));

        // Livestream controls
        document.getElementById('startStreamBtn').addEventListener('click', () => this.startStream());
        document.getElementById('stopStreamBtn').addEventListener('click', () => this.stopStream());

        // Confidence slider
        document.getElementById('confidenceSlider').addEventListener('input', (e) => {
            document.getElementById('confidenceValue').textContent = e.target.value + '%';
        });
    }

    switchPage(page) {
        this.currentPage = page;
        
        // Update navigation tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active', 'text-surgiscan', 'border-surgiscan');
            tab.classList.add('text-gray-500');
        });

        if (page === 'dashboard') {
            document.getElementById('dashboardTab').classList.add('active', 'text-surgiscan', 'border-surgiscan');
            document.getElementById('dashboardTab').classList.remove('text-gray-500');
            document.getElementById('dashboardPage').classList.remove('hidden');
            document.getElementById('livestreamPage').classList.add('hidden');
        } else {
            document.getElementById('livestreamTab').classList.add('active', 'text-surgiscan', 'border-surgiscan');
            document.getElementById('livestreamTab').classList.remove('text-gray-500');
            document.getElementById('livestreamPage').classList.remove('hidden');
            document.getElementById('dashboardPage').classList.add('hidden');
        }
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.uploadedFile = file;
        this.showNotification(`File uploaded: ${file.name}`, 'success');
        
        // Show the video upload section
        const videoSection = document.getElementById('videoUploadSection');
        videoSection.classList.remove('hidden');
        
        // Set up the original video
        const originalVideo = document.getElementById('originalVideo');
        const originalUrl = URL.createObjectURL(file);
        originalVideo.src = originalUrl;
        originalVideo.load();
        
        // Set up the processed video (output.mp4) - use API endpoint
        const processedVideo = document.getElementById('processedVideo');
        processedVideo.src = 'http://localhost:5000/api/output-video';
        processedVideo.load();
        
        // If it's a video file, we can process it
        if (file.type.startsWith('video/')) {
            this.processVideoFile(file);
        }
    }

    processVideoFile(file) {
        // When any video is uploaded, play the output.mp4 file
        const video = document.getElementById('videoStream');
        if (video) {
            // Set the video source to output.mp4 via API
            video.src = 'http://localhost:5000/api/output-video';
            video.load();
            
            // Show the video in the livestream page
            const overlay = document.getElementById('streamOverlay');
            if (overlay) {
                overlay.style.display = 'none';
            }
            
            this.showNotification('Video processed - playing output.mp4', 'success');
        }
    }

    async updateProcedures(specialty) {
        const procedureSelect = document.getElementById('procedureSelect');
        procedureSelect.innerHTML = '<option value="">Select procedure...</option>';
        
        if (!specialty) return;
        
        try {
            const response = await fetch(`http://localhost:5000/api/surgical/streamlit-procedures/${specialty}`);
            if (response.ok) {
                const data = await response.json();
                data.procedures.forEach(procedure => {
                    const option = document.createElement('option');
                    option.value = procedure;
                    option.textContent = procedure;
                    procedureSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading procedures:', error);
        }
    }

    getProceduresBySpecialty(specialty) {
        const procedures = {
            'orthopedic': [
                { value: 'tka', name: 'Total Knee Arthroplasty (TKA)' },
                { value: 'tha', name: 'Total Hip Arthroplasty (THA)' },
                { value: 'acl', name: 'Anterior Cruciate Ligament (ACL) Reconstruction' },
                { value: 'orif', name: 'Open Reduction Internal Fixation (ORIF)' },
                { value: 'shoulder', name: 'Shoulder Arthroscopy with Rotator Cuff Repair' },
                { value: 'carpal', name: 'Carpal Tunnel Release' }
            ],
            'neurosurgery': [
                { value: 'craniotomy', name: 'Craniotomy for Tumor Resection' },
                { value: 'laminectomy', name: 'Laminectomy for Spinal Stenosis' },
                { value: 'aneurysm', name: 'Aneurysm Clipping' },
                { value: 'vp_shunt', name: 'Ventriculoperitoneal (VP) Shunt Placement' }
            ],
            'cardiothoracic': [
                { value: 'cabg', name: 'Coronary Artery Bypass Grafting (CABG)' },
                { value: 'lobectomy', name: 'Lobectomy (lung resection)' },
                { value: 'thoracotomy', name: 'Thoracotomy with Pleural Decortication' },
                { value: 'vats', name: 'Video-Assisted Thoracoscopic Surgery (VATS)' }
            ],
            'general': [
                { value: 'cholecystectomy', name: 'Laparoscopic Cholecystectomy' },
                { value: 'hernia', name: 'Hernia Repair (Inguinal or Ventral)' },
                { value: 'colectomy', name: 'Colectomy (partial or total)' },
                { value: 'gastrectomy', name: 'Gastrectomy (partial or full stomach removal)' }
            ],
            'gynecologic': [
                { value: 'oophorectomy', name: 'Laparoscopic Oophorectomy' },
                { value: 'myomectomy', name: 'Myomectomy (fibroid removal)' },
                { value: 'ablation', name: 'Endometrial Ablation' },
                { value: 'cesarean', name: 'Cesarean Section (C-Section)' }
            ]
        };

        return procedures[specialty] || [];
    }

    async analyzeSurgical() {
        const selectedProcedure = document.getElementById('procedureSelect').value;
        if (!selectedProcedure) {
            this.showNotification('Please select a surgical procedure first', 'error');
            return;
        }

        // Prevent multiple simultaneous analyses
        if (this.isAnalyzing) {
            console.log('Analysis already in progress, ignoring request');
            return;
        }
        
        this.isAnalyzing = true;

        try {
            console.log('Starting MCP analysis...');
            
            // Make direct API call to MCP server
            const api = new SurgiScanAPI();
            const result = await api.analyzeSurgicalBacktable(selectedProcedure, this.getSelectedSpecialty());
            
            console.log('API result:', result);
            
            // Display results immediately
            this.displaySurgicalResults(result);
            this.showNotification('Surgical backtable analysis completed successfully', 'success');
            
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            // Always reset the analyzing flag
            this.isAnalyzing = false;
        }
    }

    displaySurgicalResults(apiResult) {
        const resultsContainer = document.getElementById('surgicalResults');
        
        // Update summary stats
        document.getElementById('confidenceScore').textContent = `${apiResult.confidenceScore}%`;
        document.getElementById('validatedItems').textContent = apiResult.validatedInstruments;
        document.getElementById('missingItems').textContent = apiResult.missingInstruments;

        // Display results
        resultsContainer.innerHTML = '';
        
        // Show detected items by category
        if (apiResult.categories && Object.keys(apiResult.categories).length > 0) {
            Object.entries(apiResult.categories).forEach(([category, instruments]) => {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'bg-dark-surface rounded-xl p-6 border border-dark-border shadow-lg mb-4';
                
                const categoryTitle = document.createElement('h4');
                categoryTitle.className = 'text-xl font-semibold text-dark-text mb-4';
                categoryTitle.textContent = category;
                categoryDiv.appendChild(categoryTitle);
                
                const instrumentsList = document.createElement('div');
                instrumentsList.className = 'space-y-3';
                
                instruments.forEach(instrument => {
                    const instrumentDiv = document.createElement('div');
                    instrumentDiv.className = 'flex items-center justify-between p-4 bg-dark-bg rounded-lg border border-dark-border';
                    
                    const instrumentName = document.createElement('span');
                    instrumentName.className = 'text-dark-text font-medium';
                    instrumentName.textContent = instrument.name;
                    
                    const statusDiv = document.createElement('div');
                    statusDiv.className = 'flex items-center space-x-3';
                    
                    const statusBadge = document.createElement('span');
                    statusBadge.className = this.getStatusBadgeClass(instrument.status);
                    statusBadge.textContent = this.getStatusText(instrument.status);
                    
                    const confidenceSpan = document.createElement('span');
                    confidenceSpan.className = 'text-sm text-gray-300';
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
        } else {
            // Show a message if no categories
            const noResultsDiv = document.createElement('div');
            noResultsDiv.className = 'text-center text-gray-400 py-8';
            noResultsDiv.innerHTML = `
                <i data-feather="info" class="w-12 h-12 mx-auto mb-4 text-surgiscan"></i>
                <p class="text-lg">Analysis completed. Check the table below for detailed results.</p>
            `;
            resultsContainer.appendChild(noResultsDiv);
        }

        this.updateLabelsTable(apiResult);
    }

    updateLabelsTable(apiResult) {
        const tableBody = document.getElementById('labelsTable');
        tableBody.innerHTML = '';

        // Combine detected items and missing items
        const allItems = [];
        
        // Add detected items (validated instruments)
        if (apiResult.detectedItems) {
            apiResult.detectedItems.forEach(item => {
                allItems.push({
                    name: item.name,
                    category: item.category,
                    status: 'validated',
                    confidence: item.confidence,
                    source: item.source || 'MCP Analysis',
                    reasoning: item.reasoning || 'Validated through multiple sources'
                });
            });
        }
        
        // Add missing items (low confidence but not zero)
        if (apiResult.missingItems) {
            apiResult.missingItems.forEach(item => {
                allItems.push({
                    name: item.name,
                    category: item.category,
                    status: 'missing',
                    confidence: item.confidence,
                    source: item.source || 'MCP Analysis',
                    reasoning: item.reasoning || 'Low confidence detection'
                });
            });
        }

        if (allItems.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" class="px-6 py-8 text-center text-gray-400">No items detected yet</td>';
            tableBody.appendChild(row);
            return;
        }

        allItems.forEach(item => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-dark-surface transition-colors duration-200';
            
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-dark-text">${item.name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">${item.category}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="${this.getStatusBadgeClass(item.status)}">${this.getStatusText(item.status)}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">${item.confidence}%</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300" title="${item.reasoning}">${item.source}</td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    getStatusBadgeClass(status) {
        switch (status) {
            case 'validated':
                return 'inline-flex px-3 py-1 text-xs font-semibold rounded-full bg-green-500 text-white shadow-sm';
            case 'missing':
                return 'inline-flex px-3 py-1 text-xs font-semibold rounded-full bg-yellow-500 text-white shadow-sm';
            case 'extra':
                return 'inline-flex px-3 py-1 text-xs font-semibold rounded-full bg-blue-500 text-white shadow-sm';
            default:
                return 'inline-flex px-3 py-1 text-xs font-semibold rounded-full bg-gray-500 text-white shadow-sm';
        }
    }

    getStatusText(status) {
        switch (status) {
            case 'validated':
                return 'Validated';
            case 'missing':
                return 'Missing';
            case 'extra':
                return 'Extra';
            default:
                return 'Unknown';
        }
    }

    startStream() {
        this.streamActive = true;
        document.getElementById('startStreamBtn').classList.add('hidden');
        document.getElementById('stopStreamBtn').classList.remove('hidden');
        
        // Simulate stream start
        this.showNotification('Live stream started', 'success');
        
        // Update segmented objects
        const segmentedObjects = document.getElementById('segmentedObjects');
        segmentedObjects.innerHTML = `
            <div class="bg-green-100 border border-green-200 rounded-lg p-3">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-green-800">Scalpel</span>
                    <span class="text-xs text-green-600">92%</span>
                </div>
            </div>
            <div class="bg-green-100 border border-green-200 rounded-lg p-3">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-green-800">Forceps</span>
                    <span class="text-xs text-green-600">88%</span>
                </div>
            </div>
            <div class="bg-yellow-100 border border-yellow-200 rounded-lg p-3">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-yellow-800">Retractor</span>
                    <span class="text-xs text-yellow-600">75%</span>
                </div>
            </div>
        `;
    }

    stopStream() {
        this.streamActive = false;
        document.getElementById('stopStreamBtn').classList.add('hidden');
        document.getElementById('startStreamBtn').classList.remove('hidden');
        
        this.showNotification('Live stream stopped', 'info');
        
        // Clear segmented objects
        const segmentedObjects = document.getElementById('segmentedObjects');
        segmentedObjects.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i data-feather="layers" class="w-8 h-8 mx-auto mb-2 text-surgiscan"></i>
                <p class="text-sm">No objects detected</p>
            </div>
        `;
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('notificationContainer');
        const notification = document.createElement('div');
        notification.className = `notification ${type} mb-2`;
        notification.textContent = message;
        
        container.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => container.removeChild(notification), 300);
        }, 3000);
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const dateString = now.toLocaleDateString();
        document.getElementById('currentTime').textContent = `${dateString} ${timeString}`;
    }

    loadSampleData() {
        // Load any initial data if needed
    }

    async loadSpecialties() {
        try {
            const response = await fetch('http://localhost:5000/api/surgical/streamlit-specialties');
            if (response.ok) {
                const data = await response.json();
                const specialtySelect = document.getElementById('specialtySelect');
                
                // Clear existing options except the first one
                specialtySelect.innerHTML = '<option value="">Select specialty...</option>';
                
                data.specialties.forEach(specialty => {
                    const option = document.createElement('option');
                    option.value = specialty;
                    option.textContent = specialty;
                    specialtySelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading specialties:', error);
        }
    }

    getSelectedSpecialty() {
        return document.getElementById('specialtySelect').value;
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SurgiScanDashboard();
}); 
