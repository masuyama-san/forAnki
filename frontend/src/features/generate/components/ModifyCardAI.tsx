import { useState } from 'react';
import { AxiosError } from 'axios';
import { modifyContent } from '../api/modifyContent';

type Status = 'idle' | 'loading' | 'success' | 'error';

interface ModifyCardAIProps {
  currentFront: string;
  currentBack: string;
  onModified: (front: string, back: string) => void;
  onCancel: () => void;
}

export function ModifyCardAI({ currentFront, currentBack, onModified, onCancel }: ModifyCardAIProps) {
  const [instruction, setInstruction] = useState('');
  const [status, setStatus] = useState<Status>('idle');
  const [error, setError] = useState('');

  const handleModify = async () => {
    if (!instruction.trim()) return;

    setStatus('loading');
    setError('');

    try {
      const response = await modifyContent({
        front: currentFront,
        back: currentBack,
        instruction: instruction,
      });
      onModified(response.front, response.back);
      setStatus('success');
    } catch (e) {
      const errorMessage =
        e instanceof AxiosError
          ? e.response?.data?.detail || 'Failed to modify content'
          : 'Failed to modify content';
      setError(errorMessage);
      setStatus('error');
    }
  };

  return (
    <div className="bg-purple-50 p-4 rounded-lg border border-purple-100 mb-4 animate-fadeIn">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">✨</span>
        <h3 className="font-bold text-purple-900 text-sm">AI Modifier</h3>
      </div>

      <div className="mb-3">
        <label className="block text-xs font-semibold text-purple-700 uppercase tracking-wide mb-1">
          Instruction
        </label>
        <textarea
          className="w-full border border-purple-200 rounded-md p-2 text-sm h-16 focus:ring-2 focus:ring-purple-500 focus:outline-none resize-none bg-white"
          placeholder="e.g. Make it shorter, Fix grammar, Add example..."
          value={instruction}
          onChange={(e) => setInstruction(e.target.value)}
          disabled={status === 'loading'}
        />
      </div>

      {error && (
        <div className="mb-3 p-2 bg-red-50 text-red-600 text-xs rounded border border-red-100">
          {error}
        </div>
      )}

      <div className="flex justify-end gap-2">
        <button
          onClick={onCancel}
          className="text-gray-500 text-xs hover:text-gray-700 px-3 py-1.5"
          disabled={status === 'loading'}
        >
          Cancel
        </button>
        <button
          onClick={handleModify}
          disabled={!instruction.trim() || status === 'loading'}
          className="bg-purple-600 text-white text-xs px-3 py-1.5 rounded-md hover:bg-purple-700 transition disabled:opacity-50 flex items-center gap-2"
        >
          {status === 'loading' ? (
            'Processing...'
          ) : (
            'Apply Changes'
          )}
        </button>
      </div>
    </div>
  );
}
