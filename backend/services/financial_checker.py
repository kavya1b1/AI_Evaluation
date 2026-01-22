def check_finance(budget):
    """
    Converts raw budget into a normalized financial score.
    Assumes optimal funding range is ₹5L – ₹25L
    """
    if budget <= 0:
        return 0

    if budget < 5_00_000:
        return 60  # underfunded risk
    elif budget <= 25_00_000:
        return 100  # optimal
    elif budget <= 50_00_000:
        return 75  # expensive but acceptable
    else:
        return 50  # high risk / low ROI
