from typing import Dict, List, Set
from datetime import datetime, timedelta
from collections import Counter


class GitHubMetricsService:
    """Calculate comprehensive GitHub profile metrics."""
    
    @staticmethod
    def calculate_metrics(profile: Dict, repos: List[Dict]) -> Dict:
        """
        Calculate comprehensive GitHub metrics from profile and repository data.
        
        Args:
            profile: GitHub profile data from API
            repos: List of repository data from API
        
        Returns:
            Dictionary containing calculated metrics
        """
        # Basic metrics
        repo_count = len(repos)
        
        # Stars and forks
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos)
        
        # Language diversity
        languages: Set[str] = set()
        language_counts: Counter = Counter()
        
        for repo in repos:
            language = repo.get("language")
            if language:
                languages.add(language)
                language_counts[language] += 1
        
        language_diversity_score = len(languages)
        
        # Average repository size (in KB)
        sizes = [repo.get("size", 0) for repo in repos if repo.get("size", 0) > 0]
        avg_repo_size = sum(sizes) / len(sizes) if sizes else 0
        
        # Recent activity score (based on pushed_at dates)
        recent_activity_score = GitHubMetricsService._calculate_activity_score(repos)
        
        # Repository quality metrics
        original_repos = [repo for repo in repos if not repo.get("fork", False)]
        forked_repos = [repo for repo in repos if repo.get("fork", False)]
        
        # Average stars per repository
        avg_stars_per_repo = total_stars / repo_count if repo_count > 0 else 0
        
        # Average forks per repository  
        avg_forks_per_repo = total_forks / repo_count if repo_count > 0 else 0
        
        # Top languages
        top_languages = language_counts.most_common(5)
        
        # Account age
        account_age_days = GitHubMetricsService._calculate_account_age(profile)
        
        # Followers/following ratio
        followers = profile.get("followers", 0)
        following = profile.get("following", 0)
        follower_ratio = followers / following if following > 0 else followers
        
        return {
            "basic_metrics": {
                "public_repos": repo_count,
                "followers": followers,
                "following": following,
                "account_age_days": account_age_days,
                "follower_ratio": follower_ratio
            },
            "engagement_metrics": {
                "total_stars": total_stars,
                "total_forks": total_forks,
                "avg_stars_per_repo": round(avg_stars_per_repo, 2),
                "avg_forks_per_repo": round(avg_forks_per_repo, 2)
            },
            "language_metrics": {
                "language_diversity": language_diversity_score,
                "languages": list(languages),
                "top_languages": top_languages
            },
            "repository_metrics": {
                "original_repos": len(original_repos),
                "forked_repos": len(forked_repos),
                "avg_repo_size_kb": round(avg_repo_size, 2),
                "recent_activity_score": recent_activity_score
            }
        }
    
    @staticmethod
    def _calculate_activity_score(repos: List[Dict]) -> int:
        """Calculate recent activity score based on repository update dates."""
        if not repos:
            return 0
        
        six_months_ago = datetime.now() - timedelta(days=180)
        one_month_ago = datetime.now() - timedelta(days=30)
        one_week_ago = datetime.now() - timedelta(days=7)
        
        recent_activity = 0
        
        for repo in repos:
            pushed_at = repo.get("pushed_at")
            if not pushed_at:
                continue
            
            try:
                push_date = datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ")
                
                if push_date > one_week_ago:
                    recent_activity += 3
                elif push_date > one_month_ago:
                    recent_activity += 2
                elif push_date > six_months_ago:
                    recent_activity += 1
            except (ValueError, TypeError):
                continue
        
        return min(recent_activity, 100)  # Cap at 100
    
    @staticmethod
    def _calculate_account_age(profile: Dict) -> int:
        """Calculate account age in days."""
        created_at = profile.get("created_at")
        if not created_at:
            return 0
        
        try:
            created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            return (datetime.now() - created_date).days
        except (ValueError, TypeError):
            return 0
