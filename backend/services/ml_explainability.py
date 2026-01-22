import joblib

FEATURE_NAMES = [
    "Semantic Novelty",
    "Proposal Length",
    "Technical Keyword Density",
    "Budget Utilization"
]

model = joblib.load("ml/evaluator_model.pkl")

def get_feature_importance():
    importances = model.feature_importances_
    return dict(zip(FEATURE_NAMES, importances))
