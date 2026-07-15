'use client';

import { getScoreColor } from './VerdictBadge';
import VerdictBadge from './VerdictBadge';

interface ScoreCardProps {
  score: number;
  verdict: string;
  subtitle?: string;
}

export default function ScoreCard({ score, verdict, subtitle = 'Credibility Score' }: ScoreCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="text-center">
        <div className={`text-6xl font-bold ${getScoreColor(score)}`}>
          {score}
        </div>
        <div className="text-slate-500 text-sm mt-2">{subtitle}</div>
        <div className="mt-4">
          <VerdictBadge verdict={verdict} size="lg" />
        </div>
      </div>
    </div>
  );
}
