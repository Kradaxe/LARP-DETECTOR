ARCHITECTURE_TERMS = [
    "load balancer",
    "redis",
    "kafka",
    "rabbitmq",
    "docker",
    "kubernetes",
    "nginx",
    "websocket",
    "microservices",
    "event driven",
    "pub sub",
    "queue"
]


def analyze_architecture(text: str):

    found = []

    for term in ARCHITECTURE_TERMS:
        if term.lower() in text.lower():
            found.append(term)

    return {
        "count": len(found),
        "found": found
    }