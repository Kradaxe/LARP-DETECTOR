def get_verdict(score: int) -> str:
    if score >= 80:
        return "Highly Credible"

    if score >= 60:
        return "Likely Genuine"

    if score >= 40:
        return "Possibly Exaggerated"

    return "Potential LARP"