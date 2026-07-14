from app.analyzers.technology_analyzer import analyze_technologies
from app.analyzers.metrics_analyzer import analyze_metrics
from app.analyzers.buzzword_analyzer import analyze_buzzwords
from app.analyzers.architecture_analyzer import analyze_architecture


def extract_signals(text: str):

    return {
        "technologies": analyze_technologies(text),
        "metrics": analyze_metrics(text),
        "buzzwords": analyze_buzzwords(text),
        "architecture": analyze_architecture(text)
    }