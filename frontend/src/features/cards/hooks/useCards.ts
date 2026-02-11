import { useState, useEffect, useCallback } from 'react';
import type { Card } from '../../../types';
import * as cardApi from '../api';

/**
 * カードデータのCRUD操作を管理するカスタムフック
 */
export const useCards = () => {
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCards = useCallback(async () => {
    setLoading(true);
    try {
      const data = await cardApi.getCards();
      setCards(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch cards');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCards();
  }, [fetchCards]);

  const addCard = async (front: string, back: string, deckName: string) => {
    try {
      await cardApi.createCard({ front, back, deckName });
      await fetchCards();
    } catch (err) {
      console.error('Failed to create card', err);
    }
  };

  const updateCard = async (id: number, front: string, back: string, tags?: string[]) => {
    try {
      await cardApi.updateCard(id, { front, back, tags });
      await fetchCards();
    } catch (err) {
      console.error('Failed to update card', err);
    }
  };

  return { cards, loading, error, addCard, updateCard };
};
