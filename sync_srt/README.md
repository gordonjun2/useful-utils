# SRT Subtitle Time Synchronizer

A Python script that helps synchronize subtitle timing in .srt files by shifting all timestamps by a specified number of seconds.

## Features

- Shifts all subtitle timestamps forward or backward
- Preserves the original subtitle formatting
- Creates a new file with modified timestamps
- Maintains millisecond precision
- Supports UTF-8 encoded subtitle files

## Usage

1. Place your .srt file in the same directory as the script
2. Modify the script parameters:
   ```python
   filename = 'your_subtitle_file.srt'  # Replace with your .srt file path
   shift_seconds = 8  # Number of seconds to shift (positive for forward, negative for backward)
   ```
3. Run the script:
   ```bash
   python sync_srt.py
   ```

## How it works

The script:

1. Reads the input .srt file
2. Identifies timestamp lines (containing " --> ")
3. Shifts both start and end times by the specified number of seconds
4. Creates a new file with "\_modified" suffix containing the adjusted timestamps

## Input Format

The script expects standard .srt format:

```
1
00:00:20,000 --> 00:00:24,400
Subtitle text here

2
00:00:24,600 --> 00:00:27,800
Next subtitle text
```

## Output

The script creates a new file with "\_modified" added to the original filename. For example:

- Input: `movie.srt`
- Output: `movie_modified.srt`

## Requirements

- Python 3.x
- No additional dependencies required
