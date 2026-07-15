from app.services.llm_service import generate
from app.services.scoring_service import calculate_score
from app.services.verdict_service import verdict


async def analyze_github_profile(profile, repos):

    repo_count = profile.get("public_repos", 0)

    stars = 0
    forks = 0
    languages = set()

    for repo in repos:
        stars += repo.get("stargazers_count", 0)
        forks += repo.get("forks_count", 0)

        language = repo.get("language")

        if language:
            languages.add(language)

    prompt = f"""
    Analyze this github profile.

    Repository Count: {repo_count}
    Total Stars: {stars}
    Total Forks: {forks}
    Languages: {list(languages)}

    Return JSON:

    {{
        "specificity": int,
        "technical_depth": int,
        "evidence": int,
        "implementation_detail": int,
        "strengths": [],
        "weaknesses": [],
        "reasoning": ""
    }}
    """

    result = await generate(prompt)

    return result