def check_finance(budget):
    score = 100
    if budget > 5000000:
        score -= 30
    return score
