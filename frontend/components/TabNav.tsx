'use client';

import { AnalysisTab } from '../types/analysis';

interface TabNavProps {
  active: AnalysisTab;
  onChange: (tab: AnalysisTab) => void;
}

const tabs: { id: AnalysisTab; label: string; description: string }[] = [
  { id: 'claim', label: 'Single Claim', description: 'Analyze a technical statement' },
  { id: 'resume', label: 'Resume', description: 'Upload PDF or DOCX' },
  { id: 'github', label: 'GitHub', description: 'Analyze a GitHub profile' },
  { id: 'report', label: 'Full Report', description: 'Combined recruiter report' },
];

export default function TabNav({ active, onChange }: TabNavProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-8">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`text-left p-4 rounded-xl border-2 transition-all ${
            active === tab.id
              ? 'border-indigo-500 bg-indigo-50 shadow-sm'
              : 'border-slate-200 bg-white hover:border-slate-300'
          }`}
        >
          <p className={`font-semibold text-sm ${active === tab.id ? 'text-indigo-700' : 'text-slate-800'}`}>
            {tab.label}
          </p>
          <p className="text-xs text-slate-500 mt-1">{tab.description}</p>
        </button>
      ))}
    </div>
  );
}
