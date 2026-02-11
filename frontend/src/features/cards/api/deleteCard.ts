import { axiosInstance } from '@/lib/axios';

/**
 * カードを削除するAPI
 */
export const deleteCard = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/cards/${id}`);
};
