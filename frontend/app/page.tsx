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
    <main className="min-h-screen bg-slate-950">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950 border-b border-slate-800">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(251,146,60,0.1),transparent_50%)]"></div>
        <div className="relative max-w-6xl mx-auto px-4 py-24 sm:py-32">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 bg-orange-500/10 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-bold text-orange-400 mb-8 border border-orange-500/20">
              <span className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></span>
              AI-Powered Technical Credibility Analysis
            </div>
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-8 tracking-tight text-slate-100">
              Detect Technical <span className="gradient-text">LARPing</span>
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
              Analyze resumes, GitHub profiles, and LinkedIn posts for credibility.
              Built for recruiters who need evidence, not buzzwords.
            </p>
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Resume Analysis
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                GitHub Profiling
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                LinkedIn Post Analysis
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-slate-950 via-transparent to-transparent"></div>
      </section>

      {/* Main Content */}
      <section className="max-w-6xl mx-auto px-4 -mt-12 pb-20">
        <div className="glass-card p-6 sm:p-8">
          <TabNav active={activeTab} onChange={setActiveTab} />

          <div className="mt-8">
            {activeTab === 'claim' && <InputBox />}
            {activeTab === 'resume' && <ResumeUpload />}
            {activeTab === 'github' && <GitHubInput />}
            {activeTab === 'linkedin-post' && <LinkedInPostInput />}
            {activeTab === 'report' && <FullReportForm />}
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-card p-6 hover:border-orange-500/30 transition-colors">
            <div className="w-12 h-12 bg-orange-500/10 rounded-xl flex items-center justify-center mb-4 border border-orange-500/20">
              <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-bold text-slate-100 mb-2">Evidence-Based Scoring</h3>
            <p className="text-sm text-slate-400">Our AI analyzes technical depth, specificity, and verifiable evidence to score claims.</p>
          </div>

          <div className="glass-card p-6 hover:border-orange-500/30 transition-colors">
            <div className="w-12 h-12 bg-orange-500/10 rounded-xl flex items-center justify-center mb-4 border border-orange-500/20">
              <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
            <h3 className="font-bold text-slate-100 mb-2">GitHub Integration</h3>
            <p className="text-sm text-slate-400">Analyze actual code contributions, repository quality, and development activity.</p>
          </div>

          <div className="glass-card p-6 hover:border-orange-500/30 transition-colors">
            <div className="w-12 h-12 bg-orange-500/10 rounded-xl flex items-center justify-center mb-4 border border-orange-500/20">
              <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="font-bold text-slate-100 mb-2">Recruiter Reports</h3>
            <p className="text-sm text-slate-400">Generate comprehensive reports with actionable insights for hiring decisions.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
