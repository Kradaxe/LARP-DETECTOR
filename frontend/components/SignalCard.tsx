'use client';

interface SignalCardProps {
  title: string;
  value: number;
  description: string;
}

function getBarColor(value: number) {
  if (value >= 8) return 'bg-emerald-500';
  if (value >= 5) return 'bg-amber-500';
  return 'bg-red-500';
}

function getTextColor(value: number) {
  if (value >= 8) return 'text-emerald-600';
  if (value >= 5) return 'text-amber-600';
  return 'text-red-600';
}

export default function SignalCard({ title, value, description }: SignalCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-slate-700">{title}</h3>
        <div className={`text-2xl font-bold ${getTextColor(value)}`}>
          {value}/10
        </div>
      </div>
      <p className="text-sm text-slate-500">{description}</p>
      <div className="mt-3 w-full bg-slate-100 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getBarColor(value)}`}
          style={{ width: `${value * 10}%` }}
        />
      </div>
    </div>
  );
}
