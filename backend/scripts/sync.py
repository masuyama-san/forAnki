import sys
import os
import argparse
import glob

# プロジェクトルートをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from instance import config
from src.clients.anki_connect import AnkiConnectClient
from src.clients.obsidian import ObsidianClient
from src.core.converter import parse_anki_markdown, markdown_to_html

def sync_file(file_path, client, obsidian):
    print(f"Processing: {file_path}")
    if not os.path.exists(file_path):
        print(f"エラー: {file_path} が見つかりません。")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    data = parse_anki_markdown(content)
    
    if not data["front"] or not data["back"]:
        print(f"⚠️ {file_path}: Question または Answer が見つかりませんでした。スキップします。")
        return

    # 2. IDまたは内容で既存チェック
    if data["id"] is None:
        # 表面フィールドで検索
        query = f'"note:{config.ANKI_MODEL_NAME}" "{data["front"]}"'
        existing_ids = client.invoke('findNotes', query=query)
        
        if existing_ids:
            print(f"⚠️ 既存のカードが見つかりました (ID: {existing_ids[0]})。IDをファイルに追記して更新します。")
            data["id"] = existing_ids[0]
            obsidian.update_file_id(file_path, data["id"])

    # 3. 追加または更新
    if data["id"] is None:
        # 追加
        print("🆕 新規カードとして登録します...")
        note = {
            "deckName": config.ANKI_DECK_NAME,
            "modelName": config.ANKI_MODEL_NAME,
            "fields": {
                config.FIELD_FRONT: markdown_to_html(data["front"]),
                config.FIELD_BACK: markdown_to_html(data["back"])
            },
            "tags": data["tags"]
        }
        new_id = client.invoke("addNote", note=note)
        
        if new_id:
            print(f"✅ 登録成功！ Note ID: {new_id}")
            obsidian.update_file_id(file_path, new_id)
            
    else:
        # 更新
        print(f"🔄 既存カード(ID: {data['id']}) を更新します...")
        note = {
            "id": data["id"],
            "fields": {
                config.FIELD_FRONT: markdown_to_html(data["front"]),
                config.FIELD_BACK: markdown_to_html(data["back"])
            },
        }
        # 注意: タグの更新ロジックはAnkiConnectでは別になっている (addTags/removeTags/updateNoteTags)
        # 現時点では、オリジナルのスクリプトのロジックに従い、フィールドのみを更新する
        result = client.invoke("updateNoteFields", note=note)
        if result is None: 
            print("✅ 更新成功！")

def main():
    # 0. 設定
    parser = argparse.ArgumentParser(description="Sync Markdown files to Anki")
    parser.add_argument("--dir", "-d", type=str, help="Subdirectory to sync (relative to SYNC_BASE_DIR)")
    parser.add_argument("--file", "-f", type=str, help="Specific file to sync")
    args = parser.parse_args()

    client = AnkiConnectClient(config.ANKI_CONNECT_URL)
    obsidian = ObsidianClient(config.OUTPUT_DIR) # update_file_idメカニズムに使用される。
    # 注意: get_existing_filesを使用する場合、ObsidianClientはファイルの検索にconfig.OUTPUT_DIRに依存する可能性があるが、
    # update_file_idは渡された特定のファイルパスを使用するため問題ない。

    files_to_sync = []
    base_dir = config.SYNC_BASE_DIR

    if args.dir:
        target_dir = os.path.join(base_dir, args.dir)
        if not os.path.exists(target_dir):
            print(f"エラー: ディレクトリ '{target_dir}' が見つかりません。")
            return
        
        # ディレクトリ内のすべての.mdファイルを同期する
        files_to_sync = glob.glob(os.path.join(target_dir, "*.md"))
        if not files_to_sync:
            print(f"⚠️ '{target_dir}' にMarkdownファイルが見つかりませんでした。")
            return
        print(f"📁 ディレクトリ同期: '{target_dir}' から {len(files_to_sync)} 個のファイルを処理します。")

    elif args.file:
        files_to_sync = [args.file]
    
    else:
        # Default legacy behavior
        if config.TARGET_FILE:
            files_to_sync = [config.TARGET_FILE]
        else:
            print("エラー: 対象ファイルまたはディレクトリを指定してください。")
            return

    # Process files
    for file_path in files_to_sync:
        try:
            sync_file(file_path, client, obsidian)
        except Exception as e:
            print(f"❌ エラー ({file_path}): {e}")

if __name__ == "__main__":
    main()
