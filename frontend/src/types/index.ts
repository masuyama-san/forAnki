/**
 * カード情報を管理する型定義
 *
 * 将来的には以下のようなフィールドを追加する可能性があります：
 * - tags: string[] (タグ機能)
 * - createdAt: string (作成日時)
 * - due: string (次回学習日 - Anki連携用)
 */
export interface Card {
  id: number;
  front: string;
  back: string;
  deckName: string;
  tags?: string[];
}
