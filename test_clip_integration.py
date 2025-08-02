#!/usr/bin/env python3
"""
Test script to verify CLIP model integration
"""
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Add CLIP directory to path
clip_dir = os.path.join(os.path.dirname(__file__), 'CLIP')
sys.path.insert(0, clip_dir)

from services import CLIPService

def test_clip_service():
    print("🧪 Testing CLIP Service Integration...")
    
    try:
        # Initialize CLIP service
        print("Initializing CLIP service...")
        clip_service = CLIPService()
        
        # Test with a sample image from your tool_images
        test_image_dir = os.path.join(os.path.dirname(__file__), 'CLIP', 'tool_images')
        
        # Find a test image
        test_image = None
        for tool_folder in os.listdir(test_image_dir):
            tool_path = os.path.join(test_image_dir, tool_folder)
            if os.path.isdir(tool_path):
                for image_file in os.listdir(tool_path):
                    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        test_image = os.path.join(tool_path, image_file)
                        print(f"Using test image: {test_image}")
                        break
                if test_image:
                    break
        
        if test_image and os.path.exists(test_image):
            print(f"\n📷 Testing classification with: {os.path.basename(test_image)}")
            result = clip_service.classify_image(test_image)
            
            print(f"✅ Classification Results:")
            print(f"  📍 Predicted Class: {result['predicted_class']}")
            print(f"  🎯 Confidence: {result['confidence']:.2%}")
            
            if 'all_probabilities' in result and result['all_probabilities']:
                print(f"  📊 Top 3 Probabilities:")
                
                # Sort probabilities and show top 3
                sorted_probs = sorted(result['all_probabilities'].items(), 
                                    key=lambda x: x[1], reverse=True)
                for i, (class_name, prob) in enumerate(sorted_probs[:3]):
                    print(f"    {i+1}. {class_name}: {prob:.2%}")
            else:
                print(f"  ⚠️  No probability data available")
                
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
                
            print(f"\n🔧 Available tool classes: {len(clip_service.class_names)}")
            print(f"Classes: {', '.join(clip_service.class_names[:5])}...")
            
        else:
            print(f"❌ No test images found in {test_image_dir}")
            
        print(f"\n✅ CLIP Service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing CLIP service: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_images():
    print("\n🔬 Testing multiple image classification...")
    
    try:
        clip_service = CLIPService()
        
        # Find multiple test images
        test_image_dir = os.path.join(os.path.dirname(__file__), 'CLIP', 'tool_images')
        test_images = []
        
        # Get a few images from different tool categories
        for tool_folder in os.listdir(test_image_dir)[:3]:  # Test with first 3 tool categories
            tool_path = os.path.join(test_image_dir, tool_folder)
            if os.path.isdir(tool_path):
                for image_file in os.listdir(tool_path)[:2]:  # 2 images per category
                    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        test_images.append(os.path.join(tool_path, image_file))
        
        if test_images:
            print(f"Testing with {len(test_images)} images...")
            results = clip_service.classify_multiple_images(test_images)
            
            print(f"📊 Aggregated Results:")
            print(f"  Total objects processed: {results['total_objects']}")
            print(f"  Tool counts detected: {results['tool_counts']}")
            
            print(f"\n🎯 Individual results:")
            for image_path, result in results['individual_results'].items():
                filename = os.path.basename(image_path)
                print(f"  {filename}: {result['predicted_class']} ({result['confidence']:.1%})")
                
        else:
            print("❌ No test images found for multiple image test")
            
    except Exception as e:
        print(f"❌ Error testing multiple images: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 CLIP Model Integration Test\n")
    
    # Test basic CLIP service
    success = test_clip_service()
    
    if success:
        # Test multiple image classification
        test_multiple_images()
    
    print("\n🏁 Testing complete!")
