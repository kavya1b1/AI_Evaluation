import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(proposal_text):
    """
    Computes similarity between uploaded proposal and past benchmark projects.
    Returns:
        novelty_score (float)
        top_matches (list)
    """

    # ---------------------------------------------------
    # ✅ Correct Path Handling
    # ---------------------------------------------------

    # Current file: backend/services/similarity_engine.py
    # BASE_DIR becomes: backend/
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Dataset is stored in: data/past_projects.csv
    csv_path = os.path.join(BASE_DIR, "..", "data", "past_projects.csv")

    # Normalize path
    csv_path = os.path.abspath(csv_path)

    # ---------------------------------------------------
    # ✅ Load CSV
    # ---------------------------------------------------
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"past_projects.csv not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    # ---------------------------------------------------
    # ✅ Ensure Required Columns
    # ---------------------------------------------------
    if "project" not in df.columns:
        raise ValueError("CSV must contain a 'project' column")

    # Optional URL column
    if "url" not in df.columns:
        df["url"] = ""

    # Fill missing values
    df["project"] = df["project"].fillna("")
    df["url"] = df["url"].fillna("")

    past_titles = df["project"].tolist()

    # ---------------------------------------------------
    # ✅ TF-IDF Similarity
    # ---------------------------------------------------
    documents = past_titles + [proposal_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    ).flatten()

    # ---------------------------------------------------
    # ✅ Top 5 Most Similar Papers
    # ---------------------------------------------------
    top_indices = similarities.argsort()[-5:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "project": df.iloc[idx]["project"],
            "similarity": round(float(similarities[idx]), 3),
            "url": df.iloc[idx]["url"]
        })

    # ---------------------------------------------------
    # ✅ Novelty Score Calculation
    # ---------------------------------------------------
    max_sim = similarities.max() if len(similarities) > 0 else 0.0

    novelty_score = round((1 - max_sim) * 100, 2)

    return novelty_score, results
