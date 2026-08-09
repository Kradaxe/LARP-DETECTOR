'use client';

import { useState } from 'react';
import { submitFeedback } from '../services/api';
import { FeedbackRequest } from '../types/analysis';

interface FeedbackFormProps {
  analysisId?: number;
}

export default function FeedbackForm({ analysisId }: FeedbackFormProps) {
  const [agreed, setAgreed] = useState<boolean | null>(null);
  const [comments, setComments] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (agreed === null) {
      setError('Please select whether you agree or disagree');
      return;
    }

    if (!analysisId) {
      setError('Analysis ID is required for feedback');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const feedback: FeedbackRequest = {
        analysis_id: analysisId,
        recruiter_agreed: agreed,
        recruiter_comments: comments || undefined,
      };

      await submitFeedback(feedback);
      setSubmitted(true);
    } catch (err) {
      setError('Failed to submit feedback. Please try again.');
      console.error('Feedback submission error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center">
          <svg className="w-5 h-5 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <p className="text-green-800 font-medium">Thank you for your feedback!</p>
        </div>
      </div>
    );
  }

  if (!analysisId) {
    return null; // Don't show form if no analysis ID
  }

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900 mb-4">
        Was this analysis accurate?
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => setAgreed(true)}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
              agreed === true
                ? 'bg-green-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            ✓ Accurate
          </button>
          <button
            type="button"
            onClick={() => setAgreed(false)}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
              agreed === false
                ? 'bg-red-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            ✗ Inaccurate
          </button>
        </div>

        <div>
          <label htmlFor="comments" className="block text-sm font-medium text-slate-700 mb-2">
            Additional comments (optional)
          </label>
          <textarea
            id="comments"
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Tell us more about why you agree or disagree..."
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
        </button>
      </form>
    </div>
  );
}