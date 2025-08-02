import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MCP-scraping'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CLIP'))

import torch
import open_clip
from PIL import Image
import pickle
import cv2
from ultralytics import YOLO
import numpy as np

# Import CLIP inference functions
from clip_inference import load_trained_model, classify_image

class SegmentationService:
    def __init__(self):
        print("Loading YOLO model...")
        self.model = YOLO(os.path.join(os.path.dirname(__file__), '..', 'yolov8n.pt'))
        print("YOLO model loaded!")
        
    def segment_image(self, image_path: str, output_dir: str = "cropped_objects") -> list:
        """Segment objects from image and return list of cropped image paths"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
            
        # Run YOLO detection
        results = self.model(image)
        
        cropped_paths = []
        for i, result in enumerate(results):
            boxes = result.boxes
            if boxes is not None:
                for j, box in enumerate(boxes):
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    
                    # Crop the object
                    cropped_object = image[y1:y2, x1:x2]
                    
                    # Save cropped object
                    crop_filename = f"crop_{i}_{j}.jpg"
                    crop_path = os.path.join(output_dir, crop_filename)
                    cv2.imwrite(crop_path, cropped_object)
                    cropped_paths.append(crop_path)
                    
        return cropped_paths

class CLIPService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Paths to trained model and metadata - fix path resolution
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Go up from backend to project root
        model_path = os.path.join(base_dir, 'CLIP', 'best_surgical_tool_clip.pth')
        metadata_path = os.path.join(base_dir, 'CLIP', 'surgical_tool_metadata.pkl')
        
        print(f"Looking for trained model at: {model_path}")
        print(f"Looking for metadata at: {metadata_path}")
        
        if os.path.exists(model_path) and os.path.exists(metadata_path):
            print("Loading trained CLIP model...")
            self.model, self.preprocess, self.tokenizer, self.metadata = load_trained_model(
                model_path, metadata_path, self.device
            )
            self.class_names = self.metadata['class_names']
            print(f"✅ Loaded trained model with {len(self.class_names)} classes: {self.class_names}")
        else:
            print(f"❌ Trained model files not found at {model_path} or {metadata_path}")
            print("Using pre-trained CLIP model without fine-tuning")
            # Load CLIP model
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                "ViT-B-32", pretrained="openai", device=self.device
            )
            self.tokenizer = open_clip.get_tokenizer("ViT-B-32")
            # Default medical tool classes
            self.class_names = [
                "scalpel", "syringe", "stethoscope", "forceps", "scissors", 
                "retractor", "clamp", "needle", "suture", "gauze", "bandage",
                "thermometer", "blood pressure cuff", "defibrillator", "oxygen mask"
            ]
            self.model.eval()
        
    def classify_image(self, image_path: str) -> dict:
        """Classify a single image and return prediction results"""
        try:
            # Check if we have trained model loaded
            if hasattr(self, 'metadata'):
                # Use the trained model with clip_inference function
                # Need to pass tokenizer as well - create a modified version
                image = Image.open(image_path).convert('RGB')
                image_input = self.preprocess(image).unsqueeze(0).to(self.device)
                
                with torch.no_grad():
                    image_features = self.model.encode_image(image_input)
                    
                    # Create text features for all classes
                    class_names = self.metadata['class_names']
                    text_inputs = [f"a photo of a {class_name}" for class_name in class_names]
                    text_tokens = self.tokenizer(text_inputs).to(self.device)
                    text_features = self.model.encode_text(text_tokens)
                    
                    # Normalize features
                    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                    
                    # Calculate similarity
                    similarity = 100.0 * image_features @ text_features.T
                    
                    # Get predictions
                    probabilities = torch.softmax(similarity, dim=-1)
                    predicted_idx = torch.argmax(similarity, dim=-1).item()
                    confidence = probabilities[0][predicted_idx].item()
                    
                    return {
                        'predicted_class': class_names[predicted_idx],
                        'confidence': confidence,
                        'all_probabilities': {
                            class_names[i]: probabilities[0][i].item() 
                            for i in range(len(class_names))
                        }
                    }
            else:
                # Use fallback classification with open_clip
                image = Image.open(image_path).convert('RGB')
                image_input = self.preprocess(image).unsqueeze(0).to(self.device)
                
                with torch.no_grad():
                    image_features = self.model.encode_image(image_input)
                    
                    # Create text features for all classes
                    text_inputs = [f"a photo of a {class_name}" for class_name in self.class_names]
                    text_tokens = self.tokenizer(text_inputs).to(self.device)
                    text_features = self.model.encode_text(text_tokens)
                    
                    # Normalize features
                    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                    
                    # Calculate similarity
                    similarity = 100.0 * image_features @ text_features.T
                    
                    # Get predictions
                    probabilities = torch.softmax(similarity, dim=-1)
                    predicted_idx = torch.argmax(similarity, dim=-1).item()
                    confidence = probabilities[0][predicted_idx].item()
                    
                    return {
                        'predicted_class': self.class_names[predicted_idx],
                        'confidence': confidence,
                        'all_probabilities': {
                            self.class_names[i]: probabilities[0][i].item() 
                            for i in range(len(self.class_names))
                        }
                    }
        except Exception as e:
            print(f"Error classifying image {image_path}: {e}")
            return {
                'predicted_class': 'unknown',
                'confidence': 0.0,
                'all_probabilities': {},
                'error': str(e)
            }
            
    def classify_multiple_images(self, image_paths: list) -> dict:
        """Classify multiple images and return aggregated results"""
        results = {}
        tool_counts = {}
        
        # Use higher confidence threshold for trained model
        confidence_threshold = 0.3 if hasattr(self, 'metadata') else 0.5
        
        for image_path in image_paths:
            result = self.classify_image(image_path)
            results[image_path] = result
            
            if 'predicted_class' in result and result['confidence'] > confidence_threshold:
                tool_name = result['predicted_class']
                tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
                print(f"Classified {os.path.basename(image_path)}: {tool_name} (confidence: {result['confidence']:.2%})")
                
        return {
            'individual_results': results,
            'tool_counts': tool_counts,
            'total_objects': len(image_paths)
        }

class MCPService:
    def __init__(self):
        try:
            from tool_requirement_agent import ToolRequirementAgent
            self.agent = ToolRequirementAgent()
        except ImportError:
            print("MCP scraping agent not available, using fallback")
            self.agent = None
            
    def get_procedure_tools(self, procedure: str) -> list:
        """Get required tools for a medical procedure"""
        if self.agent:
            try:
                result = self.agent.get_procedure_tools(procedure)
                if 'tools_needed' in result:
                    return result['tools_needed']
                elif 'crash_cart_tools' in result:
                    return result['crash_cart_tools']
            except Exception as e:
                print(f"Error getting tools from MCP agent: {e}")
                
        # Fallback tool lists for common procedures
        fallback_tools = {
            "code blue": [
                "defibrillator", "oxygen mask", "ambu bag", "iv catheter", 
                "syringe", "epinephrine", "atropine", "cardiac monitor"
            ],
            "intubation": [
                "laryngoscope", "endotracheal tube", "ambu bag", "oxygen mask",
                "suction catheter", "stylet", "syringe"
            ],
            "cardiac arrest": [
                "defibrillator", "oxygen mask", "ambu bag", "iv catheter",
                "syringe", "epinephrine", "atropine", "cardiac monitor"
            ],
            "trauma": [
                "gauze", "bandage", "iv catheter", "syringe", "saline",
                "blood pressure cuff", "stethoscope", "splint"
            ]
        }
        
        procedure_lower = procedure.lower()
        for key, tools in fallback_tools.items():
            if key in procedure_lower:
                return tools
                
        # Default emergency tools
        return [
            "stethoscope", "blood pressure cuff", "syringe", "iv catheter",
            "gauze", "bandage", "oxygen mask", "defibrillator"
        ]
