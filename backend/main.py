from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os
import uuid
from datetime import datetime
import json

from services import SegmentationService, CLIPService, MCPService

app = FastAPI(title="Medical Crash Cart Validator API", version="1.0.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
segmentation_service = SegmentationService()
clip_service = CLIPService()
mcp_service = MCPService()

# Storage for session data
sessions = {}

# --- Endpoint 1: Input procedure/emergency ---
@app.post("/input-procedure")
def input_procedure(procedure: str = Form(...)):
    """Get required tools checklist for a medical procedure"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Get tools from MCP scraping service
        required_tools = mcp_service.get_procedure_tools(procedure)
        
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

# --- Endpoint 2: Upload and process images ---
@app.post("/upload-images")
def upload_images(session_id: str = Form(...), files: List[UploadFile] = File(...)):
    """Upload images, segment objects, and classify them with CLIP"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Create unique directory for this session
        upload_dir = f"uploaded_images/{session_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        all_detected_tools = {}
        processed_images = []
        
        for file in files:
            # Save uploaded file
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Segment objects from the image
            crop_dir = f"{upload_dir}/cropped"
            cropped_paths = segmentation_service.segment_image(file_path, crop_dir)
            
            if cropped_paths:
                # Classify each cropped object with CLIP
                classification_results = clip_service.classify_multiple_images(cropped_paths)
                
                # Aggregate tool counts
                for tool, count in classification_results['tool_counts'].items():
                    all_detected_tools[tool] = all_detected_tools.get(tool, 0) + count
                
                processed_images.append({
                    "filename": file.filename,
                    "objects_detected": len(cropped_paths),
                    "tool_counts": classification_results['tool_counts']
                })
        
        # Update session with detected tools
        sessions[session_id]["detected_tools"] = all_detected_tools
        sessions[session_id]["processed_images"] = processed_images
        
        return {
            "session_id": session_id,
            "processed_images": processed_images,
            "total_detected_tools": all_detected_tools,
            "images_processed": len(files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 3: Validate inventory ---
@app.post("/validate-inventory")
def validate_inventory(session_id: str = Form(...)):
    """Cross-reference detected tools with required tools and generate validation report"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
            
        session_data = sessions[session_id]
        required_tools = session_data["required_tools"]
        detected_tools = session_data.get("detected_tools", {})
        
        # Normalize tool names for comparison (lowercase, remove common words)
        def normalize_tool_name(name):
            return name.lower().replace("_", " ").strip()
            
        # Create normalized mappings
        required_normalized = {normalize_tool_name(tool): tool for tool in required_tools}
        detected_normalized = {}
        for tool, count in detected_tools.items():
            norm_name = normalize_tool_name(tool)
            detected_normalized[norm_name] = detected_normalized.get(norm_name, 0) + count
        
        # Find matches, missing, and extra tools
        matched_tools = {}
        missing_tools = []
        extra_tools = {}
        
        # Check required tools
        for norm_req, orig_req in required_normalized.items():
            if norm_req in detected_normalized:
                matched_tools[orig_req] = detected_normalized[norm_req]
            else:
                # Check for partial matches
                found_partial = False
                for norm_det in detected_normalized.keys():
                    if norm_req in norm_det or norm_det in norm_req:
                        matched_tools[orig_req] = detected_normalized[norm_det]
                        found_partial = True
                        break
                if not found_partial:
                    missing_tools.append(orig_req)
        
        # Check for extra tools
        for norm_det, count in detected_normalized.items():
            if norm_det not in required_normalized:
                # Check if it's a partial match we already counted
                is_partial_match = False
                for norm_req in required_normalized.keys():
                    if norm_req in norm_det or norm_det in norm_req:
                        is_partial_match = True
                        break
                if not is_partial_match:
                    extra_tools[norm_det] = count
        
        # Calculate completion percentage
        total_required = len(required_tools)
        total_matched = len(matched_tools)
        completion_percentage = (total_matched / total_required * 100) if total_required > 0 else 0
        
        # Generate issues and alerts
        issues = []
        if missing_tools:
            issues.append({
                "type": "missing",
                "severity": "high",
                "message": f"Missing required tools: {', '.join(missing_tools)}",
                "tools": missing_tools
            })
        
        if extra_tools:
            issues.append({
                "type": "extra",
                "severity": "low", 
                "message": f"Extra tools detected: {', '.join(extra_tools.keys())}",
                "tools": list(extra_tools.keys())
            })
        
        # Update session
        validation_result = {
            "detected": detected_tools,
            "required": required_tools,
            "matched": matched_tools,
            "missing": missing_tools,
            "extra": extra_tools,
            "completion_percentage": round(completion_percentage, 1),
            "issues": issues,
            "validation_timestamp": datetime.now().isoformat()
        }
        
        sessions[session_id]["validation_result"] = validation_result
        sessions[session_id]["validation_complete"] = True
        
        return JSONResponse(validation_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 4: Get session data ---
@app.get("/session/{session_id}")
def get_session(session_id: str):
    """Get complete session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

# --- Endpoint 5: Logs for dashboard ---
@app.get("/logs")
def get_logs():
    """Get system logs and validation history"""
    logs = []
    for session_id, session_data in sessions.items():
        if session_data.get("validation_complete"):
            validation = session_data.get("validation_result", {})
            log_entry = {
                "session_id": session_id,
                "timestamp": session_data.get("timestamp"),
                "procedure": session_data.get("procedure"),
                "completion_percentage": validation.get("completion_percentage", 0),
                "issues_count": len(validation.get("issues", [])),
                "missing_tools": validation.get("missing", []),
                "extra_tools": list(validation.get("extra", {}).keys())
            }
            logs.append(log_entry)
    
    # Sort by timestamp (most recent first)
    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return {"logs": logs[:50]}  # Return last 50 entries

# --- Endpoint 6: Real-time validation (for live camera feed) ---
@app.post("/realtime-validate")
def realtime_validate(session_id: str = Form(...), image: UploadFile = File(...)):
    """Process single image for real-time validation"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Save temporary image
        temp_dir = f"temp_images/{session_id}"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"frame_{datetime.now().timestamp()}.jpg")
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # Quick segmentation and classification
        crop_dir = f"{temp_dir}/cropped"
        cropped_paths = segmentation_service.segment_image(temp_path, crop_dir)
        
        if cropped_paths:
            results = clip_service.classify_multiple_images(cropped_paths)
            detected_tools = results['tool_counts']
        else:
            detected_tools = {}
        
        # Quick validation against required tools
        required_tools = sessions[session_id]["required_tools"]
        missing = [tool for tool in required_tools if tool.lower() not in [d.lower() for d in detected_tools.keys()]]
        
        # Clean up temp files
        os.remove(temp_path)
        for crop_path in cropped_paths:
            if os.path.exists(crop_path):
                os.remove(crop_path)
        
        return {
            "detected_tools": detected_tools,
            "missing_tools": missing,
            "objects_found": len(cropped_paths),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Health check ---
@app.get("/")
def root():
    """API health check and status"""
    return {
        "status": "Medical Crash Cart Validator API is running",
        "version": "1.0.0",
        "endpoints": [
            "POST /input-procedure - Start new procedure validation session",
            "POST /upload-images - Upload and process crash cart images",
            "POST /validate-inventory - Cross-reference detected vs required tools",
            "POST /realtime-validate - Real-time single image validation",
            "GET /session/{session_id} - Get session data",
            "GET /logs - Get validation history logs"
        ],
        "services": {
            "segmentation": "YOLO object detection",
            "classification": "CLIP medical tool recognition",
            "scraping": "MCP protocol scraping for tool requirements"
        }
    }

# --- Run the application ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
