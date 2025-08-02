// Emergency Protocols Configuration
// Defines required equipment for different emergency types

export const EMERGENCY_PROTOCOLS = {
  'Code Blue': {
    name: 'Cardiac Arrest',
    description: 'Patient experiencing cardiac arrest requiring immediate resuscitation',
    requiredEquipment: [
      {
        name: 'AED',
        description: 'Automated External Defibrillator',
        priority: 'Critical',
        detectionKeywords: ['aed', 'defibrillator', 'defib'],
        confidence: 0.8,
      },
      {
        name: 'Crash Cart',
        description: 'Emergency medication and equipment cart',
        priority: 'Critical',
        detectionKeywords: ['crash cart', 'emergency cart', 'code cart'],
        confidence: 0.8,
      },
      {
        name: 'Airway Bag',
        description: 'Bag valve mask and airway management equipment',
        priority: 'Critical',
        detectionKeywords: ['airway bag', 'bag valve', 'bmv', 'ventilation'],
        confidence: 0.7,
      },
      {
        name: 'Oxygen Tank',
        description: 'Oxygen cylinder for patient ventilation',
        priority: 'Critical',
        detectionKeywords: ['oxygen tank', 'oxygen cylinder', 'o2 tank'],
        confidence: 0.7,
      },
      {
        name: 'Epinephrine',
        description: 'Epinephrine auto-injector or vial',
        priority: 'Critical',
        detectionKeywords: ['epinephrine', 'epi', 'adrenaline'],
        confidence: 0.6,
      },
    ],
    timeout: 30, // seconds
    location: 'ER/Ambulance',
  },
  
  'Code Red': {
    name: 'Fire Emergency',
    description: 'Fire or smoke emergency requiring evacuation',
    requiredEquipment: [
      {
        name: 'Fire Extinguisher',
        description: 'Portable fire extinguisher',
        priority: 'Critical',
        detectionKeywords: ['fire extinguisher', 'extinguisher'],
        confidence: 0.8,
      },
      {
        name: 'Emergency Exit',
        description: 'Designated emergency exit route',
        priority: 'Critical',
        detectionKeywords: ['exit', 'emergency exit', 'fire exit'],
        confidence: 0.9,
      },
      {
        name: 'Fire Alarm',
        description: 'Fire alarm system activation',
        priority: 'Critical',
        detectionKeywords: ['fire alarm', 'alarm'],
        confidence: 0.9,
      },
    ],
    timeout: 60, // seconds
    location: 'Hospital/Ambulance',
  },
  
  'Code Pink': {
    name: 'Infant/Child Abduction',
    description: 'Missing or abducted infant or child',
    requiredEquipment: [
      {
        name: 'Security Badge',
        description: 'Staff identification and access control',
        priority: 'High',
        detectionKeywords: ['badge', 'id card', 'security badge'],
        confidence: 0.7,
      },
      {
        name: 'Emergency Contact',
        description: 'Emergency contact information',
        priority: 'High',
        detectionKeywords: ['contact', 'emergency contact'],
        confidence: 0.6,
      },
      {
        name: 'Safe Room',
        description: 'Designated safe room location',
        priority: 'High',
        detectionKeywords: ['safe room', 'secure room'],
        confidence: 0.8,
      },
    ],
    timeout: 45, // seconds
    location: 'Hospital',
  },
};

export const getProtocolByType = (emergencyType) => {
  return EMERGENCY_PROTOCOLS[emergencyType] || null;
};

export const getRequiredEquipment = (emergencyType) => {
  const protocol = getProtocolByType(emergencyType);
  return protocol ? protocol.requiredEquipment : [];
};

export const getEquipmentNames = (emergencyType) => {
  const equipment = getRequiredEquipment(emergencyType);
  return equipment.map(item => item.name);
};

export const getTimeout = (emergencyType) => {
  const protocol = getProtocolByType(emergencyType);
  return protocol ? protocol.timeout : 30;
};

export const validateEquipmentDetection = (emergencyType, detectedEquipment) => {
  const requiredEquipment = getRequiredEquipment(emergencyType);
  const missingEquipment = [];
  const detectedItems = [];

  requiredEquipment.forEach(equipment => {
    const isDetected = detectedEquipment.some(detected => 
      detected.name.toLowerCase().includes(equipment.name.toLowerCase()) ||
      equipment.detectionKeywords.some(keyword => 
        detected.name.toLowerCase().includes(keyword.toLowerCase())
      )
    );

    if (isDetected) {
      detectedItems.push(equipment.name);
    } else {
      missingEquipment.push(equipment.name);
    }
  });

  return {
    success: missingEquipment.length === 0,
    detectedItems,
    missingEquipment,
    totalRequired: requiredEquipment.length,
    detectedCount: detectedItems.length,
  };
};

export const getDetectionKeywords = (equipmentName) => {
  for (const protocol of Object.values(EMERGENCY_PROTOCOLS)) {
    const equipment = protocol.requiredEquipment.find(item => 
      item.name.toLowerCase() === equipmentName.toLowerCase()
    );
    if (equipment) {
      return equipment.detectionKeywords;
    }
  }
  return [];
};

export const getEquipmentConfidence = (equipmentName) => {
  for (const protocol of Object.values(EMERGENCY_PROTOCOLS)) {
    const equipment = protocol.requiredEquipment.find(item => 
      item.name.toLowerCase() === equipmentName.toLowerCase()
    );
    if (equipment) {
      return equipment.confidence;
    }
  }
  return 0.5; // Default confidence
}; 