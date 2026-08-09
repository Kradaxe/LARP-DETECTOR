export interface AnalyzeResponse {
  credibility_score: number;
  verdict: string;
  specificity: number;
  technical_depth: number;
  evidence: number;
  implementation_detail: number;
  technologies_found: string[];
  strengths: string[];
  weaknesses: string[];
  interview_questions: string[];
  reasoning: string;
  analysis_id?: number;
}

export interface AnalyzeRequest {
  text: string;
}

export interface ClaimAnalysis {
  claim: string;
  credibility_score: number;
  verdict: string;
  reasoning: string;
}

export interface ResumeAnalysisResponse {
  overall_credibility_score: number;
  overall_verdict: string;
  claim_analyses: ClaimAnalysis[];
  suspicious_claims: string[];
  strongest_claims: string[];
  total_claims_analyzed: number;
  analysis_id?: number;
}

export interface GitHubAnalysisResponse {
  username: string;
  credibility_score: number;
  verdict: string;
  basic_metrics: Record<string, unknown>;
  engagement_metrics: Record<string, unknown>;
  language_metrics: Record<string, unknown>;
  repository_metrics: Record<string, unknown>;
  signal_scores: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  reasoning: string;
  analysis_id?: number;
}

export interface CredibilityBreakdown {
  resume_score: number;
  github_score: number;
  weighted_overall: number;
  score_distribution: Record<string, number>;
}

export interface RecruiterReportResponse {
  overall_score: number;
  verdict: string;
  credibility_breakdown: CredibilityBreakdown;
  suspicious_claims: string[];
  strengths: string[];
  weaknesses: string[];
  recruiter_summary: string;
  recommendations: string[];
}

export interface FeedbackRequest {
  analysis_id: number;
  recruiter_agreed: boolean;
  recruiter_comments?: string;
  recruiter_id?: string;
}

export type AnalysisTab = 'claim' | 'resume' | 'github' | 'linkedin-post' | 'report';

export interface LinkedInPostAnalysisResponse {
  post_url: string;
  credibility_score: number;
  verdict: string;
  post_content: {
    title: string;
    body: string;
    author: string;
    created_at: string;
    likes_count: number;
    comments_count: number;
  };
  technical_indicators: {
    code_blocks: number;
    technical_terms: string[];
    specific_details: string[];
  };
  credibility_signals: {
    specificity: number;
    technical_depth: number;
    evidence_quality: number;
    engagement_quality: number;
  };
  strengths: string[];
  weaknesses: string[];
  reasoning: string;
}
