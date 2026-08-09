from app.db.database import SessionLocal
from app.models.feedback import Feedback
from app.models.analysis import Analysis
from typing import Dict, Optional
from datetime import datetime, timedelta


class LearningService:
    """Service for learning from feedback to improve scoring."""
    
    @staticmethod
    def get_feedback_patterns(analysis_id: Optional[int] = None, days: int = 30) -> Dict:
        """
        Analyze feedback patterns to identify systematic scoring issues.
        
        Args:
            analysis_id: Optional specific analysis to analyze
            days: Number of days to look back
        
        Returns:
            Dictionary with learning insights
        """
        db = SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Get feedback records
            if analysis_id:
                feedback_records = db.query(Feedback).filter(
                    Feedback.analysis_id == analysis_id
                ).all()
            else:
                feedback_records = db.query(Feedback).filter(
                    Feedback.created_at >= cutoff_date
                ).all()
            
            if not feedback_records:
                return {"message": "No feedback data available for learning"}
            
            # Calculate feedback statistics
            total = len(feedback_records)
            agreed = sum(1 for f in feedback_records if f.recruiter_agreed)
            disagreed = total - agreed
            
            # Get associated analyses to find patterns
            analysis_ids = [f.analysis_id for f in feedback_records]
            analyses = db.query(Analysis).filter(Analysis.id.in_(analysis_ids)).all()
            
            # Calculate average scores for agreed vs disagreed
            agreed_scores = [a.credibility_score for a in analyses if 
                           any(f.analysis_id == a.id and f.recruiter_agreed for f in feedback_records)]
            disagreed_scores = [a.credibility_score for a in analyses if 
                              any(f.analysis_id == a.id and not f.recruiter_agreed for f in feedback_records)]
            
            avg_agreed_score = sum(agreed_scores) / len(agreed_scores) if agreed_scores else 0
            avg_disagreed_score = sum(disagreed_scores) / len(disagreed_scores) if disagreed_scores else 0
            
            # Learning insights
            insights = {
                "total_feedback": total,
                "agreement_rate": round((agreed / total) * 100, 2) if total > 0 else 0,
                "avg_agreed_score": round(avg_agreed_score, 2),
                "avg_disagreed_score": round(avg_disagreed_score, 2),
                "score_bias": round(avg_agreed_score - avg_disagreed_score, 2),
                "recommendations": []
            }
            
            # Generate recommendations
            if insights["agreement_rate"] < 70:
                insights["recommendations"].append(
                    "Low agreement rate - consider recalibrating scoring thresholds"
                )
            
            if insights["score_bias"] > 10:
                insights["recommendations"].append(
                    "System is too harsh - recruiters consistently disagree with low scores"
                )
            elif insights["score_bias"] < -10:
                insights["recommendations"].append(
                    "System is too lenient - recruiters consistently disagree with high scores"
                )
            
            if not insights["recommendations"]:
                insights["recommendations"].append("Scoring is well-calibrated - continue monitoring")
            
            return insights
            
        except Exception as e:
            return {"error": f"Failed to analyze feedback patterns: {str(e)}"}
        finally:
            db.close()
    
    @staticmethod
    def get_score_adjustment(score: int) -> int:
        """
        Get dynamic score adjustment based on learning.
        
        Args:
            score: Original credibility score
        
        Returns:
            Adjusted score with learning bias applied
        """
        # Get recent feedback patterns
        patterns = LearningService.get_feedback_patterns(days=30)
        
        if "error" in patterns or "message" in patterns:
            return score  # No adjustment if no data
        
        # Apply bias correction
        bias = patterns.get("score_bias", 0)
        
        # Apply adjustment (capped at ±5 points)
        adjustment = max(-5, min(5, bias))
        adjusted_score = max(0, min(100, score + adjustment))
        
        return adjusted_score