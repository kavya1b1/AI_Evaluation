import numpy as np

TECH_KEYWORDS = [
    "algorithm", "model", "system", "framework",
    "optimization", "prediction", "deep learning",
    "machine learning", "iot", "automation"
]

def extract_features(text, novelty, budget):
    text_lower = text.lower()

    keyword_hits = sum(1 for k in TECH_KEYWORDS if k in text_lower)
    keyword_density = keyword_hits / len(TECH_KEYWORDS)

    features = np.array([
        novelty / 100,                 # semantic novelty
        len(text) / 5000,              # normalized length
        keyword_density,               # technical richness
        min(budget / 5_000_000, 1.0)   # normalized budget
    ])

    return features.reshape(1, -1)
