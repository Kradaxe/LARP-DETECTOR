'use client';

interface StrengthsWeaknessesProps {
  strengths: string[];
  weaknesses: string[];
}

export default function StrengthsWeaknesses({ strengths, weaknesses }: StrengthsWeaknessesProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-emerald-700 mb-3 flex items-center gap-2">
          <span className="w-2 h-2 bg-emerald-500 rounded-full" />
          Strengths
        </h3>
        {strengths.length > 0 ? (
          <ul className="space-y-2">
            {strengths.map((item, i) => (
              <li key={i} className="text-slate-600 text-sm flex gap-2">
                <span className="text-emerald-500 shrink-0">+</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-400 text-sm">No strengths identified</p>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-red-700 mb-3 flex items-center gap-2">
          <span className="w-2 h-2 bg-red-500 rounded-full" />
          Weaknesses
        </h3>
        {weaknesses.length > 0 ? (
          <ul className="space-y-2">
            {weaknesses.map((item, i) => (
              <li key={i} className="text-slate-600 text-sm flex gap-2">
                <span className="text-red-500 shrink-0">−</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-400 text-sm">No weaknesses identified</p>
        )}
      </div>
    </div>
  );
}
