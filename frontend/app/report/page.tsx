'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import ScoreCard from '../../components/ScoreCard';
import ReportBreakdown from '../../components/ReportBreakdown';
import StrengthsWeaknesses from '../../components/StrengthsWeaknesses';
import { RecruiterReportResponse } from '../../types/analysis';

function ReportContent() {
  const searchParams = useSearchParams();
  const data = searchParams.get('data');

  if (!data) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-500">No report data found.</p>
        <Link href="/" className="text-indigo-600 hover:underline mt-4 inline-block">Go back</Link>
      </div>
    );
  }

  const result: RecruiterReportResponse = JSON.parse(decodeURIComponent(data));

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">Recruiter Report</h1>
        <p className="text-slate-500 mt-2">Combined credibility assessment</p>
      </div>

      <div className="max-w-md mx-auto">
        <ScoreCard score={result.overall_score} verdict={result.verdict} subtitle="Overall Score" />
      </div>

      <ReportBreakdown breakdown={result.credibility_breakdown} />

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-800 mb-3">Recruiter Summary</h3>
        <p className="text-slate-600 leading-relaxed">{result.recruiter_summary}</p>
      </div>

      {result.suspicious_claims.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-5">
          <h4 className="font-semibold text-red-800 mb-2">Suspicious Claims</h4>
          <ul className="space-y-1">
            {result.suspicious_claims.map((c, i) => (
              <li key={i} className="text-sm text-red-700">• {c}</li>
            ))}
          </ul>
        </div>
      )}

      <StrengthsWeaknesses strengths={result.strengths} weaknesses={result.weaknesses} />

      {result.recommendations.length > 0 && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-indigo-800 mb-4">Recommendations</h3>
          <ol className="space-y-2">
            {result.recommendations.map((rec, i) => (
              <li key={i} className="flex gap-3 text-sm text-indigo-900">
                <span className="shrink-0 w-5 h-5 bg-indigo-200 text-indigo-800 rounded-full flex items-center justify-center text-xs font-bold">
                  {i + 1}
                </span>
                <span className="pt-0.5">{rec}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      <div className="text-center pt-4">
        <Link
          href="/"
          className="inline-block bg-indigo-600 text-white py-3 px-8 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
        >
          New Analysis
        </Link>
      </div>
    </div>
  );
}

export default function ReportPage() {
  return (
    <main className="min-h-screen bg-slate-50 py-10 px-4">
      <Suspense fallback={<div className="text-center py-20 text-slate-500">Loading report...</div>}>
        <ReportContent />
      </Suspense>
    </main>
  );
}
