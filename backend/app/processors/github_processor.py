from app.services.github_service import get_repositories


async def process_github(username: str):

    repos = get_repositories(username)

    total_stars = sum(
        repo["stars"]
        for repo in repos
    )

    languages = list(
        set(
            repo["language"]
            for repo in repos
            if repo["language"]
        )
    )

    return {
        "repository_count": len(repos),
        "total_stars": total_stars,
        "languages": languages,
        "repositories": repos
    }