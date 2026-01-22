import numpy as np

def estimate_confidence_band(predictions):
    """
    predictions: list or numpy array of model scores
    """
    preds = np.array(predictions)

    mean = float(np.mean(preds))
    std = float(np.std(preds))

    # 95% confidence interval
    lower = max(0.0, mean - 1.96 * std)
    upper = min(100.0, mean + 1.96 * std)

    # Convert uncertainty to confidence (bounded)
    confidence = max(0.0, min(100.0, 100 - (std * 4)))

    return {
        "mean": round(mean, 2),
        "lower": round(lower, 2),
        "upper": round(upper, 2),
        "std": round(std, 2),
        "confidence": round(confidence, 2)
    }
