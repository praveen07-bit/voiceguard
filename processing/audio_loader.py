# processing/audio_loader.py
# This file is responsible for loading and validating audio files
# Before we analyze anything, we make sure the file is valid and readable

import librosa
import os
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from exceptions import UnsupportedFormatException, CorruptAudioException, FileTooLargeException, AudioTooShortException

def validate_file(file_path):
    # Check if the file actually exists on disk
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check if the file format is allowed
    # We split the filename by dot and take the last part (the extension)
    extension = file_path.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise UnsupportedFormatException(f"{extension} is not a supported format. Use wav, mp3, ogg or flac")

    # Check if the file size is within the allowed limit
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise FileTooLargeException(f"File is {file_size_mb:.1f}MB. Maximum allowed is {MAX_FILE_SIZE_MB}MB")

def load_audio(file_path):
    # First validate the file before trying to load it
    validate_file(file_path)

    try:
        # librosa.load reads the audio file and returns:
        # audio_data -- the actual sound as numbers
        # sample_rate -- how many samples per second (usually 22050)
        audio_data, sample_rate = librosa.load(file_path, sr=22050)
    except Exception:
        raise CorruptAudioException(f"Could not read audio file: {file_path}. File may be corrupt")

    # Calculate how long the audio is in seconds
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    # Audio must be at least 1 second long to analyze
    if duration < 1.0:
        raise AudioTooShortException(f"Audio is only {duration:.1f} seconds. Minimum is 1 second")

    return audio_data, sample_rate, duration