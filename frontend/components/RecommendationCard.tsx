'use client';

interface RecommendationCardProps {
  technologies: string[];
}

export default function RecommendationCard({ technologies }: RecommendationCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-800 mb-4">Technologies Detected</h2>
      {technologies.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {technologies.map((tech, index) => (
            <span
              key={index}
              className="inline-block bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium"
            >
              {tech}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-slate-400 text-sm">No specific technologies detected</p>
      )}
    </div>
  );
}
