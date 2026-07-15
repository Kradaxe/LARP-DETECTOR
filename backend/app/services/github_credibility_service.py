from typing import Dict, List


class GitHubCredibilityService:
    """Generate credibility signals from GitHub metrics."""
    
    @staticmethod
    def generate_credibility_signals(metrics: Dict) -> Dict:
        """
        Generate credibility signals from calculated GitHub metrics.
        
        Args:
            metrics: Calculated metrics from GitHubMetricsService
        
        Returns:
            Dictionary containing credibility signals and scores
        """
        basic = metrics["basic_metrics"]
        engagement = metrics["engagement_metrics"]
        language = metrics["language_metrics"]
        repo = metrics["repository_metrics"]
        
        # Calculate individual signal scores
        activity_score = GitHubCredibilityService._score_activity(repo["recent_activity_score"])
        engagement_score = GitHubCredibilityService._score_engagement(
            engagement["total_stars"],
            engagement["total_forks"],
            engagement["avg_stars_per_repo"]
        )
        diversity_score = GitHubCredibilityService._score_diversity(
            language["language_diversity"],
            repo["original_repos"],
            repo["forked_repos"]
        )
        consistency_score = GitHubCredibilityService._score_consistency(
            basic["account_age_days"],
            basic["public_repos"],
            repo["avg_repo_size_kb"]
        )
        
        # Calculate overall credibility score
        overall_score = (
            activity_score * 0.25 +
            engagement_score * 0.30 +
            diversity_score * 0.25 +
            consistency_score * 0.20
        )
        
        # Generate strengths and weaknesses
        strengths = GitHubCredibilityService._generate_strengths(metrics)
        weaknesses = GitHubCredibilityService._generate_weaknesses(metrics)
        
        # Generate reasoning
        reasoning = GitHubCredibilityService._generate_reasoning(metrics, overall_score)
        
        return {
            "credibility_score": int(overall_score),
            "signal_scores": {
                "activity": activity_score,
                "engagement": engagement_score,
                "diversity": diversity_score,
                "consistency": consistency_score
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "reasoning": reasoning
        }
    
    @staticmethod
    def _score_activity(recent_activity_score: int) -> int:
        """Score based on recent activity."""
        if recent_activity_score >= 20:
            return 100
        elif recent_activity_score >= 10:
            return 75
        elif recent_activity_score >= 5:
            return 50
        elif recent_activity_score >= 1:
            return 25
        return 0
    
    @staticmethod
    def _score_engagement(total_stars: int, total_forks: int, avg_stars: float) -> int:
        """Score based on community engagement."""
        score = 0
        
        # Total stars contribution
        if total_stars >= 1000:
            score += 40
        elif total_stars >= 500:
            score += 30
        elif total_stars >= 100:
            score += 20
        elif total_stars >= 10:
            score += 10
        
        # Total forks contribution
        if total_forks >= 500:
            score += 30
        elif total_forks >= 100:
            score += 20
        elif total_forks >= 10:
            score += 10
        
        # Average stars per repo contribution
        if avg_stars >= 10:
            score += 30
        elif avg_stars >= 5:
            score += 20
        elif avg_stars >= 1:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _score_diversity(language_diversity: int, original_repos: int, forked_repos: int) -> int:
        """Score based on language diversity and original work."""
        score = 0
        
        # Language diversity
        if language_diversity >= 5:
            score += 40
        elif language_diversity >= 3:
            score += 30
        elif language_diversity >= 2:
            score += 20
        elif language_diversity >= 1:
            score += 10
        
        # Original vs forked ratio
        total_repos = original_repos + forked_repos
        if total_repos > 0:
            original_ratio = original_repos / total_repos
            if original_ratio >= 0.8:
                score += 40
            elif original_ratio >= 0.6:
                score += 30
            elif original_ratio >= 0.4:
                score += 20
            elif original_ratio >= 0.2:
                score += 10
        
        # Absolute original repo count
        if original_repos >= 20:
            score += 20
        elif original_repos >= 10:
            score += 15
        elif original_repos >= 5:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _score_consistency(account_age_days: int, public_repos: int, avg_size: float) -> int:
        """Score based on account consistency and repository quality."""
        score = 0
        
        # Account age
        if account_age_days >= 365 * 5:  # 5+ years
            score += 30
        elif account_age_days >= 365 * 3:  # 3+ years
            score += 25
        elif account_age_days >= 365:  # 1+ year
            score += 20
        elif account_age_days >= 180:  # 6+ months
            score += 10
        
        # Repository count consistency
        if public_repos >= 30:
            score += 30
        elif public_repos >= 15:
            score += 25
        elif public_repos >= 5:
            score += 20
        elif public_repos >= 1:
            score += 10
        
        # Average repository size (indicates substantial work)
        if avg_size >= 1000:  # 1MB+
            score += 40
        elif avg_size >= 500:  # 500KB+
            score += 30
        elif avg_size >= 100:  # 100KB+
            score += 20
        elif avg_size >= 10:  # 10KB+
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _generate_strengths(metrics: Dict) -> List[str]:
        """Generate list of strengths based on metrics."""
        strengths = []
        
        engagement = metrics["engagement_metrics"]
        if engagement["total_stars"] >= 100:
            strengths.append(f"Strong community engagement with {engagement['total_stars']} total stars")
        
        language = metrics["language_metrics"]
        if language["language_diversity"] >= 3:
            strengths.append(f"Diverse technical background across {language['language_diversity']} languages")
        
        repo = metrics["repository_metrics"]
        if repo["original_repos"] >= 10:
            strengths.append(f"Active contributor with {repo['original_repos']} original repositories")
        
        if repo["recent_activity_score"] >= 10:
            strengths.append("Consistently active with recent repository updates")
        
        basic = metrics["basic_metrics"]
        if basic["account_age_days"] >= 365:
            strengths.append(f"Established GitHub presence ({basic['account_age_days'] // 365}+ years)")
        
        return strengths if strengths else ["Active GitHub user"]
    
    @staticmethod
    def _generate_weaknesses(metrics: Dict) -> List[str]:
        """Generate list of weaknesses based on metrics."""
        weaknesses = []
        
        engagement = metrics["engagement_metrics"]
        if engagement["total_stars"] < 10:
            weaknesses.append("Limited community engagement (low star count)")
        
        language = metrics["language_metrics"]
        if language["language_diversity"] == 1:
            weaknesses.append("Limited language diversity")
        
        repo = metrics["repository_metrics"]
        if repo["original_repos"] < 3:
            weaknesses.append("Few original repositories (mostly forks)")
        
        if repo["recent_activity_score"] < 5:
            weaknesses.append("Low recent activity")
        
        basic = metrics["basic_metrics"]
        if basic["account_age_days"] < 180:
            weaknesses.append("Recently created account")
        
        return weaknesses if weaknesses else ["No significant weaknesses detected"]
    
    @staticmethod
    def _generate_reasoning(metrics: Dict, overall_score: int) -> str:
        """Generate reasoning for the overall credibility score."""
        basic = metrics["basic_metrics"]
        engagement = metrics["engagement_metrics"]
        language = metrics["language_metrics"]
        repo = metrics["repository_metrics"]
        
        reasoning_parts = []
        
        reasoning_parts.append(
            f"User has {basic['public_repos']} public repositories with "
            f"{engagement['total_stars']} total stars and {engagement['total_forks']} forks."
        )
        
        reasoning_parts.append(
            f"Profile shows {language['language_diversity']} different programming languages, "
            f"indicating {'high' if language['language_diversity'] >= 3 else 'moderate' if language['language_diversity'] >= 2 else 'limited'} "
            "technical diversity."
        )
        
        original_ratio = repo['original_repos'] / (repo['original_repos'] + repo['forked_repos']) if (repo['original_repos'] + repo['forked_repos']) > 0 else 0
        reasoning_parts.append(
            f"Repository composition is {original_ratio:.0%} original work, "
            f"showing {'strong' if original_ratio >= 0.7 else 'moderate' if original_ratio >= 0.4 else 'limited'} "
            "original contribution."
        )
        
        if overall_score >= 75:
            reasoning_parts.append("Overall profile demonstrates strong technical credibility and active community engagement.")
        elif overall_score >= 50:
            reasoning_parts.append("Overall profile shows moderate technical credibility with room for growth.")
        else:
            reasoning_parts.append("Overall profile shows limited technical credibility indicators.")
        
        return " ".join(reasoning_parts)
