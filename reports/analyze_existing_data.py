import json
import re

# Read the existing search results
json_path = r'C:\Users\flyan\.openclaw\workspace\reports\search_results_20260322_2028.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# List of reputable sources from FINTECH_ACCOUNTS.md
reputable_sources = [
    '机器之心', '量子位', '新智元', '极客公园', '智东西',
    '馨金融', '零壹财经', '未央网', '一本财经', '十字财经',
    '移动支付网', '支付百科', '消金界', '第一消费金融',
    '轻金融', '中国银行保险报', '银行家杂志', '愉见财经',
    '零售银行', '信贷风险管理', '支行长', '银行科技研究社',
    '行长要参', '金融数字化观察', '星图金融研究院', 'CF40',
    '第一财经', '澎湃新闻', '36氪', '钛媒体', '东方财富网',
    '招商银行', '中国工商银行', '中国建设银行', '中国农业银行',
    '中国银行', '交通银行', '中国邮政储蓄银行',
    '兴业银行', '中信银行', '上海浦东发展银行',
    '中原银行', '宁波银行', '盛京银行', '蒙商银行',
    '国家金融监督管理总局', '央行发布', '中国银行业杂志',
    '麦肯锡', '波士顿咨询', 'BCG', '金融论坛',
    '金融界', '华尔街见闻', '投资明见', '商行新鲜事',
    '思维纪要社', '国际金融报', '运营商财经',
    '中金证券', '华泰证券', '招商证券'
]

print(f"Total articles in existing data: {len(data.get('articles', []))}")
print(f"Search date: {data.get('search_time', 'Unknown')}")

# Filter for reputable sources
reputable_articles = []
other_articles = []

for article in data.get('articles', []):
    source = article.get('source', '')
    title = article.get('title', '')
    
    is_reputable = False
    for reputable in reputable_sources:
        if reputable in source:
            is_reputable = True
            break
    
    if is_reputable:
        reputable_articles.append(article)
    else:
        other_articles.append(article)

print(f"\nReputable articles: {len(reputable_articles)}")
print(f"Other articles: {len(other_articles)}")

# Show reputable articles
print("\n=== Reputable Articles Found ===")
for i, article in enumerate(reputable_articles[:10]):  # Show first 10
    print(f"\n{i+1}. {article.get('title', 'No title')}")
    print(f"   Source: {article.get('source', 'Unknown')}")
    print(f"   Date: {article.get('datetime', 'Unknown')}")
    summary = article.get('summary', 'No summary')
    if len(summary) > 100:
        summary = summary[:100] + "..."
    print(f"   Summary: {summary}")

# Show some examples of other articles (to demonstrate quality difference)
print("\n=== Examples of Other Articles (Non-Reputable) ===")
for i, article in enumerate(other_articles[:5]):
    print(f"\n{i+1}. {article.get('title', 'No title')}")
    print(f"   Source: {article.get('source', 'Unknown')}")
    print(f"   Date: {article.get('datetime', 'Unknown')}")

# Categorize reputable articles
banking_keywords = ['银行', '信贷', '存款', '贷款', '网点', '柜员', '客户经理', '零售银行']
fintech_keywords = ['支付', '金融科技', '数字人民币', '区块链', '消费金融', '风控', '监管科技']
ai_keywords = ['AI', '人工智能', '大模型', '生成式AI', '机器学习', '深度学习']

banking_count = 0
fintech_count = 0
ai_count = 0
other_count = 0

for article in reputable_articles:
    title = article.get('title', '').lower()
    summary = article.get('summary', '').lower()
    
    if any(keyword in title or keyword in summary for keyword in banking_keywords):
        banking_count += 1
    elif any(keyword in title or keyword in summary for keyword in fintech_keywords):
        fintech_count += 1
    elif any(keyword in title or keyword in summary for keyword in ai_keywords):
        ai_count += 1
    else:
        other_count += 1

print(f"\n=== Categorization of Reputable Articles ===")
print(f"Banking: {banking_count}")
print(f"Fintech: {fintech_count}")
print(f"AI: {ai_count}")
print(f"Other: {other_count}")