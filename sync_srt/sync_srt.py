from datetime import datetime, timedelta

def shift_time(time_str, shift_seconds):
    # Convert time string to datetime object
    time_format = "%H:%M:%S,%f"
    time_obj = datetime.strptime(time_str, time_format)

    # Add shift_seconds to the datetime object
    shifted_time = time_obj + timedelta(seconds=shift_seconds)

    # Format shifted_time back to the original format
    shifted_time_str = shifted_time.strftime(time_format)

    return shifted_time_str[:-3]  # Keep microseconds

def process_srt_file(filename, shift_seconds):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if ' --> ' in line:
            start_end = line.strip().split(' --> ')
            new_start = shift_time(start_end[0], shift_seconds)
            new_end = shift_time(start_end[1], shift_seconds)
            modified_line = f"{new_start} --> {new_end}\n"
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    # Write modified lines to a new .srt file
    output_filename = filename.replace('.srt', '_modified.srt')
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.writelines(modified_lines)

    print(f"Modified .srt file saved as: {output_filename}")

# Example usage:
if __name__ == "__main__":
    filename = 'SINKHOLE 2021 1080p Korean FHDRip HEVC x265 BONE.srt'  # Replace with your .srt file path
    shift_seconds = 8  # Number of seconds to add

    process_srt_file(filename, shift_seconds)