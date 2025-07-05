import whisper
import whisperx
import time  # Add time module for timing
from utils import chunk_audio_with_overlap, remove_overlap_text

asr_model = "whisperx"  # whisperx, whisper
device = "cpu"  # changed from cuda to cpu
audio_file = "SISC Event 20250705 (Yuna).m4a"
compute_type = "float32"  # changed to float32 for CPU compatibility
chunk_size_seconds = 30  # adjust this value based on your needs
overlap_seconds = 3  # overlap between chunks
language = "en"  # specify language code: en, fr, de, es, it, ja, zh, etc.

# Load model and audio
if asr_model.lower() == "whisper":
    model = whisper.load_model("turbo", device)
    audio = whisper.load_audio(audio_file)
else:
    model = whisperx.load_model("medium", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)

# Chunk audio
audio_chunks = chunk_audio_with_overlap(audio, chunk_size_seconds,
                                        overlap_seconds)

# Process each chunk and collect transcriptions
prev_chunk_text = ""
all_transcriptions = []
total_processing_time = 0  # Track total processing time
print(f"\nProcessing audio file: {audio_file}")
print(f"Total chunks: {len(audio_chunks)} (with {overlap_seconds}s overlap)\n")
print("=" * 80)

for i, chunk in enumerate(audio_chunks):
    print(f"\nChunk {i+1}/{len(audio_chunks)}")
    print("-" * 40)

    # Start timing this chunk
    chunk_start_time = time.time()

    # Transcribe the chunk
    result = model.transcribe(chunk, language=language)

    # Keep only segments after chunk_start
    chunk_text = " ".join(segment["text"].strip()
                          for segment in result["segments"])

    # Remove overlap with previous chunk
    if prev_chunk_text:
        chunk_text = remove_overlap_text(prev_chunk_text, chunk_text)

    # Calculate and display time taken for this chunk
    chunk_time = time.time() - chunk_start_time
    total_processing_time += chunk_time
    print(f"Chunk: {chunk_text}\n")
    print(f"\nChunk processing time: {chunk_time:.2f} seconds")
    print(
        f"Average time per chunk so far: {(total_processing_time/(i+1)):.2f} seconds"
    )

    # Add to all transcriptions
    all_transcriptions.append(chunk_text)
    prev_chunk_text = chunk_text
    print("-" * 40)

# Print final timing statistics
print(f"\nTotal processing time: {total_processing_time:.2f} seconds")
print(
    f"Average time per chunk: {(total_processing_time/len(audio_chunks)):.2f} seconds"
)

# Combine all transcriptions
final_transcription = " ".join(all_transcriptions)

# Save to file
output_file = audio_file.split(".")[0] + "_transcription.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_transcription)

print("\n" + "=" * 80)
print(f"\nFull transcription saved to: {output_file}")
