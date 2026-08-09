'use client';

import { useState } from 'react';
import TabNav from '../components/TabNav';
import InputBox from '../components/InputBox';
import ResumeUpload from '../components/ResumeUpload';
import GitHubInput from '../components/GitHubInput';
import LinkedInPostInput from '../components/LinkedInPostInput';
import FullReportForm from '../components/FullReportForm';
import { AnalysisTab } from '../types/analysis';

export default function Home() {
  const [activeTab, setActiveTab] = useState<AnalysisTab>('claim');

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">🎭 LARP Detector</h1>
              <p className="text-sm text-gray-600 mt-1">Catch the fake tech bros before they catch you</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <section className="max-w-6xl mx-auto px-4 py-8">
        <div className="card p-6">
          <TabNav active={activeTab} onChange={setActiveTab} />

          <div className="mt-6">
            {activeTab === 'claim' && <InputBox />}
            {activeTab === 'resume' && <ResumeUpload />}
            {activeTab === 'github' && <GitHubInput />}
            {activeTab === 'linkedin-post' && <LinkedInPostInput />}
            {activeTab === 'report' && <FullReportForm />}
          </div>
        </div>
      </section>
    </main>
  );
}
