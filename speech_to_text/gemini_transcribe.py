import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

prompt = """Generate a transcript of the audio."""

client = genai.Client(api_key=GEMINI_API_KEY)

# path to the file to upload
file_path = "SISC.m4a"

# Upload the file to the File API
uploaded_file = client.files.upload(file=file_path)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt, uploaded_file],
)

print(response.text)
