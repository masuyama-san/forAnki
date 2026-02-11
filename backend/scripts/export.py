import sys
import os

import argparse

# プロジェクトルートをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from instance import config
from src.clients.anki_connect import AnkiConnectClient
from src.clients.obsidian import ObsidianClient
from src.core.converter import create_markdown_content

def main():
    # 0. 設定
    parser = argparse.ArgumentParser(description="Export Anki notes to Markdown")
    parser.add_argument("--deck", "-d", type=str, default=config.ANKI_DECK_NAME, help="Name of the Anki deck to export")
    args = parser.parse_args()
    
    deck_name = args.deck

    client = AnkiConnectClient(config.ANKI_CONNECT_URL)
    obsidian = ObsidianClient(config.OUTPUT_DIR)
    
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        print(f"📁 フォルダを作成しました: {config.OUTPUT_DIR}")

    # 1. デッキ確認
    print(f"🔍 デッキ '{deck_name}' からカードを検索中...")
    query = f'"deck:{deck_name}"'
    note_ids = client.invoke('findNotes', query=query)
    
    if not note_ids:
        print("⚠️ カードが見つかりませんでした。")
        return

    print(f"📋 {len(note_ids)} 件のカードが見つかりました。詳細を取得します...")

    # 2. ノート詳細取得
    notes_info = client.invoke('notesInfo', notes=note_ids)

    # 3. 既存ファイル取得
    existing_files = obsidian.get_existing_files()

    # 4. ファイル書き出し
    count = 0
    updated_count = 0
    renamed_count = 0

    for note in notes_info:
        note_id = note['noteId']
        # 設定からフィールド名を渡す
        title, content = create_markdown_content(note, config.FIELD_FRONT, config.FIELD_BACK)
        
        new_filename = f"{title}_{note_id}.md"
        new_filepath = os.path.join(config.OUTPUT_DIR, new_filename)

        if note_id in existing_files:
            old_filename = existing_files[note_id]
            if old_filename != new_filename:
                old_filepath = os.path.join(config.OUTPUT_DIR, old_filename)
                try:
                    os.remove(old_filepath)
                    print(f"🔄 リネーム: '{old_filename}' -> '{new_filename}'")
                    renamed_count += 1
                except OSError as e:
                    print(f"⚠️ 旧ファイル削除エラー: {e}")
            else:
                updated_count += 1
        else:
            count += 1

        with open(new_filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        total_processed = count + updated_count + renamed_count
        if (total_processed) % 10 == 0:
            print(f"Processing... {total_processed}/{len(note_ids)}")

    print(f"✅ 完了！")
    print(f"  - 新規作成: {count} 件")
    print(f"  - 更新: {updated_count} 件")
    print(f"  - リネーム(更新): {renamed_count} 件")
    print(f"  - 合計: {count + updated_count + renamed_count} 件")

if __name__ == "__main__":
    main()
