def check_finance(total_budget: float):
    """
    Finance compliance rules based on MoC / CIL S&T Guidelines (simplified).
    """

    violations = []

    # Rule 1: Budget too high
    if total_budget > 2_00_00_000:  # ₹2 Crore limit
        violations.append("Budget exceeds maximum allowed limit (₹2 Cr).")

    # Rule 2: Budget too low
    if total_budget < 5_00_000:
        violations.append("Budget seems unrealistically low for an R&D proposal.")

    # Score calculation
    if len(violations) == 0:
        finance_score = 95
    elif len(violations) == 1:
        finance_score = 70
    else:
        finance_score = 40

    return {
        "finance_score": finance_score,
        "violations": violations
    }
