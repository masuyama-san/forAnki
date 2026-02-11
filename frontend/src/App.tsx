import { useState } from 'react';
import { MainLayout } from './components/Layout/MainLayout';
import { CardForm } from './features/cards/components/CardForm';
import { CardList } from './features/cards/components/CardList';
import { useCards } from './features/cards/hooks/useCards';
import { GenerateCard } from './features/generate/components/GenerateCard';

/**
 * アプリケーションのエントリーポイント
 * 必要に応じて、ここに React Router (Routes, Route) や Context Provider を追加してください。
 */
function App() {
  const { cards, addCard, updateCard } = useCards();
  const [newCard, setNewCard] = useState({ front: '', back: '' });

  const handleCardGenerated = (front: string, back: string) => {
    setNewCard({ front, back });
  };

  return (
    <MainLayout totalCards={cards.length}>
      <div className="grid gap-8 md:grid-cols-[350px_1fr]">
        {/* Sidebar: Add New Card Form */}
        <aside>
          <GenerateCard onCardGenerated={handleCardGenerated} />
          <CardForm
            onAdd={addCard}
            frontValue={newCard.front}
            backValue={newCard.back}
            onFrontChange={(v) => setNewCard(prev => ({ ...prev, front: v }))}
            onBackChange={(v) => setNewCard(prev => ({ ...prev, back: v }))}
          />
        </aside>

        {/* Main Content: Card List */}
        <main>
          <CardList cards={cards} onUpdate={updateCard} />
        </main>
      </div>
    </MainLayout>
  );
}

export default App;
