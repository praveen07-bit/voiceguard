# main.py
# This is the entry point of the entire application
# It creates the Flask web app and connects all modules together
# Run this file to start the web server

import os
from flask import Flask, request, render_template, jsonify
from config import UPLOAD_FOLDER, SECRET_KEY
from processing import load_audio, validate_file, segment_audio
from features import extract_features_from_segments
from model import predict_audio
from database import create_tables, save_upload, save_detection, get_all_detections
from exceptions import (
    UnsupportedFormatException,
    CorruptAudioException,
    NoVoiceDetectedException,
    FileTooLargeException,
    AudioTooShortException,
    ModelPredictionException,
    DatabaseException
)

# Create the Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create database tables when app starts
create_tables()

# Make sure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    # This function runs when someone visits the home page
    # It loads all past detections from the database and shows them
    detections = get_all_detections()
    return render_template("index.html", detections=detections)

@app.route("/analyze", methods=["POST"])
def analyze():
    # This function runs when someone uploads an audio file
    # It goes through the full pipeline:
    # validate → load → segment → extract features → predict → save → return result

    try:
        # Step 1 -- Check if a file was actually uploaded
        if "audio_file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["audio_file"]

        # Check if the file has a name
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Step 2 -- Save the uploaded file to the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Step 3 -- Load and validate the audio file
        audio_data, sample_rate, duration = load_audio(file_path)

        # Step 4 -- Get file size in MB
        file_size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 2)

        # Step 5 -- Recursively split audio into segments
        segments = segment_audio(audio_data, sample_rate)

        # Step 6 -- Extract MFCC features from each segment
        all_features = extract_features_from_segments(segments, sample_rate)

        # Step 7 -- Run prediction on all features
        result = predict_audio(all_features)

        # Step 8 -- Save upload and detection result to database
        upload_id = save_upload(file.filename, file_size_mb, duration)
        save_detection(upload_id, result)

        # Step 9 -- Add file info to result and return it
        result["filename"] = file.filename
        result["duration"] = round(duration, 1)
        result["file_size_mb"] = file_size_mb

        return jsonify(result)

    except UnsupportedFormatException as e:
        return jsonify({"error": str(e)}), 400
    except FileTooLargeException as e:
        return jsonify({"error": str(e)}), 400
    except AudioTooShortException as e:
        return jsonify({"error": str(e)}), 400
    except CorruptAudioException as e:
        return jsonify({"error": str(e)}), 400
    except ModelPredictionException as e:
        return jsonify({"error": str(e)}), 500
    except DatabaseException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    # Start the Flask development server
    # debug=True means the server restarts automatically when you change code
    app.run(debug=True, port=5000)