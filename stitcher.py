import cv2
import os
from natsort import natsorted

# Settings
image_folder = 'detr_output_smoothed/overlays'        # Folder containing .jpg files
output_file = 'output.mp4'     # Output video file
fps = 10                       # Frames per second

# Get list of .jpg files, sorted naturally
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images = natsorted(images)  # Ensures images like img1.jpg, img2.jpg, ..., img10.jpg are ordered correctly

# Read first image to get size
if not images:
    raise Exception("No .jpg images found in the folder.")

first_frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, _ = first_frame.shape

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for .avi
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Write each image frame
for image in images:
    frame = cv2.imread(os.path.join(image_folder, image))
    if frame is None:
        print(f"Warning: Could not read {image}, skipping.")
        continue
    resized = cv2.resize(frame, (width, height))
    out.write(resized)

out.release()
print(f"Video saved to {output_file}")
