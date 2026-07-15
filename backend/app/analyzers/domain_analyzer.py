DOMAINS = {
    "backend": [
        "redis",
        "postgres",
        "kafka",
        "rabbitmq"
    ],
    "frontend": [
        "react",
        "nextjs",
        "tailwind"
    ],
    "ml": [
        "transformers",
        "rag",
        "embedding",
        "vector database"
    ]
}


def detect_domain(text):

    results = {}

    for domain, keywords in DOMAINS.items():
        count = 0

        for keyword in keywords:
            if keyword.lower() in text.lower():
                count += 1

        results[domain] = count

    return results