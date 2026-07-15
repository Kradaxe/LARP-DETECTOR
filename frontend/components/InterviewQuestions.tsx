'use client';

interface InterviewQuestionsProps {
  questions: string[];
}

export default function InterviewQuestions({ questions }: InterviewQuestionsProps) {
  if (questions.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h3 className="text-lg font-semibold text-slate-800 mb-4">Suggested Interview Questions</h3>
      <ol className="space-y-3">
        {questions.map((q, i) => (
          <li key={i} className="flex gap-3 text-sm text-slate-600">
            <span className="shrink-0 w-6 h-6 bg-indigo-100 text-indigo-700 rounded-full flex items-center justify-center text-xs font-bold">
              {i + 1}
            </span>
            <span className="pt-0.5">{q}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}
