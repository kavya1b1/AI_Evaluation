from backend.services.similarity_engine import compute_similarity


def novelty_analysis(proposal_text):
    novelty_score, top_matches = compute_similarity(proposal_text)

    return {
        "novelty_score": novelty_score,
        "similar_projects": top_matches
    }
