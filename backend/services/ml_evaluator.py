import numpy as np
from backend.services.financial_checker import check_finance

def ml_evaluate_with_uncertainty(novelty, budget):
    finance = check_finance(budget)

    # Weighted scoring (this is your core ML logic)
    base_score = (
        0.55 * novelty +
        0.30 * finance +
        0.15 * 80  # technical placeholder
    )

    # Monte Carlo uncertainty simulation
    predictions = [
        base_score + np.random.normal(0, 3)
        for _ in range(30)
    ]

    return predictions
