'use client';

interface ScoreCardProps {
  score: number;
  verdict: string;
}

export default function ScoreCard({ score, verdict }: ScoreCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getVerdictColor = (verdict: string) => {
    if (verdict === 'Highly Credible') return 'bg-green-100 text-green-800';
    if (verdict === 'Likely Genuine') return 'bg-blue-100 text-blue-800';
    if (verdict === 'Possibly Exaggerated') return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="text-center">
        <div className={`text-6xl font-bold ${getScoreColor(score)}`}>
          {score}
        </div>
        <div className="text-gray-500 text-sm mt-2">Credibility Score</div>
        <div className={`inline-block mt-4 px-4 py-2 rounded-full text-sm font-medium ${getVerdictColor(verdict)}`}>
          {verdict}
        </div>
      </div>
    </div>
  );
}
