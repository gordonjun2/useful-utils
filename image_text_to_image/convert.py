from openai import OpenAI
import base64
from config import OPENAI_API_KEY
from PIL import Image
import os

client = OpenAI(api_key=OPENAI_API_KEY)

prompt = """generate a techno-orientalism (asian style in futuristic world) version of this image. the human must be replicated as close as possible (facial features). add some chinese architecture together with skyscrapers as well."""

# Open and convert image to RGBA
image = Image.open("anon_ninja.png")
rgba_image = image.convert("RGBA")

# Save image as temporary PNG file
temp_image_path = "temp_image.png"
rgba_image.save(temp_image_path, format="PNG")

# Create a transparent mask (0 = fully transparent, edit everything)
mask = Image.new("L", image.size, 0)

# Save mask as temporary PNG file
temp_mask_path = "temp_mask.png"
mask.save(temp_mask_path, format="PNG")

try:
    # Open the temporary file and send to API
    with open(temp_image_path, "rb") as image_file, open(temp_mask_path,
                                                         "rb") as mask_file:
        # For images.edit, we need both a mask and an image
        result = client.images.edit(model="dall-e-2",
                                    image=image_file,
                                    mask=mask_file,
                                    prompt=prompt,
                                    n=5,
                                    size="1024x1024")

    # Check if we got a valid response
    if result and result.data and len(result.data) > 0:
        print(f"Generated {len(result.data)} edited versions:")
        for i, image_data in enumerate(result.data):
            if hasattr(image_data, 'url'):
                print(f"Edited image {i+1} URL: {image_data.url}")
            elif hasattr(image_data, 'b64_json'):
                # Save each image with a unique name
                image_base64 = image_data.b64_json
                image_bytes = base64.b64decode(image_base64)
                output_filename = f"edited_anon_ninja_{i+1}.png"
                with open(output_filename, "wb") as f:
                    f.write(image_bytes)
                print(f"Edited image {i+1} saved as {output_filename}")
            else:
                print(f"Edited image {i+1}: Unexpected format")
    else:
        print("No image data received in the response")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print(f"Error type: {type(e)}")
    print(f"Full error details: {e.__dict__}")

finally:
    # Clean up temporary files
    for file in [temp_image_path, temp_mask_path]:
        if os.path.exists(file):
            os.remove(file)
