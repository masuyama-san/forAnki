import { axiosInstance as axios } from '@/lib/axios';

export type ModifyRequest = {
  front: string;
  back: string;
  instruction: string;
};

export type ModifyResponse = {
  front: string;
  back: string;
};

export const modifyContent = async (data: ModifyRequest): Promise<ModifyResponse> => {
  const response = await axios.post<ModifyResponse>('/generate/modify', data);
  return response.data;
};
