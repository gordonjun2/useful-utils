import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from utils import convert_text_to_pdf, convert_text_to_md, sys_msg, sys_msg_final_summary

load_dotenv()

file_path = "../speech_to_text/SISC_transcription.txt"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

chunk_size_in_token = 32000
chunk_size_in_len = chunk_size_in_token * 4

print(f"Reading text from: {file_path}")
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()
print(f"Successfully read text file. Total length: {len(text)} characters\n")

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size_in_len,
    chunk_overlap=chunk_size_in_len * 0.01,
    length_function=len,
    is_separator_regex=False,
)

# Split the text into chunks
print("Splitting text into chunks...")
chunks = text_splitter.split_text(text)
print(f"Text split into {len(chunks)} chunks")

# Process each chunk and collect responses
chunk_responses = []
print("\nProcessing chunks with LLM...\n")
for i, chunk in enumerate(chunks, 1):
    print(f"Processing chunk {i}/{len(chunks)}...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=sys_msg),
        contents=chunk)
    chunk_responses.append(response.text)
    print(f"✓ Chunk {i} processed successfully\n")

    # Sleep for 10 seconds between chunks
    time.sleep(10)

print("\nCombining all responses...\n")
# Combine all responses
combined_responses = "\n\n".join(chunk_responses)

print("Generating final summary...")
# Generate final summary
final_response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=sys_msg_final_summary),
    contents=combined_responses)

final_text = final_response.text
print("Final summary generated successfully.")

print("\nConverting output to MD and PDF formats...")
# Convert to MD and PDF
convert_text_to_md(final_text)
print("✓ Markdown file created")
convert_text_to_pdf(final_text)
print("✓ PDF file created")

print("\nDiscussion insight extraction completed successfully!")
