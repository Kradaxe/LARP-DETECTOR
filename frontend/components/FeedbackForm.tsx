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

      console.log('Submitting feedback:', feedback);
      const result = await submitFeedback(feedback);
      console.log('Feedback submission result:', result);
      setSubmitted(true);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit feedback. Please try again.';
      setError(errorMessage);
      console.error('Feedback submission error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded p-4">
        <div className="flex items-center">
          <svg className="w-5 h-5 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <p className="text-green-800 font-medium">Thanks for helping us catch LARPs! 🎭</p>
        </div>
      </div>
    );
  }

  if (!analysisId) {
    return null; // Don't show form if no analysis ID
  }

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        🎭 Was this LARP detection accurate?
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => setAgreed(true)}
            className={`flex-1 py-3 px-4 rounded font-medium transition-colors ${
              agreed === true
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            ✓ Actually legit
          </button>
          <button
            type="button"
            onClick={() => setAgreed(false)}
            className={`flex-1 py-3 px-4 rounded font-medium transition-colors ${
              agreed === false
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            ✗ Total LARP
          </button>
        </div>

        <div>
          <label htmlFor="comments" className="block text-sm font-medium text-gray-700 mb-2">
            Roast them here (optional) 💀
          </label>
          <textarea
            id="comments"
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Tell us why this was/wasn't a LARP..."
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded p-3">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full btn-primary disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Submitting...' : '🎭 Submit Feedback'}
        </button>
      </form>
    </div>
  );
}