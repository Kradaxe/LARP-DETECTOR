def build_explanation(
    score,
    technologies,
    metrics,
    architecture
):

    explanation = []

    if technologies:
        explanation.append(
            f"Detected {len(technologies)} technologies."
        )

    if metrics:
        explanation.append(
            f"Detected {len(metrics)} measurable outcomes."
        )

    if architecture:
        explanation.append(
            f"Detected {len(architecture)} architecture concepts."
        )

    if score < 50:
        explanation.append(
            "Claims lack implementation detail."
        )

    return explanation