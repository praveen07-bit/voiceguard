# features/extractor.py
# This file extracts multiple audio features from each segment
# We use feature fusion -- combining multiple features gives better accuracy
# Each feature captures a different characteristic of the voice

import numpy as np
import librosa
from exceptions import ModelPredictionException

def extract_features(audio_segment, sample_rate):
    # This function extracts 5 different features from one audio segment
    # and combines them into one single feature vector

    try:
        # Feature 1 -- MFCC (Mel Frequency Cepstral Coefficients)
        # Captures the tonal fingerprint of the voice
        # We extract 40 MFCC values and take the mean of each
        mfcc = librosa.feature.mfcc(y=audio_segment, sr=sample_rate, n_mfcc=40)
        mfcc_mean = np.mean(mfcc, axis=1)

        # Feature 2 -- Zero Crossing Rate
        # Counts how many times the audio signal crosses zero per second
        # AI voices have suspiciously consistent zero crossing patterns
        zcr = librosa.feature.zero_crossing_rate(audio_segment)
        zcr_mean = np.mean(zcr)

        # Feature 3 -- Spectral Rolloff
        # Measures where most of the audio energy is concentrated
        # Real voices spread energy naturally, AI voices concentrate it
        rolloff = librosa.feature.spectral_rolloff(y=audio_segment, sr=sample_rate)
        rolloff_mean = np.mean(rolloff)

        # Feature 4 -- RMS Energy
        # Measures loudness patterns over time
        # AI voices have unnaturally consistent energy levels
        rms = librosa.feature.rms(y=audio_segment)
        rms_mean = np.mean(rms)

        # Feature 5 -- Spectral Centroid
        # Measures the brightness of the voice
        # AI voices have different brightness patterns than real voices
        centroid = librosa.feature.spectral_centroid(y=audio_segment, sr=sample_rate)
        centroid_mean = np.mean(centroid)

        # Combine all features into one single array
        # This is called feature fusion
        extra_features = np.array([zcr_mean, rolloff_mean, rms_mean, centroid_mean])
        feature_vector = np.concatenate([mfcc_mean, extra_features])

        return feature_vector

    except Exception as e:
        raise ModelPredictionException(f"Failed to extract features: {str(e)}")

def extract_features_from_segments(segments, sample_rate):
    # Extract combined features from every segment
    # Returns a list of feature vectors -- one per segment
    all_features = []

    for segment in segments:
        # Only process segments that have enough audio data
        if len(segment) > 100:
            features = extract_features(segment, sample_rate)
            all_features.append(features)

    return all_features

# Keep this for backward compatibility
def extract_mfcc(audio_segment, sample_rate):
    return extract_features(audio_segment, sample_rate)