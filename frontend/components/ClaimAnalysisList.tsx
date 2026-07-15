'use client';

import { useState } from 'react';
import { ClaimAnalysis } from '../types/analysis';
import VerdictBadge, { getScoreColor } from './VerdictBadge';

interface ClaimAnalysisListProps {
  claims: ClaimAnalysis[];
  suspiciousClaims?: string[];
  strongestClaims?: string[];
}

export default function ClaimAnalysisList({
  claims,
  suspiciousClaims = [],
  strongestClaims = [],
}: ClaimAnalysisListProps) {
  const [expanded, setExpanded] = useState<number | null>(null);

  return (
    <div className="space-y-4">
      {(suspiciousClaims.length > 0 || strongestClaims.length > 0) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {suspiciousClaims.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4">
              <h4 className="font-semibold text-red-800 mb-2">Suspicious Claims</h4>
              <ul className="space-y-1">
                {suspiciousClaims.map((c, i) => (
                  <li key={i} className="text-sm text-red-700">• {c}</li>
                ))}
              </ul>
            </div>
          )}
          {strongestClaims.length > 0 && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
              <h4 className="font-semibold text-emerald-800 mb-2">Strongest Claims</h4>
              <ul className="space-y-1">
                {strongestClaims.map((c, i) => (
                  <li key={i} className="text-sm text-emerald-700">• {c}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="text-lg font-semibold text-slate-800">
            Per-Claim Analysis ({claims.length})
          </h3>
        </div>
        <div className="divide-y divide-slate-100">
          {claims.map((claim, i) => (
            <div key={i} className="px-6 py-4">
              <button
                onClick={() => setExpanded(expanded === i ? null : i)}
                className="w-full text-left flex items-start justify-between gap-4"
              >
                <p className="text-sm text-slate-700 flex-1">{claim.claim}</p>
                <div className="flex items-center gap-3 shrink-0">
                  <span className={`text-lg font-bold ${getScoreColor(claim.credibility_score)}`}>
                    {claim.credibility_score}
                  </span>
                  <VerdictBadge verdict={claim.verdict} size="sm" />
                  <span className="text-slate-400 text-xs">{expanded === i ? '▲' : '▼'}</span>
                </div>
              </button>
              {expanded === i && (
                <p className="mt-3 text-sm text-slate-500 bg-slate-50 rounded-lg p-3">
                  {claim.reasoning}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
