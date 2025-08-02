import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import open_clip
import json
from tqdm import tqdm
import numpy as np
from sklearn.model_selection import train_test_split
import pickle

class SurgicalToolDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        # Load image
        image = Image.open(image_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

def load_dataset_from_folder(root_dir):
    """Load images and labels from the tool_images folder structure"""
    image_paths = []
    labels = []
    label_to_idx = {}
    idx = 0
    
    # Walk through all subdirectories
    for tool_folder in os.listdir(root_dir):
        tool_path = os.path.join(root_dir, tool_folder)
        
        if os.path.isdir(tool_path) and not tool_folder.startswith('.'):
            # Add label to mapping
            if tool_folder not in label_to_idx:
                label_to_idx[tool_folder] = idx
                idx += 1
            
            # Get all images in this tool folder
            for image_file in os.listdir(tool_path):
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(tool_path, image_file)
                    image_paths.append(image_path)
                    labels.append(label_to_idx[tool_folder])
    
    return image_paths, labels, label_to_idx

def train_clip_model(model, train_loader, val_loader, device, num_epochs=10, learning_rate=5e-5):
    """Train the CLIP model"""
    model.train()
    
    # Use Adam optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Loss function
    criterion = nn.CrossEntropyLoss()
    
    best_val_loss = float('inf')
    
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        
        # Training loop
        for batch_idx, (images, labels) in enumerate(tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}')):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            
            # Get image and text features
            image_features = model.encode_image(images)
            
            # Create text features for all classes
            text_inputs = [f"a photo of a {class_name}" for class_name in class_names]
            text_tokens = tokenizer(text_inputs).to(device)
            text_features = model.encode_text(text_tokens)
            
            # Normalize features
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # Calculate similarity
            similarity = 100.0 * image_features @ text_features.T
            
            # Calculate loss
            loss = criterion(similarity, labels)
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                
                image_features = model.encode_image(images)
                text_inputs = [f"a photo of a {class_name}" for class_name in class_names]
                text_tokens = tokenizer(text_inputs).to(device)
                text_features = model.encode_text(text_tokens)
                
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                
                similarity = 100.0 * image_features @ text_features.T
                loss = criterion(similarity, labels)
                
                val_loss += loss.item()
                
                _, predicted = torch.max(similarity, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        accuracy = 100 * correct / total
        
        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'  Train Loss: {avg_train_loss:.4f}')
        print(f'  Val Loss: {avg_val_loss:.4f}')
        print(f'  Val Accuracy: {accuracy:.2f}%')
        
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), 'best_surgical_tool_clip.pth')
            print(f'  Saved best model with validation loss: {best_val_loss:.4f}')

def main():
    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load CLIP model
    print("Loading CLIP model...")
    model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai", device=device)
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    
    # Load dataset
    print("Loading dataset...")
    root_dir = "tool_images"
    image_paths, labels, label_to_idx = load_dataset_from_folder(root_dir)
    
    # Create reverse mapping for class names
    idx_to_label = {v: k for k, v in label_to_idx.items()}
    class_names = [idx_to_label[i] for i in range(len(idx_to_label))]
    
    print(f"Found {len(image_paths)} images across {len(class_names)} classes:")
    for i, class_name in enumerate(class_names):
        count = labels.count(i)
        print(f"  {class_name}: {count} images")
    
    # Split dataset
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Create datasets
    train_dataset = SurgicalToolDataset(train_paths, train_labels, transform=preprocess)
    val_dataset = SurgicalToolDataset(val_paths, val_labels, transform=preprocess)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)
    
    print(f"Training set: {len(train_dataset)} images")
    print(f"Validation set: {len(val_dataset)} images")
    
    # Train the model
    print("Starting training...")
    train_clip_model(model, train_loader, val_loader, device, num_epochs=15, learning_rate=5e-5)
    
    # Save metadata
    metadata = {
        'label_to_idx': label_to_idx,
        'idx_to_label': idx_to_label,
        'class_names': class_names,
        'num_classes': len(class_names)
    }
    
    with open('surgical_tool_metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)
    
    print("Training completed!")
    print("Saved files:")
    print("  - best_surgical_tool_clip.pth (trained model)")
    print("  - surgical_tool_metadata.pkl (label mappings)")

if __name__ == "__main__":
    main() 