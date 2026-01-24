import re


def extract_budget_from_text(proposal_text: str):
    """
    Extracts budget numbers written in ₹ or INR format from proposal text.

    Example Matches:
    ₹5,00,000
    INR 200000
    Rs. 3.5 lakh
    """

    budget_values = []

    # Pattern 1: ₹1,00,000 or ₹500000
    pattern_rupee = r"₹\s?[\d,]+"

    # Pattern 2: INR 500000
    pattern_inr = r"INR\s?[\d,]+"

    # Find matches
    matches = re.findall(pattern_rupee, proposal_text)
    matches += re.findall(pattern_inr, proposal_text)

    for m in matches:
        num = re.sub(r"[₹,INR\s]", "", m)
        if num.isdigit():
            budget_values.append(float(num))

    # If nothing found
    if not budget_values:
        return None

    # Return maximum budget found
    return max(budget_values)
