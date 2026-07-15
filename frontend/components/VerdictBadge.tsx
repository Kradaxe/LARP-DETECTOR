'use client';

interface VerdictBadgeProps {
  verdict: string;
  size?: 'sm' | 'md' | 'lg';
}

export function getVerdictStyles(verdict: string) {
  const lower = verdict.toLowerCase();
  if (lower.includes('highly') || lower.includes('strong')) {
    return 'bg-emerald-100 text-emerald-800 border-emerald-200';
  }
  if (lower.includes('likely') || lower.includes('genuine') || lower.includes('credible')) {
    return 'bg-blue-100 text-blue-800 border-blue-200';
  }
  if (lower.includes('possibly') || lower.includes('moderate') || lower.includes('mixed')) {
    return 'bg-amber-100 text-amber-800 border-amber-200';
  }
  return 'bg-red-100 text-red-800 border-red-200';
}

export function getScoreColor(score: number) {
  if (score >= 80) return 'text-emerald-600';
  if (score >= 60) return 'text-blue-600';
  if (score >= 40) return 'text-amber-600';
  return 'text-red-600';
}

export default function VerdictBadge({ verdict, size = 'md' }: VerdictBadgeProps) {
  const sizeClasses = {
    sm: 'px-2.5 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base',
  };

  return (
    <span
      className={`inline-block rounded-full font-medium border ${getVerdictStyles(verdict)} ${sizeClasses[size]}`}
    >
      {verdict}
    </span>
  );
}
