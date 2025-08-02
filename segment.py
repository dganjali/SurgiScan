#!/usr/bin/env python3
"""
YOLO object detection with manual bounding boxes (no labels)
Click on detected objects to crop them for Google Lens
"""

import cv2
import os
from datetime import datetime
from ultralytics import YOLO

print("Loading YOLO model...")
model = YOLO("yolov8n.pt")
print("Model loaded!")

# Create output directory
output_dir = "cropped_objects"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Starting detection... Press 'c' to crop all objects, 'q' to quit")

# Global variables for mouse interaction
selected_box = None
current_boxes = []
frame_count = 0

def mouse_callback(event, x, y, flags, param):
    global selected_box
    if event == cv2.EVENT_LBUTTONDOWN and current_boxes:
        # Check which box was clicked
        for i, (x1, y1, x2, y2) in enumerate(current_boxes):
            if x1 <= x <= x2 and y1 <= y <= y2:
                selected_box = i
                print(f"Selected object {i}")
                break

cv2.namedWindow('Object Detection', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Object Detection', mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Flip for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Run YOLO detection
    results = model(frame, verbose=False)
    
    # Extract bounding boxes manually (no labels)
    current_boxes = []
    if results[0].boxes is not None:
        for box in results[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            current_boxes.append((x1, y1, x2, y2))
    
    # Draw boxes without labels
    display_frame = frame.copy()
    for i, (x1, y1, x2, y2) in enumerate(current_boxes):
        # Color: green if selected, blue otherwise
        color = (0, 255, 0) if i == selected_box else (255, 0, 0)
        thickness = 3 if i == selected_box else 2
        
        cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, thickness)
        
        # Just show box number, no class name
        cv2.putText(display_frame, str(i), (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Instructions
    cv2.putText(display_frame, "Press 'c' to crop ALL objects, 'q' quit", 
               (10, display_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow('Object Detection', display_frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
    elif key == ord('c') and current_boxes:
        # Crop ALL detected objects
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, (x1, y1, x2, y2) in enumerate(current_boxes):
            # Add padding
            padding = 20
            h, w = frame.shape[:2]
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(w, x2 + padding)
            y2 = min(h, y2 + padding)
            
            # Crop
            cropped = frame[y1:y2, x1:x2]
            
            # Save each object
            filename = f"{output_dir}/object_{i}_{timestamp}_{frame_count:04d}.jpg"
            cv2.imwrite(filename, cropped)
            print(f"Saved object {i}: {filename}")
        
        print(f"Saved {len(current_boxes)} objects!")
        frame_count += 1

cap.release()
cv2.destroyAllWindows()
print("Done!")#!/usr/bin/env python3
"""
Minimal YOLO object detection with webcam
"""

import cv2
from ultralytics import YOLO

print("Loading YOLO model...")
model = YOLO("yolov8n.pt")  # This will auto-download on first run
print("Model loaded!")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Starting detection... Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Run YOLO detection
    results = model(frame, verbose=False)
    
    # Draw results on frame
    annotated_frame = results[0].plot()
    
    cv2.imshow('YOLO Detection', annotated_frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Done!")