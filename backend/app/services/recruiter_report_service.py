from typing import Dict, List, Optional
from app.services.verdict_service import verdict as get_verdict


class RecruiterReportService:
    """Generate recruiter-facing reports combining resume and GitHub analysis."""
    
    @staticmethod
    def generate_report(
        resume_analysis: Optional[Dict] = None,
        github_analysis: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a comprehensive recruiter report from resume and GitHub analysis.
        
        Args:
            resume_analysis: Output from resume analysis endpoint
            github_analysis: Output from GitHub analysis endpoint
        
        Returns:
            Dictionary containing recruiter-friendly report
        """
        # Extract scores
        resume_score = resume_analysis.get("overall_credibility_score", 0) if resume_analysis else 0
        github_score = github_analysis.get("credibility_score", 0) if github_analysis else 0
        
        # Calculate weighted overall score (resume weighted more heavily)
        if resume_analysis and github_analysis:
            weighted_overall = int(resume_score * 0.6 + github_score * 0.4)
        elif resume_analysis:
            weighted_overall = resume_score
        elif github_analysis:
            weighted_overall = github_score
        else:
            weighted_overall = 0
        
        # Get verdict
        verdict = get_verdict(weighted_overall)
        
        # Create credibility breakdown
        credibility_breakdown = RecruiterReportService._create_breakdown(
            resume_score, github_score, weighted_overall
        )
        
        # Aggregate suspicious claims
        suspicious_claims = RecruiterReportService._aggregate_suspicious_claims(
            resume_analysis, github_analysis
        )
        
        # Aggregate strengths
        strengths = RecruiterReportService._aggregate_strengths(
            resume_analysis, github_analysis
        )
        
        # Aggregate weaknesses
        weaknesses = RecruiterReportService._aggregate_weaknesses(
            resume_analysis, github_analysis
        )
        
        # Generate recruiter summary
        recruiter_summary = RecruiterReportService._generate_summary(
            weighted_overall, verdict, resume_analysis, github_analysis
        )
        
        # Generate recommendations
        recommendations = RecruiterReportService._generate_recommendations(
            weighted_overall, suspicious_claims, strengths, weaknesses
        )
        
        return {
            "overall_score": weighted_overall,
            "verdict": verdict,
            "credibility_breakdown": credibility_breakdown,
            "suspicious_claims": suspicious_claims,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recruiter_summary": recruiter_summary,
            "recommendations": recommendations
        }
    
    @staticmethod
    def _create_breakdown(resume_score: int, github_score: int, weighted_overall: int) -> Dict:
        """Create credibility breakdown with score distribution."""
        return {
            "resume_score": resume_score,
            "github_score": github_score,
            "weighted_overall": weighted_overall,
            "score_distribution": {
                "resume_contribution": int(resume_score * 0.6) if resume_score else 0,
                "github_contribution": int(github_score * 0.4) if github_score else 0
            }
        }
    
    @staticmethod
    def _aggregate_suspicious_claims(
        resume_analysis: Optional[Dict],
        github_analysis: Optional[Dict]
    ) -> List[str]:
        """Aggregate suspicious claims from both analyses."""
        suspicious_claims = []
        
        if resume_analysis:
            suspicious_claims.extend(resume_analysis.get("suspicious_claims", []))
        
        # Add GitHub-related suspicious indicators
        if github_analysis:
            github_score = github_analysis.get("credibility_score", 0)
            if github_score < 50:
                suspicious_claims.append(
                    f"GitHub profile shows low credibility ({github_score}/100)"
                )
            
            # Check for low activity
            repo_metrics = github_analysis.get("repository_metrics", {})
            if repo_metrics.get("recent_activity_score", 0) < 5:
                suspicious_claims.append("Low recent GitHub activity")
            
            # Check for high fork ratio
            original_repos = repo_metrics.get("original_repos", 0)
            forked_repos = repo_metrics.get("forked_repos", 0)
            total_repos = original_repos + forked_repos
            if total_repos > 0 and (forked_repos / total_repos) > 0.7:
                suspicious_claims.append("High ratio of forked repositories")
        
        return suspicious_claims
    
    @staticmethod
    def _aggregate_strengths(
        resume_analysis: Optional[Dict],
        github_analysis: Optional[Dict]
    ) -> List[str]:
        """Aggregate strengths from both analyses."""
        strengths = []
        
        if resume_analysis:
            strongest_claims = resume_analysis.get("strongest_claims", [])
            if strongest_claims:
                strengths.append(f"Strong technical claims: {len(strongest_claims)} high-credibility claims")
        
        if github_analysis:
            github_strengths = github_analysis.get("strengths", [])
            strengths.extend(github_strengths)
            
            # Add GitHub-specific strengths
            engagement = github_analysis.get("engagement_metrics", {})
            if engagement.get("total_stars", 0) >= 100:
                strengths.append(f"Strong GitHub presence with {engagement['total_stars']} stars")
            
            language = github_analysis.get("language_metrics", {})
            if language.get("language_diversity", 0) >= 3:
                strengths.append(f"Diverse technical stack: {language['language_diversity']} languages")
        
        return strengths if strengths else ["No significant strengths identified"]
    
    @staticmethod
    def _aggregate_weaknesses(
        resume_analysis: Optional[Dict],
        github_analysis: Optional[Dict]
    ) -> List[str]:
        """Aggregate weaknesses from both analyses."""
        weaknesses = []
        
        if github_analysis:
            github_weaknesses = github_analysis.get("weaknesses", [])
            weaknesses.extend(github_weaknesses)
        
        if resume_analysis:
            total_claims = resume_analysis.get("total_claims_analyzed", 0)
            suspicious_count = len(resume_analysis.get("suspicious_claims", []))
            
            if total_claims > 0 and (suspicious_count / total_claims) > 0.3:
                weaknesses.append(
                    f"High proportion of suspicious claims ({suspicious_count}/{total_claims})"
                )
        
        return weaknesses if weaknesses else ["No significant weaknesses identified"]
    
    @staticmethod
    def _generate_summary(
        overall_score: int,
        verdict: str,
        resume_analysis: Optional[Dict],
        github_analysis: Optional[Dict]
    ) -> str:
        """Generate a recruiter-friendly summary."""
        summary_parts = []
        
        # Overall assessment
        if overall_score >= 85:
            summary_parts.append("Candidate demonstrates strong technical credibility with verifiable claims and active GitHub presence.")
        elif overall_score >= 70:
            summary_parts.append("Candidate shows good technical credibility with some areas for verification.")
        elif overall_score >= 50:
            summary_parts.append("Candidate has moderate technical credibility; claims require careful verification.")
        else:
            summary_parts.append("Candidate shows low technical credibility; significant verification needed.")
        
        # Resume-specific summary
        if resume_analysis:
            total_claims = resume_analysis.get("total_claims_analyzed", 0)
            suspicious_count = len(resume_analysis.get("suspicious_claims", []))
            strongest_count = len(resume_analysis.get("strongest_claims", []))
            
            summary_parts.append(
                f"Resume analysis evaluated {total_claims} claims, "
                f"identifying {strongest_count} strong claims and {suspicious_count} suspicious claims."
            )
        
        # GitHub-specific summary
        if github_analysis:
            github_score = github_analysis.get("credibility_score", 0)
            username = github_analysis.get("username", "unknown")
            basic_metrics = github_analysis.get("basic_metrics", {})
            
            summary_parts.append(
                f"GitHub profile for '{username}' scored {github_score}/100 "
                f"with {basic_metrics.get('public_repos', 0)} public repositories "
                f"and {basic_metrics.get('followers', 0)} followers."
            )
        
        # Final recommendation
        if overall_score >= 75:
            summary_parts.append("Recommended for technical interviews with focused verification on key claims.")
        elif overall_score >= 50:
            summary_parts.append("Consider for technical interviews with thorough claim verification.")
        else:
            summary_parts.append("Proceed with caution; requires extensive verification and technical screening.")
        
        return " ".join(summary_parts)
    
    @staticmethod
    def _generate_recommendations(
        overall_score: int,
        suspicious_claims: List[str],
        strengths: List[str],
        weaknesses: List[str]
    ) -> List[str]:
        """Generate actionable recommendations for recruiters."""
        recommendations = []
        
        # Score-based recommendations
        if overall_score >= 85:
            recommendations.append("Focus technical interview on verifying strongest claims")
            recommendations.append("Consider candidate for senior or technical lead roles")
        elif overall_score >= 70:
            recommendations.append("Verify key technical claims during interview")
            recommendations.append("Assess practical skills through coding exercises")
        elif overall_score >= 50:
            recommendations.append("Conduct thorough technical verification")
            recommendations.append("Include practical coding assessment")
            recommendations.append("Verify GitHub contributions match resume claims")
        else:
            recommendations.append("Require extensive technical verification")
            recommendations.append("Consider additional screening before interview")
            recommendations.append("Verify all claims through practical assessment")
        
        # Suspicious claims recommendations
        if suspicious_claims:
            recommendations.append(f"Address {len(suspicious_claims)} suspicious claims during interview")
        
        # Strengths-based recommendations
        if len(strengths) >= 3:
            recommendations.append("Leverage candidate's diverse technical strengths")
        
        # Weaknesses-based recommendations
        if weaknesses:
            recommendations.append("Probe areas of concern during technical discussion")
        
        return recommendations
