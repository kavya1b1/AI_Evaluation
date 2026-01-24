# backend/services/rule_engine.py

def load_guidelines():
    """
    NaCCER / MoC S&T guideline constraints
    (can later be moved to YAML/JSON config)
    """
    return {
        "max_budget": 50000000,          # ₹5 Crore
        "overhead_limit": 0.10,          # 10%
        "equipment_limit": 0.30,         # 30%
        "travel_limit": 0.08,            # 8%
        "duration_max_years": 3
    }


def validate_budget(budget_breakdown):
    """
    Checks budget allocation against guideline caps.

    Input example:
    {
        "total": 40000000,
        "equipment": 12000000,
        "travel": 2000000,
        "overhead": 3000000,
        "duration": 2
    }
    """

    rules = load_guidelines()
    violations = []

    total = budget_breakdown["total"]

    # Rule 1: Max total cost
    if total > rules["max_budget"]:
        violations.append("Total budget exceeds maximum allowed limit.")

    # Rule 2: Overhead cap
    if budget_breakdown["overhead"] > rules["overhead_limit"] * total:
        violations.append("Overhead exceeds 10% guideline cap.")

    # Rule 3: Equipment cap
    if budget_breakdown["equipment"] > rules["equipment_limit"] * total:
        violations.append("Equipment cost exceeds 30% guideline cap.")

    # Rule 4: Travel cap
    if budget_breakdown["travel"] > rules["travel_limit"] * total:
        violations.append("Travel cost exceeds 8% guideline cap.")

    # Rule 5: Duration constraint
    if budget_breakdown["duration"] > rules["duration_max_years"]:
        violations.append("Project duration exceeds 3-year maximum allowed.")

    # Final compliance score
    compliance_score = max(0, 100 - len(violations) * 20)

    return compliance_score, violations
