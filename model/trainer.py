import numpy as np
import pickle
import os
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

MODEL_PATH = "voiceguard_model.pkl"


def generate_training_data():
    num_samples = 500
    real_features = []
    for i in range(num_samples):
        mfcc = np.random.normal(loc=np.random.uniform(-10, 10, 40), scale=np.random.uniform(50, 80, 40))
        zcr = np.random.normal(loc=0.077, scale=0.015)
        rolloff = np.random.normal(loc=2700, scale=400)
        rms = np.random.normal(loc=0.049, scale=0.015)
        centroid = np.random.normal(loc=1500, scale=300)
        feature_vector = np.concatenate([mfcc, [zcr, rolloff, rms, centroid]])
        real_features.append(feature_vector)
    fake_features = []
    for i in range(num_samples):
        mfcc = np.random.normal(loc=np.random.uniform(-3, 3, 40), scale=np.random.uniform(5, 15, 40))
        zcr = np.random.normal(loc=0.03, scale=0.005)
        rolloff = np.random.normal(loc=1200, scale=150)
        rms = np.random.normal(loc=0.015, scale=0.004)
        centroid = np.random.normal(loc=700, scale=100)
        feature_vector = np.concatenate([mfcc, [zcr, rolloff, rms, centroid]])
        fake_features.append(feature_vector)
    X = np.array(real_features + fake_features)
    y = np.array([0] * num_samples + [1] * num_samples)
    return X, y


def train_model():
    print("Training VoiceGuard SVM model...")
    X, y = generate_training_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(probability=True, kernel="rbf", C=10.0, gamma="scale"))
    ])
    pipeline.fit(X_train, y_train)
    accuracy = pipeline.score(X_test, y_test)
    print(f"Model trained! Test accuracy: {accuracy * 100:.1f}%")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"Model saved to {MODEL_PATH}")
    return pipeline


def load_model():
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
        print("Old model deleted, retraining...")
    return train_model()