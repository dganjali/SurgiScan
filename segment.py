
# Detectron2-based real-time object detection and cropping
import cv2
import os
from datetime import datetime
import torch
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

output_dir = "cropped_objects"
os.makedirs(output_dir, exist_ok=True)

# Setup Detectron2 config for Mask R-CNN
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
predictor = DefaultPredictor(cfg)
metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Starting Detectron2 detection... Press 'c' to crop all objects, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    outputs = predictor(frame)
    instances = outputs["instances"]
    boxes = instances.pred_boxes.tensor.cpu().numpy() if instances.has("pred_boxes") else []
    scores = instances.scores.cpu().numpy() if instances.has("scores") else []
    classes = instances.pred_classes.cpu().numpy() if instances.has("pred_classes") else []

    v = Visualizer(frame[:, :, ::-1], metadata=metadata, scale=1.0)
    out = v.draw_instance_predictions(instances.to("cpu"))
    vis_frame = out.get_image()[:, :, ::-1]

    cv2.imshow('Detectron2 Object Detection', vis_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c') and len(boxes) > 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for i, (box, cls, score) in enumerate(zip(boxes, classes, scores)):
            x1, y1, x2, y2 = box.astype(int)
            crop = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
            label = metadata.get("thing_classes", ["object"])[cls] if hasattr(metadata, "thing_classes") else str(cls)
            filename = f"{output_dir}/object_{label}_{i}_{timestamp}.jpg"
            cv2.imwrite(filename, crop)
            print(f"Saved {filename}")

cap.release()
cv2.destroyAllWindows()
print("Done!")