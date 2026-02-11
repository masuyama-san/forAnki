import { useState } from 'react';
import { ModifyCardAI } from '../../generate/components/ModifyCardAI';

interface CardFormProps {
  onAdd: (front: string, back: string, deckName: string) => void;
  // External control
  frontValue: string;
  backValue: string;
  onFrontChange: (value: string) => void;
  onBackChange: (value: string) => void;
}

/**
 * 新しいカードを作成するためのフォームコンポーネント (Controlled Component)
 */
export function CardForm({ onAdd, frontValue, backValue, onFrontChange, onBackChange }: CardFormProps) {
  const [showModifyAI, setShowModifyAI] = useState(false);
  const [deckName, setDeckName] = useState('');

  const handleClick = () => {
    // バリデーション: 空文字チェック
    if (!frontValue || !backValue) return;

    // 親コンポーネントの追加ロジックを呼び出す
    onAdd(frontValue, backValue, deckName);

    // フォームのリセット (External state update)
    onFrontChange('');
    onBackChange('');
    // deckNameは維持する
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 sticky top-8">
      <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
        <span className="w-6 h-6 rounded bg-blue-100 text-blue-600 flex items-center justify-center text-xs">
          ＋
        </span>
        Add New Card
      </h2>
      <div className="space-y-4">
        {showModifyAI ? (
          <ModifyCardAI
            currentFront={frontValue}
            currentBack={backValue}
            onModified={(f, b) => {
              onFrontChange(f);
              onBackChange(b);
              setShowModifyAI(false);
            }}
            onCancel={() => setShowModifyAI(false)}
          />
        ) : (
          (frontValue || backValue) && (
            <button
              onClick={() => setShowModifyAI(true)}
              className="w-full py-2 bg-purple-50 text-purple-600 rounded-lg text-xs font-semibold hover:bg-purple-100 transition border border-purple-200 mb-2"
            >
              ✨ Refine Draft with AI
            </button>
          )
        )}

        {/* Deck Name Input */}
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Deck Name
          </label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition block"
            placeholder="e.g. Vocabulary"
            value={deckName}
            onChange={(e) => setDeckName(e.target.value)}
          />
        </div>

        {/* Front Input */}
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Front (Question)
          </label>
          <textarea
            className="w-full border border-gray-300 rounded-lg p-2.5 text-sm h-28 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition"
            placeholder="Enter the question..."
            value={frontValue}
            onChange={(e) => onFrontChange(e.target.value)}
          />
        </div>

        {/* Back Input */}
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Back (Answer)
          </label>
          <textarea
            className="w-full border border-gray-300 rounded-lg p-2.5 text-sm h-28 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition"
            placeholder="Enter the answer..."
            value={backValue}
            onChange={(e) => onBackChange(e.target.value)}
          />
        </div>

        {/* Submit Button */}
        <button
          onClick={handleClick}
          disabled={!frontValue || !backValue}
          className="w-full bg-blue-600 text-white py-2.5 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-sm active:scale-[0.98]"
        >
          Create Card
        </button>
      </div>
    </div>
  );
}
