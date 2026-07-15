from typing import List
from app.services.analysis_service import analyze_text
from app.services.claim_splitter import ClaimSplitter
from app.services.verdict_service import verdict as get_verdict
from app.schemas.response_schema import ClaimAnalysis


class ResumeAnalysisService:
    """Service for analyzing resumes and calculating overall credibility."""
    
    @staticmethod
    async def analyze_resume(text: str) -> dict:
        """
        Analyze resume text by splitting into claims and evaluating each.
        
        Args:
            text: Extracted resume text
        
        Returns:
            Dictionary containing overall score, claim analyses, and categorized claims
        """
        # Split text into individual claims
        claims = ClaimSplitter.split_claims(text)
        
        if not claims:
            return {
                "overall_credibility_score": 0,
                "overall_verdict": "No Claims Found",
                "claim_analyses": [],
                "suspicious_claims": [],
                "strongest_claims": [],
                "total_claims_analyzed": 0
            }
        
        # Analyze each claim
        claim_analyses = []
        total_score = 0
        
        for claim in claims:
            try:
                result = await analyze_text(claim)
                
                claim_analysis = ClaimAnalysis(
                    claim=claim,
                    credibility_score=result["credibility_score"],
                    verdict=result["verdict"],
                    reasoning=result["reasoning"]
                )
                
                claim_analyses.append(claim_analysis)
                total_score += result["credibility_score"]
                
            except Exception as e:
                # If analysis fails for a claim, skip it but continue with others
                print(f"Failed to analyze claim: {claim[:50]}... Error: {str(e)}")
                continue
        
        # Calculate overall score (average of all claim scores)
        num_analyzed = len(claim_analyses)
        if num_analyzed > 0:
            overall_score = total_score // num_analyzed
        else:
            overall_score = 0
        
        overall_verdict = get_verdict(overall_score)
        
        # Categorize claims
        suspicious_claims = [
            ca.claim for ca in claim_analyses 
            if ca.credibility_score < 50
        ]
        
        strongest_claims = [
            ca.claim for ca in claim_analyses 
            if ca.credibility_score >= 75
        ]
        
        return {
            "overall_credibility_score": overall_score,
            "overall_verdict": overall_verdict,
            "claim_analyses": claim_analyses,
            "suspicious_claims": suspicious_claims,
            "strongest_claims": strongest_claims,
            "total_claims_analyzed": num_analyzed
        }
