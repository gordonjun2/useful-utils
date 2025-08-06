import subprocess
import sys
import os


def convert_mp4_to_webm_with_transparency(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + "_transparent.webm"

    # Complex filter chain to:
    # 1. Split video into background and foreground
    # 2. Apply colorkey to background and crop foreground
    # 3. Overlay foreground on keyed background
    command = [
        "ffmpeg",
        "-i",
        input_path,
        "-filter_complex",
        # 1. Split input into two: one for RGB processing, one for alpha extraction
        "split=2[fg][alpha_src];" +

        # 2. Remove black from alpha source using colorkey and extract alpha
        "[alpha_src]colorkey=black:0.4:0.2,format=yuva420p[ck];" +
        "[ck]alphaextract[alpha];" + "[alpha]erosion=1[alpha_eroded];" +

        # 3. Strip alpha to get RGB only for later merging
        "[ck]format=yuv420p[video_rgb];" +

        # 4. Merge cleaned alpha with RGB
        "[video_rgb][alpha_eroded]alphamerge[bg_cleaned];" +

        # 5. Crop the center rectangle from untouched input
        "[fg]crop=iw*0.6:ih*0.3:iw*0.2:ih*0.35[fg_center];" +

        # 6. Overlay the preserved center on cleaned background
        "[bg_cleaned][fg_center]overlay=x=(W-w)/2:y=(H-h)/2,format=yuva420p",
        "-c:v",
        "libvpx",
        "-pix_fmt",
        "yuva420p",
        "-auto-alt-ref",
        "0",
        "-y",
        output_path
    ]

    print("Running ffmpeg command:")
    print(" ".join(command))

    try:
        subprocess.run(command, check=True)
        print(f"✅ Conversion complete: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during conversion: {e}")


if __name__ == "__main__":
    convert_mp4_to_webm_with_transparency(
        "serendip_mascots_welcome_short_no_background.mp4")
