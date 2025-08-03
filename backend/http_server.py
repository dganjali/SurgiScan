#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
import os
from datetime import datetime
import uuid
import random

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_json_response({
                "status": "Simple Medical Dashboard API is running",
                "version": "1.0.0",
                "note": "Basic HTTP server without FastAPI dependencies"
            })
        elif self.path == '/video':
            self.serve_video()
        elif self.path == '/crops-analysis':
            self.serve_crops_analysis()
        elif self.path == '/logs':
            self.serve_logs()
        elif self.path == '/tool-reference':
            self.serve_tool_reference()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/input-procedure':
            self.handle_input_procedure()
        elif self.path == '/realtime-validate':
            self.handle_realtime_validate()
        else:
            self.send_error(404, "Not Found")

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def serve_video(self):
        video_path = '../output.mp4'
        if os.path.exists(video_path):
            self.send_response(200)
            self.send_header('Content-type', 'video/mp4')
            self.send_header('Content-Length', str(os.path.getsize(video_path)))
            self.end_headers()
            with open(video_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "Video file not found")

    def serve_crops_analysis(self):
        crops_dir = "../detr_output_smoothed/crops"
        if os.path.exists(crops_dir):
            crop_files = [f for f in os.listdir(crops_dir) if f.endswith('.jpg')]
            total_objects = len(crop_files)
        else:
            total_objects = 0

        simulated_tools = [
            'syringe', 'scalpel', 'stethoscope', 'defibrillator_pad', 
            'oxygen_mask', 'iv_bag', 'endotracheal_tube', 'gauze',
            'forceps', 'clamp', 'catheter', 'bandage'
        ]
        
        random.seed(42)
        detected_tools = random.sample(simulated_tools, min(8, len(simulated_tools)))
        
        data = {
            "total_objects": total_objects,
            "unique_tools": len(detected_tools),
            "most_common": detected_tools[0] if detected_tools else None,
            "confidence_avg": 0.85,
            "tool_types": detected_tools
        }
        self.send_json_response(data)

    def serve_logs(self):
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
                "timestamp": datetime.now().isoformat(),
                "procedure": "Intubation",
                "completion_percentage": 95,
                "issues_count": 0,
                "missing_tools": [],
                "extra_tools": ["extra_gauze"]
            }
        ]
        self.send_json_response({"logs": sample_logs})

    def serve_tool_reference(self):
        tools = [
            {"name": "Syringe", "image": "/tool_images/syringe.jpg"},
            {"name": "Scalpel", "image": "/tool_images/scalpel.jpg"},
            {"name": "Stethoscope", "image": "/tool_images/stethoscope.jpg"},
            {"name": "Defibrillator Pad", "image": "/tool_images/defibrillator.jpg"},
            {"name": "Oxygen Mask", "image": "/tool_images/oxygen_mask.jpg"},
            {"name": "IV Bag", "image": "/tool_images/iv_bag.jpg"},
            {"name": "Endotracheal Tube", "image": "/tool_images/endotracheal.jpg"},
            {"name": "Gauze", "image": "/tool_images/gauze.jpg"}
        ]
        self.send_json_response({"tools": tools})

    def handle_input_procedure(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parse form data
        parsed_data = urllib.parse.parse_qs(post_data)
        procedure = parsed_data.get('procedure', [''])[0]
        
        session_id = str(uuid.uuid4())
        
        procedure_tools = {
            "Code Blue": ["defibrillator", "epinephrine", "ambu_bag", "iv_catheter", "cardiac_monitor"],
            "Cardiac Arrest": ["defibrillator", "epinephrine", "amiodarone", "atropine", "oxygen_mask"],
            "Intubation": ["laryngoscope", "endotracheal_tube", "ambu_bag", "suction_catheter", "oxygen"],
            "Trauma Response": ["scalpel", "forceps", "gauze", "iv_bag", "blood_pressure_cuff"],
            "Respiratory Distress": ["oxygen_mask", "nebulizer", "stethoscope", "pulse_oximeter", "ambu_bag"]
        }
        
        required_tools = procedure_tools.get(procedure, ["stethoscope", "syringe", "gauze", "gloves"])
        
        response = {
            "session_id": session_id,
            "procedure": procedure,
            "required_tools": required_tools,
            "total_required": len(required_tools)
        }
        self.send_json_response(response)

    def handle_realtime_validate(self):
        # Simulate detection results
        simulated_detected_tools = {
            "syringe": 2,
            "stethoscope": 1,
            "gauze": 3
        }
        
        response = {
            "detected_tools": simulated_detected_tools,
            "missing_tools": ["defibrillator", "epinephrine"],
            "objects_found": 6,
            "bounding_boxes": [],
            "annotated_image_url": "",
            "timestamp": datetime.now().isoformat()
        }
        self.send_json_response(response)

def run_server():
    PORT = 8000
    
    # Change to the backend directory to serve files relative to it
    os.chdir('/Users/dganjali/GitHub/terrahacksJADE/backend')
    
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
