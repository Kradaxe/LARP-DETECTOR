import {
  AnalyzeResponse,
  FeedbackRequest,
  GitHubAnalysisResponse,
  LinkedInPostAnalysisResponse,
  RecruiterReportResponse,
  ResumeAnalysisResponse,
} from '../types/analysis';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function handleResponse<T>(response: Response, fallbackMessage: string): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail || fallbackMessage);
  }
  return response.json();
}

export async function analyzeText(text: string): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  return handleResponse(response, 'Failed to analyze text');
}

export async function analyzeResume(file: File): Promise<ResumeAnalysisResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/v1/resume/analyze`, {
    method: 'POST',
    body: formData,
  });
  return handleResponse(response, 'Failed to analyze resume');
}

export async function analyzeGitHub(username: string): Promise<GitHubAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/github/${encodeURIComponent(username)}`);
  return handleResponse(response, 'Failed to analyze GitHub profile');
}

export async function generateReport(
  resumeAnalysis?: ResumeAnalysisResponse,
  githubAnalysis?: GitHubAnalysisResponse
): Promise<RecruiterReportResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/report/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_analysis: resumeAnalysis ?? null,
      github_analysis: githubAnalysis ?? null,
    }),
  });
  return handleResponse(response, 'Failed to generate report');
}

export async function submitFeedback(feedback: FeedbackRequest): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(feedback),
  });
  return handleResponse(response, 'Failed to submit feedback');
}

export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`);
  return handleResponse(response, 'API is unreachable');
}

export async function analyzeLinkedInPost(postUrl: string): Promise<LinkedInPostAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/linkedin-post/analyze-linkedin-post`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ post_url: postUrl }),
  });
  return handleResponse(response, 'Failed to analyze LinkedIn post');
}
