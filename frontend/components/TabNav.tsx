'use client';

import { AnalysisTab } from '../types/analysis';

interface TabNavProps {
  active: AnalysisTab;
  onChange: (tab: AnalysisTab) => void;
}

const tabs: { id: AnalysisTab; label: string; description: string; icon: string }[] = [
  { id: 'claim', label: 'Single Claim', description: 'Analyze a technical statement', icon: '💬' },
  { id: 'resume', label: 'Resume', description: 'Upload PDF or DOCX', icon: '📄' },
  { id: 'github', label: 'GitHub', description: 'Analyze a GitHub profile', icon: '🔗' },
  { id: 'linkedin-post', label: 'LinkedIn Post', description: 'Analyze LinkedIn posts', icon: '💼' },
  { id: 'report', label: 'Full Report', description: 'Combined recruiter report', icon: '📊' },
];

export default function TabNav({ active, onChange }: TabNavProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`relative group text-left p-4 rounded-xl border-2 transition-all duration-300 ${
            active === tab.id
              ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-cyan-50 shadow-md shadow-blue-500/10'
              : 'border-slate-200 bg-white hover:border-blue-300 hover:shadow-md'
          }`}
        >
          <div className="flex items-start gap-3">
            <span className="text-2xl">{tab.icon}</span>
            <div className="flex-1">
              <p className={`font-semibold text-sm transition-colors ${
                active === tab.id ? 'text-blue-700' : 'text-slate-800 group-hover:text-blue-600'
              }`}>
                {tab.label}
              </p>
              <p className="text-xs text-slate-500 mt-1">{tab.description}</p>
            </div>
          </div>
          {active === tab.id && (
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full shadow-md"></div>
          )}
        </button>
      ))}
    </div>
  );
}
