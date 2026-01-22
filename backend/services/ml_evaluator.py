import random

def ml_evaluate_with_uncertainty(novelty, budget):
    """
    Simulate multiple ML predictions (like ensemble models)
    """
    predictions = []

    for _ in range(20):  # ensemble simulation
        noise = random.uniform(-3, 3)
        score = (0.6 * novelty) + (0.4 * 100) + noise
        predictions.append(score)

    return predictions
