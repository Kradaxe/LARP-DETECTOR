BUZZWORDS = [
    "scalable",
    "robust",
    "production-ready",
    "enterprise-grade",
    "highly available",
    "distributed",
    "microservices",
    "real-time",
    "AI-powered",
    "state-of-the-art"
]


def analyze_buzzwords(text: str):

    found = []

    for word in BUZZWORDS:
        if word.lower() in text.lower():
            found.append(word)

    return {
        "count": len(found),
        "found": found
    }