# processing/segmenter.py
# This file splits audio into small chunks for analysis
# We use recursion to keep splitting chunks that are still too long

import numpy as np
from config import SEGMENT_DURATION

def segment_audio(audio_data, sample_rate, chunk_duration=SEGMENT_DURATION):
    # Convert chunk duration from seconds to number of samples
    # Example: 3 seconds x 22050 samples per second = 66150 samples per chunk
    chunk_size = chunk_duration * sample_rate

    # Base case for recursion -- if audio is shorter than one chunk, return it as is
    if len(audio_data) <= chunk_size:
        return [audio_data]

    # Split the audio into a list of equal sized chunks
    chunks = split_into_chunks(audio_data, chunk_size)

    # Use recursion to check each chunk
    # If any chunk is still too long, split it again
    all_segments = []
    for chunk in chunks:
        if len(chunk) > chunk_size:
            # Recursively split this chunk further
            smaller_chunks = segment_audio(chunk, sample_rate, chunk_duration)
            all_segments.extend(smaller_chunks)
        else:
            # Chunk is small enough, add it directly
            all_segments.append(chunk)

    return all_segments

def split_into_chunks(audio_data, chunk_size):
    # Split audio array into equal sized pieces
    chunks = []
    start = 0

    while start < len(audio_data):
        # Take a slice of audio from start to start + chunk_size
        end = start + chunk_size
        chunk = audio_data[start:end]
        chunks.append(chunk)
        # Move start forward by chunk_size for next iteration
        start = end

    return chunks