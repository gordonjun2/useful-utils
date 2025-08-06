# Remove Solid Background from Video

A Python utility that converts videos to transparent GIFs by intelligently removing solid-colored backgrounds. It uses advanced computer vision techniques for high-quality results, preserving edge details and textures while maintaining smooth transitions between frames.

## Features

- Interactive background color selection via mouse click
- Advanced color matching across multiple color spaces (BGR, LAB, HSV)
- Multi-scale texture and edge preservation
- Progressive noise removal and edge refinement
- Smart frame rate optimization for smooth animations
- Original color and contrast preservation in non-background regions
- Optimized GIF output with proper transparency handling

## Requirements

```
opencv-python
numpy
Pillow
```

## Installation

1. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your input video file in the same directory as the script
2. Run the script:
   ```bash
   python remove_background.py
   ```
3. When the preview window appears, click on the background color you want to remove
4. Press Enter to start the processing
5. Wait for the script to complete - it will create a transparent GIF with the same base name as your input video

## Input Requirements

- The input video should have a solid-colored background
- The video should be relatively stable (minimal camera movement)
- For best results, ensure good contrast between the subject and background
- Recommended video length: 2-30 seconds (longer videos will result in larger GIF files)

## Output

The script generates a transparent GIF with:

- Optimized frame rate (10-24 fps)
- Frame-by-frame transparency
- Preserved edge quality and texture details
- Original color accuracy in non-background regions

## Advanced Parameters

You can adjust these parameters in the script for fine-tuning:

- `tolerance` (default: 20): Controls how strictly to match the background color
- `min_distance` (default: 50): Minimum color difference to preserve
- `max_dimension` (default: 500): Maximum dimension for output size

## Example

Input: `serendip_mascots_welcome_short.mp4`
Output: `serendip_mascots_welcome_short_transparent.gif`

## Limitations

- Works best with solid-colored backgrounds
- May require parameter adjustments for optimal results with different videos
- Output GIF size depends on video length, resolution, and content complexity
- Processing time increases with video length and resolution
