'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import ScoreCard from '../../../components/ScoreCard';
import ClaimAnalysisList from '../../../components/ClaimAnalysisList';
import { ResumeAnalysisResponse } from '../../../types/analysis';

function ResumeResultsContent() {
  const searchParams = useSearchParams();
  const data = searchParams.get('data');

  if (!data) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-500">No resume analysis data found.</p>
        <Link href="/" className="text-indigo-600 hover:underline mt-4 inline-block">Go back</Link>
      </div>
    );
  }

  const result: ResumeAnalysisResponse = JSON.parse(decodeURIComponent(data));

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">Resume Analysis</h1>
        <p className="text-slate-500 mt-2">
          {result.total_claims_analyzed} technical claims analyzed
        </p>
      </div>

      <div className="max-w-md mx-auto">
        <ScoreCard
          score={result.overall_credibility_score}
          verdict={result.overall_verdict}
          subtitle="Overall Resume Score"
        />
      </div>

      <ClaimAnalysisList
        claims={result.claim_analyses}
        suspiciousClaims={result.suspicious_claims}
        strongestClaims={result.strongest_claims}
      />

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

export default function ResumeResultsPage() {
  return (
    <main className="min-h-screen bg-slate-50 py-10 px-4">
      <Suspense fallback={<div className="text-center py-20 text-slate-500">Loading results...</div>}>
        <ResumeResultsContent />
      </Suspense>
    </main>
  );
}
