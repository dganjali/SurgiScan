# CLIP Surgical Tool Classification

This project trains a CLIP (Contrastive Language-Image Pre-training) model to classify surgical tools based on images organized in folders by tool type.

## Project Structure

```
tool_images/
├── Adson forceps/
├── Army-Navy retractor/
├── Bulldog clamp/
├── Deaver retractor/
├── Mayo-Hegar needle holder/
├── Metzenbaum scissors/
├── Mosquito clamp/
├── Raytec surgical sponge/
├── Scalpel with blade/
├── Sponge forceps/
├── Sterile basin (metal)/
├── Sterile gauze pad/
├── Sterile surgical towel/
├── Weitlaner retractor/
└── Yankauer suction tip/
```

Each folder contains multiple images of the respective surgical tool.

## Files

- `clip_training.py`: Main training script
- `clip_inference.py`: Script to classify new images using the trained model
- `clip_requirements.txt`: Required Python packages
- `CLIP_README.md`: This documentation

## Setup

1. Install the required dependencies:
```bash
pip install -r clip_requirements.txt
```

2. Make sure your `tool_images` folder is in the same directory as the scripts.

## Training

Run the training script to train the CLIP model:

```bash
python clip_training.py
```

The script will:
- Load all images from the `tool_images` folder structure
- Use folder names as class labels
- Split the data into training (80%) and validation (20%) sets
- Train a CLIP model for 15 epochs
- Save the best model as `best_surgical_tool_clip.pth`
- Save metadata (label mappings) as `surgical_tool_metadata.pkl`

## Inference

After training, you can use the trained model to classify new images:

```bash
python clip_inference.py
```

The inference script will:
- Load the trained model and metadata
- Classify a test image (currently set to a scalpel image)
- Show the predicted class and confidence scores

To classify your own images, modify the `test_image_path` variable in `clip_inference.py`.

## Model Details

- **Base Model**: CLIP ViT-B/32
- **Training**: Fine-tuned on surgical tool images
- **Classes**: 15 different surgical tools
- **Text Prompts**: Uses "a photo of a [tool_name]" format
- **Loss**: Cross-entropy loss on similarity scores

## Output Files

After training, you'll get:
- `best_surgical_tool_clip.pth`: Trained model weights
- `surgical_tool_metadata.pkl`: Label mappings and class information

## Customization

You can modify the training parameters in `clip_training.py`:
- `num_epochs`: Number of training epochs (default: 15)
- `learning_rate`: Learning rate (default: 5e-5)
- `batch_size`: Batch size (default: 32)

## Usage Example

```python
from clip_inference import load_trained_model, classify_image

# Load the trained model
model, preprocess, metadata = load_trained_model(
    "best_surgical_tool_clip.pth", 
    "surgical_tool_metadata.pkl", 
    "cuda"
)

# Classify an image
result = classify_image("path/to/your/image.jpg", model, preprocess, metadata, "cuda")
print(f"Predicted: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Notes

- The model uses GPU if available, otherwise falls back to CPU
- Training time depends on the number of images and your hardware
- The model is designed to work with the specific surgical tool categories in your dataset
- You can add new tool categories by adding new folders to the `tool_images` directory and retraining 