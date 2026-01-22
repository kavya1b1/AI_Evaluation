from ml.embedding_model import get_embedding
from ml.vector_store import search_vector

def novelty_score(proposal_text):
    emb = get_embedding(proposal_text)
    distance = search_vector(emb)
    return float(max(0, 100 - float(distance)))

