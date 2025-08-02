#!/bin/bash

echo "🚀 Starting Medical Crash Cart Validator Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if YOLO model exists
if [ ! -f "../yolov8n.pt" ]; then
    echo "Downloading YOLO model..."
    cd ..
    python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
    cd backend
fi

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation available at http://localhost:8000/docs"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
