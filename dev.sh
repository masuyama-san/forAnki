#!/bin/bash

# 文字色設定
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 終了時(Ctrl+C)に子プロセスも道連れにする設定
trap "kill 0" EXIT

echo -e "${GREEN}🚀 Starting ForAnki Development Environment...${NC}"

# --- Backend ---
echo -e "${BLUE}[Backend]${NC} Setting up..."
cd backend
# 仮想環境の作成とアクティベート
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
# 仮想環境が存在しない場合は作成
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

echo -e "${BLUE}[Backend]${NC} Starting Server on http://localhost:8000 ..."
# バックグラウンドで起動 (&)
uvicorn src.server:app --reload --port 8000 &
cd ..

# --- Frontend ---
echo -e "${BLUE}[Frontend]${NC} Starting React App..."
cd frontend
# 依存関係がまだインストールされていない場合のガードを入れるならここだが、
# 今回はシンプルに実行する
npm run dev &
cd ..

# プロセスが終了するのを待機
wait
