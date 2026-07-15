'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import ScoreCard from '../../../components/ScoreCard';
import GitHubMetricsCard from '../../../components/GitHubMetricsCard';
import StrengthsWeaknesses from '../../../components/StrengthsWeaknesses';
import AnalysisSummary from '../../../components/AnalysisSummary';
import { GitHubAnalysisResponse } from '../../../types/analysis';

function GitHubResultsContent() {
  const searchParams = useSearchParams();
  const data = searchParams.get('data');

  if (!data) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-500">No GitHub analysis data found.</p>
        <Link href="/" className="text-indigo-600 hover:underline mt-4 inline-block">Go back</Link>
      </div>
    );
  }

  const result: GitHubAnalysisResponse = JSON.parse(decodeURIComponent(data));

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">GitHub Analysis</h1>
        <p className="text-slate-500 mt-2">Profile credibility for @{result.username}</p>
      </div>

      <div className="max-w-md mx-auto">
        <ScoreCard score={result.credibility_score} verdict={result.verdict} />
      </div>

      <GitHubMetricsCard
        username={result.username}
        basicMetrics={result.basic_metrics}
        engagementMetrics={result.engagement_metrics}
        languageMetrics={result.language_metrics}
        repositoryMetrics={result.repository_metrics}
        signalScores={result.signal_scores}
      />

      <StrengthsWeaknesses strengths={result.strengths} weaknesses={result.weaknesses} />

      <AnalysisSummary reasoning={result.reasoning} />

      <div className="text-center pt-4">
        <Link
          href="/"
          className="inline-block bg-indigo-600 text-white py-3 px-8 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
        >
          Analyze Another
        </Link>
      </div>
    </div>
  );
}

export default function GitHubResultsPage() {
  return (
    <main className="min-h-screen bg-slate-50 py-10 px-4">
      <Suspense fallback={<div className="text-center py-20 text-slate-500">Loading results...</div>}>
        <GitHubResultsContent />
      </Suspense>
    </main>
  );
}
