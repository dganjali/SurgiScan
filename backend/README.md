# Medical Crash Cart Validator - Backend API

## Overview
FastAPI backend that integrates:
- **YOLO segmentation** for object detection from crash cart images
- **CLIP classification** for medical tool identification  
- **MCP scraping** for procedure-specific tool requirements
- **Cross-referencing** detected vs required tools for validation

## API Endpoints

### 1. Start Procedure Session
```bash
POST /input-procedure
Content-Type: application/x-www-form-urlencoded

procedure=code+blue
```

### 2. Upload and Process Images
```bash
POST /upload-images
Content-Type: multipart/form-data

session_id=<session_id>
files=<image_files>
```

### 3. Validate Inventory
```bash
POST /validate-inventory
Content-Type: application/x-www-form-urlencoded

session_id=<session_id>
```

### 4. Real-time Validation
```bash
POST /realtime-validate
Content-Type: multipart/form-data

session_id=<session_id>
image=<single_image>
```

### 5. Get Session Data
```bash
GET /session/{session_id}
```

### 6. Get Logs
```bash
GET /logs
```

## Installation and Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download YOLO model** (if not present):
   ```bash
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```

3. **Start the server:**
   ```bash
   ./start.sh
   # OR
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API documentation:**
   - http://localhost:8000/docs (Swagger UI)
   - http://localhost:8000/redoc (ReDoc)

## Workflow

1. **Input Procedure:** POST `/input-procedure` with emergency type
2. **Upload Images:** POST `/upload-images` with crash cart photos
3. **Validate:** POST `/validate-inventory` to cross-reference tools
4. **Get Results:** Validation report with missing/extra tools

## Integration Notes

- **CLIP Model:** Uses open_clip_torch with optional fine-tuned weights
- **YOLO Segmentation:** Crops detected objects for classification
- **MCP Agent:** Scrapes medical protocols for tool requirements
- **Session Management:** Tracks validation sessions with UUIDs
- **CORS Enabled:** Ready for frontend integration

## Example Response

```json
{
  "detected": {"scalpel": 1, "syringe": 2},
  "required": ["scalpel", "syringe", "retractor"],
  "matched": {"scalpel": 1, "syringe": 2},
  "missing": ["retractor"],
  "extra": {},
  "completion_percentage": 66.7,
  "issues": [
    {
      "type": "missing",
      "severity": "high", 
      "message": "Missing required tools: retractor",
      "tools": ["retractor"]
    }
  ]
}
```
