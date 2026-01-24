def check_finance(budget):
    violations = []
    score = 100

    if budget > 5000000:
        violations.append("Budget exceeds maximum allowed limit (₹50L).")
        score -= 30

    if budget < 100000:
        violations.append("Budget seems unrealistically low.")
        score -= 10

    return {
        "finance_score": score,
        "violations": violations
    }
