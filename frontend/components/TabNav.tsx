'use client';

import { AnalysisTab } from '../types/analysis';

interface TabNavProps {
  active: AnalysisTab;
  onChange: (tab: AnalysisTab) => void;
}

const tabs: { id: AnalysisTab; label: string; description: string }[] = [
  { id: 'claim', label: 'Single Claim', description: "Paste their BS claims here" },
  { id: 'resume', label: 'Resume', description: "Check if they're lying on paper" },
  { id: 'github', label: 'GitHub', description: "See if their code actually exists" },
  { id: 'linkedin-post', label: 'LinkedIn Post', description: "Their humblebrags (probably fake)" },
  { id: 'report', label: 'Full Report', description: "Complete LARP investigation" },
];

export default function TabNav({ active, onChange }: TabNavProps) {
  return (
    <div className="border-b border-gray-200">
      <nav className="flex space-x-8">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              active === tab.id
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
