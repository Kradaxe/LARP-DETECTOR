'use client';

interface AnalysisSummaryProps {
  reasoning: string;
}

export default function AnalysisSummary({ reasoning }: AnalysisSummaryProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-800 mb-4">AI Analysis</h2>
      <p className="text-slate-600 leading-relaxed text-sm">{reasoning}</p>
    </div>
  );
}
