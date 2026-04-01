# exceptions/custom.py
# This file defines all our custom exceptions
# Custom exceptions make error messages clear and specific
# Instead of a random crash, we get a meaningful error message

class UnsupportedFormatException(Exception):
    # Raised when user uploads a file that is not audio
    # Example: uploading a .pdf instead of a .wav
    pass

class CorruptAudioException(Exception):
    # Raised when the audio file exists but cannot be read
    # Example: a file that got damaged during upload
    pass

class NoVoiceDetectedException(Exception):
    # Raised when no human voice is found in the audio
    # Example: uploading a silent file or background noise only
    pass

class FileTooLargeException(Exception):
    # Raised when the uploaded file exceeds the size limit
    # Example: uploading a 1 hour long recording
    pass

class AudioTooShortException(Exception):
    # Raised when audio is too short to analyze properly
    # Example: a 0.5 second clip -- not enough to detect anything
    pass

class ModelPredictionException(Exception):
    # Raised when the ML model fails to make a prediction
    # Example: feature array has wrong shape
    pass

class DatabaseException(Exception):
    # Raised when something goes wrong saving to the database
    # Example: database file got corrupted
    pass