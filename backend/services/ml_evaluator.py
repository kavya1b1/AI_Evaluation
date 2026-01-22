import joblib
from backend.services.feature_extractor import extract_features

model = joblib.load("ml/evaluator_model.pkl")

def ml_evaluate(text, novelty, budget):
    features = extract_features(text, novelty, budget)
    score = model.predict(features)[0]
    return float(score)
