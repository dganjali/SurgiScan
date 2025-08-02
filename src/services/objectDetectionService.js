// Object Detection Service
// Handles integration with OpenMV for real-time equipment detection

class ObjectDetectionService {
  constructor() {
    this.isActive = false;
    this.detectionInterval = null;
    this.onDetectionCallback = null;
    this.currentEmergencyType = null;
    this.detectedEquipment = [];
    this.confidenceThreshold = 0.6;
  }

  // Initialize the detection service
  initialize(emergencyType, callback) {
    this.currentEmergencyType = emergencyType;
    this.onDetectionCallback = callback;
    this.detectedEquipment = [];
    this.isActive = true;
    
    console.log(`Object detection initialized for ${emergencyType}`);
    
    // Start detection loop
    this.startDetection();
  }

  // Start the detection loop
  startDetection() {
    if (this.detectionInterval) {
      clearInterval(this.detectionInterval);
    }

    // Simulate detection updates every 2 seconds
    this.detectionInterval = setInterval(() => {
      this.performDetection();
    }, 2000);
  }

  // Perform object detection (simulated for now, will integrate with OpenMV)
  async performDetection() {
    if (!this.isActive) return;

    try {
      // Simulate detection results
      const detectionResults = this.simulateDetection();
      
      // Process detection results
      this.processDetectionResults(detectionResults);
      
      // Notify callback with updated results
      if (this.onDetectionCallback) {
        this.onDetectionCallback(this.detectedEquipment);
      }
    } catch (error) {
      console.error('Detection error:', error);
    }
  }

  // Simulate detection results (replace with actual OpenMV integration)
  simulateDetection() {
    const possibleEquipment = [
      { name: 'AED', confidence: 0.85 },
      { name: 'Crash Cart', confidence: 0.78 },
      { name: 'Airway Bag', confidence: 0.72 },
      { name: 'Oxygen Tank', confidence: 0.68 },
      { name: 'Epinephrine', confidence: 0.55 },
    ];

    // Randomly detect 1-3 pieces of equipment
    const numDetections = Math.floor(Math.random() * 3) + 1;
    const shuffled = possibleEquipment.sort(() => 0.5 - Math.random());
    const detected = shuffled.slice(0, numDetections);

    // Add some randomness to confidence scores
    return detected.map(item => ({
      ...item,
      confidence: item.confidence + (Math.random() * 0.2 - 0.1), // ±0.1 variation
      timestamp: new Date(),
    }));
  }

  // Process detection results
  processDetectionResults(results) {
    results.forEach(detection => {
      if (detection.confidence >= this.confidenceThreshold) {
        // Update or add detection
        const existingIndex = this.detectedEquipment.findIndex(
          item => item.name === detection.name
        );

        if (existingIndex >= 0) {
          // Update existing detection
          this.detectedEquipment[existingIndex] = {
            ...this.detectedEquipment[existingIndex],
            confidence: detection.confidence,
            lastSeen: detection.timestamp,
            detectionCount: (this.detectedEquipment[existingIndex].detectionCount || 0) + 1,
          };
        } else {
          // Add new detection
          this.detectedEquipment.push({
            name: detection.name,
            confidence: detection.confidence,
            firstSeen: detection.timestamp,
            lastSeen: detection.timestamp,
            detectionCount: 1,
          });
        }
      }
    });

    // Remove stale detections (not seen in last 10 seconds)
    const now = new Date();
    this.detectedEquipment = this.detectedEquipment.filter(item => {
      const timeSinceLastSeen = (now - item.lastSeen) / 1000;
      return timeSinceLastSeen < 10; // Keep if seen within 10 seconds
    });
  }

  // Get current detection status
  getDetectionStatus() {
    return {
      isActive: this.isActive,
      detectedEquipment: [...this.detectedEquipment],
      totalDetected: this.detectedEquipment.length,
      emergencyType: this.currentEmergencyType,
    };
  }

  // Stop detection service
  stop() {
    this.isActive = false;
    if (this.detectionInterval) {
      clearInterval(this.detectionInterval);
      this.detectionInterval = null;
    }
    console.log('Object detection service stopped');
  }

  // Set confidence threshold
  setConfidenceThreshold(threshold) {
    this.confidenceThreshold = Math.max(0, Math.min(1, threshold));
  }

  // Get detection statistics
  getDetectionStats() {
    const stats = {
      totalDetections: this.detectedEquipment.length,
      averageConfidence: 0,
      mostDetected: null,
      detectionHistory: [],
    };

    if (this.detectedEquipment.length > 0) {
      const totalConfidence = this.detectedEquipment.reduce(
        (sum, item) => sum + item.confidence, 0
      );
      stats.averageConfidence = totalConfidence / this.detectedEquipment.length;

      // Find most frequently detected item
      stats.mostDetected = this.detectedEquipment.reduce((max, item) => 
        (item.detectionCount || 0) > (max.detectionCount || 0) ? item : max
      );
    }

    return stats;
  }

  // Integration with OpenMV (placeholder for future implementation)
  async connectToOpenMV(deviceAddress) {
    try {
      console.log(`Connecting to OpenMV device at ${deviceAddress}`);
      
      // TODO: Implement actual OpenMV connection
      // This would involve:
      // 1. Establishing WebSocket connection to OpenMV
      // 2. Sending detection requests
      // 3. Receiving detection results
      // 4. Processing results in real-time
      
      return true;
    } catch (error) {
      console.error('OpenMV connection failed:', error);
      return false;
    }
  }

  // Send detection request to OpenMV
  async requestDetection(frameData) {
    try {
      // TODO: Send frame data to OpenMV for processing
      // This would involve:
      // 1. Converting frame to appropriate format
      // 2. Sending to OpenMV via WebSocket
      // 3. Receiving detection results
      
      console.log('Detection request sent to OpenMV');
      return this.simulateDetection(); // Fallback to simulation
    } catch (error) {
      console.error('Detection request failed:', error);
      return [];
    }
  }

  // Configure detection parameters
  configureDetection(params) {
    const {
      confidenceThreshold = 0.6,
      detectionInterval = 2000,
      maxDetections = 10,
    } = params;

    this.confidenceThreshold = confidenceThreshold;
    
    if (this.detectionInterval) {
      clearInterval(this.detectionInterval);
      this.detectionInterval = setInterval(() => {
        this.performDetection();
      }, detectionInterval);
    }
  }
}

// Export singleton instance
export const objectDetectionService = new ObjectDetectionService();
export default objectDetectionService; 