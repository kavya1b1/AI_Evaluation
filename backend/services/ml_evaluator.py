import numpy as np


def ml_evaluate_with_uncertainty(novelty_score, budget):
    """
    Simulated ML Ensemble Evaluation with randomness
    Returns multiple predictions for uncertainty estimation
    """

    predictions = []

    for _ in range(10):  # 10 ensemble samples
        score = (
            0.6 * novelty_score +
            0.4 * (100 - (budget / 1000000) * 10)
        )

        noise = np.random.normal(0, 3)
        predictions.append(score + noise)

    return predictions
