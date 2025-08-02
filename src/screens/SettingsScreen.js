import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
} from 'react-native';
import { Card, Title, Paragraph, List, Divider, Button } from 'react-native-paper';
import { MaterialIcons } from '@expo/vector-icons';

const SettingsScreen = ({ navigation }) => {
  const [settings, setSettings] = useState({
    audioAlerts: true,
    visualAlerts: true,
    autoLogging: true,
    cameraEnabled: true,
    emergencyTimeout: 30,
    locationTracking: true,
  });

  const [equipmentProtocols, setEquipmentProtocols] = useState({
    'Code Blue': {
      AED: true,
      'Crash Cart': true,
      'Airway Bag': true,
      'Oxygen Tank': true,
      'Epinephrine': true,
    },
    'Code Red': {
      'Fire Extinguisher': true,
      'Emergency Exit': true,
      'Fire Alarm': true,
    },
    'Code Pink': {
      'Security Badge': true,
      'Emergency Contact': true,
      'Safe Room': true,
    },
  });

  const toggleSetting = (key) => {
    setSettings(prev => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const updateEmergencyTimeout = (timeout) => {
    setSettings(prev => ({
      ...prev,
      emergencyTimeout: timeout,
    }));
  };

  const toggleEquipmentProtocol = (emergencyType, equipment) => {
    setEquipmentProtocols(prev => ({
      ...prev,
      [emergencyType]: {
        ...prev[emergencyType],
        [equipment]: !prev[emergencyType][equipment],
      },
    }));
  };

  const resetSettings = () => {
    Alert.alert(
      'Reset Settings',
      'Are you sure you want to reset all settings to default?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: () => {
            setSettings({
              audioAlerts: true,
              visualAlerts: true,
              autoLogging: true,
              cameraEnabled: true,
              emergencyTimeout: 30,
              locationTracking: true,
            });
          },
        },
      ]
    );
  };

  const exportSettings = () => {
    Alert.alert(
      'Export Settings',
      'Settings export functionality will be implemented',
      [{ text: 'OK' }]
    );
  };

  const renderSettingItem = (title, description, value, onToggle, type = 'switch') => (
    <List.Item
      title={title}
      description={description}
      left={(props) => <MaterialIcons {...props} name="settings" size={24} color="#1e3a8a" />}
      right={() => (
        type === 'switch' ? (
          <Switch
            value={value}
            onValueChange={onToggle}
            trackColor={{ false: '#d1d5db', true: '#1e3a8a' }}
            thumbColor={value ? '#fff' : '#fff'}
          />
        ) : (
          <Text style={styles.settingValue}>{value}</Text>
        )
      )}
      style={styles.settingItem}
    />
  );

  return (
    <ScrollView style={styles.container}>
      {/* General Settings */}
      <Card style={styles.settingsCard}>
        <Card.Content>
          <Title>General Settings</Title>
          <Divider style={styles.divider} />
          
          {renderSettingItem(
            'Audio Alerts',
            'Play sound alerts for missing equipment',
            settings.audioAlerts,
            () => toggleSetting('audioAlerts')
          )}
          
          {renderSettingItem(
            'Visual Alerts',
            'Show visual alerts and notifications',
            settings.visualAlerts,
            () => toggleSetting('visualAlerts')
          )}
          
          {renderSettingItem(
            'Auto Logging',
            'Automatically log all emergency events',
            settings.autoLogging,
            () => toggleSetting('autoLogging')
          )}
          
          {renderSettingItem(
            'Camera Integration',
            'Enable camera for object detection',
            settings.cameraEnabled,
            () => toggleSetting('cameraEnabled')
          )}
          
          {renderSettingItem(
            'Location Tracking',
            'Track emergency location for logging',
            settings.locationTracking,
            () => toggleSetting('locationTracking')
          )}
          
          {renderSettingItem(
            'Emergency Timeout',
            'Time limit for equipment verification (seconds)',
            `${settings.emergencyTimeout}s`,
            null,
            'value'
          )}
        </Card.Content>
      </Card>

      {/* Emergency Protocols */}
      <Card style={styles.settingsCard}>
        <Card.Content>
          <Title>Emergency Protocols</Title>
          <Paragraph style={styles.sectionDescription}>
            Configure required equipment for different emergency types
          </Paragraph>
          
          {Object.entries(equipmentProtocols).map(([emergencyType, equipment]) => (
            <View key={emergencyType} style={styles.protocolSection}>
              <Text style={styles.protocolTitle}>{emergencyType}</Text>
              {Object.entries(equipment).map(([item, required]) => (
                <List.Item
                  key={item}
                  title={item}
                  left={(props) => (
                    <MaterialIcons 
                      {...props} 
                      name="medical-services" 
                      size={20} 
                      color="#6b7280" 
                    />
                  )}
                  right={() => (
                    <Switch
                      value={required}
                      onValueChange={() => toggleEquipmentProtocol(emergencyType, item)}
                      trackColor={{ false: '#d1d5db', true: '#10b981' }}
                      thumbColor={required ? '#fff' : '#fff'}
                    />
                  )}
                  style={styles.equipmentItem}
                />
              ))}
            </View>
          ))}
        </Card.Content>
      </Card>

      {/* System Information */}
      <Card style={styles.settingsCard}>
        <Card.Content>
          <Title>System Information</Title>
          <Divider style={styles.divider} />
          
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>App Version</Text>
            <Text style={styles.infoValue}>1.0.0</Text>
          </View>
          
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>Build Date</Text>
            <Text style={styles.infoValue}>January 2024</Text>
          </View>
          
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>Device ID</Text>
            <Text style={styles.infoValue}>ER-SYSTEM-001</Text>
          </View>
          
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>Last Updated</Text>
            <Text style={styles.infoValue}>2024-01-15</Text>
          </View>
        </Card.Content>
      </Card>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity style={styles.actionButton} onPress={exportSettings}>
          <MaterialIcons name="file-download" size={20} color="#1e3a8a" />
          <Text style={styles.actionButtonText}>Export Settings</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.actionButton, styles.resetButton]} 
          onPress={resetSettings}
        >
          <MaterialIcons name="refresh" size={20} color="#ef4444" />
          <Text style={[styles.actionButtonText, styles.resetButtonText]}>Reset to Default</Text>
        </TouchableOpacity>
      </View>

      {/* Timeout Configuration */}
      <Card style={styles.settingsCard}>
        <Card.Content>
          <Title>Emergency Timeout Configuration</Title>
          <Paragraph style={styles.sectionDescription}>
            Set the time limit for equipment verification during emergencies
          </Paragraph>
          
          <View style={styles.timeoutButtons}>
            {[15, 30, 45, 60].map((timeout) => (
              <TouchableOpacity
                key={timeout}
                style={[
                  styles.timeoutButton,
                  settings.emergencyTimeout === timeout && styles.timeoutButtonActive
                ]}
                onPress={() => updateEmergencyTimeout(timeout)}
              >
                <Text style={[
                  styles.timeoutButtonText,
                  settings.emergencyTimeout === timeout && styles.timeoutButtonTextActive
                ]}>
                  {timeout}s
                </Text>
              </TouchableOpacity>
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
  settingsCard: {
    margin: 16,
    elevation: 4,
  },
  divider: {
    marginVertical: 8,
  },
  settingItem: {
    paddingVertical: 8,
  },
  settingValue: {
    fontSize: 16,
    color: '#1e3a8a',
    fontWeight: '600',
  },
  sectionDescription: {
    color: '#6b7280',
    marginBottom: 16,
  },
  protocolSection: {
    marginBottom: 20,
  },
  protocolTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
    marginTop: 8,
  },
  equipmentItem: {
    paddingVertical: 4,
  },
  infoItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  infoLabel: {
    fontSize: 14,
    color: '#6b7280',
  },
  infoValue: {
    fontSize: 14,
    color: '#374151',
    fontWeight: '500',
  },
  actionButtons: {
    margin: 16,
    gap: 12,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    elevation: 2,
  },
  actionButtonText: {
    marginLeft: 8,
    fontSize: 16,
    fontWeight: '600',
    color: '#1e3a8a',
  },
  resetButton: {
    borderWidth: 1,
    borderColor: '#ef4444',
  },
  resetButtonText: {
    color: '#ef4444',
  },
  timeoutButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  timeoutButton: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#d1d5db',
    backgroundColor: '#fff',
  },
  timeoutButtonActive: {
    backgroundColor: '#1e3a8a',
    borderColor: '#1e3a8a',
  },
  timeoutButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#6b7280',
  },
  timeoutButtonTextActive: {
    color: '#fff',
  },
});

export default SettingsScreen; 