# Simple Detectron2 test script
# This script loads a sample image and runs inference with Mask R-CNN
import cv2
import torch
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog


# Use webcam for Detectron2 inference
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
predictor = DefaultPredictor(cfg)
metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam")
    exit(1)

print("Detectron2 webcam test: Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break
    outputs = predictor(frame)
    instances = outputs["instances"]
    v = Visualizer(frame[:, :, ::-1], metadata=metadata, scale=1.0)
    out = v.draw_instance_predictions(instances.to("cpu"))
    vis_frame = out.get_image()[:, :, ::-1]
    cv2.imshow("Detectron2 Webcam Test", vis_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print("Detectron2 webcam test completed.")
