from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example database of past funded projects
PAST_PROJECTS = [
    "AI-based crop disease detection using drone imagery",
    "Smart traffic optimization system using deep learning",
    "Healthcare chatbot for rural vaccination awareness",
    "IoT + AI energy monitoring for smart buildings",
    "Blockchain-based secure academic certificate verification"
]


def compute_similarity(proposal_text):
    """
    Computes similarity between proposal and past projects.
    Returns novelty score + top matching projects.
    """

    # Encode proposal + past projects
    proposal_embedding = model.encode(proposal_text, convert_to_tensor=True)
    past_embeddings = model.encode(PAST_PROJECTS, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.cos_sim(proposal_embedding, past_embeddings)[0]

    # Convert to numpy
    sim_scores = similarities.cpu().numpy()

    # Top 3 matches
    top_idx = np.argsort(sim_scores)[::-1][:3]

    top_matches = [
        {
            "project": PAST_PROJECTS[i],
            "similarity": float(sim_scores[i])
        }
        for i in top_idx
    ]

    # Novelty Score = inverse similarity
    max_similarity = float(sim_scores[top_idx[0]])
    novelty_score = round((1 - max_similarity) * 100, 2)

    return novelty_score, top_matches
