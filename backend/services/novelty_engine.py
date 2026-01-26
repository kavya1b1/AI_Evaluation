from backend.services.similarity_engine import compute_similarity


def novelty_analysis(proposal_text):

    if proposal_text.strip() == "":
        return {
            "novelty_score": 0.0,
            "similar_projects": []
        }

    novelty_score, top_matches = compute_similarity(proposal_text)

    if novelty_score != novelty_score:  # NaN check
        novelty_score = 0.0

    return {
        "novelty_score": float(novelty_score),
        "similar_projects": top_matches
    }
