import re

TECHNOLOGIES = [
    "python",
    "fastapi",
    "redis",
    "postgresql",
    "mongodb",
    "docker",
    "kubernetes",
    "kafka",
    "aws",
    "gcp",
    "react",
    "nextjs",
    "typescript",
    "nodejs",
    "tensorflow",
    "pytorch",
    "langchain",
    "rag"
]

ACTION_VERBS = [
    "built",
    "implemented",
    "designed",
    "optimized",
    "deployed",
    "reduced",
    "improved",
    "scaled",
    "developed",
    "integrated"
]


def extract_signals(text: str):
    lower_text = text.lower()

    technologies_found = [
        tech for tech in TECHNOLOGIES
        if tech in lower_text
    ]

    action_verbs_found = [
        verb for verb in ACTION_VERBS
        if verb in lower_text
    ]

    numbers_found = re.findall(r'\d+(?:\.\d+)?', text)

    percentages_found = re.findall(r'\d+(?:\.\d+)?%', text)

    latency_found = re.findall(
        r'\d+\s?(?:ms|milliseconds|seconds|sec)',
        lower_text
    )

    return {
        "technology_count": len(technologies_found),
        "technologies_found": technologies_found,
        "action_verbs_found": action_verbs_found,
        "numbers_found": numbers_found,
        "percentages_found": percentages_found,
        "latency_found": latency_found
    }