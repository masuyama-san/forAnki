import axios from 'axios';
import { API_URL } from '../config';

// Axiosの共通インスタンス作成
export const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// レスポンスインターセプター（共通のエラーハンドリング用）
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 共通のエラー処理をここに記述できます
    // 例: 401エラーならログイン画面へリダイレクトなど
    const message = error.response?.data?.message || 'Something went wrong';
    console.error('API Error:', message);
    return Promise.reject(error);
  }
);
