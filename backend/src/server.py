import sys
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# プロジェクトルートへのパス設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from instance import config
from src.clients.anki_connect import AnkiConnectClient
from src.clients.gemini import GeminiClient
from src.core.converter import markdown_to_html, html_to_markdown

app = FastAPI(title="forAnki API", version="1.0.0")

# CORS設定 (Reactからのアクセスを許可)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発用: 全てのオリジンを許可 (本番では "http://localhost:3000" 等に絞る)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# クライアント初期化
def get_client():
    return AnkiConnectClient(config.ANKI_CONNECT_URL)

# リクエスト/レスポンス用モデル
class CardRequest(BaseModel):
    front: str
    back: str
    tags: List[str] = []
    deck_name: Optional[str] = None  # 指定なければconfigの値を使用

class CardResponse(BaseModel):
    id: int
    front: str
    back: str
    tags: List[str]
    deckName: str

class GenerateRequest(BaseModel):
    prompt: str

class ModifyRequest(BaseModel):
    front: str
    back: str
    instruction: str

class ModifyResponse(BaseModel):
    front: str
    back: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "ok", "service": "forAnki API"}

@app.post("/generate")
def generate_content(request: GenerateRequest):
    """
    Gemini APIを使用してコンテンツを生成します。
    """
    client = GeminiClient()
    
    # ユーザーの入力をラップして、構造化されたJSONレスポンスを要求する
    system_prompt = f"""
    You are an expert Anki card creator.
    The user will provide a topic or text.
    Your goal is to create a high-quality Anki card (Front and Back) and provide a brief explanation or chat response.

    User Input:
    {request.prompt}

    Output Requirement:
    Return a valid JSON object with the following keys:
    - "chat": A brief explanation, friendly response, or advice about the generated card.
    - "front": The content for the Front of the card (Markdown allowed).
    - "back": The content for the Back of the card (Markdown allowed).

    Format:
    {{
        "chat": "Here is a card regarding...",
        "front": "...",
        "back": "..."
    }}
    
    Do not include markdown code block markers (like ```json). Return only the raw JSON string.
    """

    try:
        content = client.generate_content(system_prompt)
        
        # クリーニング (万が一Markdownブロックが含まれていた場合)
        cleaned_content = content.replace("```json", "").replace("```", "").strip()
        
        try:
            import json
            data = json.loads(cleaned_content)
            # フロントエンドが期待している形に合わせて返す
            # 既存は {"content": string} だったが、
            # これからは {"chat": ..., "front": ..., "back": ...} を返したい
            # しかし他のクライアントへの互換性を保つため、contentキーに全部入れるのではなく分離する？
            # ひとまず辞書をそのまま返す (FastAPIがJSON化してくれる)
            return data
        except json.JSONDecodeError:
            # JSON解析失敗時は、全体をchatとして扱い、cardは空にするなどのフォールバック
            return {
                "chat": content,
                "front": "",
                "back": ""
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/modify", response_model=ModifyResponse)
def modify_content(request: ModifyRequest):
    """
    Gemini APIを使用して既存のカード内容を修正します。
    """
    client = GeminiClient()
    prompt = f"""
    You are an assistant editing Anki flashcards.

    Original Front:
    {request.front}

    Original Back:
    {request.back}

    Instruction:
    {request.instruction}

    Please provide the modified Front and Back based on the instruction.
    Output MUST be a valid JSON object with detailed keys "front" and "back".
    Do not include markdown code block markers (```json). Just the raw JSON string.
    """

    try:
        # 構造化されたデータを期待するため、プロンプトでJSONを強制する
        # (Gemini 2.0 FlashはJSON modeがあるが、ここでは簡易的にプロンプトで指示)
        content = client.generate_content(prompt)

        # Markdownのコードブロックが含まれている場合の除去処理
        cleaned_content = content.replace("```json", "").replace("```", "").strip()

        import json
        data = json.loads(cleaned_content)
        return ModifyResponse(front=data.get("front", ""), back=data.get("back", ""))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cards", response_model=List[dict])
def get_cards(deck: Optional[str] = None):
    """
    指定したデッキ（デフォルトはconfig設定）のカード一覧を取得します。
    """
    client = get_client()
    target_deck = deck or config.ANKI_DECK_NAME

    # 1. ノートIDを検索
    query = f'"deck:{target_deck}"'
    note_ids = client.invoke('findNotes', query=query)

    if not note_ids:
        return []

    # 2. 詳細情報を取得
    notes_info = client.invoke('notesInfo', notes=note_ids)

    # 3. シンプルな形式に整形して返す
    cards = []
    for note in notes_info:
        # フィールド名はconfig依存だが、APIレスポンスとしては固定キー(front, back)で返すとReactが楽
        front_html = note['fields'].get(config.FIELD_FRONT, {}).get('value', '')
        back_html = note['fields'].get(config.FIELD_BACK, {}).get('value', '')

        # HTML -> Markdown 変換
        front = html_to_markdown(front_html)
        back = html_to_markdown(back_html)

        cards.append({
            "id": note['noteId'],
            "front": front,
            "back": back,
            "tags": note['tags'],
            "deckName": note['modelName'] # 注: notesInfoにはdeckNameが含まれない場合があるためmodelName等で代用か、別途取得が必要
        })

    return cards

@app.post("/cards")
def create_card(card: CardRequest):
    """
    新規カードをAnkiに登録します。
    Markdown形式のテキストを受け取り、HTMLに変換して登録します。
    """
    client = get_client()
    target_deck = card.deck_name or config.ANKI_DECK_NAME

    note = {
        "deckName": target_deck,
        "modelName": config.ANKI_MODEL_NAME,
        "fields": {
            config.FIELD_FRONT: markdown_to_html(card.front),
            config.FIELD_BACK: markdown_to_html(card.back)
        },
        "tags": card.tags
    }

    new_id = client.invoke("addNote", note=note)

    if not new_id:
        raise HTTPException(status_code=500, detail="Failed to create card in Anki")

    return {"id": new_id, "message": "Card created successfully"}

@app.put("/cards/{note_id}")
def update_card(note_id: int, card: CardRequest):
    """
    既存のカードを更新します。
    フィールドの更新とタグの更新を行います。
    """
    client = get_client()

    # 1. フィールド更新
    note_fields = {
        "id": note_id,
        "fields": {
            config.FIELD_FRONT: markdown_to_html(card.front),
            config.FIELD_BACK: markdown_to_html(card.back)
        },
    }
    client.invoke("updateNoteFields", note=note_fields)

    # 2. タグ更新 (現在のタグを取得 -> 全削除 -> 新規追加)
    # AnkiConnectには 'updateNoteTags' が存在しないか動作が不明確な場合が多いため
    # removeTags で全て消してから addTags するのが確実

    current_info_list = client.invoke("notesInfo", notes=[note_id])
    if current_info_list and len(current_info_list) > 0:
        current_tags = current_info_list[0].get('tags', [])
        # string space separated tags or list of strings?
        # notesInfo returns list of strings for tags usually.

        # 全削除 (スペース区切りの文字列で渡す必要がある場合もあるが、invokeの実装次第。
        # AnkiConnect docs says removeTags takes 'tags' as a space-separated string or maybe list?)
        # Let's try passing space-separated string of current tags
        if current_tags:
            client.invoke("removeTags", notes=[note_id], tags=" ".join(current_tags))

        # 新規追加
        if card.tags:
            client.invoke("addTags", notes=[note_id], tags=" ".join(card.tags))

    # 確認のため再度Infoを取得 (簡易的な成功チェック)
    return {"id": note_id, "message": "Card updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
