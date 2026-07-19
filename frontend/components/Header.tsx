'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-white/80 backdrop-blur-xl border-b border-slate-200/50 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20 group-hover:shadow-blue-500/40 transition-all duration-300">
              LD
            </div>
            <div className="hidden sm:block">
              <h1 className="text-lg font-bold text-slate-900 leading-tight group-hover:text-blue-600 transition-colors">
                LARP Detector
              </h1>
              <p className="text-xs text-slate-500">Technical credibility analysis</p>
            </div>
          </Link>
          
          <nav className="flex items-center gap-6">
            <Link 
              href="/" 
              className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors relative group"
            >
              Analyze
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-blue-600 group-hover:w-full transition-all duration-300"></span>
            </Link>
            <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
              <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
              <span>System Online</span>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}
