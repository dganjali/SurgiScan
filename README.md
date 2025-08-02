# Surgical Instrument Tracking Dashboard

A modern, real-time surgical instrument tracking system with a React frontend and Python Flask backend. Designed for operating room environments with a focus on sterility, accessibility, and quick visual feedback.

## 🏗️ Architecture

### Frontend (React)
- **Left Panel (10%)**: Procedure overview and session information
- **Center Panel (60%)**: Real-time visual feedback with live video feed
- **Right Panel (30%)**: Smart checklist and validation system

### Backend (Python Flask)
- RESTful API for instrument detection
- YOLO-based object detection
- Real-time data processing
- Checklist management

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- npm or yarn

### Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Access the application:**
   Open [http://localhost:3000](http://localhost:3000) in your browser

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask server:**
   ```bash
   python app.py
   ```

5. **API will be available at:**
   [http://localhost:5000](http://localhost:5000)

## 🎯 Features

### Left Panel - Procedure Overview
- **Procedure Selection**: Dropdown with common surgical procedures
- **Session Information**: Start time, patient ID (with privacy toggle)
- **Expected Instruments**: Total count of required tools
- **Privacy Mode**: Toggle to hide sensitive patient information

### Center Panel - Real-Time Visual Feedback
- **Live Video Feed**: Real-time camera input with object detection
- **Overlay System**: 
  - ✅ Green boxes for correctly identified instruments
  - ❌ Red boxes for extra/unneeded items
  - ⚠️ Yellow boxes for missing optional items
  - 🔲 Empty outlines for missing required items
- **Playback Controls**: Live/Frame-by-frame/Pause modes
- **Timeline Slider**: Navigate through recorded frames
- **Snapshot Capture**: Take still images for review

### Right Panel - Smart Checklist & Validation
- **Instrument Checklist**: 
  - Collapsible tool groups
  - Real-time status updates
  - Count tracking (found/required)
- **Issues Log**: 
  - Real-time system observations
  - Timestamped entries
  - Color-coded by issue type
- **Action Buttons**:
  - 🟢 "Confirm Setup" - Validate current configuration
  - 🔄 "Re-Scan" - Trigger new detection cycle

## 🎨 Design Principles

### Sterility & Security
- **No Popups/Modals**: Prevents contamination risks
- **No Typing Required**: Touch-friendly interface
- **Colorblind-Safe**: All feedback uses accessible color schemes
- **AORN Standards**: Tool naming follows medical standards

### Responsive Design
- **Tablet Optimized**: Primary target for OR wall-mounted screens
- **Large Fonts**: Readable from across the room
- **Clear Iconography**: Intuitive visual feedback
- **Minimal Colors**: Blues/greys/greens for professional appearance

## 🔧 API Endpoints

### Procedures
- `GET /api/procedures` - List available procedures
- `GET /api/procedure/<name>` - Get procedure details

### Detection
- `POST /api/detect` - Process image/video for instrument detection
- `GET /api/status` - Get system status

### Checklist
- `GET /api/checklist` - Get current checklist status
- `POST /api/checklist/confirm` - Confirm current setup
- `POST /api/rescan` - Trigger new detection cycle

## 🛠️ Development

### Frontend Structure
```
src/
├── components/
│   ├── LeftPanel.js      # Procedure overview
│   ├── CenterPanel.js    # Video feed and controls
│   └── RightPanel.js     # Checklist and validation
├── styles/
│   └── GlobalStyles.js   # Global styling
└── App.js               # Main application
```

### Backend Structure
```
backend/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
└── models/            # ML models (if needed)
```

## 🧪 Testing

### Frontend Testing
```bash
npm test
```

### Backend Testing
```bash
cd backend
python -m pytest
```

## 🚀 Deployment

### Frontend Build
```bash
npm run build
```

### Backend Deployment
```bash
cd backend
gunicorn app:app
```

## 📋 Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=1
MODEL_PATH=./models/yolov8n.pt
CAMERA_INDEX=0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support or questions, please open an issue in the GitHub repository.

---

**Note**: This is a development version. For production use in medical environments, additional validation, testing, and regulatory compliance measures are required.
