import requests
from app.services.github_profile_service import analyze_github_profile
from app.config.settings import settings


async def process_github(username: str):
    """
    Process GitHub username analysis with error handling.
    
    Args:
        username: GitHub username to analyze
    
    Returns:
        Dictionary containing GitHub analysis results
    
    Raises:
        ValueError: If user not found or API error occurs
    """
    # Prepare headers with optional GitHub token for higher rate limits
    headers = {}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"
    
    try:
        # Fetch profile data
        profile_response = requests.get(
            f"https://api.github.com/users/{username}",
            headers=headers
        )
        
        if profile_response.status_code == 404:
            raise ValueError(f"GitHub user '{username}' not found")
        
        if profile_response.status_code != 200:
            raise ValueError(f"GitHub API error: {profile_response.status_code}")
        
        profile_data = profile_response.json()
        
        # Fetch repositories
        repos_url = profile_data.get("repos_url")
        if not repos_url:
            raise ValueError("Could not fetch repositories URL from profile")
        
        repos_response = requests.get(repos_url, headers=headers)
        
        if repos_response.status_code != 200:
            raise ValueError(f"Failed to fetch repositories: {repos_response.status_code}")
        
        repos = repos_response.json()
        
        # Handle case where repos is not a list (API error)
        if not isinstance(repos, list):
            repos = []
        
        return await analyze_github_profile(profile_data, repos)
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error while fetching GitHub data: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing GitHub analysis: {str(e)}")