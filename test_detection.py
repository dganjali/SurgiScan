# Object Detection Test Script
# This script takes a single image, detects objects using Detectron2 RetinaNet,
# draws bounding boxes around detected objects, and prints detection results.

import cv2
import torch
import os
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

def test_object_detection(image_path, output_path="test_detection_output.jpg"):
    """
    Test object detection on a single image
    
    Args:
        image_path (str): Path to input image
        output_path (str): Path to save output image with bounding boxes
    """
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return
    
    print(f"Loading image: {image_path}")
    print(f"Image shape: {img.shape}")
    
    # Setup Detectron2 RetinaNet
    print("Setting up Detectron2 RetinaNet...")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/retinanet_R_50_FPN_3x.yaml"))
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    predictor = DefaultPredictor(cfg)
    metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    
    print(f"Using device: {cfg.MODEL.DEVICE}")
    
    # Run detection
    print("Running object detection...")
    outputs = predictor(img)
    instances = outputs["instances"]
    
    # Get detection results
    boxes = instances.pred_boxes.tensor.cpu().numpy() if instances.has("pred_boxes") else []
    scores = instances.scores.cpu().numpy() if instances.has("scores") else []
    classes = instances.pred_classes.cpu().numpy() if instances.has("pred_classes") else []
    
    print(f"\nDetection Results:")
    print(f"Number of objects detected: {len(boxes)}")
    
    if len(boxes) > 0:
        print("Objects detected: YES")
        
        # Draw bounding boxes on image
        img_with_boxes = img.copy()
        
        for i, (box, score, cls) in enumerate(zip(boxes, scores, classes)):
            x1, y1, x2, y2 = box.astype(int)
            
            # Get class name
            class_name = metadata.thing_classes[cls] if hasattr(metadata, 'thing_classes') else f"class_{cls}"
            
            print(f"  Object {i+1}: {class_name} (confidence: {score:.2f}) at [{x1}, {y1}, {x2}, {y2}]")
            
            # Draw bounding box (red color, thick line)
            cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), (0, 0, 255), 3)
            
            # Draw label background
            label = f"{class_name}: {score:.2f}"
            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(img_with_boxes, (x1, y1 - label_height - 10), (x1 + label_width, y1), (0, 0, 255), -1)
            
            # Draw label text
            cv2.putText(img_with_boxes, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Save output image
        cv2.imwrite(output_path, img_with_boxes)
        print(f"\nOutput image saved to: {output_path}")
        
    else:
        print("Objects detected: NO")
        print("No objects detected in the image.")
        
        # Save original image as output
        cv2.imwrite(output_path, img)
        print(f"\nOriginal image saved to: {output_path}")

if __name__ == "__main__":
    # Test with a sample image
    test_image_path = "testimg.png"  # Change this to your test image path
    
    if len(os.sys.argv) > 1:
        test_image_path = os.sys.argv[1]
    
    print("Object Detection Test Script")
    print("=" * 40)
    
    test_object_detection(test_image_path)
    
    print("\nTest completed!")
