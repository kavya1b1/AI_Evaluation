def generate_explanation(novelty, finance, technical):
    explanation = []

    if novelty > 85:
        explanation.append("Proposal shows high novelty compared to past and ongoing projects.")
    elif novelty > 60:
        explanation.append("Proposal has moderate novelty with some similarity to existing work.")
    else:
        explanation.append("Proposal shows significant overlap with existing projects.")

    if finance == 100:
        explanation.append("Budget complies fully with S&T funding guidelines.")
    else:
        explanation.append("Budget exceeds recommended limits and requires revision.")

    if technical >= 80:
        explanation.append("Technical approach is feasible and well-defined.")
    else:
        explanation.append("Technical feasibility needs further clarification.")

    return explanation
