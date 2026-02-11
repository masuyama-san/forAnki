import re

def sanitize_filename(text):
    """ファイル名に使えない文字を置換し、長さを制限する"""
    text = re.sub(r'[\\/*?:"<>|]', "", text) # 禁止文字を除去
    text = text.replace("\n", " ")           # 改行をスペースに
    return text[:50].strip()                 # 50文字制限
