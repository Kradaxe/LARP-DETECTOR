'use client';

interface RecommendationCardProps {
  technologies: string[];
}

export default function RecommendationCard({ technologies }: RecommendationCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Technologies Detected</h2>
      {technologies.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {technologies.map((tech, index) => (
            <span
              key={index}
              className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
            >
              {tech}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-gray-500 text-sm">No specific technologies detected</p>
      )}
    </div>
  );
}
