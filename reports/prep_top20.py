# -*- coding: utf-8 -*-
import json, os, re

BASE = r"C:\Users\flyan\.openclaw\workspace\reports"

# Load v4_final.json for scores and march flags
with open(os.path.join(BASE, 'v4_final.json'), encoding='utf-8') as f:
    raw = json.load(f)
arts = raw if isinstance(raw, list) else raw.get('final_selection', [])

# Load v4_articles_extracted.json for summaries (from v4.md)
with open(os.path.join(BASE, 'v4_articles_extracted.json'), encoding='utf-8') as f:
    extracted = json.load(f)

# Build URL->summary map from extracted
url_to_summary = {}
for a in extracted:
    url_to_summary[a.get('url', '')] = a.get('summary', '')

# Filter march 2026, sort by score desc
march = [a for a in arts if a.get('_march2026')]
march_sorted = sorted(march, key=lambda x: -(x.get('_score') or 0))

# Take top 20
top20 = march_sorted[:20]

# Merge summaries
result = []
for a in top20:
    url = a.get('url', '')
    summary = url_to_summary.get(url, a.get('summary', ''))
    result.append({
        'title': a.get('title', ''),
        'source': a.get('source', ''),
        'date': a.get('date_text') or a.get('datetime', '')[:10],
        'score': a.get('_score') or 0,
        'url': url,
        'summary': summary
    })
    print(f"[{a.get('_score')}] {a.get('source','')[:12]} | {a.get('title','')[:35]}")
    print(f"  Summary len: {len(summary)}")

# Save
out_path = os.path.join(BASE, 'top20_march2026.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(result)} articles to {out_path}")
