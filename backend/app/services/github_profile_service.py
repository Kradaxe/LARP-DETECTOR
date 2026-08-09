from app.services.github_metrics_service import GitHubMetricsService
from app.services.github_credibility_service import GitHubCredibilityService
from app.services.verdict_service import verdict as get_verdict
from app.services.persistence_service import save_analysis
from app.services.learning_service import LearningService


async def analyze_github_profile(profile: dict, repos: list) -> dict:
    """
    Analyze GitHub profile using comprehensive metrics and credibility signals.
    
    Args:
        profile: GitHub profile data from API
        repos: List of repository data from API
    
    Returns:
        Dictionary containing complete GitHub analysis
    """
    username = profile.get("login", "unknown")
    
    # Calculate comprehensive metrics
    metrics = GitHubMetricsService.calculate_metrics(profile, repos)
    
    # Generate credibility signals
    credibility = GitHubCredibilityService.generate_credibility_signals(metrics)
    
    # Get verdict based on credibility score
    verdict = get_verdict(credibility["credibility_score"])
    
    # Apply learning-based score adjustment
    adjusted_score = LearningService.get_score_adjustment(credibility["credibility_score"])
    learning_adjusted = adjusted_score != credibility["credibility_score"]
    
    # Save analysis to database
    analysis_id = save_analysis(
        text=f"GitHub profile analysis for {username}",
        score=credibility["credibility_score"],  # Store original score
        verdict=verdict,
        technologies=list(metrics.get("language_metrics", {}).get("languages", {}).keys()),
        reasoning=credibility["reasoning"]
    )
    
    return {
        "username": username,
        "credibility_score": adjusted_score,
        "original_score": credibility["credibility_score"],
        "learning_adjusted": learning_adjusted,
        "verdict": verdict,
        "basic_metrics": metrics["basic_metrics"],
        "engagement_metrics": metrics["engagement_metrics"],
        "language_metrics": metrics["language_metrics"],
        "repository_metrics": metrics["repository_metrics"],
        "signal_scores": credibility["signal_scores"],
        "strengths": credibility["strengths"],
        "weaknesses": credibility["weaknesses"],
        "reasoning": credibility["reasoning"],
        "analysis_id": analysis_id
    }