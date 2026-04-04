import json
import re
from datetime import datetime

# Read the JSON file
with open('C:\\Users\\flyan\\.openclaw\\workspace\\reports\\search_results_20260322_2028.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# List of reputable sources from our FINTECH_ACCOUNTS.md
reputable_sources = [
    '机器之心', '量子位', '新智元', '极客公园', '智东西',
    '馨金融', '零壹财经', '未央网', '一本财经', '十字财经',
    '移动支付网', '支付百科', '消金界', '第一消费金融',
    '轻金融', '中国银行保险报', '银行家杂志', '愉见财经',
    '零售银行', '信贷风险管理', '支行长', '银行科技研究社',
    '行长要参', '金融数字化观察', '星图金融研究院', 'CF40',
    '第一财经', '澎湃新闻', '36氪', '钛媒体', '东方财富网'
]

# Filter articles by date (March 2026) and source quality
march_articles = []
for article in data.get('articles', []):
    # Check if date is in March 2026
    date_str = article.get('datetime', '')
    if not date_str:
        continue
    
    # Extract date (simplified check for March 2026)
    if '2026-03' in date_str:
        march_articles.append(article)

print(f"Total articles in March 2026: {len(march_articles)}")

# Categorize articles
banking_articles = []
fintech_articles = []
ai_articles = []

# Keywords for categorization
banking_keywords = ['银行', '信贷', '存款', '贷款', '网点', '柜员', '客户经理', '零售银行']
fintech_keywords = ['支付', '金融科技', '数字人民币', '区块链', '消费金融', '风控', '监管科技']
ai_keywords = ['AI', '人工智能', '大模型', '生成式AI', '机器学习', '深度学习']

for article in march_articles:
    title = article.get('title', '').lower()
    summary = article.get('summary', '').lower()
    source = article.get('source', '')
    
    # Check if source is reputable
    is_reputable = any(reputable in source for reputable in reputable_sources)
    
    # Categorize based on keywords
    if any(keyword in title or keyword in summary for keyword in banking_keywords):
        banking_articles.append((article, is_reputable))
    elif any(keyword in title or keyword in summary for keyword in fintech_keywords):
        fintech_articles.append((article, is_reputable))
    elif any(keyword in title or keyword in summary for keyword in ai_keywords):
        ai_articles.append((article, is_reputable))

print(f"\nBanking articles: {len(banking_articles)} (reputable: {sum(1 for _, rep in banking_articles if rep)})")
print(f"Fintech articles: {len(fintech_articles)} (reputable: {sum(1 for _, rep in fintech_articles if rep)})")
print(f"AI articles: {len(ai_articles)} (reputable: {sum(1 for _, rep in ai_articles if rep)})")

# Show top samples from each category
print("\n=== Sample Banking Articles ===")
for i, (article, is_reputable) in enumerate(banking_articles[:3]):
    print(f"\n{i+1}. {article.get('title', 'No title')}")
    print(f"   Source: {article.get('source', 'Unknown')} {'(Reputable)' if is_reputable else ''}")
    print(f"   Date: {article.get('datetime', 'Unknown')}")
    print(f"   Summary: {article.get('summary', 'No summary')[:100]}...")

print("\n=== Sample Fintech Articles ===")
for i, (article, is_reputable) in enumerate(fintech_articles[:3]):
    print(f"\n{i+1}. {article.get('title', 'No title')}")
    print(f"   Source: {article.get('source', 'Unknown')} {'(Reputable)' if is_reputable else ''}")
    print(f"   Date: {article.get('datetime', 'Unknown')}")
    print(f"   Summary: {article.get('summary', 'No summary')[:100]}...")

print("\n=== Sample AI Articles ===")
for i, (article, is_reputable) in enumerate(ai_articles[:3]):
    print(f"\n{i+1}. {article.get('title', 'No title')}")
    print(f"   Source: {article.get('source', 'Unknown')} {'(Reputable)' if is_reputable else ''}")
    print(f"   Date: {article.get('datetime', 'Unknown')}")
    print(f"   Summary: {article.get('summary', 'No summary')[:100]}...")