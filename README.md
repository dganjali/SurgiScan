# Critical Object Confirmation System (Code Blue)

A real-time emergency equipment verification system for Code Blue events in ER and ambulance settings, built with React Native for cross-platform deployment.

## Features

- **Emergency Event Detection**: Manual trigger or sensor-based Code Blue activation
- **Protocol Mapping**: Automatic mapping of required equipment for Code Blue events
- **Real-Time Video Integration**: Live feed processing from ER/ambulance cameras
- **Object Detection**: YOLOv8-based detection of critical medical equipment (OpenMV ready)
- **Time-Based Alerts**: 30-second countdown with missing equipment alerts
- **Post-Event Logging**: Comprehensive logging for compliance and improvement
- **Cross-Platform**: Works on iOS, Android, and Web

## Required Equipment for Code Blue

- AED (Automated External Defibrillator)
- Crash Cart
- Airway Bag
- Oxygen Tank
- Epinephrine Auto-injector

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Expo CLI (`npm install -g @expo/cli`)

### Installation
```bash
# Install dependencies
npm install

# Start the development server
npm start

# Run on web
npm run web

# Run on iOS (requires Xcode)
npm run ios

# Run on Android (requires Android Studio)
npm run android
```

## Project Structure

```
src/
├── screens/           # Main application screens
│   ├── DashboardScreen.js
│   ├── EmergencyScreen.js
│   ├── LogsScreen.js
│   └── SettingsScreen.js
├── services/          # Business logic services
│   ├── objectDetectionService.js
│   └── loggingService.js
└── utils/            # Utility functions
    └── emergencyProtocols.js
```

## Architecture

- **Frontend**: React Native with Expo for cross-platform development
- **UI Framework**: React Native Paper for Material Design components
- **Navigation**: React Navigation for screen management
- **Computer Vision**: OpenMV integration ready for object detection
- **Database**: SQLite for local data storage
- **Audio**: Expo AV for alert sounds
- **Camera**: Expo Camera for video feed integration

## OpenMV Integration

The system is designed to integrate with OpenMV for real-time object detection:

1. **Object Detection Service**: Handles communication with OpenMV device
2. **Detection Keywords**: Configurable keywords for equipment recognition
3. **Confidence Scoring**: Adjustable confidence thresholds
4. **Real-time Processing**: Continuous monitoring during emergencies

## Emergency Protocols

The system supports multiple emergency types:
- **Code Blue**: Cardiac arrest (primary focus)
- **Code Red**: Fire emergency
- **Code Pink**: Infant/Child abduction

Each protocol has configurable equipment requirements and timeouts.

## Development

### Adding New Emergency Types
1. Update `src/utils/emergencyProtocols.js`
2. Add equipment definitions with detection keywords
3. Configure timeout and location settings

### Customizing Object Detection
1. Modify `src/services/objectDetectionService.js`
2. Implement OpenMV WebSocket connection
3. Configure detection parameters

### Database Schema
The system uses SQLite with three main tables:
- `emergency_events`: Logs of emergency events
- `equipment_detections`: Individual equipment detections
- `system_logs`: System-level logging

## Deployment

### Web Deployment
```bash
npm run web
# Deploy to hosting service (Netlify, Vercel, etc.)
```

### Mobile Deployment
```bash
# Build for production
expo build:android
expo build:ios

# Or use EAS Build
eas build --platform all
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
