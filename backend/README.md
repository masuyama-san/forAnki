# ForAnki Backend

AnkiとMarkdown(Obsidian)を連携させるためのバックエンドサービスおよびツール群です。

## ディレクトリ構成
- `src/`: FastAPI サーバーおよびアプリケーションロジック
- `scripts/`: 単体実行用スクリプト (Ankiエクスポートなど)
- `instance/`: 設定ファイル
- `tests/`: テストコード

## セットアップ (個別実行する場合)

ルートディレクトリの `dev.sh` を使用する場合は以下の手順は不要ですが、バックエンド単体で開発・テストを行う場合は以下のようにセットアップしてください。

### 1. 仮想環境の作成とライブラリのインストール
```bash
# backendディレクトリにて
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 設定
`instance/` 内の `config.py` や `.env` を環境に合わせて編集してください。

#### 環境変数 (.env)
ルート直下に `.env` ファイルを作成してください（`.env.example` 参照）。
Gemini API を利用する場合は `GEMINI_API_KEY` の設定が必須です。

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.0-flash
```

## サーバー起動

```bash
uvicorn src.server:app --reload
```

## API エンドポイント

- **GET /cards**: カード一覧取得
- **POST /cards**: カード作成
- **PUT /cards/{id}**: カード更新
- **POST /generate**: プロンプトからのコンテンツ生成 (Gemini)
- **POST /generate/modify**: 既存コンテンツの修正 (Gemini)

## スクリプトの使い方

### Export (Anki -> Markdown)
AnkiのデータをMarkdownファイルとして出力するスクリプトです。

```bash
python scripts/export.py
```
`instance/config.py` で指定されたデッキのカードをMarkdownとして出力します。

オプションでデッキ名を指定して実行することも可能です：
```bash
python scripts/export.py --deck "デッキ名"
```


