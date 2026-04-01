# config.py
# This file stores all settings used across the entire project
# Instead of hardcoding values everywhere, we store them here
# So if we need to change something, we change it in one place only

import os

# The folder where uploaded audio files will be saved
UPLOAD_FOLDER = "uploads"

# Only these audio formats are allowed
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg", "flac"}

# Each audio segment length in seconds
# We split audio into 3 second chunks for analysis
SEGMENT_DURATION = 3

# If fake probability is above this number, we call it FAKE
# 0.5 means 50% -- if model is more than 50% sure it's fake, we flag it
FAKE_THRESHOLD = 0.5

# Database file name -- SQLite stores everything in one file
DATABASE_NAME = "voiceguard.db"

# Flask secret key -- required for Flask to run securely
SECRET_KEY = "voiceguard_secret_key"

# Maximum audio file size -- 16 megabytes
MAX_FILE_SIZE_MB = 16