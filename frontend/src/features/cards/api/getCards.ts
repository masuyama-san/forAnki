import { axiosInstance } from '@/lib/axios';
import type { Card } from '@/types';

/**
 * すべてのカードを取得するAPI
 */
export const getCards = async (): Promise<Card[]> => {
  const response = await axiosInstance.get('/cards');
  return response.data;
};
