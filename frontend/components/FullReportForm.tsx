'use client';

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { analyzeResume, analyzeGitHub, generateReport } from '../services/api';

export default function FullReportForm() {
  const [file, setFile] = useState<File | null>(null);
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanUsername = username.trim().replace(/^@/, '');
    if (!file && !cleanUsername) {
      setError('Provide a resume, GitHub username, or both');
      return;
    }

    setLoading(true);
    setError('');
    try {
      let resumeResult = null;
      let githubResult = null;

      if (file) {
        setStep('Analyzing resume...');
        resumeResult = await analyzeResume(file);
      }
      if (cleanUsername) {
        setStep('Analyzing GitHub profile...');
        githubResult = await analyzeGitHub(cleanUsername);
      }

      setStep('Generating recruiter report...');
      const report = await generateReport(resumeResult ?? undefined, githubResult ?? undefined);
      router.push(`/report?data=${encodeURIComponent(JSON.stringify(report))}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Report generation failed');
    } finally {
      setLoading(false);
      setStep('');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <p className="text-sm text-slate-500 mb-4">
        Upload a resume and/or enter a GitHub username to generate a combined recruiter report.
      </p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Resume (optional)</label>
          <div
            onClick={() => inputRef.current?.click()}
            className="border-2 border-dashed border-slate-200 rounded-lg p-6 text-center cursor-pointer hover:border-slate-300 transition-colors"
          >
            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.docx"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
            {file ? (
              <p className="text-sm font-medium text-slate-800">{file.name}</p>
            ) : (
              <p className="text-sm text-slate-500">Click to upload PDF or DOCX</p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="report-github" className="block text-sm font-medium text-slate-700 mb-2">
            GitHub username (optional)
          </label>
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">@</span>
            <input
              id="report-github"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="octocat"
              className="w-full pl-8 pr-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm"
              disabled={loading}
            />
          </div>
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}
        {step && <p className="text-sm text-indigo-600">{step}</p>}

        <button
          type="submit"
          disabled={loading || (!file && !username.trim())}
          className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Generating Report...' : 'Generate Recruiter Report'}
        </button>
      </form>
    </div>
  );
}
