import { axiosInstance as axios } from '@/lib/axios';

export type GenerateRequest = {
  prompt: string;
};

export type GenerateResponse = {
  chat: string;
  front: string;
  back: string;
};

export const generateContent = async (data: GenerateRequest): Promise<GenerateResponse> => {
  const response = await axios.post<GenerateResponse>('/generate', data);
  // 古いAPIレスポンスとの互換性（念のため）
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  if ('content' in (response.data as any)) {
      return {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          chat: (response.data as any).content,
          front: '',
          back: ''
      };
  }
  return response.data;
};
