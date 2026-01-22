"""
Explainability Module
---------------------
Contains:
1. Human-readable explanation generation
2. ML feature importance extraction
"""

# ---------------- HUMAN EXPLANATION ----------------
def generate_explanation(novelty, finance, technical):
    explanation = []

    if novelty > 80:
        explanation.append(
            "The proposal demonstrates high novelty compared to past and ongoing projects."
        )
    else:
        explanation.append(
            "The proposal shows moderate novelty with some similarities to existing work."
        )

    if finance < 70:
        explanation.append(
        "The requested budget is relatively high compared to expected innovation impact, increasing financial risk."
    )
    else:
        explanation.append(
        "The budget is well-aligned with the proposed innovation scope and expected outcomes."
    )


    if technical >= 75:
        explanation.append(
            "The technical approach is feasible and well-structured."
        )
    else:
        explanation.append(
            "The technical approach may require further clarification or validation."
        )

    return explanation


# ---------------- ML FEATURE IMPORTANCE ----------------
def get_feature_importance():
    """
    Returns normalized feature importance values.
    These are static / mock values unless you attach them to a trained model.
    """

    return {
        "Novelty": 0.45,
        "Financial Compliance": 0.35,
        "Technical Feasibility": 0.20
    }
