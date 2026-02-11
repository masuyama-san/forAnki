import re
import datetime
import html
import markdown
import markdownify
from src.core.processor import sanitize_filename

def html_to_markdown(html_content):
    """
    HTMLタグをMarkdownに変換する (markdownifyを使用)
    Anki特有のクセなどを吸収するための前処理/後処理を含む
    """
    if not html_content:
        return ""
    
    # Anki特有の挙動への対応:
    # <div>...</div> は改行として扱いたいが、markdownifyはブロックとして扱うため、
    # 場合によっては意図しない空行が入る可能性がある。
    # ここではライブラリの標準挙動を信頼しつつ、よくあるゴミを除去する。

    # markdownify で変換
    # heading_style="atx": # ではなく <h1> に変換されるのを防ぐ (## 形式にする)
    text = markdownify.markdownify(html_content, heading_style="atx")
    
    # 後処理:
    # 連続する空行を整理 (3つ以上 -> 2つに)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 前後の空白削除
    return text.strip()

def create_markdown_content(note, field_front, field_back):
    """
    AnkiのノートデータからMarkdownテキストを生成して、.mdファイルとして保存できるようにする。
    """
    note_id = note['noteId']
    tags = note['tags']
    
    # フィールド取得 (存在しない場合は空文字)
    front_html = note['fields'].get(field_front, {}).get('value', '')
    back_html = note['fields'].get(field_back, {}).get('value', '')

    # HTML -> Markdown 変換
    front = html_to_markdown(front_html)
    back = html_to_markdown(back_html)

    # タイトル生成（表面の最初の行などを利用）
    title = sanitize_filename(front)
    if not title:
        title = f"NoTitle_{note_id}"

    # YAML形式のタグリスト作成
    # Ankiの階層タグ (Parent::Child) を Obsidian形式 (Parent/Child) に変換
    formatted_tags = [t.replace("::", "/") for t in tags]
    tags_str = "\n".join([f"  - {t}" for t in formatted_tags])
    
    today = datetime.date.today().strftime("%Y-%m-%d")

    # テンプレートに埋め込み
    content = f"""---
type: AnkiCards
title: {title}
date: {today}
tags:
{tags_str}
id: {note_id}
---

# Card: {title}

## Question
{front}

## Answer
{back}
"""
    return title, content

def parse_anki_markdown(content):
    """
    Markdownからデータを抽出
    JSON形式でID、タグ、表面、裏面を返してAnkiへの登録/更新に利用する
    """
    data = {"id": None, "tags": [], "front": "", "back": ""}
    
    # YAML Frontmatter
    yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if yaml_match:
        yaml_text = yaml_match.group(1)
        # ID
        id_match = re.search(r'^id:\s*(.+)$', yaml_text, re.MULTILINE)
        if id_match:
            raw_id = id_match.group(1).strip()
            if raw_id and raw_id not in ["id番号", "新規カード"]: # "id番号", "新規カード" はIDなしとみなす
                try:
                    data["id"] = int(raw_id)
                except ValueError:
                    print(f"⚠️ Warning: Invalid ID format '{raw_id}'. Treating as new card.")
                    data["id"] = None
        # Tags
        tags_match = re.search(r'^tags:\s*\n((?:\s*-\s+.*\n?)+)', yaml_text, re.MULTILINE)
        if tags_match:
            # "- " を除去してリスト化し、Obsidian形式 (/) から Anki形式 (::) に戻す
            data["tags"] = [
                line.strip().replace("- ", "").replace("/", "::") 
                for line in tags_match.group(1).strip().split('\n')
            ]

    # Body
    body_text = content[yaml_match.end():] if yaml_match else content
    q_match = re.search(r'## Question\s*\n(.*?)\n## Answer', body_text, re.DOTALL)
    if q_match: data["front"] = q_match.group(1).strip()
    a_match = re.search(r'## Answer\s*\n(.*)', body_text, re.DOTALL)
    if a_match: data["back"] = a_match.group(1).strip()

    return data

def markdown_to_html(text):
    """
    Markdownライブラリを使用した変換
    Anki向けに改行(nl2br)やテーブル(tables)などの拡張を有効化
    """
    if not text:
        return ""
    
    # 拡張機能:
    # - nl2br: 改行を <br> に変換 (Ankiのデフォルト挙動に合わせる)
    # - fences: コードブロック対応
    # - tables: 表組み対応
    # - sane_lists: リストの挙動を標準的にする
    extensions = ['nl2br', 'fenced_code', 'tables', 'sane_lists']
    
    html_content = markdown.markdown(text, extensions=extensions)
    
    return html_content
