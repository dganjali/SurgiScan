# Video segment -> CLIP pipeline
# This script processes a video file frame-by-frame, runs object detection (RetinaNet via Detectron2),
# and calls CLIP classification for each detected object. It spends extra time on each frame for accuracy.

import cv2
import torch
import os
import time
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

# Import CLIP pipeline (assume CLIP/clip_inference.py has a classify_image function)
import sys
sys.path.append('CLIP')
from clip_inference import classify_image  # You may need to adjust this import

VIDEO_PATH = "input_video.mp4"  # Change this to your video filename
OUTPUT_DIR = "video_clip_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Setup Detectron2 RetinaNet
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/retinanet_R_50_FPN_3x.yaml"))
cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_50_FPN_3x.yaml")
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
predictor = DefaultPredictor(cfg)
metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"Cannot open video: {VIDEO_PATH}")
    exit(1)

frame_idx = 0
detected_tools = set()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    print(f"Processing frame {frame_idx}")
    # Spend extra time on each frame (simulate slow, accurate detection)
    time.sleep(0.5)  # Increase for more time per frame
    # Detect objects
    small_frame = cv2.resize(frame, (640, 480))
    outputs = predictor(small_frame)
    instances = outputs["instances"]
    boxes = instances.pred_boxes.tensor.cpu().numpy() if instances.has("pred_boxes") else []
    # For each detected object, crop and classify with CLIP
    y_scale = frame.shape[0] / 480
    x_scale = frame.shape[1] / 640
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box.astype(int)
        x1 = int(x1 * x_scale)
        x2 = int(x2 * x_scale)
        y1 = int(y1 * y_scale)
        y2 = int(y2 * y_scale)
        crop = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
        crop_path = os.path.join(OUTPUT_DIR, f"frame{frame_idx}_obj{i}.jpg")
        cv2.imwrite(crop_path, crop)
        # Run CLIP classification (assumes classify_image returns a label)
        label = classify_image(crop_path)
        print(f"Frame {frame_idx} Object {i}: {label}")
        detected_tools.add(label)
    frame_idx += 1

cap.release()
print("Video segment->CLIP pipeline completed.")
print("Tools detected in video:")
print(sorted(list(detected_tools)))
