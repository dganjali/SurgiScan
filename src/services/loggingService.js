// Logging Service
// Handles emergency event logging and analytics

import * as SQLite from 'expo-sqlite';

class LoggingService {
  constructor() {
    this.db = null;
    this.initializeDatabase();
  }

  // Initialize SQLite database
  async initializeDatabase() {
    try {
      this.db = SQLite.openDatabase('emergency_logs.db');
      
      // Create tables if they don't exist
      await this.createTables();
      console.log('Logging service initialized');
    } catch (error) {
      console.error('Database initialization failed:', error);
    }
  }

  // Create database tables
  async createTables() {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        // Emergency events table
        tx.executeSql(
          `CREATE TABLE IF NOT EXISTS emergency_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            location TEXT,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            duration INTEGER,
            success BOOLEAN,
            missing_equipment TEXT,
            detected_equipment TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
          )`
        );

        // Equipment detections table
        tx.executeSql(
          `CREATE TABLE IF NOT EXISTS equipment_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            equipment_name TEXT NOT NULL,
            confidence REAL,
            detected_at DATETIME,
            detection_count INTEGER DEFAULT 1,
            FOREIGN KEY (event_id) REFERENCES emergency_events (id)
          )`
        );

        // System logs table
        tx.executeSql(
          `CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
          )`
        );
      }, reject, resolve);
    });
  }

  // Log emergency event
  async logEmergencyEvent(eventData) {
    const {
      eventType,
      location,
      startTime,
      endTime,
      duration,
      success,
      missingEquipment,
      detectedEquipment,
      notes,
    } = eventData;

    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `INSERT INTO emergency_events (
            event_type, location, start_time, end_time, duration, 
            success, missing_equipment, detected_equipment, notes
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [
            eventType,
            location,
            startTime.toISOString(),
            endTime ? endTime.toISOString() : null,
            duration,
            success ? 1 : 0,
            JSON.stringify(missingEquipment),
            JSON.stringify(detectedEquipment),
            notes,
          ],
          (_, result) => {
            const eventId = result.insertId;
            resolve(eventId);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Log equipment detection
  async logEquipmentDetection(eventId, detectionData) {
    const {
      equipmentName,
      confidence,
      detectedAt,
      detectionCount,
    } = detectionData;

    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `INSERT INTO equipment_detections (
            event_id, equipment_name, confidence, detected_at, detection_count
          ) VALUES (?, ?, ?, ?, ?)`,
          [
            eventId,
            equipmentName,
            confidence,
            detectedAt.toISOString(),
            detectionCount || 1,
          ],
          (_, result) => {
            resolve(result.insertId);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Log system message
  async logSystemMessage(level, message) {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `INSERT INTO system_logs (level, message) VALUES (?, ?)`,
          [level, message],
          (_, result) => {
            resolve(result.insertId);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Get all emergency events
  async getEmergencyEvents(limit = 50) {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `SELECT * FROM emergency_events 
           ORDER BY start_time DESC 
           LIMIT ?`,
          [limit],
          (_, { rows }) => {
            const events = rows._array.map(event => ({
              ...event,
              missingEquipment: JSON.parse(event.missing_equipment || '[]'),
              detectedEquipment: JSON.parse(event.detected_equipment || '[]'),
            }));
            resolve(events);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Get event by ID
  async getEventById(eventId) {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `SELECT * FROM emergency_events WHERE id = ?`,
          [eventId],
          (_, { rows }) => {
            if (rows.length > 0) {
              const event = rows._array[0];
              resolve({
                ...event,
                missingEquipment: JSON.parse(event.missing_equipment || '[]'),
                detectedEquipment: JSON.parse(event.detected_equipment || '[]'),
              });
            } else {
              resolve(null);
            }
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Get equipment detections for an event
  async getEquipmentDetections(eventId) {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `SELECT * FROM equipment_detections 
           WHERE event_id = ? 
           ORDER BY detected_at ASC`,
          [eventId],
          (_, { rows }) => {
            resolve(rows._array);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Get analytics data
  async getAnalytics() {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        // Get total events
        tx.executeSql(
          `SELECT COUNT(*) as total FROM emergency_events`,
          [],
          (_, { rows }) => {
            const totalEvents = rows._array[0].total;

            // Get successful events
            tx.executeSql(
              `SELECT COUNT(*) as successful FROM emergency_events WHERE success = 1`,
              [],
              (_, { rows }) => {
                const successfulEvents = rows._array[0].successful;

                // Get average duration
                tx.executeSql(
                  `SELECT AVG(duration) as avgDuration FROM emergency_events WHERE duration IS NOT NULL`,
                  [],
                  (_, { rows }) => {
                    const avgDuration = rows._array[0].avgDuration || 0;

                    // Get events by type
                    tx.executeSql(
                      `SELECT event_type, COUNT(*) as count FROM emergency_events GROUP BY event_type`,
                      [],
                      (_, { rows }) => {
                        const eventsByType = rows._array;

                        resolve({
                          totalEvents,
                          successfulEvents,
                          successRate: totalEvents > 0 ? (successfulEvents / totalEvents * 100).toFixed(1) : 0,
                          avgDuration: Math.round(avgDuration),
                          eventsByType,
                        });
                      }
                    );
                  }
                );
              }
            );
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Export logs to JSON
  async exportLogs(startDate, endDate) {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `SELECT * FROM emergency_events 
           WHERE start_time BETWEEN ? AND ?
           ORDER BY start_time DESC`,
          [startDate.toISOString(), endDate.toISOString()],
          (_, { rows }) => {
            const events = rows._array.map(event => ({
              ...event,
              missingEquipment: JSON.parse(event.missing_equipment || '[]'),
              detectedEquipment: JSON.parse(event.detected_equipment || '[]'),
            }));
            resolve(events);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Clear old logs
  async clearOldLogs(daysToKeep = 30) {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);

    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `DELETE FROM emergency_events WHERE start_time < ?`,
          [cutoffDate.toISOString()],
          (_, result) => {
            console.log(`Cleared ${result.rowsAffected} old log entries`);
            resolve(result.rowsAffected);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }

  // Get system logs
  async getSystemLogs(limit = 100) {
    return new Promise((resolve, reject) => {
      this.db.transaction(tx => {
        tx.executeSql(
          `SELECT * FROM system_logs 
           ORDER BY timestamp DESC 
           LIMIT ?`,
          [limit],
          (_, { rows }) => {
            resolve(rows._array);
          },
          (_, error) => {
            reject(error);
          }
        );
      });
    });
  }
}

// Export singleton instance
export const loggingService = new LoggingService();
export default loggingService; 