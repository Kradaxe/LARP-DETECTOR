def calculate_score(
    specificity,
    technical_depth,
    evidence,
    implementation_detail,
    technology_count,
    metrics_count,
    architecture_count
):

    score = (
        specificity * 0.25 +
        technical_depth * 0.30 +
        evidence * 0.25 +
        implementation_detail * 0.20
    ) * 10

    score += min(technology_count * 2, 10)
    score += min(metrics_count * 3, 10)
    score += min(architecture_count * 2, 10)

    return min(round(score), 100)