'use client';

interface SignalCardProps {
  title: string;
  value: number;
  description: string;
}

export default function SignalCard({ title, value, description }: SignalCardProps) {
  const getColor = (value: number) => {
    if (value >= 8) return 'bg-green-500';
    if (value >= 5) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-gray-700">{title}</h3>
        <div className={`text-2xl font-bold ${getColor(value)}`}>
          {value}/10
        </div>
      </div>
      <p className="text-sm text-gray-500">{description}</p>
      <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getColor(value)}`}
          style={{ width: `${value * 10}%` }}
        />
      </div>
    </div>
  );
}
