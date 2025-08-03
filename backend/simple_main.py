from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
import os
import uuid
from datetime import datetime
import json
import random

app = FastAPI(title="Simple Medical Dashboard API", version="1.0.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving the video
app.mount("/static", StaticFiles(directory=".."), name="static")

# Storage for session data (simplified)
sessions = {}

# --- Endpoint 1: Input procedure (simplified) ---
@app.post("/input-procedure")
def input_procedure(procedure: str = Form(...)):
    """Get required tools checklist for a medical procedure (simplified)"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Simulated required tools based on procedure
        procedure_tools = {
            "Code Blue": ["defibrillator", "epinephrine", "ambu_bag", "iv_catheter", "cardiac_monitor"],
            "Cardiac Arrest": ["defibrillator", "epinephrine", "amiodarone", "atropine", "oxygen_mask"],
            "Intubation": ["laryngoscope", "endotracheal_tube", "ambu_bag", "suction_catheter", "oxygen"],
            "Trauma Response": ["scalpel", "forceps", "gauze", "iv_bag", "blood_pressure_cuff"],
            "Respiratory Distress": ["oxygen_mask", "nebulizer", "stethoscope", "pulse_oximeter", "ambu_bag"]
        }
        
        required_tools = procedure_tools.get(procedure, ["stethoscope", "syringe", "gauze", "gloves"])
        
        # Store session data
        sessions[session_id] = {
            "procedure": procedure,
            "required_tools": required_tools,
            "timestamp": datetime.now().isoformat(),
            "detected_tools": {},
            "validation_complete": False
        }
        
        return {
            "session_id": session_id,
            "procedure": procedure, 
            "required_tools": required_tools,
            "total_required": len(required_tools)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 2: Get crops analysis (simplified) ---
@app.get("/crops-analysis")
def get_crops_analysis():
    """Get analysis of unique crops from detr_output_smoothed folder (simplified)"""
    try:
        crops_dir = "../detr_output_smoothed/crops"
        if not os.path.exists(crops_dir):
            # Return simulated data if crops don't exist
            return {
                "total_objects": 0,
                "unique_tools": 0,
                "most_common": None,
                "confidence_avg": 0,
                "tool_types": []
            }
        
        # Get all crop files
        crop_files = [f for f in os.listdir(crops_dir) if f.endswith('.jpg')]
        
        # Simulate tool classification
        simulated_tools = [
            'syringe', 'scalpel', 'stethoscope', 'defibrillator_pad', 
            'oxygen_mask', 'iv_bag', 'endotracheal_tube', 'gauze',
            'forceps', 'clamp', 'catheter', 'bandage'
        ]
        
        # Randomly assign tools to simulate classification
        random.seed(42)  # For consistent results
        detected_tools = random.sample(simulated_tools, min(8, len(simulated_tools)))
        
        return {
            "total_objects": len(crop_files),
            "unique_tools": len(detected_tools),
            "most_common": detected_tools[0] if detected_tools else None,
            "confidence_avg": 0.85,
            "tool_types": detected_tools
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 3: Logs (simplified) ---
@app.get("/logs")
def get_logs():
    """Get system logs and validation history (simplified)"""
    # Return some sample logs
    sample_logs = [
        {
            "session_id": "abc123",
            "timestamp": datetime.now().isoformat(),
            "procedure": "Code Blue",
            "completion_percentage": 85,
            "issues_count": 1,
            "missing_tools": ["epinephrine"],
            "extra_tools": []
        },
        {
            "session_id": "def456",
            "timestamp": (datetime.now()).isoformat(),
            "procedure": "Intubation",
            "completion_percentage": 95,
            "issues_count": 0,
            "missing_tools": [],
            "extra_tools": ["extra_gauze"]
        }
    ]
    
    return {"logs": sample_logs}

# --- Endpoint 4: Get session data ---
@app.get("/session/{session_id}")
def get_session(session_id: str):
    """Get complete session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

# --- Endpoint 5: Realtime validate (simplified) ---
@app.post("/realtime-validate")
def realtime_validate(session_id: str = Form(...), image: Optional[UploadFile] = File(None)):
    """Process single image for real-time validation (simplified)"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Simulate detection results
        simulated_detected_tools = {
            "syringe": 2,
            "stethoscope": 1,
            "gauze": 3
        }
        
        required_tools = sessions[session_id]["required_tools"]
        missing = [tool for tool in required_tools if tool.lower() not in [d.lower() for d in simulated_detected_tools.keys()]]
        
        return {
            "detected_tools": simulated_detected_tools,
            "missing_tools": missing,
            "objects_found": 6,
            "bounding_boxes": [],
            "annotated_image_url": "",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 6: Tool reference (for tool images) ---
@app.get("/tool-reference")
def get_tool_reference():
    """Get reference tool images and names"""
    try:
        # Check if tool_images directory exists
        tool_images_dir = "../CLIP/tool_images"
        if not os.path.exists(tool_images_dir):
            # Return simulated tool reference data
            return {
                "tools": [
                    {"name": "Syringe", "image": "/static/tool_images/syringe.jpg"},
                    {"name": "Scalpel", "image": "/static/tool_images/scalpel.jpg"},
                    {"name": "Stethoscope", "image": "/static/tool_images/stethoscope.jpg"},
                    {"name": "Defibrillator Pad", "image": "/static/tool_images/defibrillator.jpg"},
                    {"name": "Oxygen Mask", "image": "/static/tool_images/oxygen_mask.jpg"},
                    {"name": "IV Bag", "image": "/static/tool_images/iv_bag.jpg"},
                    {"name": "Endotracheal Tube", "image": "/static/tool_images/endotracheal.jpg"},
                    {"name": "Gauze", "image": "/static/tool_images/gauze.jpg"}
                ]
            }
        
        # Get actual tool images
        tool_files = [f for f in os.listdir(tool_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        tools = []
        for filename in tool_files:
            name = filename.rsplit('.', 1)[0].replace('_', ' ').title()
            tools.append({
                "name": name,
                "image": f"/static/CLIP/tool_images/{filename}"
            })
        
        return {"tools": tools}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Health check ---
@app.get("/")
def root():
    """API health check and status"""
    return {
        "status": "Simple Medical Dashboard API is running",
        "version": "1.0.0",
        "endpoints": [
            "POST /input-procedure - Start new procedure validation session",
            "GET /crops-analysis - Get crops analysis data",
            "POST /realtime-validate - Simulate real-time validation",
            "GET /session/{session_id} - Get session data",
            "GET /logs - Get validation history logs"
        ],
        "note": "This is a simplified version without heavy ML dependencies"
    }

# --- Serve the video file ---
@app.get("/video")
def get_video():
    """Serve the output.mp4 video file"""
    video_path = os.path.join(os.path.dirname(__file__), "../output.mp4")  # Adjusted file path to be relative to the script
    print(f"Attempting to serve video from: {video_path}")  # Log the file path
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4", filename="output.mp4")
    else:
        print("Video file not found at the specified path.")  # Log error
        raise HTTPException(status_code=404, detail="Video file not found")

# --- Run the application ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
