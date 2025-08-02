from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from datetime import datetime
import json
import os

# Import torch and add safe globals for YOLO
import torch
from torch.serialization import add_safe_globals

# Add safe globals for YOLO model loading
try:
    from ultralytics import YOLO
    from ultralytics.nn.tasks import DetectionModel
    add_safe_globals([DetectionModel])
except ImportError:
    print("Warning: ultralytics not available, using simulation mode")
    YOLO = None

app = Flask(__name__)
CORS(app)

# Initialize YOLO model with error handling
model = None
try:
    if YOLO:
        print("Loading YOLO model...")
        model = YOLO("yolov8n.pt")
        print("Model loaded!")
    else:
        print("Running in simulation mode (no YOLO model)")
except Exception as e:
    print(f"Warning: Could not load YOLO model: {e}")
    print("Running in simulation mode")
    model = None

# Simulated data for development
PROCEDURES = {
    "Laparoscopic Cholecystectomy": {
        "expected_instruments": 24,
        "required_tools": [
            {"name": "Kelly Hemostat", "count": 5, "category": "hemostats"},
            {"name": "Mosquito Hemostat", "count": 1, "category": "hemostats"},
            {"name": "#10 Blade", "count": 1, "category": "scalpels"},
            {"name": "#15 Blade", "count": 1, "category": "scalpels"},
            {"name": "Army-Navy Retractor", "count": 1, "category": "retractors"},
            {"name": "Weitlaner Retractor", "count": 1, "category": "retractors"}
        ]
    },
    "Appendectomy": {
        "expected_instruments": 18,
        "required_tools": [
            {"name": "Kelly Hemostat", "count": 3, "category": "hemostats"},
            {"name": "Mosquito Hemostat", "count": 2, "category": "hemostats"},
            {"name": "#10 Blade", "count": 1, "category": "scalpels"}
        ]
    }
}

@app.route('/api/procedures', methods=['GET'])
def get_procedures():
    """Get list of available procedures"""
    return jsonify(list(PROCEDURES.keys()))

@app.route('/api/procedure/<procedure_name>', methods=['GET'])
def get_procedure_details(procedure_name):
    """Get details for a specific procedure"""
    if procedure_name in PROCEDURES:
        return jsonify(PROCEDURES[procedure_name])
    return jsonify({"error": "Procedure not found"}), 404

@app.route('/api/detect', methods=['POST'])
def detect_instruments():
    """Detect instruments in uploaded image or video frame"""
    try:
        # For now, return simulated detection results
        # In production, this would process actual image/video data
        
        detected_instruments = [
            {
                "id": 1,
                "name": "Kelly Hemostat",
                "count": 4,
                "status": "found",
                "required": 5,
                "confidence": 0.95,
                "bbox": [100, 150, 180, 210]
            },
            {
                "id": 2,
                "name": "Mosquito Hemostat",
                "count": 1,
                "status": "found",
                "required": 1,
                "confidence": 0.92,
                "bbox": [300, 200, 370, 250]
            },
            {
                "id": 3,
                "name": "#10 Blade",
                "count": 1,
                "status": "found",
                "required": 1,
                "confidence": 0.88,
                "bbox": [500, 100, 560, 140]
            },
            {
                "id": 4,
                "name": "Syringe",
                "count": 1,
                "status": "extra",
                "required": 0,
                "confidence": 0.85,
                "bbox": [200, 400, 290, 430]
            }
        ]
        
        issues = [
            {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "type": "missing",
                "message": "Kelly Hemostat (1)"
            },
            {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "type": "extra",
                "message": "Syringe (not listed)"
            }
        ]
        
        return jsonify({
            "detected_instruments": detected_instruments,
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
            "model_status": "simulation" if model is None else "loaded"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/checklist', methods=['GET'])
def get_checklist():
    """Get current checklist status"""
    checklist = {
        "found": [
            {"name": "Kelly Hemostat", "count": 4, "required": 5, "status": "partial"},
            {"name": "Mosquito Hemostat", "count": 1, "required": 1, "status": "found"},
            {"name": "#10 Blade", "count": 1, "required": 1, "status": "found"},
            {"name": "#15 Blade", "count": 1, "required": 1, "status": "found"}
        ],
        "missing": [
            {"name": "Army-Navy Retractor", "count": 0, "required": 1, "status": "missing"}
        ],
        "optional": [],
        "confirmed": False
    }
    
    return jsonify(checklist)

@app.route('/api/checklist/confirm', methods=['POST'])
def confirm_checklist():
    """Confirm the current checklist"""
    try:
        data = request.get_json()
        # In production, this would validate the checklist and update database
        return jsonify({"status": "confirmed", "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rescan', methods=['POST'])
def rescan():
    """Trigger a new scan"""
    try:
        # In production, this would trigger a new detection cycle
        return jsonify({"status": "rescan_initiated", "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify({
        "status": "operational",
        "model_loaded": model is not None,
        "camera_connected": True,
        "last_update": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Surgical Instrument Tracking Backend...")
    print(f"📊 Model Status: {'Loaded' if model else 'Simulation Mode'}")
    print("🔧 API available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 