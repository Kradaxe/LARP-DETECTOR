from app.services.signal_extractor import extract_signals


async def process_text(text: str):

    signals = extract_signals(text)

    return {
        "raw_text": text,
        "signals": signals
    }