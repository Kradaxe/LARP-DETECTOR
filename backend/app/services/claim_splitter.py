import re
from typing import List


class ClaimSplitter:
    """Split resume text into individual technical claims."""
    
    @staticmethod
    def split_claims(text: str) -> List[str]:
        """
        Split resume text into individual technical claims.
        
        This uses heuristics to identify bullet points, numbered lists,
        and sentence boundaries that likely represent separate claims.
        
        Args:
            text: Extracted resume text
        
        Returns:
            List of individual claim strings
        """
        # Clean up text
        text = text.strip()
        
        # Split by common bullet point patterns
        bullet_patterns = [
            r'[\n\r]+[•\-\*]\s+',  # Bullet points
            r'[\n\r]+\d+[\.|\)]\s+',  # Numbered lists
            r'[\n\r]+[a-z][\.\)]\s+',  # Lettered lists
        ]
        
        # First try to split by bullet points
        claims = []
        for pattern in bullet_patterns:
            if re.search(pattern, text):
                claims = re.split(pattern, text)
                break
        
        # If no bullet points found, split by sentences
        if not claims:
            # Split by sentence boundaries (period, exclamation, question mark)
            claims = re.split(r'(?<=[.!?])\s+', text)
        
        # Clean and filter claims
        cleaned_claims = []
        for claim in claims:
            claim = claim.strip()
            # Filter out very short claims and headers
            if len(claim) > 20 and not ClaimSplitter._is_header(claim):
                cleaned_claims.append(claim)
        
        return cleaned_claims
    
    @staticmethod
    def _is_header(text: str) -> bool:
        """Check if text is likely a section header."""
        header_indicators = [
            'experience',
            'education',
            'skills',
            'projects',
            'summary',
            'objective',
            'contact',
            'certifications',
            'achievements'
        ]
        
        text_lower = text.lower()
        for indicator in header_indicators:
            if indicator in text_lower and len(text) < 50:
                return True
        
        # All caps short text is likely a header
        if text.isupper() and len(text) < 30:
            return True
        
        return False
