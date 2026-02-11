import { axiosInstance } from '@/lib/axios';
import type { Card } from '@/types';

type CreateCardDTO = Omit<Card, 'id'> & { deckName: string };

/**
 * 新しいカードを作成するAPI
 */
export const createCard = async (data: CreateCardDTO): Promise<Card> => {
  const response = await axiosInstance.post('/cards', data);
  return response.data;
};
