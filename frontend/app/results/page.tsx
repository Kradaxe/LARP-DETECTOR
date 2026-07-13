'use client';

import { useSearchParams } from 'next/navigation';
import ScoreCard from '../../components/ScoreCard';
import RadarChart from '../../components/RadarChart';
import SignalCard from '../../components/SignalCard';
import AnalysisSummary from '../../components/AnalysisSummary';
import RecommendationCard from '../../components/RecommendationCard';

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const data = searchParams.get('data');

  if (!data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  const result = JSON.parse(decodeURIComponent(data));

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Analysis Results</h1>
          <p className="text-lg text-gray-600">Credibility assessment for your technical claim</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ScoreCard score={result.credibility_score} verdict={result.verdict} />
          <RadarChart
            specificity={result.specificity}
            technical_depth={result.technical_depth}
            evidence={result.evidence}
            implementation_detail={result.implementation_detail}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <SignalCard
            title="Specificity"
            value={result.specificity}
            description="How concrete and specific is the statement?"
          />
          <SignalCard
            title="Technical Depth"
            value={result.technical_depth}
            description="Does the author understand underlying systems?"
          />
          <SignalCard
            title="Evidence"
            value={result.evidence}
            description="Are numbers, measurements, or outcomes provided?"
          />
          <SignalCard
            title="Implementation Detail"
            value={result.implementation_detail}
            description="Does the author explain HOW they built it?"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <AnalysisSummary reasoning={result.reasoning} />
          <RecommendationCard technologies={result.technologies_found} />
        </div>

        <div className="text-center">
          <button
            onClick={() => window.location.href = '/'}
            className="bg-blue-600 text-white py-3 px-8 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Analyze Another Claim
          </button>
        </div>
      </div>
    </main>
  );
}
