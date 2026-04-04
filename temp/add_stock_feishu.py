import json, pathlib

p = pathlib.Path(r'C:\Users\flyan\.openclaw\openclaw.json')
d = json.loads(p.read_text(encoding='utf-8'))

# 1. 加飞书 stock 账号
accounts = d['channels']['feishu']['accounts']
if 'stock' not in accounts:
    accounts['stock'] = {
        "appId": "cli_a94f8217b1f81bd2",
        "appSecret": "rZEpowPYNdNtO0YQczVhXyzmzYqWPbmG",
        "connectionMode": "websocket",
        "domain": "feishu",
        "groupPolicy": "open"
    }
    print('Added stock feishu account')
else:
    print('Stock account already exists')

# 2. 加 binding
bindings = d['bindings']
if not any(b.get('agentId') == 'stock' for b in bindings):
    bindings.append({
        "agentId": "stock",
        "match": {
            "channel": "feishu",
            "accountId": "stock"
        }
    })
    print('Added stock binding')
else:
    print('Stock binding already exists')

p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print('Done')
