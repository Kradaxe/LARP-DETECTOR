def verdict(score: int):

    if score >= 85:
        return "Actually Legit 💯"

    if score >= 70:
        return "Probably Real (Maybe) 🤔"

    if score >= 50:
        return "Sketchy Vibes 🤨"

    return "Total LARP 🎭"