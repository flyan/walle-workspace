#!/usr/bin/env python3
"""
Stage 2 v3 revised: 金融银行专项评分过滤
"""

import json

REPORTS_DIR = r"C:\Users\flyan\.openclaw\workspace\reports"

# 专业公众号评分表
SOURCES_SCORING = {
    "机器之心": 85, "量子位": 85, "新智元": 82, "智东西": 82,
    "馨金融": 83, "零壹财经": 82, "未央网": 84, "移动支付网": 82,
    "轻金融": 82, "中国银行保险报": 88, "银行家杂志": 85,
    "行长要参": 80, "银行科技研究社": 82,
    "国家金融监督管理总局": 95, "央行发布": 92,
    "中国银行业杂志": 86, "CF40": 88, "星图金融研究院": 85,
    "第一财经": 85, "澎湃新闻": 86, "华尔街见闻": 82,
    "36氪": 82, "券商中国": 84,
}

def get_source_score(source):
    if not source:
        return 0
    if source in SOURCES_SCORING:
        return SOURCES_SCORING[source]
    # 模糊匹配
    for key, val in SOURCES_SCORING.items():
        if key in source or source in key:
            return max(0, val - 15)
    # 基础加分
    bank_words = ["银行", "金融", "科技", "财经", "支付", "证券", "投资"]
    for w in bank_words:
        if w in source:
            return 15
    return 5

def score_article(article):
    source = article.get("source", "")
    title = article.get("title", "")
    summary = article.get("summary", "")
    dt = article.get("datetime", "")
    
    source_score = get_source_score(source)
    
    # 时间加权
    time_bonus = 0
    if dt.startswith("2026-03"):
        time_bonus = 15
    elif dt.startswith("2026-02"):
        time_bonus = 8
    elif dt.startswith("2026-01"):
        time_bonus = 4
    
    # 关键词评分 - 金融银行专业度
    text = (title + " " + summary).lower()
    
    # 高价值词（在标题中）
    high_title = ["银行", "信贷", "存款", "贷款", "风控", "净息差", "不良贷款", "金融科技", "数字人民币", 
                   "开放银行", "供应链金融", "移动支付", "反洗钱", "监管科技", "财富管理", "智能风控",
                   "银行大模型", "金融大模型", "银行数字化", "网点转型", "零售银行", "对公业务",
                   "信用卡", "电子支付", "跨境支付", "村镇银行", "城商行", "农商行", "国有大行", "股份制银行",
                   "中小银行", "银行科技", "银行IT", "银行AI", "AI银行", "智能银行"]
    medium_title = ["消费金融", "普惠金融", "绿色金融", " fintech", "区块链", "云计算", "大数据", 
                    "数据要素", "API银行", "开放API", "智能投顾", "智能客服", "智能营销",
                    "模型", "大模型", "生成式AI", "LLM", "AI应用", "人工智能"]
    low_title = ["AI", "人工智能", "机器学习", "深度学习", "GPT", "ChatGPT"]
    
    bonus = 0
    for kw in high_title:
        if kw in title:
            bonus += 8
        if kw in text:
            bonus += 3
    for kw in medium_title:
        if kw in title:
            bonus += 4
        if kw in text:
            bonus += 2
    for kw in low_title:
        if kw in title:
            bonus += 1
        if kw in text:
            bonus += 0.5
    
    return source_score + time_bonus + bonus

def classify_article(article):
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    source = article.get("source", "").lower()
    text = title + " " + summary + " " + source
    
    ai_keywords = ["ai", "大模型", "生成式", "机器学习", "人工智能", "gpt", "llm", "深度学习", "智能化", "模型"]
    fintech_keywords = ["支付", "数字人民币", "区块链", "消费金融", "监管科技", "开放银行", "api", "供应链金融", "跨境", "金融科技"]
    bank_keywords = ["银行", "信贷", "存款", "贷款", "网点", "零售", "财富", "风控", "资本", "资产", "净息差", "不良", "信用卡", "网点", "对公"]
    
    ai_score = sum(3 if k in title else 1 for k in ai_keywords if k in text)
    fintech_score = sum(3 if k in title else 1 for k in fintech_keywords if k in text)
    bank_score = sum(3 if k in title else 1 for k in bank_keywords if k in text)
    
    scores = {"AI": ai_score, "金融科技": fintech_score, "银行业": bank_score}
    return max(scores, key=scores.get)

def main():
    search_file = f"{REPORTS_DIR}\\search_results_2026_v3.json"
    with open(search_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"加载文章: {len(articles)}篇")
    
    scored = []
    for a in articles:
        score = score_article(a)
        dt = a.get("datetime", "")
        a["quality_score"] = score
        a["is_march_2026"] = dt.startswith("2026-03")
        scored.append(a)
    
    scored.sort(key=lambda x: -x["quality_score"])
    
    # 统计
    march_count = sum(1 for a in scored if a["is_march_2026"])
    print(f"2026年3月文章: {march_count}篇")
    
    # 显示top 60
    print("\nTop 60 分数分布:")
    for i, a in enumerate(scored[:60]):
        print(f"  {i+1:2d}. [{a['quality_score']:5.1f}] {a.get('datetime','')[:10]} | {a.get('source','')[:20]:20s} | {a.get('title','')[:50]}")
    
    # 取前55篇（优先3月的）
    march = [a for a in scored if a["is_march_2026"]]
    other = [a for a in scored if not a["is_march_2026"]]
    
    final = march[:55]
    if len(final) < 50:
        final += other[:50-len(final)]
    
    print(f"\n最终: {len(final)}篇 (3月:{sum(1 for a in final if a['is_march_2026'])})")
    
    cats = {"银行业": [], "金融科技": [], "AI": []}
    for a in final:
        cat = classify_article(a)
        cats[cat].append(a)
    
    for cat in cats:
        cats[cat].sort(key=lambda x: -x["quality_score"])
    
    print(f"\n分类: 银行业{len(cats['银行业'])} 金融科技{len(cats['金融科技'])} AI{len(cats['AI'])}")
    
    filtered_file = f"{REPORTS_DIR}\\filtered_articles_v3.json"
    with open(filtered_file, 'w', encoding='utf-8') as f:
        json.dump({"final_selection": final, "categories": cats}, f, ensure_ascii=False, indent=2)
    print(f"保存到: {filtered_file}")

if __name__ == "__main__":
    main()
