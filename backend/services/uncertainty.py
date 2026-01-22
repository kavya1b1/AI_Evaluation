import numpy as np
from backend.services.ml_evaluator import ml_evaluate

def estimate_confidence(text, novelty, budget, runs=20):
    scores = [
        ml_evaluate(text, novelty, budget) + np.random.normal(0, 1)
        for _ in range(runs)
    ]

    mean = np.mean(scores)
    std = np.std(scores)

    confidence = max(0, 100 - std * 5)
    return float(round(confidence, 2))
