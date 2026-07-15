'use client';

import { CredibilityBreakdown } from '../types/analysis';
import { getScoreColor } from './VerdictBadge';

interface ReportBreakdownProps {
  breakdown: CredibilityBreakdown;
}

export default function ReportBreakdown({ breakdown }: ReportBreakdownProps) {
  const { resume_score, github_score, weighted_overall, score_distribution } = breakdown;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {resume_score > 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 text-center">
            <p className="text-sm text-slate-500 mb-1">Resume Score</p>
            <p className={`text-3xl font-bold ${getScoreColor(resume_score)}`}>{resume_score}</p>
          </div>
        )}
        {github_score > 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 text-center">
            <p className="text-sm text-slate-500 mb-1">GitHub Score</p>
            <p className={`text-3xl font-bold ${getScoreColor(github_score)}`}>{github_score}</p>
          </div>
        )}
        <div className="bg-indigo-50 rounded-xl border border-indigo-200 p-5 text-center">
          <p className="text-sm text-indigo-600 mb-1">Weighted Overall</p>
          <p className={`text-3xl font-bold ${getScoreColor(weighted_overall)}`}>{weighted_overall}</p>
        </div>
      </div>

      {Object.keys(score_distribution).length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <h4 className="font-semibold text-slate-800 mb-3">Score Distribution</h4>
          <div className="space-y-2">
            {Object.entries(score_distribution).map(([label, count]) => (
              <div key={label} className="flex items-center justify-between text-sm">
                <span className="text-slate-600 capitalize">{label.replace(/_/g, ' ')}</span>
                <span className="font-semibold text-slate-800">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
