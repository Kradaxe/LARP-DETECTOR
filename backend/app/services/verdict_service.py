def verdict(score: int):

    if score >= 85:
        return "Highly Credible"

    if score >= 70:
        return "Likely Genuine"

    if score >= 50:
        return "Possibly Exaggerated"

    return "Potential LARP"