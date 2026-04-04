# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\flyan\.openclaw\workspace\reports\2026年3月银行业金融科技AI咨询报告_v3.md"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print("Total chars:", len(content))
print("Total lines:", len(lines))

# Count articles
article_markers = [l for l in lines if l.startswith('\u25cf [')]
print("Articles found:", len(article_markers))

# Show last 60 lines
print("\n--- Last 60 lines ---")
for l in lines[-60:]:
    print(repr(l)[:100])
