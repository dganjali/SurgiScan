# Simple Detectron2 test script
# This script loads a sample image and runs inference with Mask R-CNN
import cv2
import torch
import threading
import time
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog


# Use webcam for Detectron2 inference

# Use Faster R-CNN for speed

# Use RetinaNet for faster object detection
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/retinanet_R_50_FPN_3x.yaml"))
cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_50_FPN_3x.yaml")
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
predictor = DefaultPredictor(cfg)
metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])


cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open webcam")
    exit(1)

print("Detectron2 webcam test: Press 'q' to quit.")

# Shared state for threading
latest_boxes = []
latest_boxes_lock = threading.Lock()
latest_frame = None
latest_frame_lock = threading.Lock()
running = True

def detect_thread_func():
    global latest_boxes, latest_frame, running
    while running:
        # Copy the latest frame for detection
        with latest_frame_lock:
            frame_for_detect = None if latest_frame is None else latest_frame.copy()
        if frame_for_detect is not None:
            small_frame = cv2.resize(frame_for_detect, (640, 480))
            outputs = predictor(small_frame)
            instances = outputs["instances"]
            boxes = []
            if instances.has("pred_boxes"):
                boxes = instances.pred_boxes.tensor.cpu().numpy()
            with latest_boxes_lock:
                latest_boxes = boxes
        time.sleep(0.1)  # ~10 fps for detection

# Start detection thread
detect_thread = threading.Thread(target=detect_thread_func)
detect_thread.start()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break
    # Update the latest frame for detection
    with latest_frame_lock:
        latest_frame = frame.copy()
    # Draw boxes from latest detection
    display_frame = frame.copy()
    with latest_boxes_lock:
        boxes = latest_boxes.copy()
    if len(boxes) > 0:
        y_scale = frame.shape[0] / 480
        x_scale = frame.shape[1] / 640
        for box in boxes:
            x1, y1, x2, y2 = box.astype(int)
            x1 = int(x1 * x_scale)
            x2 = int(x2 * x_scale)
            y1 = int(y1 * y_scale)
            y2 = int(y2 * y_scale)
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Detectron2 Webcam Test", display_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        running = False
        break
cap.release()
cv2.destroyAllWindows()
detect_thread.join()
print("Detectron2 webcam test completed.")
