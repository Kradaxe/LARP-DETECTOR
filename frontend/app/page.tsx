'use client';

import { useState } from 'react';
import TabNav from '../components/TabNav';
import InputBox from '../components/InputBox';
import ResumeUpload from '../components/ResumeUpload';
import GitHubInput from '../components/GitHubInput';
import FullReportForm from '../components/FullReportForm';
import { AnalysisTab } from '../types/analysis';

export default function Home() {
  const [activeTab, setActiveTab] = useState<AnalysisTab>('claim');

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="bg-gradient-to-br from-indigo-600 to-slate-900 text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold mb-4">Detect Technical LARPing</h1>
          <p className="text-lg text-indigo-200 max-w-2xl mx-auto">
            Analyze resumes, GitHub profiles, and technical claims for credibility.
            Built for recruiters who need evidence, not buzzwords.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-4 -mt-8 pb-16">
        <TabNav active={activeTab} onChange={setActiveTab} />

        {activeTab === 'claim' && <InputBox />}
        {activeTab === 'resume' && <ResumeUpload />}
        {activeTab === 'github' && <GitHubInput />}
        {activeTab === 'report' && <FullReportForm />}
      </section>
    </main>
  );
}
