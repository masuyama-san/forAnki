
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Anki 設定
ANKI_DECK_NAME = os.getenv("ANKI_DECK_NAME")
ANKI_MODEL_NAME = os.getenv("ANKI_MODEL_NAME")
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL")

# ファイル設定
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "export_sample")
SYNC_BASE_DIR = os.getenv("SYNC_BASE_DIR", ".") # 同期用ベースディレクトリ
TARGET_FILE = os.getenv("TARGET_FILE", "sample_anki_card.md")

# フィールド名
FIELD_FRONT = os.getenv("FIELD_FRONT", "表面")
FIELD_BACK = os.getenv("FIELD_BACK", "裏面")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
