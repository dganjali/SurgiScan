# Video Object Detection Pipeline (Manual Labeling)
# This script processes a video file frame-by-frame using:
# 1. Detectron2 RetinaNet for object detection
# 2. Labels each detected object with letters (a, b, c, etc.) for manual review
# 3. No CLIP classification - human labeling instead

import cv2
import torch
import os
import time
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

# Import for object detection only (no CLIP needed)
import sys

# No CLIP import needed for manual labeling
CLIP_AVAILABLE = False
print("Manual labeling mode - CLIP classification disabled")

VIDEO_PATH = "video.mp4"  # Change this to your video filename

OUTPUT_DIR = "video_clip_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames_with_boxes")
os.makedirs(FRAMES_DIR, exist_ok=True)

def process_video_with_detection():
    """
    Process video frame by frame with object detection and CLIP classification
    """
    # Setup Detectron2 RetinaNet with balanced settings for accurate detection
    print("Setting up Detectron2 RetinaNet with balanced detection settings...")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/retinanet_R_50_FPN_3x.yaml"))
    
    # Use balanced thresholds - not too low (false positives) not too high (missed detections)
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.45  # Balanced threshold between 0.3 and 0.6
    cfg.MODEL.RETINANET.NMS_THRESH_TEST = 0.5     # Standard NMS threshold
    cfg.MODEL.RETINANET.TOPK_CANDIDATES_TEST = 500  # Moderate candidate limit
    
    # Load model weights
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    predictor = DefaultPredictor(cfg)
    metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    
    print(f"Using device: {cfg.MODEL.DEVICE}")
    print(f"Detection threshold: {cfg.MODEL.RETINANET.SCORE_THRESH_TEST} (balanced for accuracy and coverage)")
    print(f"This will detect objects with moderate confidence")
    print(f"Bounding boxes will only be drawn for objects with ≥0.65 confidence")
    
    # Open video
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"Cannot open video: {VIDEO_PATH}")
        return
    
    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / original_fps if original_fps > 0 else 0
    
    # Target processing rate: 10 frames per second
    target_fps = 10
    frame_skip = max(1, int(original_fps / target_fps))  # Skip frames to achieve target FPS
    
    print(f"Processing video: {VIDEO_PATH}")
    print(f"Original FPS: {original_fps:.2f}, Total frames: {total_frames}, Duration: {duration:.2f}s")
    print(f"Target processing rate: {target_fps} FPS (processing every {frame_skip} frames)")
    print(f"Estimated frames to process: {total_frames // frame_skip}")
    
    frame_idx = 0
    processed_frame_count = 0
    detected_tools = set()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Skip frames to achieve target framerate (only process every Nth frame)
        if frame_idx % frame_skip != 0:
            frame_idx += 1
            continue
            
        print(f"Processing frame {frame_idx} (processed frame #{processed_frame_count + 1})")
        
        # Run Detectron2 detection on full frame (single strategy for cleaner results)
        outputs = predictor(frame)
        instances = outputs["instances"]
        
        # Get detection results
        boxes = instances.pred_boxes.tensor.cpu().numpy() if instances.has("pred_boxes") else []
        scores = instances.scores.cpu().numpy() if instances.has("scores") else []
        classes = instances.pred_classes.cpu().numpy() if instances.has("pred_classes") else []
        
        print(f"  Frame {frame_idx}: {len(boxes)} objects detected")
        
        # Create a copy of the frame for drawing
        frame_with_boxes = frame.copy()
        
        if len(boxes) > 0:
            for i, (box, score, cls) in enumerate(zip(boxes, scores, classes)):
                x1, y1, x2, y2 = box.astype(int)
                
                # Get class name from COCO classes
                class_name = metadata.thing_classes[cls] if hasattr(metadata, 'thing_classes') else f"class_{cls}"
                
                # Crop the detected object
                crop = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
                
                # Save crop for CLIP analysis
                crop_path = os.path.join(OUTPUT_DIR, f"frame{frame_idx}_obj{i}.jpg")
                cv2.imwrite(crop_path, crop)
                
                # Initialize variables for confidence checking
                final_confidence = score  # Default to detection confidence
                draw_box = False
                
                # Use CLIP classification for surgical tool identification
                if CLIP_AVAILABLE:
                    try:
                        clip_result = classify_image(crop_path, clip_model, clip_preprocess, clip_metadata, clip_device, clip_tokenizer)
                        clip_label = clip_result['predicted_class']
                        clip_confidence = clip_result['confidence']
                        label = f"{clip_label} ({clip_confidence:.2f})"
                        detected_tools.add(clip_label)
                        final_confidence = clip_confidence  # Use CLIP confidence for threshold
                        print(f"    Object {i+1}: CLIP classified as '{clip_label}' (confidence: {clip_confidence:.2f}, COCO: {class_name})")
                    except Exception as e:
                        label = f"{class_name}: {score:.2f}"
                        detected_tools.add(class_name)
                        final_confidence = score  # Use detection confidence
                        print(f"    Object {i+1}: CLIP failed ({e}), using COCO: {class_name} (conf: {score:.2f})")
                else:
                    label = f"{class_name}: {score:.2f}"
                    detected_tools.add(class_name)
                    final_confidence = score  # Use detection confidence
                    print(f"    Object {i+1}: {class_name} (confidence: {score:.2f}) - CLIP not available")
                
                # Only draw bounding box if confidence is 0.65 or higher
                if final_confidence >= 0.65:
                    draw_box = True
                    # Draw bounding box (red color, thick line)
                    cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    
                    # Draw label background
                    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(frame_with_boxes, (x1, y1 - label_height - 10), (x1 + label_width, y1), (0, 0, 255), -1)
                    
                    # Draw label text
                    cv2.putText(frame_with_boxes, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                else:
                    print(f"    Object {i+1}: Confidence {final_confidence:.2f} below threshold (0.65), not drawing box")
        
        # Save frame with bounding boxes (use processed frame count for consistent numbering)
        frame_box_path = os.path.join(FRAMES_DIR, f"frame_{processed_frame_count:05d}.jpg")
        cv2.imwrite(frame_box_path, frame_with_boxes)
        
        processed_frame_count += 1
        frame_idx += 1
        
        # Remove the delay since we're already processing at lower framerate
        # time.sleep(0.1)  # Removed since frame skipping already reduces processing load
    
    cap.release()
    
    print(f"\nVideo processing completed!")
    print(f"Total frames in video: {frame_idx}")
    print(f"Frames actually processed: {processed_frame_count}")
    print(f"Processing rate: {processed_frame_count/frame_idx*100:.1f}% of frames (target: {target_fps} FPS)")
    print(f"Tools/objects detected in video:")
    for tool in sorted(list(detected_tools)):
        print(f"  - {tool}")
    print(f"\nFrames with bounding boxes saved to: {FRAMES_DIR}")
    print(f"Cropped objects saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_video_with_detection()
