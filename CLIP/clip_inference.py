import torch
import open_clip
from PIL import Image
import pickle
import os

def load_trained_model(model_path, metadata_path, device):
    """Load the trained CLIP model and metadata"""
    # Load CLIP model
    model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai", device=device)
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    
    # Load trained weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    # Load metadata
    with open(metadata_path, 'rb') as f:
        metadata = pickle.load(f)
    
    return model, preprocess, tokenizer, metadata

def classify_image(image_path, model, preprocess, metadata, device):
    """Classify a single image"""
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    image_input = preprocess(image).unsqueeze(0).to(device)
    
    # Get image features
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        
        # Create text features for all classes
        class_names = metadata['class_names']
        text_inputs = [f"a photo of a {class_name}" for class_name in class_names]
        text_tokens = tokenizer(text_inputs).to(device)
        text_features = model.encode_text(text_tokens)
        
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
            'all_probabilities': {class_names[i]: probabilities[0][i].item() for i in range(len(class_names))}
        }

def main():
    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model and metadata
    model_path = "best_surgical_tool_clip.pth"
    metadata_path = "surgical_tool_metadata.pkl"
    
    if not os.path.exists(model_path):
        print(f"Error: Model file {model_path} not found. Please run the training script first.")
        return
    
    if not os.path.exists(metadata_path):
        print(f"Error: Metadata file {metadata_path} not found. Please run the training script first.")
        return
    
    print("Loading trained model...")
    model, preprocess, tokenizer, metadata = load_trained_model(model_path, metadata_path, device)
    
    print(f"Loaded model with {len(metadata['class_names'])} classes:")
    for i, class_name in enumerate(metadata['class_names']):
        print(f"  {i}: {class_name}")
    
    # Example: classify an image
    # You can replace this with your own image path
    test_image_path = "tool_images/Scalpel with blade/search_1_000001.jpg"
    
    if os.path.exists(test_image_path):
        print(f"\nClassifying image: {test_image_path}")
        result = classify_image(test_image_path, model, preprocess, metadata, device)
        
        print(f"Predicted class: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print("\nAll probabilities:")
        for class_name, prob in sorted(result['all_probabilities'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {class_name}: {prob:.2%}")
    else:
        print(f"Test image not found: {test_image_path}")
        print("Please provide a valid image path to test the model.")

if __name__ == "__main__":
    main() 