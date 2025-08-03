import cv2
import numpy as np
import os
from glob import glob
from sklearn.metrics.pairwise import cosine_similarity

def load_downscaled_frame(video_path, frame_idx, max_dim=480):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w = rgb_frame.shape[:2]
    scale = max_dim / max(h, w)
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        rgb_frame = cv2.resize(rgb_frame, (new_w, new_h))
    return rgb_frame

def crop_object(image, mask):
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return None, None
    x1, x2 = xs.min(), xs.max()
    y1, y2 = ys.min(), ys.max()
    cropped_img = image[y1:y2+1, x1:x2+1].copy()
    cropped_mask = mask[y1:y2+1, x1:x2+1]
    # Broadcast mask for 3 color channels
    cropped_img[~cropped_mask[..., None]] = 0
    return cropped_img, cropped_mask

def extract_color_hist(image, mask, bins=32):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([hsv], [0,1,2], mask.astype(np.uint8), [bins]*3, [0,180,0,256,0,256])
    cv2.normalize(hist, hist)
    return hist.flatten()

def load_masks_for_frame(mask_folder, frame_idx):
    mask_files = sorted(glob(os.path.join(mask_folder, f"mask_{frame_idx:04d}_*.png")))
    masks = []
    for mf in mask_files:
        m = cv2.imread(mf, cv2.IMREAD_GRAYSCALE)
        if m is None:
            continue
        masks.append(m > 128)
    return masks

def identify_and_save_unique_objects(video_path, mask_folder, frame_indices, distance_threshold=0.85, max_dim=480):
    descriptors = []
    object_ids = []
    unique_objects = {}

    for frame_idx in frame_indices:
        print(f"Processing frame {frame_idx}...")
        rgb_frame = load_downscaled_frame(video_path, frame_idx, max_dim)
        if rgb_frame is None:
            print(f"Failed to load frame {frame_idx}")
            continue
        masks = load_masks_for_frame(mask_folder, frame_idx)
        print(f"  Found {len(masks)} masks.")

        for mask in masks:
            crop, cropped_mask = crop_object(rgb_frame, mask)
            if crop is None:
                continue
            desc = extract_color_hist(crop, cropped_mask)

            if len(descriptors) == 0:
                unique_id = 0
                unique_objects[unique_id] = [(frame_idx, crop)]
                descriptors.append(desc)
                object_ids.append(unique_id)
                continue

            sims = cosine_similarity([desc], descriptors)[0]
            best_idx = np.argmax(sims)
            best_sim = sims[best_idx]

            if best_sim > distance_threshold:
                uid = object_ids[best_idx]
                unique_objects[uid].append((frame_idx, crop))
            else:
                uid = max(object_ids) + 1
                unique_objects[uid] = [(frame_idx, crop)]
                descriptors.append(desc)
                object_ids.append(uid)

    print(f"Identified {len(unique_objects)} unique objects.")
    save_dir = "unique_crops"
    os.makedirs(save_dir, exist_ok=True)
    for uid, crops in unique_objects.items():
        obj_dir = os.path.join(save_dir, f"object_{uid}")
        os.makedirs(obj_dir, exist_ok=True)
        for frame_i, crop_img in crops:
            save_path = os.path.join(obj_dir, f"frame{frame_i:04d}.png")
            cv2.imwrite(save_path, cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR))

    print(f"Cropped unique objects saved under '{save_dir}'.")

if __name__ == "__main__":
    video_path = "video.mp4"  # Replace with your video path
    mask_folder = "sam_output/masks"  # Must match your SAM output folder
    
    # You processed every 5 frames, get those frames indices from your SAM script
    frame_indices = list(range(0, 200, 5))  # Change 200 to max frame you processed
    
    identify_and_save_unique_objects(video_path, mask_folder, frame_indices)
