RECRUITER_SIGNALS = [
    "improved",
    "reduced",
    "increased",
    "latency",
    "throughput",
    "availability",
    "uptime",
    "cost reduction",
    "optimization",
    "deployed",
    "scaled",
    "migrated",
    "designed"
]


def analyze_recruiter_signals(text):

    found = []

    for signal in RECRUITER_SIGNALS:
        if signal.lower() in text.lower():
            found.append(signal)

    return {
        "count": len(found),
        "found": found
    }