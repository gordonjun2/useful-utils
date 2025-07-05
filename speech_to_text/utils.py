import ssl
import urllib3
import requests
import difflib
import numpy as np
from huggingface_hub import configure_http_backend

ssl._create_default_https_context = ssl._create_unverified_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# [OPTIONAL] Use if there is SSL certificate verification issues
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session


configure_http_backend(backend_factory=backend_factory)


def chunk_audio_with_overlap(audio_array,
                             chunk_size_seconds=30,
                             overlap_seconds=3,
                             sample_rate=16000):
    """Split audio into overlapping chunks."""
    chunk_size = chunk_size_seconds * sample_rate
    overlap_size = overlap_seconds * sample_rate
    step = chunk_size - overlap_size

    chunks = []
    for i in range(0, len(audio_array), step):
        chunk = audio_array[i:i + chunk_size]
        if len(chunk) < chunk_size:
            chunk = np.pad(chunk, (0, chunk_size - len(chunk)))
        chunks.append(chunk)
    return chunks


def remove_overlap_text(prev_text,
                        curr_text,
                        window_words=20,
                        similarity_threshold=0.85):
    """
    Remove overlapping part from the start of curr_text that duplicates the end of prev_text,
    based on longest matching sequence of words.
    
    Args:
        prev_text (str): Previous chunk's full transcription.
        curr_text (str): Current chunk's full transcription.
        window_words (int): Number of words to consider at the overlap boundary.
        similarity_threshold (float): Minimum similarity to consider a match.
        
    Returns:
        str: Current chunk's transcription with overlapping start removed.
    """

    prev_words = prev_text.split()
    curr_words = curr_text.split()

    # Get last window_words from prev_text and first window_words from curr_text
    prev_tail = prev_words[-window_words:]
    curr_head = curr_words[:window_words]

    # Find longest matching sequence of words at the boundary
    # We'll try decreasing length sequences from window_words down to 1,
    # stopping at the longest matching sequence with similarity >= threshold.

    for overlap_len in range(window_words, 0, -1):
        prev_sub = prev_tail[-overlap_len:]
        curr_sub = curr_head[:overlap_len]

        # Compute similarity between word sequences (join to string and use difflib)
        prev_sub_str = " ".join(prev_sub)
        curr_sub_str = " ".join(curr_sub)
        ratio = difflib.SequenceMatcher(None, prev_sub_str,
                                        curr_sub_str).ratio()

        if ratio >= similarity_threshold:
            # Remove the overlapping words from the start of curr_text
            # Rejoin words skipping the overlap
            return " ".join(curr_words[overlap_len:]).lstrip()

    # No sufficient overlap found, return original curr_text
    return curr_text
