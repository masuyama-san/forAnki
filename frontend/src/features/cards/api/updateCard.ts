import { axiosInstance } from '@/lib/axios';
import type { Card } from '@/types';

type UpdateCardDTO = {
  front: string;
  back: string;
  tags?: string[];
};

/**
 * 既存のカードを更新するAPI
 */
export const updateCard = async (id: number, data: UpdateCardDTO): Promise<Card> => {
  // backend server converts markdown to html, but expects plain text in request?
  // Let's check server.py: it expects CardRequest which has front/back/tags/use_deck_name
  // And server converts markdown_to_html.
  const response = await axiosInstance.put(`/cards/${id}`, data);
  return response.data;
};
