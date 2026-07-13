def calculate_score(
    specificity: int,
    technical_depth: int,
    evidence: int,
    implementation_detail: int,
    signals: dict
) -> int:

    score = (
        specificity * 0.25 +
        technical_depth * 0.30 +
        evidence * 0.25 +
        implementation_detail * 0.20
    ) * 10

    score += min(signals["technology_count"] * 2, 10)

    score += min(
        len(signals["action_verbs_found"]) * 2,
        10
    )

    score += min(
        len(signals["percentages_found"]) * 3,
        10
    )

    score += min(
        len(signals["latency_found"]) * 3,
        10
    )

    return min(round(score), 100)