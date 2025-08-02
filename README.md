# 🏥 Medical Crash Cart Validator

Real-time computer vision system for validating surgical tool inventory in medical crash carts using YOLO segmentation, trained CLIP classification, and MCP protocol scraping.

## 🎯 Features

- **Real-time Webcam Feed** with live tool detection
- **YOLO Object Segmentation** for precise tool identification  
- **Trained CLIP (Contrastive Language-Image Pre-Training) Classification** on 16 surgical tool types
- **MCP Protocol Scraping** for procedure-specific requirements
- **Live Validation Dashboard** with missing/extra tool alerts
- **Session Management** for tracking validation history

## 🚀 Quick Start

### 1. Start Backend API
```bash
cd backend
./start.sh
# Backend runs on http://localhost:8000
```

### 2. Start Frontend
```bash
cd frontend
./start.sh
# Frontend runs on http://localhost:3000
```

## 📋 Usage Workflow

1. **Enter Procedure:** Type emergency procedure (e.g. "Code Blue")
2. **Start Session:** System scrapes protocol requirements  
3. **Live Detection:** Point camera at crash cart tools
4. **Real-time Validation:** See detected vs required tools
5. **Validation Report:** Get completion percentage and alerts

## 🛠️ Supported Tools

The trained CLIP model recognizes these 16 surgical tools:
- Metzenbaum scissors, Army-Navy retractor, Yankauer suction tip
- Sterile surgical towel, Scalpel with blade, Weitlaner retractor  
- Mosquito clamp, Sterile gauze pad, Raytec surgical sponge
- Mayo-Hegar needle holder, Sponge forceps, Deaver retractor
- Adson forceps, Sterile basin (metal), Bulldog clamp

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Web     │───▶│   FastAPI        │───▶│   YOLO + CLIP   │
│   Frontend      │    │   Backend        │    │   Detection     │
│   (Port 3000)   │    │   (Port 8000)    │    │   Services      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   MCP Scraping   │
                       │   Agent          │
                       └──────────────────┘
```

## 📱 Frontend Components

- **Webcam Feed:** Live camera stream with detection overlays
- **Procedure Input:** Emergency procedure selection
- **Detection Stats:** Real-time tool counts and completion percentage
- **Tool Checklist:** Required vs detected tools with status indicators
- **Controls:** Capture, validate, and reset functions

## � API Endpoints

- `POST /input-procedure` - Start new validation session
- `POST /realtime-validate` - Process single camera frame
- `POST /validate-inventory` - Full inventory cross-reference
- `GET /session/{id}` - Get session data
- `GET /logs` - Validation history

## 💻 Development

### Backend Requirements
```bash
pip install -r backend/requirements.txt
```

### Frontend Requirements  
```bash
cd frontend && npm install
```

### File Structure
```
├── backend/          # FastAPI server
│   ├── main.py      # API endpoints
│   ├── services.py  # YOLO + CLIP integration
│   └── requirements.txt
├── frontend/         # React app
│   ├── src/App.js   # Main component
│   └── package.json
├── CLIP/            # Trained model
│   ├── best_surgical_tool_clip.pth
│   └── surgical_tool_metadata.pkl
└── MCP-scraping/    # Protocol scraper
```

## 🎮 Demo

1. Run both backend and frontend
2. Navigate to http://localhost:3000  
3. Enter "Code Blue" as procedure
4. Point camera at medical tools
5. Watch real-time detection and validation!

## 🔬 Technical Details

- **YOLO:** Object detection and segmentation
- **CLIP:** Fine-tuned on surgical instruments  
- **MCP:** Medical protocol scraping agent
- **FastAPI:** RESTful backend with session management
- **React:** Real-time frontend with webcam integration

Built for TerraHacks medical AI hackathon 🏆

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
