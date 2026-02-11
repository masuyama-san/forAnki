from fastapi import FastAPI
from pydantic import BaseModel

# 1. アプリケーションのインスタンスを作成
app = FastAPI()

# 2. データモデルを定義 (Pydantic)
# これだけで型チェックとドキュメント生成が自動で行われます
class Card(BaseModel):
    front: str
    back: str
    deck_name: str = "Default Deck"  # デフォルト値

# 3. ルート (エンドポイント) の定義: GETリクエスト
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!", "status": "running"}

# 4. パスパラメータの例: GET /items/5
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "description": "This is a sample item."}

# 5. データ送信の例: POST /cards/
# リクエストボディとしてJSONを受け取ります
@app.post("/cards/")
async def create_card(card: Card):
    # ここでAnkiへの登録処理などを行うイメージ
    return {
        "status": "success",
        "received_card": card,
        "message": f"Created card: {card.front}"
    }

# 実行方法 (ターミナルで以下を実行):
# uvicorn tests.try_fastapi:app --reload
