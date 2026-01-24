from backend.services.rule_engine import validate_budget


def check_finance(budget):
    """
    Budget is currently numeric input.
    Convert it into structured breakdown.
    """

    budget_data = {
        "total": budget,
        "equipment": budget * 0.25,
        "travel": budget * 0.05,
        "overhead": budget * 0.08,
        "duration": 2
    }

    score, violations = validate_budget(budget_data)

    return {
        "finance_score": score,
        "violations": violations
    }
