def final_score(novelty, finance, technical):
    return round(
        novelty * 0.4 +
        finance * 0.3 +
        technical * 0.3, 2
    )
