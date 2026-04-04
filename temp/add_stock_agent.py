import json, pathlib

p = pathlib.Path(r'C:\Users\flyan\.openclaw\openclaw.json')
d = json.loads(p.read_text(encoding='utf-8'))

# 1. 在 agents.list 里加 stock
agents_list = d['agents']['list']
if not any(a.get('id') == 'stock' for a in agents_list):
    agents_list.append({
        "id": "stock",
        "name": "stock",
        "workspace": "C:\\Users\\flyan\\.openclaw\\workspace\\agents-workspaces\\stock",
        "agentDir": "C:\\Users\\flyan\\.openclaw\\workspace\\agents\\stock\\agent"
    })
    print('Added stock to agents list')
else:
    print('Stock already in agents list')

# 2. 在 main 的 subagents.allowAgents 里加 stock
for a in agents_list:
    if a.get('id') == 'main':
        allow = a.setdefault('subagents', {}).setdefault('allowAgents', [])
        if 'stock' not in allow:
            allow.append('stock')
            print('Added stock to main allowAgents')
        break

p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print('openclaw.json updated')
