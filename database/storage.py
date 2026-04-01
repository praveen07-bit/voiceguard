# database/storage.py
# This file handles all database operations
# We use SQLite which is built into Python -- no extra setup needed
# Every detection result is saved here for future reference

import sqlite3
import os
from datetime import datetime
from config import DATABASE_NAME
from exceptions import DatabaseException

def create_tables():
    # This function creates the database tables if they don't exist yet
    # It runs every time the app starts -- safe to run multiple times
    try:
        # Connect to the SQLite database file
        # If the file doesn't exist, SQLite creates it automatically
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        # Create the uploads table -- stores info about every uploaded file
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_size_mb REAL,
                duration_seconds REAL,
                uploaded_at TEXT NOT NULL
            )
        """)

        # Create the detections table -- stores the analysis result
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upload_id INTEGER NOT NULL,
                verdict TEXT NOT NULL,
                confidence REAL NOT NULL,
                overall_fake_score REAL NOT NULL,
                total_segments INTEGER NOT NULL,
                fake_segments_count INTEGER NOT NULL,
                detected_at TEXT NOT NULL,
                FOREIGN KEY (upload_id) REFERENCES uploads (id)
            )
        """)

        # Save changes and close connection
        connection.commit()
        connection.close()

    except Exception as e:
        raise DatabaseException(f"Failed to create database tables: {str(e)}")

def save_upload(filename, file_size_mb, duration_seconds):
    # Save information about the uploaded file
    # Returns the ID of the saved record so we can link it to detection results
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        # Insert upload record with current timestamp
        cursor.execute("""
            INSERT INTO uploads (filename, file_size_mb, duration_seconds, uploaded_at)
            VALUES (?, ?, ?, ?)
        """, (filename, file_size_mb, duration_seconds, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Get the ID of the record we just inserted
        upload_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return upload_id

    except Exception as e:
        raise DatabaseException(f"Failed to save upload record: {str(e)}")

def save_detection(upload_id, result):
    # Save the detection result linked to the upload
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO detections (
                upload_id, verdict, confidence, overall_fake_score,
                total_segments, fake_segments_count, detected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            upload_id,
            result["verdict"],
            result["confidence"],
            result["overall_fake_score"],
            result["total_segments"],
            result["fake_segments_count"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()
        connection.close()

    except Exception as e:
        raise DatabaseException(f"Failed to save detection result: {str(e)}")

def get_all_detections():
    # Retrieve all past detections from the database
    # Used to show detection history on the web interface
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        # Join uploads and detections tables to get full information
        cursor.execute("""
            SELECT
                uploads.filename,
                uploads.duration_seconds,
                detections.verdict,
                detections.confidence,
                detections.total_segments,
                detections.fake_segments_count,
                detections.detected_at
            FROM detections
            JOIN uploads ON detections.upload_id = uploads.id
            ORDER BY detections.detected_at DESC
        """)

        # Fetch all rows and convert to list of dictionaries
        rows = cursor.fetchall()
        connection.close()

        detections = []
        for row in rows:
            detections.append({
                "filename": row[0],
                "duration": round(row[1], 1),
                "verdict": row[2],
                "confidence": row[3],
                "total_segments": row[4],
                "fake_segments_count": row[5],
                "detected_at": row[6]
            })

        return detections

    except Exception as e:
        raise DatabaseException(f"Failed to retrieve detections: {str(e)}")