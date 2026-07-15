import requests
from app.services.github_profile_service import analyze_github_profile


async def process_github(username: str):
    profile_data = requests.get(
        f"https://api.github.com/users/{username}"
    ).json()

    repos = requests.get(
        profile_data["repos_url"]
    ).json()

    return await analyze_github_profile(
        profile_data,
        repos
    )