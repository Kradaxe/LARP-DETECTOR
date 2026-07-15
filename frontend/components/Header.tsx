'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-slate-900 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 hover:opacity-90 transition-opacity">
          <div className="w-9 h-9 bg-indigo-500 rounded-lg flex items-center justify-center font-bold text-sm">
            LD
          </div>
          <div>
            <h1 className="text-lg font-bold leading-tight">LARP Detector</h1>
            <p className="text-xs text-slate-400">Technical credibility analysis</p>
          </div>
        </Link>
        <nav className="hidden sm:flex items-center gap-6 text-sm text-slate-300">
          <Link href="/" className="hover:text-white transition-colors">Analyze</Link>
        </nav>
      </div>
    </header>
  );
}
