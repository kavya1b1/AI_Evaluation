import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(proposal_text):

    # ✅ Correct path (data/past_projects.csv)
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(ROOT_DIR, "data", "past_projects.csv")

    df = pd.read_csv(csv_path)

    # Required column
    if "project" not in df.columns:
        raise ValueError("CSV must contain a 'project' column")

    if "url" not in df.columns:
        df["url"] = ""

    titles = df["project"].fillna("").tolist()

    documents = titles + [proposal_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    top_indices = similarities.argsort()[-5:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "project": df.iloc[idx]["project"],
            "similarity": float(similarities[idx]),
            "url": str(df.iloc[idx]["url"]) if not pd.isna(df.iloc[idx]["url"]) else ""
        })

    novelty_score = (1 - similarities.max()) * 100

    return novelty_score, results
