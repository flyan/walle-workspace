# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\flyan\.openclaw\workspace\reports\filtered_articles_v3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Show some summaries
for i, a in enumerate(data['final_selection'][:15]):
    title = a.get('title', '')
    summary = a.get('summary', '')
    print(f'--- {i+1}. {title[:60]} ---')
    print(f'Summary: {summary[:200]}')
    print()
