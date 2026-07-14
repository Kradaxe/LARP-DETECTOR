from github import Github
from app.config.settings import settings


github_client = Github(settings.GITHUB_TOKEN)


def get_user(username: str):
    return github_client.get_user(username)


def get_repositories(username: str):
    user = get_user(username)

    repos = []

    for repo in user.get_repos():
        repos.append(
            {
                "name": repo.name,
                "stars": repo.stargazers_count,
                "language": repo.language,
                "forks": repo.forks_count
            }
        )

    return repos