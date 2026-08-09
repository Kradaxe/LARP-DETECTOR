'use client';

import { getScoreColor } from './VerdictBadge';
import VerdictBadge from './VerdictBadge';

interface ScoreCardProps {
  score: number;
  verdict: string;
  subtitle?: string;
}

export default function ScoreCard({ score, verdict, subtitle = 'LARP Probability' }: ScoreCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="text-center">
        <div className={`text-6xl font-bold ${getScoreColor(score)}`}>
          {score}
        </div>
        <div className="text-gray-500 text-sm mt-2">{subtitle}</div>
        <div className="mt-4">
          <VerdictBadge verdict={verdict} size="lg" />
        </div>
        <div className="text-xs text-gray-400 mt-2">
          {score < 50 ? "100% Certified LARP 🎭" : score < 70 ? "High LARP Probability 🤨" : "Low LARP Probability 🤔"}
        </div>
      </div>
    </div>
  );
}
