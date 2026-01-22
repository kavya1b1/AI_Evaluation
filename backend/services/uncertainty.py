import numpy as np

def estimate_confidence_band(predictions: list[float]):
    """
    Takes multiple model predictions and returns:
    mean, std, confidence interval
    """
    preds = np.array(predictions)

    mean_score = preds.mean()
    std_dev = preds.std()

    lower = max(0, mean_score - 1.96 * std_dev)
    upper = min(100, mean_score + 1.96 * std_dev)

    confidence = max(0, 100 - std_dev * 10)

    return {
        "mean": round(mean_score, 2),
        "std": round(std_dev, 2),
        "lower": round(lower, 2),
        "upper": round(upper, 2),
        "confidence": round(confidence, 2)
    }
