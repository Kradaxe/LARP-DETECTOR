'use client';

import { getScoreColor } from './VerdictBadge';

interface GitHubMetricsCardProps {
  username: string;
  basicMetrics: Record<string, unknown>;
  engagementMetrics: Record<string, unknown>;
  languageMetrics: Record<string, unknown>;
  repositoryMetrics: Record<string, unknown>;
  signalScores: Record<string, number>;
}

function MetricGrid({ title, metrics }: { title: string; metrics: Record<string, unknown> }) {
  const entries = Object.entries(metrics);
  if (entries.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
      <h4 className="font-semibold text-slate-800 mb-3">{title}</h4>
      <div className="grid grid-cols-2 gap-3">
        {entries.map(([key, value]) => (
          <div key={key} className="bg-slate-50 rounded-lg px-3 py-2">
            <p className="text-xs text-slate-500 capitalize">{key.replace(/_/g, ' ')}</p>
            <p className="text-sm font-semibold text-slate-800">
              {typeof value === 'number' ? value.toLocaleString() : String(value)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function GitHubMetricsCard({
  username,
  basicMetrics,
  engagementMetrics,
  languageMetrics,
  repositoryMetrics,
  signalScores,
}: GitHubMetricsCardProps) {
  const signalEntries = Object.entries(signalScores);

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
        <h3 className="text-lg font-semibold text-slate-800 mb-1">
          @{username}
        </h3>
        <p className="text-sm text-slate-500">GitHub profile metrics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <MetricGrid title="Basic Metrics" metrics={basicMetrics} />
        <MetricGrid title="Engagement" metrics={engagementMetrics} />
        <MetricGrid title="Languages" metrics={languageMetrics} />
        <MetricGrid title="Repositories" metrics={repositoryMetrics} />
      </div>

      {signalEntries.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <h4 className="font-semibold text-slate-800 mb-4">Signal Scores</h4>
          <div className="space-y-3">
            {signalEntries.map(([key, value]) => (
              <div key={key}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600 capitalize">{key.replace(/_/g, ' ')}</span>
                  <span className={`font-bold ${getScoreColor(value * 10)}`}>{value}/10</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-indigo-500 transition-all"
                    style={{ width: `${value * 10}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
