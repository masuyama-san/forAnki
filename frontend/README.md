# ForAnki Frontend

ForAnki プロジェクトのフロントエンドアプリケーションです。
React + TypeScript + Vite で構築されています。

## 技術スタック

- React
- TypeScript
- Vite
- Tailwind CSS

## セットアップ & 起動 (個別実行する場合)

ルートディレクトリの `dev.sh` を使用する場合は以下の手順は不要です。

```bash
# frontendディレクトリにて

# 依存パッケージのインストール
npm install

# 開発サーバーの起動
npm run dev
```

## ビルド

```bash
npm run build
```

## ディレクトリ構成

保守性と拡張性を考慮し、機能(Features)ベースのディレクトリ構成を採用しています。

```
src/
├── assets/         # 画像、アイコン、グローバルなCSS
├── components/     # プロジェクト全体で使う共通部品（Layoutなど）
├── config/         # 環境変数や定数
├── features/       # 【重要】機能ごとのフォルダ (例: cards)
│   ├── cards/      # カード表示・管理・編集
│   │   ├── components/
│   │   └── hooks/
│   └── generate/   # AI生成・修正機能
│       ├── api/    # 生成系API呼び出し
│       └── components/ # 生成・修正用UI
├── hooks/          # アプリ全体で使う共通カスタムフック
├── lib/            # ライブラリの初期化（axios, firebaseなど）
├── services/       # 外部API通信などのビジネスロジック（featuresに入れない場合）
├── types/          # アプリ全体で使う共有型定義
└── utils/          # 共通のユーティリティ関数（日付操作など）
```

- **Features (`src/features/`)**:
  各機能をここに集約します。例えば「カード管理機能」であれば `src/features/cards` とし、その下に `components`, `hooks`, `types` などを配置することで、機能単位での独立性を高めています。

- **Components (`src/components/`)**:
  アプリケーション全体で横断的に使用されるUI部品（ヘッダー、ボタン、レイアウトなど）を配置します。

- **Types (`src/types/`)**:
  アプリケーション全体で使用される共通の型定義（ドメインモデルなど）を配置します。
