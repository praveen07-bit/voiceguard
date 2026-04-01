# This file makes exceptions/ a Python package
# It also imports all exceptions so they are easy to access
# Instead of writing: from exceptions.custom import CorruptAudioException
# We can write: from exceptions import CorruptAudioException

from exceptions.custom import (
    UnsupportedFormatException,
    CorruptAudioException,
    NoVoiceDetectedException,
    FileTooLargeException,
    AudioTooShortException,
    ModelPredictionException,
    DatabaseException
)