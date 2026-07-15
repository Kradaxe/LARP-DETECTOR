'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import ScoreCard from '../../components/ScoreCard';
import RadarChart from '../../components/RadarChart';
import SignalCard from '../../components/SignalCard';
import AnalysisSummary from '../../components/AnalysisSummary';
import RecommendationCard from '../../components/RecommendationCard';
import StrengthsWeaknesses from '../../components/StrengthsWeaknesses';
import InterviewQuestions from '../../components/InterviewQuestions';
import { AnalyzeResponse } from '../../types/analysis';

function ResultsContent() {
  const searchParams = useSearchParams();
  const data = searchParams.get('data');

  if (!data) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-500">No analysis data found.</p>
        <Link href="/" className="text-indigo-600 hover:underline mt-4 inline-block">Go back</Link>
      </div>
    );
  }

  const result: AnalyzeResponse = JSON.parse(decodeURIComponent(data));

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">Claim Analysis</h1>
        <p className="text-slate-500 mt-2">Credibility assessment for your technical claim</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ScoreCard score={result.credibility_score} verdict={result.verdict} />
        <RadarChart
          specificity={result.specificity}
          technical_depth={result.technical_depth}
          evidence={result.evidence}
          implementation_detail={result.implementation_detail}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SignalCard title="Specificity" value={result.specificity} description="How concrete and specific is the statement?" />
        <SignalCard title="Technical Depth" value={result.technical_depth} description="Does the author understand underlying systems?" />
        <SignalCard title="Evidence" value={result.evidence} description="Are numbers, measurements, or outcomes provided?" />
        <SignalCard title="Implementation Detail" value={result.implementation_detail} description="Does the author explain HOW they built it?" />
      </div>

      <StrengthsWeaknesses strengths={result.strengths ?? []} weaknesses={result.weaknesses ?? []} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnalysisSummary reasoning={result.reasoning} />
        <RecommendationCard technologies={result.technologies_found} />
      </div>

      <InterviewQuestions questions={result.interview_questions ?? []} />

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

export default function ResultsPage() {
  return (
    <main className="min-h-screen bg-slate-50 py-10 px-4">
      <Suspense fallback={<div className="text-center py-20 text-slate-500">Loading results...</div>}>
        <ResultsContent />
      </Suspense>
    </main>
  );
}
