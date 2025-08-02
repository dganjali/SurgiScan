import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Dimensions,
  ScrollView,
  Animated,
} from 'react-native';
import { Card, Title, Paragraph, Button, ProgressBar } from 'react-native-paper';
import { MaterialIcons } from '@expo/vector-icons';
import { Audio } from 'expo-av';
import { Camera } from 'expo-camera';

const { width, height } = Dimensions.get('window');

const EmergencyScreen = ({ navigation }) => {
  const [timeRemaining, setTimeRemaining] = useState(30);
  const [isActive, setIsActive] = useState(true);
  const [equipmentStatus, setEquipmentStatus] = useState({
    AED: { detected: false, confidence: 0, lastSeen: null },
    'Crash Cart': { detected: false, confidence: 0, lastSeen: null },
    'Airway Bag': { detected: false, confidence: 0, lastSeen: null },
    'Oxygen Tank': { detected: false, confidence: 0, lastSeen: null },
    'Epinephrine': { detected: false, confidence: 0, lastSeen: null },
  });
  const [cameraPermission, setCameraPermission] = useState(null);
  const [sound, setSound] = useState();
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // Code Blue required equipment
  const requiredEquipment = [
    'AED',
    'Crash Cart', 
    'Airway Bag',
    'Oxygen Tank',
    'Epinephrine'
  ];

  useEffect(() => {
    setupEmergency();
    return () => {
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, []);

  useEffect(() => {
    if (isActive && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timeRemaining === 0) {
      handleTimeExpired();
    }
  }, [timeRemaining, isActive]);

  useEffect(() => {
    // Simulate object detection updates
    const detectionInterval = setInterval(() => {
      simulateObjectDetection();
    }, 2000);

    return () => clearInterval(detectionInterval);
  }, []);

  const setupEmergency = async () => {
    // Request camera permission
    const { status } = await Camera.requestCameraPermissionsAsync();
    setCameraPermission(status === 'granted');

    // Setup alert sound
    try {
      const { sound } = await Audio.Sound.createAsync(
        require('../assets/alert.mp3')
      );
      setSound(sound);
    } catch (error) {
      console.log('Sound setup error:', error);
    }

    // Start pulse animation
    startPulseAnimation();
  };

  const startPulseAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.2,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const simulateObjectDetection = () => {
    // Simulate random equipment detection
    const randomEquipment = requiredEquipment[Math.floor(Math.random() * requiredEquipment.length)];
    const confidence = Math.random() * 0.4 + 0.6; // 60-100% confidence
    
    setEquipmentStatus(prev => ({
      ...prev,
      [randomEquipment]: {
        detected: true,
        confidence: confidence,
        lastSeen: new Date(),
      }
    }));
  };

  const handleTimeExpired = () => {
    setIsActive(false);
    playAlertSound();
    
    const missingEquipment = requiredEquipment.filter(
      item => !equipmentStatus[item].detected
    );

    Alert.alert(
      'Time Expired',
      `Emergency verification time expired. Missing equipment: ${missingEquipment.join(', ')}`,
      [
        {
          text: 'End Emergency',
          onPress: () => navigation.navigate('Dashboard'),
        },
        {
          text: 'Continue Monitoring',
          onPress: () => {
            setTimeRemaining(30);
            setIsActive(true);
          },
        },
      ]
    );
  };

  const playAlertSound = async () => {
    if (sound) {
      try {
        await sound.replayAsync();
      } catch (error) {
        console.log('Sound play error:', error);
      }
    }
  };

  const getEquipmentStatusColor = (detected, confidence) => {
    if (detected && confidence > 0.8) return '#10b981';
    if (detected && confidence > 0.6) return '#f59e0b';
    return '#ef4444';
  };

  const getEquipmentStatusIcon = (detected, confidence) => {
    if (detected && confidence > 0.8) return 'check-circle';
    if (detected && confidence > 0.6) return 'warning';
    return 'error';
  };

  const endEmergency = () => {
    Alert.alert(
      'End Emergency',
      'Are you sure you want to end this emergency?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'End Emergency',
          style: 'destructive',
          onPress: () => navigation.navigate('Dashboard'),
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      {/* Emergency Header */}
      <Animated.View 
        style={[
          styles.emergencyHeader,
          { transform: [{ scale: pulseAnim }] }
        ]}
      >
        <MaterialIcons name="emergency" size={32} color="#fff" />
        <Text style={styles.emergencyTitle}>CODE BLUE EMERGENCY</Text>
        <Text style={styles.emergencySubtitle}>Equipment Verification Active</Text>
      </Animated.View>

      {/* Countdown Timer */}
      <Card style={styles.timerCard}>
        <Card.Content>
          <Title style={styles.timerTitle}>Time Remaining</Title>
          <Text style={[styles.timerText, timeRemaining <= 10 && styles.timerWarning]}>
            {Math.floor(timeRemaining / 60)}:{(timeRemaining % 60).toString().padStart(2, '0')}
          </Text>
          <ProgressBar 
            progress={timeRemaining / 30} 
            color={timeRemaining <= 10 ? '#ef4444' : '#1e3a8a'}
            style={styles.progressBar}
          />
        </Card.Content>
      </Card>

      {/* Equipment Status */}
      <Card style={styles.equipmentCard}>
        <Card.Content>
          <Title>Equipment Verification</Title>
          <View style={styles.equipmentList}>
            {requiredEquipment.map((equipment, index) => {
              const status = equipmentStatus[equipment];
              const statusColor = getEquipmentStatusColor(status.detected, status.confidence);
              const statusIcon = getEquipmentStatusIcon(status.detected, status.confidence);
              
              return (
                <View key={index} style={styles.equipmentItem}>
                  <View style={styles.equipmentHeader}>
                    <MaterialIcons 
                      name={statusIcon} 
                      size={24} 
                      color={statusColor} 
                    />
                    <Text style={styles.equipmentName}>{equipment}</Text>
                  </View>
                  
                  <View style={styles.equipmentDetails}>
                    <Text style={[styles.statusText, { color: statusColor }]}>
                      {status.detected ? 'Detected' : 'Missing'}
                    </Text>
                    {status.detected && (
                      <Text style={styles.confidenceText}>
                        Confidence: {(status.confidence * 100).toFixed(1)}%
                      </Text>
                    )}
                    {status.lastSeen && (
                      <Text style={styles.lastSeenText}>
                        Last seen: {status.lastSeen.toLocaleTimeString()}
                      </Text>
                    )}
                  </View>
                </View>
              );
            })}
          </View>
        </Card.Content>
      </Card>

      {/* Camera Preview Placeholder */}
      <Card style={styles.cameraCard}>
        <Card.Content>
          <Title>Video Feed</Title>
          <View style={styles.cameraPlaceholder}>
            <MaterialIcons name="videocam" size={48} color="#6b7280" />
            <Text style={styles.cameraText}>Camera feed will be integrated with OpenMV</Text>
            <Text style={styles.cameraSubtext}>Object detection running in background</Text>
          </View>
        </Card.Content>
      </Card>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity
          style={styles.endButton}
          onPress={endEmergency}
        >
          <MaterialIcons name="stop" size={24} color="#fff" />
          <Text style={styles.endButtonText}>End Emergency</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  emergencyHeader: {
    backgroundColor: '#dc2626',
    padding: 20,
    alignItems: 'center',
    marginBottom: 16,
  },
  emergencyTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 8,
  },
  emergencySubtitle: {
    fontSize: 14,
    color: '#fecaca',
    marginTop: 4,
  },
  timerCard: {
    margin: 16,
    elevation: 4,
  },
  timerTitle: {
    textAlign: 'center',
    color: '#1e3a8a',
  },
  timerText: {
    fontSize: 48,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#1e3a8a',
    marginVertical: 10,
  },
  timerWarning: {
    color: '#ef4444',
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
  },
  equipmentCard: {
    margin: 16,
    elevation: 4,
  },
  equipmentList: {
    marginTop: 10,
  },
  equipmentItem: {
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
    paddingVertical: 12,
  },
  equipmentHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  equipmentName: {
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 12,
    color: '#374151',
  },
  equipmentDetails: {
    marginLeft: 36,
  },
  statusText: {
    fontSize: 14,
    fontWeight: '500',
  },
  confidenceText: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 2,
  },
  lastSeenText: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 2,
  },
  cameraCard: {
    margin: 16,
    elevation: 2,
  },
  cameraPlaceholder: {
    alignItems: 'center',
    padding: 40,
    backgroundColor: '#f3f4f6',
    borderRadius: 8,
    marginTop: 10,
  },
  cameraText: {
    marginTop: 16,
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
  },
  cameraSubtext: {
    marginTop: 8,
    fontSize: 14,
    color: '#9ca3af',
    textAlign: 'center',
  },
  actionButtons: {
    margin: 16,
  },
  endButton: {
    backgroundColor: '#dc2626',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    elevation: 4,
  },
  endButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default EmergencyScreen; 