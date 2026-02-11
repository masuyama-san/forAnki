import os
import re

class ObsidianClient:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def get_existing_files(self):
        """
        出力ディレクトリ内のファイルをスキャンし、Note ID とファイルパスの対応マップを作成する
        戻り値: { note_id (int): filename (str) }
        """
        existing_files = {}
        if not os.path.exists(self.output_dir):
            return existing_files

        pattern = re.compile(r'_(\d+)\.md$')

        for filename in os.listdir(self.output_dir):
            if not filename.endswith(".md"):
                continue
            
            match = pattern.search(filename)
            if match:
                note_id = int(match.group(1))
                existing_files[note_id] = filename

        return existing_files

    def update_file_id(self, filepath, new_id):
        """Obsidianファイルの id: 部分を書き換える"""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # "id: id番号", "id: 新規カード", または "id: (空白)" を "id: 12345..." に置換
        new_content = re.sub(
            r'^id:\s*(id番号|新規カード|)$', 
            f'id: {new_id}', 
            content, 
            count=1, 
            flags=re.MULTILINE
        )
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"💾 ファイルを更新しました: ID {new_id} を書き込みました")
