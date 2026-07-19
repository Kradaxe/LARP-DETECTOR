import re
from typing import Dict, List, Any
from app.services.analysis_service import analyze_text

async def analyze_linkedin_post(post_url: str) -> Dict[str, Any]:
    """
    Analyze a LinkedIn post for technical credibility and potential LARPing.
    
    Note: This is a placeholder implementation. Actual LinkedIn post fetching
    requires LinkedIn API integration which needs authentication and permissions.
    """
    
    # Validate the URL
    if not is_valid_linkedin_url(post_url):
        raise ValueError("Invalid LinkedIn post URL")
    
    # TODO: Implement actual LinkedIn API integration
    # For now, we'll simulate the analysis with placeholder data
    # In production, you would:
    # 1. Use LinkedIn API to fetch post content
    # 2. Extract text, author, engagement metrics
    # 3. Analyze the content for technical credibility
    
    # Simulated post content (in production, this would come from LinkedIn API)
    post_content = {
        "title": "LinkedIn Post",
        "body": "This is a placeholder for actual LinkedIn post content. In production, this would be fetched using the LinkedIn API.",
        "author": "LinkedIn User",
        "created_at": "2024-01-01T00:00:00Z",
        "likes_count": 100,
        "comments_count": 25
    }
    
    # Combine title and body for analysis
    text_to_analyze = f"{post_content['title']}\n\n{post_content['body']}"
    
    # Use existing analysis service to evaluate credibility
    analysis_result = await analyze_text(text_to_analyze)
    
    # Extract technical indicators
    technical_indicators = extract_technical_indicators(text_to_analyze)
    
    # Calculate credibility signals
    credibility_signals = calculate_credibility_signals(
        post_content,
        technical_indicators,
        analysis_result
    )
    
    # Generate strengths and weaknesses
    strengths, weaknesses = generate_strengths_weaknesses(
        technical_indicators,
        credibility_signals
    )
    
    # Calculate overall credibility score
    credibility_score = calculate_overall_score(credibility_signals)
    
    # Generate verdict
    verdict = generate_verdict(credibility_score)
    
    # Generate reasoning
    reasoning = generate_reasoning(
        credibility_signals,
        technical_indicators,
        analysis_result
    )
    
    return {
        "post_url": post_url,
        "credibility_score": credibility_score,
        "verdict": verdict,
        "post_content": post_content,
        "technical_indicators": technical_indicators,
        "credibility_signals": credibility_signals,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "reasoning": reasoning
    }

def is_valid_linkedin_url(url: str) -> bool:
    """
    Validate if the URL is a valid LinkedIn post URL.
    """
    pattern = r'https?://(www\.)?linkedin\.com/(posts|feed/update)/.*'
    return bool(re.match(pattern, url))

def extract_technical_indicators(text: str) -> Dict[str, Any]:
    """
    Extract technical indicators from the post content.
    """
    # Count code blocks (markdown-style)
    code_blocks = len(re.findall(r'```', text)) // 2
    
    # Extract technical terms (common programming/tech terms)
    technical_terms = []
    tech_keywords = [
        'API', 'REST', 'GraphQL', 'SQL', 'NoSQL', 'Python', 'JavaScript',
        'React', 'Node.js', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
        'microservices', 'frontend', 'backend', 'database', 'algorithm',
        'machine learning', 'AI', 'cloud', 'DevOps', 'CI/CD'
    ]
    
    for keyword in tech_keywords:
        if keyword.lower() in text.lower():
            technical_terms.append(keyword)
    
    # Extract specific details (numbers, metrics, specific technologies)
    specific_details = []
    # Look for patterns like "10k requests", "99.9% uptime", etc.
    metric_patterns = [
        r'\d+k\s*(?:requests|users|downloads)',
        r'\d+\.?\d*%\s*(?:uptime|availability|accuracy)',
        r'\d+\s*(?:ms|seconds|minutes)\s*(?:latency|response time)'
    ]
    
    for pattern in metric_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        specific_details.extend(matches)
    
    return {
        "code_blocks": code_blocks,
        "technical_terms": technical_terms,
        "specific_details": specific_details
    }

def calculate_credibility_signals(
    post_content: Dict[str, Any],
    technical_indicators: Dict[str, Any],
    analysis_result: Dict[str, Any]
) -> Dict[str, float]:
    """
    Calculate various credibility signals from the post.
    """
    # Specificity: Based on technical terms and specific details
    specificity = min(1.0, (
        len(technical_indicators['technical_terms']) * 0.1 +
        len(technical_indicators['specific_details']) * 0.15 +
        (analysis_result.get('specificity', 0) * 0.3)
    ))
    
    # Technical depth: Based on code blocks and technical terms
    technical_depth = min(1.0, (
        technical_indicators['code_blocks'] * 0.2 +
        len(technical_indicators['technical_terms']) * 0.08 +
        (analysis_result.get('technical_depth', 0) * 0.3)
    ))
    
    # Evidence quality: Based on specific details and code blocks
    evidence_quality = min(1.0, (
        len(technical_indicators['specific_details']) * 0.2 +
        technical_indicators['code_blocks'] * 0.15 +
        (analysis_result.get('evidence', 0) * 0.3)
    ))
    
    # Engagement quality: Based on likes/comments ratio
    total_engagement = post_content.get('likes_count', 0) + post_content.get('comments_count', 0)
    engagement_quality = min(1.0, total_engagement / 1000)  # Normalize to 0-1
    
    return {
        "specificity": round(specificity, 2),
        "technical_depth": round(technical_depth, 2),
        "evidence_quality": round(evidence_quality, 2),
        "engagement_quality": round(engagement_quality, 2)
    }

def generate_strengths_weaknesses(
    technical_indicators: Dict[str, Any],
    credibility_signals: Dict[str, float]
) -> tuple[List[str], List[str]]:
    """
    Generate strengths and weaknesses based on the analysis.
    """
    strengths = []
    weaknesses = []
    
    # Strengths
    if technical_indicators['code_blocks'] > 0:
        strengths.append("Includes code examples")
    if len(technical_indicators['technical_terms']) > 3:
        strengths.append("Uses appropriate technical terminology")
    if len(technical_indicators['specific_details']) > 0:
        strengths.append("Provides specific metrics and details")
    if credibility_signals['technical_depth'] > 0.6:
        strengths.append("Shows good technical depth")
    
    # Weaknesses
    if technical_indicators['code_blocks'] == 0:
        weaknesses.append("Lacks code examples")
    if len(technical_indicators['technical_terms']) < 2:
        weaknesses.append("Limited technical terminology")
    if len(technical_indicators['specific_details']) == 0:
        weaknesses.append("No specific metrics or details provided")
    if credibility_signals['evidence_quality'] < 0.4:
        weaknesses.append("Low evidence quality")
    if credibility_signals['specificity'] < 0.4:
        weaknesses.append("Claims lack specificity")
    
    return strengths, weaknesses

def calculate_overall_score(credibility_signals: Dict[str, float]) -> int:
    """
    Calculate overall credibility score from individual signals.
    """
    weights = {
        "specificity": 0.3,
        "technical_depth": 0.3,
        "evidence_quality": 0.25,
        "engagement_quality": 0.15
    }
    
    weighted_score = sum(
        credibility_signals[signal] * weight 
        for signal, weight in weights.items()
    )
    
    return int(weighted_score * 100)

def generate_verdict(score: int) -> str:
    """
    Generate a verdict based on the credibility score.
    """
    if score >= 80:
        return "High Credibility"
    elif score >= 60:
        return "Moderate Credibility"
    elif score >= 40:
        return "Low Credibility"
    else:
        return "Very Low Credibility"

def generate_reasoning(
    credibility_signals: Dict[str, float],
    technical_indicators: Dict[str, Any],
    analysis_result: Dict[str, Any]
) -> str:
    """
    Generate a reasoning explanation for the credibility assessment.
    """
    reasoning_parts = []
    
    # Specificity reasoning
    if credibility_signals['specificity'] > 0.7:
        reasoning_parts.append("The post shows high specificity with detailed claims.")
    elif credibility_signals['specificity'] > 0.4:
        reasoning_parts.append("The post has moderate specificity with some detailed claims.")
    else:
        reasoning_parts.append("The post lacks specificity with vague claims.")
    
    # Technical depth reasoning
    if credibility_signals['technical_depth'] > 0.7:
        reasoning_parts.append("Strong technical depth demonstrated through terminology and concepts.")
    elif credibility_signals['technical_depth'] > 0.4:
        reasoning_parts.append("Moderate technical depth with basic technical concepts.")
    else:
        reasoning_parts.append("Limited technical depth with minimal technical content.")
    
    # Evidence reasoning
    if credibility_signals['evidence_quality'] > 0.7:
        reasoning_parts.append("Good evidence quality with specific metrics and examples.")
    elif credibility_signals['evidence_quality'] > 0.4:
        reasoning_parts.append("Moderate evidence quality with some supporting details.")
    else:
        reasoning_parts.append("Poor evidence quality lacking supporting details.")
    
    return " ".join(reasoning_parts)
