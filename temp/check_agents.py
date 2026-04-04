import json, pathlib
d = json.loads(pathlib.Path(r'C:\Users\flyan\.openclaw\openclaw.json').read_text(encoding='utf-8', errors='replace'))
agents = d.get('agents', {})
for k, v in agents.items():
    if isinstance(v, dict):
        print(f'[{k}]')
        print(f'  model: {str(v.get("model","?"))[:80]}')
        print(f'  workspace: {v.get("workspace","?")}' )
        print(f'  channel: {str(v.get("channel","?"))[:80]}')
        print()
