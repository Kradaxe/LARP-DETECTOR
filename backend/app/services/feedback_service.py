from app.db.database import SessionLocal
from app.models.feedback import Feedback
from app.models.analysis import Analysis
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class FeedbackService:
    """Service for managing recruiter feedback operations."""
    
    @staticmethod
    def create_feedback(
        analysis_id: int,
        recruiter_agreed: bool,
        recruiter_comments: Optional[str] = None,
        recruiter_id: Optional[str] = None
    ) -> Feedback:
        """
        Create a new feedback record.
        
        Args:
            analysis_id: ID of the analysis being rated
            recruiter_agreed: Whether the recruiter agrees with the score
            recruiter_comments: Optional comments from the recruiter
            recruiter_id: Optional identifier for the recruiter
        
        Returns:
            Created Feedback object
        """
        db = SessionLocal()
        try:
            # Verify analysis exists
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if not analysis:
                raise LookupError(f"Analysis with id {analysis_id} not found")
            
            feedback = Feedback(
                analysis_id=analysis_id,
                recruiter_agreed=recruiter_agreed,
                recruiter_comments=recruiter_comments,
                recruiter_id=recruiter_id,
                created_at=datetime.utcnow()
            )
            
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            
            return feedback
        except LookupError:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to create feedback: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def get_feedback_stats(days: int = 30) -> Dict:
        """
        Get feedback statistics for a given time period.
        
        Args:
            days: Number of days to look back (default: 30)
        
        Returns:
            Dictionary containing feedback statistics
        """
        db = SessionLocal()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Get all feedback in the time period
            feedback_records = db.query(Feedback).filter(
                Feedback.created_at >= cutoff_date
            ).all()
            
            total_feedback = len(feedback_records)
            agreed_count = sum(1 for f in feedback_records if f.recruiter_agreed)
            disagreed_count = total_feedback - agreed_count
            
            # Calculate agreement rate
            agreement_rate = (agreed_count / total_feedback * 100) if total_feedback > 0 else 0
            
            # Get feedback per recruiter
            recruiter_feedback = {}
            for feedback in feedback_records:
                if feedback.recruiter_id:
                    if feedback.recruiter_id not in recruiter_feedback:
                        recruiter_feedback[feedback.recruiter_id] = {"agreed": 0, "disagreed": 0}
                    if feedback.recruiter_agreed:
                        recruiter_feedback[feedback.recruiter_id]["agreed"] += 1
                    else:
                        recruiter_feedback[feedback.recruiter_id]["disagreed"] += 1
            
            return {
                "period_days": days,
                "total_feedback": total_feedback,
                "agreed_count": agreed_count,
                "disagreed_count": disagreed_count,
                "agreement_rate": round(agreement_rate, 2),
                "recruiter_breakdown": recruiter_feedback
            }
        except Exception as e:
            raise ValueError(f"Failed to get feedback stats: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def get_feedback_by_analysis(analysis_id: int) -> List[Feedback]:
        """
        Get all feedback for a specific analysis.
        
        Args:
            analysis_id: ID of the analysis
        
        Returns:
            List of Feedback objects
        """
        db = SessionLocal()
        try:
            feedback = db.query(Feedback).filter(
                Feedback.analysis_id == analysis_id
            ).all()
            return feedback
        except Exception as e:
            raise ValueError(f"Failed to get feedback: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def get_feedback_by_recruiter(recruiter_id: str, limit: int = 100) -> List[Feedback]:
        """
        Get all feedback from a specific recruiter.
        
        Args:
            recruiter_id: ID of the recruiter
            limit: Maximum number of records to return
        
        Returns:
            List of Feedback objects
        """
        db = SessionLocal()
        try:
            feedback = db.query(Feedback).filter(
                Feedback.recruiter_id == recruiter_id
            ).order_by(Feedback.created_at.desc()).limit(limit).all()
            return feedback
        except Exception as e:
            raise ValueError(f"Failed to get feedback: {str(e)}")
        finally:
            db.close()
