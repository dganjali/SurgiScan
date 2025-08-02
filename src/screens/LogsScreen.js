import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Card, Title, Paragraph, Button, Chip, DataTable } from 'react-native-paper';
import { MaterialIcons } from '@expo/vector-icons';
import * as SQLite from 'expo-sqlite';

const LogsScreen = ({ navigation }) => {
  const [logs, setLogs] = useState([]);
  const [selectedLog, setSelectedLog] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  // Sample data for demonstration
  const sampleLogs = [
    {
      id: 1,
      timestamp: new Date('2024-01-15T14:30:00'),
      eventType: 'Code Blue',
      location: 'ER Room A',
      duration: 180,
      success: true,
      missingEquipment: [],
      equipmentDetected: ['AED', 'Crash Cart', 'Airway Bag', 'Oxygen Tank', 'Epinephrine'],
      notes: 'All equipment verified within time limit',
    },
    {
      id: 2,
      timestamp: new Date('2024-01-14T09:15:00'),
      eventType: 'Code Blue',
      location: 'Ambulance 3',
      duration: 300,
      success: false,
      missingEquipment: ['Epinephrine'],
      equipmentDetected: ['AED', 'Crash Cart', 'Airway Bag', 'Oxygen Tank'],
      notes: 'Epinephrine not detected within time limit',
    },
    {
      id: 3,
      timestamp: new Date('2024-01-13T16:45:00'),
      eventType: 'Code Blue',
      location: 'ER Room B',
      duration: 240,
      success: true,
      missingEquipment: [],
      equipmentDetected: ['AED', 'Crash Cart', 'Airway Bag', 'Oxygen Tank', 'Epinephrine'],
      notes: 'Equipment verification successful',
    },
  ];

  useEffect(() => {
    setLogs(sampleLogs);
  }, []);

  const getSuccessColor = (success) => {
    return success ? '#10b981' : '#ef4444';
  };

  const getSuccessIcon = (success) => {
    return success ? 'check-circle' : 'error';
  };

  const formatDuration = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const viewLogDetails = (log) => {
    setSelectedLog(log);
    setShowDetails(true);
  };

  const exportLogs = () => {
    Alert.alert(
      'Export Logs',
      'Export functionality will be implemented for CSV/PDF export',
      [{ text: 'OK' }]
    );
  };

  const getAnalytics = () => {
    const totalEvents = logs.length;
    const successfulEvents = logs.filter(log => log.success).length;
    const successRate = totalEvents > 0 ? (successfulEvents / totalEvents * 100).toFixed(1) : 0;
    const avgDuration = logs.length > 0 
      ? (logs.reduce((sum, log) => sum + log.duration, 0) / logs.length).toFixed(0)
      : 0;

    return {
      totalEvents,
      successfulEvents,
      successRate,
      avgDuration,
    };
  };

  const analytics = getAnalytics();

  return (
    <ScrollView style={styles.container}>
      {/* Analytics Summary */}
      <Card style={styles.analyticsCard}>
        <Card.Content>
          <Title>Event Analytics</Title>
          <View style={styles.analyticsGrid}>
            <View style={styles.analyticsItem}>
              <Text style={styles.analyticsNumber}>{analytics.totalEvents}</Text>
              <Text style={styles.analyticsLabel}>Total Events</Text>
            </View>
            <View style={styles.analyticsItem}>
              <Text style={styles.analyticsNumber}>{analytics.successRate}%</Text>
              <Text style={styles.analyticsLabel}>Success Rate</Text>
            </View>
            <View style={styles.analyticsItem}>
              <Text style={styles.analyticsNumber}>{analytics.avgDuration}s</Text>
              <Text style={styles.analyticsLabel}>Avg Duration</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Export Button */}
      <View style={styles.exportContainer}>
        <TouchableOpacity style={styles.exportButton} onPress={exportLogs}>
          <MaterialIcons name="file-download" size={20} color="#1e3a8a" />
          <Text style={styles.exportButtonText}>Export Logs</Text>
        </TouchableOpacity>
      </View>

      {/* Logs List */}
      <Card style={styles.logsCard}>
        <Card.Content>
          <Title>Emergency Event Logs</Title>
          {logs.map((log, index) => (
            <TouchableOpacity
              key={log.id}
              style={styles.logItem}
              onPress={() => viewLogDetails(log)}
            >
              <View style={styles.logHeader}>
                <View style={styles.logInfo}>
                  <Text style={styles.logTimestamp}>
                    {log.timestamp.toLocaleDateString()} {log.timestamp.toLocaleTimeString()}
                  </Text>
                  <Text style={styles.logLocation}>{log.location}</Text>
                </View>
                <View style={styles.logStatus}>
                  <MaterialIcons
                    name={getSuccessIcon(log.success)}
                    size={24}
                    color={getSuccessColor(log.success)}
                  />
                  <Chip
                    mode="outlined"
                    textStyle={{ color: getSuccessColor(log.success) }}
                    style={{ borderColor: getSuccessColor(log.success) }}
                  >
                    {log.success ? 'Success' : 'Failed'}
                  </Chip>
                </View>
              </View>
              
              <View style={styles.logDetails}>
                <Text style={styles.logDuration}>
                  Duration: {formatDuration(log.duration)}
                </Text>
                {log.missingEquipment.length > 0 && (
                  <Text style={styles.missingEquipment}>
                    Missing: {log.missingEquipment.join(', ')}
                  </Text>
                )}
              </View>
            </TouchableOpacity>
          ))}
        </Card.Content>
      </Card>

      {/* Log Details Modal */}
      {showDetails && selectedLog && (
        <View style={styles.modalOverlay}>
          <Card style={styles.modalCard}>
            <Card.Content>
              <View style={styles.modalHeader}>
                <Title>Event Details</Title>
                <TouchableOpacity onPress={() => setShowDetails(false)}>
                  <MaterialIcons name="close" size={24} color="#6b7280" />
                </TouchableOpacity>
              </View>

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Event Type:</Text>
                <Text style={styles.detailValue}>{selectedLog.eventType}</Text>
              </View>

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Location:</Text>
                <Text style={styles.detailValue}>{selectedLog.location}</Text>
              </View>

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Timestamp:</Text>
                <Text style={styles.detailValue}>
                  {selectedLog.timestamp.toLocaleString()}
                </Text>
              </View>

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Duration:</Text>
                <Text style={styles.detailValue}>
                  {formatDuration(selectedLog.duration)}
                </Text>
              </View>

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Status:</Text>
                <Chip
                  mode="outlined"
                  textStyle={{ color: getSuccessColor(selectedLog.success) }}
                  style={{ borderColor: getSuccessColor(selectedLog.success) }}
                >
                  {selectedLog.success ? 'Success' : 'Failed'}
                </Chip>
              </View>

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Equipment Detected:</Text>
                <View style={styles.equipmentChips}>
                  {selectedLog.equipmentDetected.map((equipment, index) => (
                    <Chip key={index} style={styles.equipmentChip}>
                      {equipment}
                    </Chip>
                  ))}
                </View>
              </View>

              {selectedLog.missingEquipment.length > 0 && (
                <View style={styles.detailItem}>
                  <Text style={styles.detailLabel}>Missing Equipment:</Text>
                  <View style={styles.equipmentChips}>
                    {selectedLog.missingEquipment.map((equipment, index) => (
                      <Chip 
                        key={index} 
                        style={[styles.equipmentChip, styles.missingChip]}
                        textStyle={{ color: '#ef4444' }}
                      >
                        {equipment}
                      </Chip>
                    ))}
                  </View>
                </View>
              )}

              <View style={styles.detailItem}>
                <Text style={styles.detailLabel}>Notes:</Text>
                <Text style={styles.detailValue}>{selectedLog.notes}</Text>
              </View>
            </Card.Content>
          </Card>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  analyticsCard: {
    margin: 16,
    elevation: 4,
  },
  analyticsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  analyticsItem: {
    alignItems: 'center',
  },
  analyticsNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1e3a8a',
  },
  analyticsLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
  },
  exportContainer: {
    margin: 16,
  },
  exportButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    padding: 12,
    borderRadius: 8,
    elevation: 2,
  },
  exportButtonText: {
    marginLeft: 8,
    fontSize: 16,
    fontWeight: '600',
    color: '#1e3a8a',
  },
  logsCard: {
    margin: 16,
    elevation: 4,
  },
  logItem: {
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
    paddingVertical: 16,
  },
  logHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  logInfo: {
    flex: 1,
  },
  logTimestamp: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
  },
  logLocation: {
    fontSize: 14,
    color: '#6b7280',
    marginTop: 2,
  },
  logStatus: {
    alignItems: 'center',
  },
  logDetails: {
    marginTop: 8,
  },
  logDuration: {
    fontSize: 14,
    color: '#6b7280',
  },
  missingEquipment: {
    fontSize: 14,
    color: '#ef4444',
    marginTop: 4,
  },
  modalOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  modalCard: {
    margin: 20,
    maxHeight: '80%',
    width: '90%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  detailItem: {
    marginBottom: 16,
  },
  detailLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 4,
  },
  detailValue: {
    fontSize: 16,
    color: '#6b7280',
  },
  equipmentChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 8,
  },
  equipmentChip: {
    margin: 2,
    backgroundColor: '#e0f2fe',
  },
  missingChip: {
    backgroundColor: '#fee2e2',
  },
});

export default LogsScreen; 