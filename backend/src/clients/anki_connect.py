import json
import urllib.request
import sys
import os

# 必要に応じてインポートを解決するためにプロジェクトルートを sys.path に追加する、
# ただし、通常はモジュールとして実行するか PYTHONPATH を設定する方が良い。
# 現時点では、インポートが機能するコンテキストから実行されるか、相対インポートを使用すると仮定する。

class AnkiConnectClient:
    def __init__(self, url="http://localhost:8765"):
        self.url = url

    def invoke(self, action, **params):
        requestJson = json.dumps({'action': action, 'params': params, 'version': 6}).encode('utf-8')
        try:
            req = urllib.request.Request(self.url, requestJson)
            with urllib.request.urlopen(req) as response:
                resp = json.load(response)
                
            if resp.get('error') is not None:
                raise Exception(resp['error'])
            return resp['result']
        except Exception as e:
            print(f"❌ AnkiConnect Error: {e}")
            return None
