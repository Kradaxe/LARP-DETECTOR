'use client';

interface AnalysisSummaryProps {
  reasoning: string;
}

export default function AnalysisSummary({ reasoning }: AnalysisSummaryProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h2 className="text-xl font-bold text-gray-800 mb-4">AI Analysis</h2>
      <p className="text-gray-600 leading-relaxed">{reasoning}</p>
    </div>
  );
}
