import type { ReactNode } from 'react';

interface MainLayoutProps {
  children: ReactNode;
  totalCards?: number;
}

/**
 * アプリケーション全体のレイアウトコンポーネント
 * ヘッダー、フッター、サイドバーなどの共通要素をここで定義します。
 */
export function MainLayout({ children, totalCards = 0 }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50 p-8 text-gray-800">
      <div className="max-w-5xl mx-auto">
        <header className="mb-8 flex items-center justify-between border-b pb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">🗂️ ForAnki Card Manager</h1>
            <p className="text-gray-600 mt-1 text-sm">
              Manage your flashcards and export to Obsidian/Anki
            </p>
          </div>
          <div className="text-right">
            <span className="block text-sm font-medium text-gray-500">Total Cards</span>
            <span className="text-2xl font-bold text-blue-600">{totalCards}</span>
          </div>
        </header>

        <main>{children}</main>
        
        {/* TODO: Add Footer here if needed */}
      </div>
    </div>
  );
}
