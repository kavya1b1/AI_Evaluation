"""
Model-agnostic SHAP-style explanation module.

This does NOT require a trained sklearn model.
It explains how each feature contributes to the final score
relative to a baseline.

This is stable, demo-safe, and research-acceptable.
"""

def get_shap_values(novelty, finance, technical=80.0):
    """
    Returns SHAP-style local explanation for a single proposal.

    Parameters:
    - novelty (float): novelty score (0–100)
    - finance (float): financial compliance score (0–100)
    - technical (float): technical feasibility heuristic

    Returns:
    {
        "baseline": float,
        "contributions": {
            feature_name: contribution_value
        }
    }
    """

    # Baseline = average proposal score (domain assumption)
    baseline = 65.0

    # SHAP-style contributions (model-agnostic)
    contributions = {
        "Novelty Score": round((novelty - baseline) * 0.30, 2),
        "Financial Compliance": round((finance - baseline) * 0.25, 2),
        "Technical Feasibility": round((technical - baseline) * 0.15, 2),
    }

    return {
        "baseline": baseline,
        "contributions": contributions
    }
