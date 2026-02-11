# ForAnki Project

AnkiとMarkdown(Obsidian)を連携させるためのツール群です。
フロントエンド(React)とバックエンド(FastAPI/Python)のモノレポ構成になっています。

## 主な機能

- **Anki連携**: AnkiConnectを利用して、ローカルのAnkiデッキからカードを取得・作成・更新
- **Markdown対応**: カードの裏面・表面でMarkdown記法をサポート
- **AI支援機能**: Google Gemini APIを利用して、カード内容の自動生成や既存カードの推敲・修正が可能

## プロジェクト構成

- **frontend/**: React + Vite によるフロントエンドアプリケーション
- **backend/**: Python (FastAPI) によるバックエンド API およびスクリプト

## クイックスタート (開発環境)

ルートディレクトリにある `dev.sh` を使用することで、バックエンドとフロントエンドを一度に起動できます。

### 前提条件
- Python 3.x
- Node.js (npm)

### 初回セットアップ & 起動

```bash
# 実行権限がない場合
chmod +x dev.sh

# 開発環境の起動
./dev.sh
```

このスクリプトは以下の処理を自動的に行います：
1. **Backend**: 仮想環境(`.venv`)の作成・有効化、ライブラリインストール、サーバー起動 (port: 8000)
2. **Frontend**: 開発サーバーの起動 (port: 5173)

起動後は以下のURLにアクセスしてください。
- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs

---

## 個別の開発手順

詳細な仕様や個別での実行方法は、各ディレクトリの README を参照してください。

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

