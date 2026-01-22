import faiss
import numpy as np
import pandas as pd
from ml.embedding_model import get_embedding

dimension = 384
index = faiss.IndexFlatL2(dimension)
stored_texts = []

def load_past_projects(csv_path="data/past_projects.csv"):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        text = row["abstract"]
        emb = get_embedding(text)
        index.add(np.array([emb]))
        stored_texts.append(text)

def search_vector(embedding):
    if index.ntotal == 0:
        return 100  # no past data → full novelty
    D, I = index.search(np.array([embedding]), 1)
    return D[0][0]
