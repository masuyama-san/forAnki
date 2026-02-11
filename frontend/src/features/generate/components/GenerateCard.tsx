import { useState } from 'react';
import { AxiosError } from 'axios';
import { generateContent } from '../api/generateContent';

type GenerateStatus = 'idle' | 'loading' | 'success' | 'error';

interface GenerateCardProps {
  onCardGenerated?: (front: string, back: string) => void;
}

export function GenerateCard({ onCardGenerated }: GenerateCardProps) {
  const [prompt, setPrompt] = useState('');
  const [status, setStatus] = useState<GenerateStatus>('idle');
  const [chatResult, setChatResult] = useState('');
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setStatus('loading');
    setError('');
    setChatResult('');

    try {
      const response = await generateContent({ prompt });
      
      setChatResult(response.chat);
      setStatus('success');
      
      if (onCardGenerated && response.front && response.back) {
        onCardGenerated(response.front, response.back);
      }
    } catch (e) {
      const errorMessage =
        e instanceof AxiosError
          ? e.response?.data?.detail || 'Failed to generate content'
          : 'Failed to generate content';
      setError(errorMessage);
      setStatus('error');
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
      <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
        <span className="w-6 h-6 rounded bg-purple-100 text-purple-600 flex items-center justify-center text-xs">
          ✨
        </span>
        AI Generate
      </h2>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Prompt
          </label>
          <textarea
            className="w-full border border-gray-300 rounded-lg p-2.5 text-sm h-20 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 focus:outline-none transition resize-none"
            placeholder="What should the card be about?"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={status === 'loading'}
          />
        </div>

        <button
          onClick={handleGenerate}
          disabled={!prompt.trim() || status === 'loading'}
          className="w-full bg-purple-600 text-white py-2.5 px-4 rounded-lg hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-sm flex items-center justify-center gap-2"
        >
          {status === 'loading' ? (
            <>
              <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating...
            </>
          ) : (
            'Generate Content'
          )}
        </button>

        {error && (
          <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg">
            {error}
          </div>
        )}

        {status === 'success' && chatResult && (
          <div className="mt-4">
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
              AI Response
            </label>
            <div className="p-3 bg-purple-50 rounded-lg text-sm whitespace-pre-wrap border border-purple-100 text-purple-900 max-h-60 overflow-y-auto">
              {chatResult}
            </div>
            <div className="mt-2 text-xs text-green-600 font-medium text-right flex items-center justify-end gap-1">
              <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span>
              Card content has been applied to the form below
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
