'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { analyzeGitHub } from '../services/api';

export default function GitHubInput() {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const clean = username.trim().replace(/^@/, '');
    if (!clean) return;

    setLoading(true);
    setError('');
    try {
      const result = await analyzeGitHub(clean);
      router.push(`/github/results?data=${encodeURIComponent(JSON.stringify(result))}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'GitHub analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="github-username" className="block text-sm font-bold text-slate-200 mb-2">
            GitHub username
          </label>
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">@</span>
            <input
              id="github-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="octocat"
              className="w-full pl-8 pr-4 py-3 border border-slate-700 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm bg-slate-800 focus:bg-slate-900 transition-colors placeholder:text-slate-500 text-slate-100"
              disabled={loading}
            />
          </div>
        </div>
        {error && <p className="text-sm text-red-400 bg-red-500/10 p-3 rounded-lg border border-red-500/20">{error}</p>}
        <button
          type="submit"
          disabled={loading || !username.trim()}
          className="w-full bg-gradient-to-r from-orange-500 to-amber-600 text-slate-950 py-3 px-6 rounded-xl font-bold hover:from-orange-600 hover:to-amber-700 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed disabled:text-slate-400 transition-all duration-300 shadow-lg shadow-orange-500/20 hover:shadow-xl hover:shadow-orange-500/30"
        >
          {loading ? 'Analyzing Profile...' : 'Analyze GitHub Profile'}
        </button>
      </form>
    </div>
  );
}
