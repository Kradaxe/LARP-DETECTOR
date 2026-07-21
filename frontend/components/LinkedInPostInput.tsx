'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { analyzeLinkedInPost } from '../services/api';

export default function LinkedInPostInput() {
  const [postUrl, setPostUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const clean = postUrl.trim();
    if (!clean) return;

    // Basic LinkedIn URL validation
    if (!clean.includes('linkedin.com')) {
      setError('Please enter a valid LinkedIn post URL');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const result = await analyzeLinkedInPost(clean);
      router.push(`/linkedin-post/results?data=${encodeURIComponent(JSON.stringify(result))}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'LinkedIn post analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="linkedin-url" className="block text-sm font-bold text-slate-200 mb-2">
            LinkedIn post URL
          </label>
          <input
            id="linkedin-url"
            type="url"
            value={postUrl}
            onChange={(e) => setPostUrl(e.target.value)}
            placeholder="https://www.linkedin.com/posts/username-post-id-1234567890"
            className="w-full p-4 border border-slate-700 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-slate-800 focus:bg-slate-900 transition-colors placeholder:text-slate-500 text-sm text-slate-100"
            disabled={loading}
          />
          <p className="text-xs text-slate-400 mt-2">
            Paste the URL of a LinkedIn post to analyze its technical credibility
          </p>
        </div>
        {error && (
          <div className="flex items-center gap-2 text-sm text-red-400 bg-red-500/10 p-3 rounded-lg border border-red-500/20">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {error}
          </div>
        )}
        <button
          type="submit"
          disabled={loading || !postUrl.trim()}
          className="w-full bg-gradient-to-r from-orange-500 to-amber-600 text-slate-950 py-3 px-6 rounded-xl font-bold hover:from-orange-600 hover:to-amber-700 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed disabled:text-slate-400 transition-all duration-300 shadow-lg shadow-orange-500/20 hover:shadow-xl hover:shadow-orange-500/30 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Analyzing Post...
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              Analyze LinkedIn Post
            </>
          )}
        </button>
      </form>
    </div>
  );
}
