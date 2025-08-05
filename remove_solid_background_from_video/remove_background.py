import cv2
import numpy as np
from PIL import Image
import os

# Global variables for mouse callback
selected_color = None
clicked = False

def pick_color(event, x, y, flags, param):
    global selected_color, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_color = param[y, x]
        selected_color = bgr_color
        clicked = True
        print("🎨 Selected background color (BGR):", bgr_color)

def resize_frame(frame, max_dimension=500):
    height, width = frame.shape[:2]
    if max(height, width) <= max_dimension:
        return frame
    
    scale = max_dimension / float(max(height, width))
    new_width = int(width * scale)
    new_height = int(height * scale)
    return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

def create_background_mask(frame, bg_color, tolerance=30, min_distance=50):
    """Create a mask for background removal with enhanced texture and contrast preservation."""
    # Convert to float32 for accurate calculations
    frame_float = frame.astype(np.float32)
    bg_float = bg_color.astype(np.float32)
    
    # Calculate color difference in multiple color spaces for better accuracy
    # BGR difference
    diff_bgr = frame_float - bg_float
    color_distance_bgr = np.sqrt(np.sum(diff_bgr**2, axis=2))
    
    # LAB color space for perceptual color difference
    frame_lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    bg_lab = cv2.cvtColor(bg_color.reshape(1, 1, 3), cv2.COLOR_BGR2LAB)
    diff_lab = frame_lab.astype(np.float32) - bg_lab.astype(np.float32)
    color_distance_lab = np.sqrt(np.sum(diff_lab**2, axis=2))
    
    # HSV color space for better handling of color variations
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    bg_hsv = cv2.cvtColor(bg_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)
    diff_hsv = frame_hsv.astype(np.float32) - bg_hsv.astype(np.float32)
    color_distance_hsv = np.sqrt(np.sum(diff_hsv**2, axis=2))
    
    # Combine color distances with adjusted weights
    color_distance = (0.3 * color_distance_bgr + 0.3 * color_distance_lab + 0.4 * color_distance_hsv)
    
    # Create initial mask with increased tolerance
    mask = color_distance <= (tolerance * 1.2)
    
    # Calculate texture measure using local variance and gradient
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Multi-scale edge and texture detection
    textures = []
    edges = []
    
    # Multiple scales for Laplacian
    for ksize in [3, 5, 7]:
        texture = cv2.Laplacian(gray, cv2.CV_32F, ksize=ksize)
        textures.append(np.abs(texture))
    
    # Multiple scales for Sobel
    for ksize in [3, 5, 7]:
        sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=ksize)
        edge = np.sqrt(sobelx**2 + sobely**2)
        edges.append(edge)
    
    # Combine multi-scale information
    texture = np.maximum.reduce(textures)
    edge_magnitude = np.maximum.reduce(edges)
    
    # Weighted combination of texture and edge information
    texture_edge = 0.3 * texture + 0.7 * edge_magnitude
    
    # Protect areas with high texture or strong edges
    texture_threshold = np.percentile(texture_edge, 85)
    high_detail = texture_edge > texture_threshold
    
    # Calculate color distinctness with relaxed threshold
    color_distinctness = color_distance >= (min_distance * 0.85)
    
    # Combine masks with texture and edge protection
    mask = mask & ~color_distinctness & ~high_detail
    
    # Convert to uint8
    mask = (mask * 255).astype(np.uint8)
    
    # Multi-stage refinement process
    # 1. Progressive noise removal with multiple kernel sizes
    for kernel_size in [3, 5, 7]:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 2. Multi-scale edge refinement
    for kernel_size in [3, 5, 7]:
        kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernel_size, kernel_size))
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel_cross)
        mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel_cross)
    
    # 3. Remove small isolated blobs with increased threshold
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    min_blob_size = 200  # Further increased minimum blob size
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] < min_blob_size:
            mask[labels == i] = 0
    
    # Advanced multi-stage edge smoothing
    # 1. Initial strong Gaussian blur
    mask = cv2.GaussianBlur(mask, (9, 9), 2.0)
    
    # 2. Progressive bilateral filtering with multiple passes
    for _ in range(3):
        mask = cv2.bilateralFilter(mask, 9, 20, 20)
    
    # 3. Edge-preserving smoothing with larger kernel
    mask = cv2.medianBlur(mask, 7)
    
    # 4. Gaussian pyramid smoothing
    original_size = mask.shape[:2]
    mask_down = cv2.pyrDown(mask)
    mask_down = cv2.pyrDown(mask_down)
    mask_up = cv2.pyrUp(mask_down)
    mask_up = cv2.pyrUp(mask_up, dstsize=(original_size[1], original_size[0]))  # Specify target size
    
    # Blend original and pyramid smoothed masks
    mask = cv2.addWeighted(mask, 0.6, mask_up, 0.4, 0)
    
    # 5. Final refinement stages
    mask = cv2.GaussianBlur(mask, (7, 7), 1.5)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    mask = cv2.GaussianBlur(mask, (5, 5), 1.0)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    mask = cv2.GaussianBlur(mask, (3, 3), 0.8)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    
    return mask

def preserve_original_colors(frame, mask):
    """Preserve original colors and contrast of non-background regions."""
    # Convert to LAB color space for better color processing
    frame_lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Split channels
    l, a, b = cv2.split(frame_lab)
    
    # Apply CLAHE to L channel only where mask is not active
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l_enhanced = clahe.apply(l)
    
    # Blend original and enhanced L channel based on mask
    mask_float = mask.astype(float) / 255
    l_final = l * mask_float + l_enhanced * (1 - mask_float)
    
    # Merge channels back
    enhanced_lab = cv2.merge([l_final.astype(np.uint8), a, b])
    
    # Convert back to BGR
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

input_path = "serendip_mascots_welcome_short.mp4"
temp_dir = "temp_frames"
output_path = input_path.split(".")[0] + "_transparent.gif"

# Create temp directory
os.makedirs(temp_dir, exist_ok=True)

# Color matching parameters
tolerance = 20  # Reduced tolerance for less aggressive matching
min_distance = 50  # Minimum color distance to preserve

# Open video
cap = cv2.VideoCapture(input_path)
fps = cap.get(cv2.CAP_PROP_FPS)
# Adjust FPS for smoother GIF (between 10 and 24 fps)
target_fps = min(max(10, fps), 24)
frame_interval = int(fps / target_fps)

# Read first frame
ret, first_frame = cap.read()
if not ret:
    raise Exception("Cannot read video.")

# Resize first frame for preview
preview_frame = resize_frame(first_frame)

# Create window for color picking
cv2.namedWindow('Pick Background Color')
cv2.setMouseCallback('Pick Background Color', pick_color, preview_frame)

print("👆 Click on the background color you want to remove, then press 'Enter'")
while not clicked:
    cv2.imshow('Pick Background Color', preview_frame)
    if cv2.waitKey(1) == 13:  # Enter key
        break

cv2.destroyAllWindows()

if not clicked:
    raise Exception("No color selected!")

# Process frames
print("🎬 Processing frames...")
frame_count = 0
pil_frames = []
frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Process every nth frame for target FPS
    if frame_number % frame_interval != 0:
        frame_number += 1
        continue
        
    # Resize frame
    frame = resize_frame(frame)
    
    # Create mask with enhanced texture preservation
    mask = create_background_mask(frame, selected_color, tolerance, min_distance)
    
    # Preserve original colors and contrast
    frame = preserve_original_colors(frame, mask)
    
    # Create PIL Image with transparency
    rgba = np.zeros((frame.shape[0], frame.shape[1], 4), dtype=np.uint8)
    rgba[..., :3] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    rgba[..., 3] = cv2.bitwise_not(mask)  # Alpha channel
    
    # Convert to PIL Image
    pil_image = Image.fromarray(rgba)
    pil_frames.append(pil_image)
    
    frame_number += 1
    
    if frame_number % 10 == 0:
        print(f"Processed {frame_number} frames...")

cap.release()

# Save optimized GIF
print("🎨 Creating transparent GIF...")
duration = int(1000 / target_fps)  # Duration in milliseconds

# Save with PIL for better transparency handling
pil_frames[0].save(
    output_path,
    save_all=True,
    append_images=pil_frames[1:],
    duration=duration,
    loop=0,
    optimize=False,
    disposal=2  # Clear previous frame before rendering next frame
)

print("✅ Done! Transparent GIF saved to:", output_path)
print(f"\nℹ️  GIF Details:")
print(f"   - Frame Rate: {target_fps} fps")
print(f"   - Frame Count: {len(pil_frames)}")
print(f"   - Frame Interval: {duration}ms")
