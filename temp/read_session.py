import json, pathlib
p = pathlib.Path(r'C:\Users\flyan\.openclaw\agents\writer\sessions\45f8f493-221f-4751-a3ff-1673c89993c8.jsonl')
lines = p.read_text(encoding='utf-8', errors='replace').strip().split('\n')
for line in lines[-15:]:
    try:
        obj = json.loads(line)
        if obj.get('type') == 'message':
            msg = obj.get('message', {})
            role = msg.get('role', '?')
            content = msg.get('content', '')
            ts = obj.get('timestamp', '')[:19]
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get('type') == 'text':
                        text = c.get('text', '')[:300]
                        print(f'[{ts}][{role}]: {text}')
                    elif isinstance(c, dict) and c.get('type') == 'tool_use':
                        print(f'[{ts}][{role}][TOOL]: {c.get("name","")} - {str(c.get("input",""))[:150]}')
            elif isinstance(content, str):
                print(f'[{ts}][{role}]: {content[:300]}')
    except Exception as e:
        print('ERR:', e)
