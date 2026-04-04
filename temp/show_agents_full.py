import json, pathlib
d = json.loads(pathlib.Path(r'C:\Users\flyan\.openclaw\openclaw.json').read_text(encoding='utf-8', errors='replace'))
agents = d.get('agents', {})
for k, v in agents.items():
    if isinstance(v, dict) and k != 'defaults':
        print(f'--- [{k}] ---')
        print(json.dumps(v, ensure_ascii=False, indent=2))
        print()
