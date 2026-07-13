export interface AnalyzeResponse {
  credibility_score: number;
  verdict: string;
  specificity: number;
  technical_depth: number;
  evidence: number;
  implementation_detail: number;
  technologies_found: string[];
  reasoning: string;
}

export interface AnalyzeRequest {
  text: string;
}
