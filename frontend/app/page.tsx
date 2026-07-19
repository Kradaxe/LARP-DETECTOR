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
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-cyan-50 to-emerald-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-cyan-600 to-teal-700 text-white">
        <div className="relative max-w-6xl mx-auto px-4 py-20 sm:py-28">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium text-cyan-100 mb-6 border border-white/20">
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
              AI-Powered Technical Credibility Analysis
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 tracking-tight">
              Detect Technical LARPing
            </h1>
            <p className="text-lg sm:text-xl text-cyan-100 max-w-3xl mx-auto leading-relaxed">
              Analyze resumes, GitHub profiles, and technical claims for credibility.
              Built for recruiters who need evidence, not buzzwords.
            </p>
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <div className="flex items-center gap-2 text-sm text-cyan-200">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Resume Analysis
              </div>
              <div className="flex items-center gap-2 text-sm text-cyan-200">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                GitHub Profiling
              </div>
              <div className="flex items-center gap-2 text-sm text-cyan-200">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Claim Verification
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-slate-50 via-transparent to-transparent"></div>
      </section>

      {/* Main Content */}
      <section className="max-w-6xl mx-auto px-4 -mt-12 pb-20">
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-white/20 p-6 sm:p-8">
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
          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 mb-2">Evidence-Based Scoring</h3>
            <p className="text-sm text-slate-600">Our AI analyzes technical depth, specificity, and verifiable evidence to score claims.</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-cyan-100 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 mb-2">GitHub Integration</h3>
            <p className="text-sm text-slate-600">Analyze actual code contributions, repository quality, and development activity.</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 mb-2">Recruiter Reports</h3>
            <p className="text-sm text-slate-600">Generate comprehensive reports with actionable insights for hiring decisions.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
