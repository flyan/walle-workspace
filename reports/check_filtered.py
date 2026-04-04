#!/usr/bin/env python3
import json

with open(r'C:\Users\flyan\.openclaw\workspace\reports\filtered_articles.json','r',encoding='utf-8') as f:
    arts = json.load(f)

print(f'过滤后文章数: {len(arts)}')
sources = {}
dates = {}
for a in arts:
    s = a.get('source','未知')
    sources[s] = sources.get(s,0)+1
    d = a.get('datetime','')[:7] if a.get('datetime') else '未知'
    dates[d] = dates.get(d,0)+1

print('来源分布:', sorted(sources.items(),key=lambda x:-x[1])[:5])
print('日期分布:', sorted(dates.items(),key=lambda x:-x[1])[:5])
print()
for a in arts[:3]:
    print(f"  - [{a.get('source')}] {a.get('title','无标题')[:30]} ({a.get('datetime','')[:10]}) 评分:{a.get('quality_score')}")