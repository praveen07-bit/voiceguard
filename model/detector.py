# model/detector.py
import numpy as np
from exceptions import ModelPredictionException
from config import FAKE_THRESHOLD

# Global variable to hold the model
svm_model = None

def get_model():
    # Load model only when needed
    # This avoids circular import issues
    global svm_model
    if svm_model is None:
        from model.trainer import load_model
        svm_model = load_model()
    return svm_model

def predict_segment(features):
    # Predict whether a single audio segment is real or fake
    try:
        # Get the model
        model = get_model()

        # Reshape features for sklearn -- needs 2D array
        feature_array = np.array(features).reshape(1, -1)

        # Get probability scores from SVM
        probabilities = model.predict_proba(feature_array)[0]

        fake_score = float(probabilities[1])
        real_score = float(probabilities[0])

        is_fake = fake_score > FAKE_THRESHOLD
        verdict = "FAKE" if is_fake else "REAL"

        return {
            "verdict": verdict,
            "fake_score": round(fake_score, 4),
            "confidence": round(fake_score * 100 if is_fake else real_score * 100, 1)
        }

    except Exception as e:
        raise ModelPredictionException(f"Prediction failed: {str(e)}")

def predict_audio(all_features):
    # Run prediction on all segments and combine into final result
    if not all_features:
        raise ModelPredictionException("No features to analyze")

    segment_results = []
    fake_scores = []

    for i, features in enumerate(all_features):
        result = predict_segment(features)
        result["segment_number"] = i + 1
        segment_results.append(result)
        fake_scores.append(result["fake_score"])

    overall_fake_score = float(round(np.mean(fake_scores), 4))
    is_fake = overall_fake_score > FAKE_THRESHOLD
    fake_segments = [r for r in segment_results if r["verdict"] == "FAKE"]

    return {
        "verdict": "FAKE" if is_fake else "REAL",
        "confidence": float(round(
            overall_fake_score * 100 if is_fake else (1 - overall_fake_score) * 100, 1
        )),
        "overall_fake_score": overall_fake_score,
        "total_segments": len(segment_results),
        "fake_segments_count": len(fake_segments),
        "segment_results": segment_results
    }