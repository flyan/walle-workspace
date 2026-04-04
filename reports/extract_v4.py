# -*- coding: utf-8 -*-
"""
extract_v4.py
Parse v4.md to extract all articles, then generate v5 with:
- No tables
- Consumer finance as separate category
- Links only at end
- Better summary quality (reuse v4 summaries)
"""

import json, re, os

BASE = r"C:\Users\flyan\.openclaw\workspace\reports"

# --- 1. Load v4_final.json for URLs ---
with open(os.path.join(BASE, 'v4_final.json'), encoding='utf-8') as f:
    raw = json.load(f)
arts_json = raw if isinstance(raw, list) else raw.get('final_selection', [])

# Build URL map by title (normalized)
def norm(t):
    return re.sub(r'\s+', '', t).lower()[:30]

url_map = {}
for a in arts_json:
    t = norm(a.get('title', ''))
    url = a.get('url') or a.get('link') or ''
    if t and url:
        url_map[t] = url

print(f"URL map built: {len(url_map)} entries")

# --- 2. Parse v4.md to extract articles ---
with open(os.path.join(BASE, '2026年3月咨询报告_v4.md'), encoding='utf-8') as f:
    v4 = f.read()

# Each article block looks like:
# **N. Title**\n[Source] [Date] 评分：Xscore\n> Summary\n
article_pattern = re.compile(
    r'\*\*(\d+)\.\s*(.+?)\*\*\s*\n'
    r'\[(.+?)\]\s*\[([^\]]+)\]\s*评分[:：]\s*(\d+)分\s*\n'
    r'>\s*(.+?)(?=\n\n|\Z)',
    re.DOTALL
)

articles = []
for m in article_pattern.finditer(v4):
    num = int(m.group(1))
    title = m.group(2).strip()
    source = m.group(3).strip()
    date = m.group(4).strip()
    score = int(m.group(5))
    summary = re.sub(r'\s+', ' ', m.group(6).strip())
    
    # Get URL
    url = url_map.get(norm(title), '')
    
    articles.append({
        'num': num,
        'title': title,
        'source': source,
        'date': date,
        'score': score,
        'summary': summary,
        'url': url,
        'march': '2026-03' in date,
    })

print(f"Extracted {len(articles)} articles from v4.md")
for a in articles[:3]:
    print(f"  #{a['num']} [{a['score']}] {a['source']}: {a['title'][:40]}")
    print(f"     Summary len: {len(a['summary'])} chars")
    print(f"     URL: {a['url'][:60] if a['url'] else 'MISSING'}")

# Save for subagent to use
out_path = os.path.join(BASE, 'v4_articles_extracted.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print(f"Saved: {out_path} ({os.path.getsize(out_path)} bytes)")
