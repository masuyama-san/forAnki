import { useState } from 'react';
import type { Card } from '../../../types';
import { ModifyCardAI } from '../../generate/components/ModifyCardAI';

interface CardListProps {
  cards: Card[];
  onUpdate: (id: number, front: string, back: string, tags?: string[]) => void;
}

interface EditableCardHelperProps {
  card: Card;
  onUpdate: (id: number, front: string, back: string, tags?: string[]) => void;
}

function EditableCard({ card, onUpdate }: EditableCardHelperProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [front, setFront] = useState(card.front);
  const [back, setBack] = useState(card.back);
  const [tags, setTags] = useState(card.tags ? card.tags.join(', ') : '');
  const [showModifyAI, setShowModifyAI] = useState(false);

  // Reset state when card changes or editing is cancelled
  const handleCancel = () => {
    setIsEditing(false);
    setFront(card.front);
    setBack(card.back);
    setTags(card.tags ? card.tags.join(', ') : '');
    setShowModifyAI(false);
  };

  const handleSave = () => {
    // Split by comma (or space) -> trim -> filter empty
    // Allowing both comma and space might be confusing if tags contain spaces, but Anki tags usually don't have spaces.
    // Let's stick to comma separated for input convenience.
    const tagList = tags.split(',').map(t => t.trim()).filter(Boolean);
    onUpdate(card.id, front, back, tagList);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="bg-white p-5 rounded-xl shadow-md border-2 border-blue-100">
        <div className="mb-4 flex justify-between items-center">
          <h3 className="text-sm font-bold text-blue-600">Editing Card</h3>
          <button
             onClick={() => setShowModifyAI(!showModifyAI)}
             className="text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded border border-purple-200 hover:bg-purple-100"
          >
            {showModifyAI ? 'Hide AI' : '✨ Modify with AI'}
          </button>
        </div>

        {showModifyAI && (
          <ModifyCardAI
            currentFront={front}
            currentBack={back}
            onModified={(f, b) => {
              setFront(f);
              setBack(b);
            }}
            onCancel={() => setShowModifyAI(false)}
          />
        )}

        <div className="mb-4">
          <label className="block text-xs font-bold text-gray-400 uppercase mb-1">Tags (comma separated)</label>
          <input
            type="text"
            className="w-full border p-2 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="example, important, vocabulary"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-xs font-bold text-gray-400 uppercase mb-1">Front</label>
            <textarea
              className="w-full border p-2 rounded text-sm h-32 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={front}
              onChange={(e) => setFront(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-400 uppercase mb-1">Back</label>
            <textarea
              className="w-full border p-2 rounded text-sm h-32 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={back}
              onChange={(e) => setBack(e.target.value)}
            />
          </div>
        </div>
        <div className="flex justify-end gap-2">
          <button onClick={handleCancel} className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded">
            Cancel
          </button>
          <button onClick={handleSave} className="px-3 py-1.5 text-sm bg-blue-600 text-white hover:bg-blue-700 rounded shadow-sm">
            Save
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-white p-5 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
      {/* Header: DeckName, Tags & Actions */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-medium px-2.5 py-1 bg-gray-100 text-gray-600 rounded-md">
            {card.deckName}
          </span>
          {card.tags && card.tags.map((tag) => (
            <span key={tag} className="text-xs font-medium px-2 py-0.5 bg-blue-50 text-blue-600 rounded border border-blue-100">
              #{tag}
            </span>
          ))}
        </div>
        <div className="opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
          <button
            onClick={() => setIsEditing(true)}
            className="text-xs font-medium text-gray-500 hover:text-blue-600"
          >
            Edit
          </button>
        </div>
      </div>

      {/* Content: Front & Back */}
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
            Front
          </h3>
          <p className="text-base text-gray-900 font-medium whitespace-pre-wrap">
            {card.front}
          </p>
        </div>
        <div className="md:border-l md:pl-6 border-gray-100">
          <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
            Back
          </h3>
          <p className="text-base text-gray-700 whitespace-pre-wrap">{card.back}</p>
        </div>
      </div>
    </div>
  );
}

/**
 * カードリストを表示するコンポーネント
 * カードの一覧表示、編集開始アクションを提供します。
 */
export function CardList({ cards, onUpdate }: CardListProps) {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // 全カードからユニークなタグを抽出してソート
  const allTags = Array.from(new Set(cards.flatMap(c => c.tags || []))).sort();

  // 選択されたタグでフィルタリング (AND検索: 選択した全てのタグを持っているカードを表示)
  // OR検索にしたい場合は .some() を使いますが、通常フィルタは絞り込み(AND)が直感的です。
  // ここでは「選択したタグのいずれかを含む(OR)」か「すべてを含む(AND)」か迷うところですが、
  // タグフィルタは通常「このタグに関連するもの」を見たいので、複数選択時はOR（いずれかを含む）の方が
  // 緩やかに集合を作れて使いやすいことが多いです。
  // しかし、AnkiのBrowser検索などでは AND がデフォルトのことが多いです。
  // ユーザーの意図としては「これとこれに関連するカード」を見たい場合が多いので、
  // ここでは OR (いずれかを含む) を採用してみます。もし絞り込みすぎると何も出なくなるため。

  // 選択されたすべてのタグを含むカードを表示 (AND検索)
  // ユーザー要望により、複数選択時は A AND B で絞り込みます。
  const filteredCards = selectedTags.length > 0
    ? cards.filter(c => selectedTags.every(tag => c.tags?.includes(tag)))
    : cards;

  const toggleTag = (tag: string) => {
    setSelectedTags(prev =>
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  return (
    <div>
      <div className="flex flex-col gap-4 mb-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-800">Your Cards <span className="text-sm font-normal text-gray-500">({filteredCards.length})</span></h2>
        </div>

        {/* Tag Filters */}
        {allTags.length > 0 && (
          <div className="flex flex-wrap gap-2 pb-2">
            <button
              onClick={() => setSelectedTags([])}
              className={`px-3 py-1 text-xs font-medium rounded-full transition-colors ${
                selectedTags.length === 0
                  ? 'bg-gray-800 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              All
            </button>
            {allTags.map(tag => (
              <button
                key={tag}
                onClick={() => toggleTag(tag)}
                className={`px-3 py-1 text-xs font-medium rounded-full transition-colors ${
                  selectedTags.includes(tag)
                    ? 'bg-blue-600 text-white'
                    : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                }`}
              >
                #{tag}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-4">
        {filteredCards.map((card) => (
          <EditableCard
            key={card.id}
            card={card}
            onUpdate={onUpdate}
          />
        ))}

        {/* Empty State */}
        {filteredCards.length === 0 && (
          <div className="text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
            <p className="text-gray-400 mb-2">No cards found</p>
            {selectedTags.length > 0 ? (
               <p className="text-sm text-gray-500">
                 Try selecting different tags or clear the filter.
               </p>
            ) : (
              <p className="text-sm text-gray-500">
                Create your first card using the form on the left.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
