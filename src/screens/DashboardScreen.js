import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Dimensions,
  ScrollView,
} from 'react-native';
import { Card, Title, Paragraph, Button, FAB } from 'react-native-paper';
import { MaterialIcons } from '@expo/vector-icons';
import { Audio } from 'expo-av';

const { width, height } = Dimensions.get('window');

const DashboardScreen = ({ navigation }) => {
  const [isEmergencyActive, setIsEmergencyActive] = useState(false);
  const [systemStatus, setSystemStatus] = useState('Ready');
  const [lastEvent, setLastEvent] = useState(null);

  useEffect(() => {
    // Initialize audio for alerts
    setupAudio();
  }, []);

  const setupAudio = async () => {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: false,
        staysActiveInBackground: true,
        playsInSilentModeIOS: true,
        shouldDuckAndroid: true,
        playThroughEarpieceAndroid: false,
      });
    } catch (error) {
      console.log('Audio setup error:', error);
    }
  };

  const triggerCodeBlue = () => {
    Alert.alert(
      'Code Blue Emergency',
      'Are you sure you want to trigger a Code Blue emergency?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Trigger Emergency',
          style: 'destructive',
          onPress: () => {
            setIsEmergencyActive(true);
            setSystemStatus('Emergency Active');
            setLastEvent(new Date());
            navigation.navigate('Emergency');
          },
        },
      ]
    );
  };

  const getStatusColor = () => {
    switch (systemStatus) {
      case 'Ready':
        return '#10b981';
      case 'Emergency Active':
        return '#ef4444';
      case 'System Error':
        return '#f59e0b';
      default:
        return '#6b7280';
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Critical Object Confirmation</Text>
        <Text style={styles.subtitle}>Code Blue Emergency System</Text>
      </View>

      {/* System Status Card */}
      <Card style={styles.statusCard}>
        <Card.Content>
          <View style={styles.statusRow}>
            <View style={[styles.statusIndicator, { backgroundColor: getStatusColor() }]} />
            <View style={styles.statusText}>
              <Title>System Status</Title>
              <Paragraph style={{ color: getStatusColor() }}>{systemStatus}</Paragraph>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Emergency Trigger Card */}
      <Card style={styles.triggerCard}>
        <Card.Content>
          <Title style={styles.triggerTitle}>Emergency Trigger</Title>
          <Paragraph style={styles.triggerDescription}>
            Trigger a Code Blue emergency to begin equipment verification
          </Paragraph>
          
          <TouchableOpacity
            style={[styles.emergencyButton, isEmergencyActive && styles.emergencyButtonActive]}
            onPress={triggerCodeBlue}
            disabled={isEmergencyActive}
          >
            <MaterialIcons 
              name="emergency" 
              size={32} 
              color={isEmergencyActive ? '#fff' : '#dc2626'} 
            />
            <Text style={[styles.emergencyButtonText, isEmergencyActive && styles.emergencyButtonTextActive]}>
              {isEmergencyActive ? 'EMERGENCY ACTIVE' : 'TRIGGER CODE BLUE'}
            </Text>
          </TouchableOpacity>
        </Card.Content>
      </Card>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Logs')}
        >
          <MaterialIcons name="history" size={24} color="#1e3a8a" />
          <Text style={styles.actionText}>Event Logs</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Settings')}
        >
          <MaterialIcons name="settings" size={24} color="#1e3a8a" />
          <Text style={styles.actionText}>Settings</Text>
        </TouchableOpacity>
      </View>

      {/* Last Event Info */}
      {lastEvent && (
        <Card style={styles.lastEventCard}>
          <Card.Content>
            <Title>Last Emergency Event</Title>
            <Paragraph>
              {lastEvent.toLocaleString()}
            </Paragraph>
          </Card.Content>
        </Card>
      )}

      {/* Equipment Status Preview */}
      <Card style={styles.equipmentCard}>
        <Card.Content>
          <Title>Required Equipment (Code Blue)</Title>
          <View style={styles.equipmentList}>
            {['AED', 'Crash Cart', 'Airway Bag', 'Oxygen Tank', 'Epinephrine'].map((item, index) => (
              <View key={index} style={styles.equipmentItem}>
                <MaterialIcons 
                  name="medical-services" 
                  size={20} 
                  color="#6b7280" 
                />
                <Text style={styles.equipmentText}>{item}</Text>
              </View>
            ))}
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    padding: 20,
    backgroundColor: '#1e3a8a',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#cbd5e1',
    marginTop: 5,
    textAlign: 'center',
  },
  statusCard: {
    margin: 16,
    elevation: 4,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 12,
  },
  statusText: {
    flex: 1,
  },
  triggerCard: {
    margin: 16,
    elevation: 4,
  },
  triggerTitle: {
    color: '#dc2626',
    fontWeight: 'bold',
  },
  triggerDescription: {
    marginVertical: 10,
    color: '#6b7280',
  },
  emergencyButton: {
    backgroundColor: '#fee2e2',
    borderWidth: 2,
    borderColor: '#dc2626',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    marginTop: 10,
  },
  emergencyButtonActive: {
    backgroundColor: '#dc2626',
  },
  emergencyButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#dc2626',
    marginTop: 8,
  },
  emergencyButtonTextActive: {
    color: '#fff',
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    margin: 16,
  },
  actionButton: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 2,
    minWidth: 100,
  },
  actionText: {
    marginTop: 8,
    fontSize: 14,
    fontWeight: '600',
    color: '#1e3a8a',
  },
  lastEventCard: {
    margin: 16,
    elevation: 2,
  },
  equipmentCard: {
    margin: 16,
    elevation: 2,
  },
  equipmentList: {
    marginTop: 10,
  },
  equipmentItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  equipmentText: {
    marginLeft: 12,
    fontSize: 16,
    color: '#374151',
  },
});

export default DashboardScreen; 