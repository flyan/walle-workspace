#!/usr/bin/env python3
"""
Stage 2: 评分和过滤
"""

import json
from datetime import datetime

# 专业公众号评分表
SOURCES = {
    "机器之心": 85, "量子位": 85, "新智元": 82, "智东西": 82,
    "馨金融": 83, "零壹财经": 82, "未央网": 84, "移动支付网": 82,
    "支付百科": 78, "消金界": 80, "第一消费金融": 80,
    "轻金融": 82, "中国银行保险报": 88, "银行家杂志": 85,
    "愉见财经": 80, "零售银行": 80, "信贷风险管理": 82,
    "行长要参": 80, "支行长": 78, "银行科技研究社": 82,
    "银行青年": 76, "国家金融监督管理总局": 95, "央行发布": 92,
    "中国银行业杂志": 86, "CF40": 88, "星图金融研究院": 85,
    "第一财经": 85, "澎湃新闻": 86, "金融界": 80, "华尔街见闻": 82,
    "36氪": 82, "钛媒体": 80, "东方财富网": 80, "中金证券": 85,
    "华泰证券": 84, "招商证券": 84,
    "中国工商银行": 82, "中国建设银行": 82, "中国农业银行": 82,
    "中国银行": 82, "中国邮政储蓄银行": 82, "交通银行": 82,
    "招商银行": 84, "招商银行信用卡": 82, "兴业银行": 80, "中信银行": 82,
}

def score_article(article):
    """给文章打分"""
    source = article.get("source", "")
    base_score = SOURCES.get(source, 0)
    
    # 时间加权
    dt = article.get("datetime", "")
    time_bonus = 0
    if dt.startswith("2026-03-"):
        time_bonus = 5
    elif dt.startswith("2026-02-"):
        time_bonus = 2
    elif dt.startswith("2025-"):
        time_bonus = 0
    else:
        time_bonus = -5  # 2024年以前的扣分
    
    return base_score + time_bonus

def main():
    # 加载搜索结果
    search_file = r"C:\Users\flyan\.openclaw\workspace\reports\search_results_batch.json"
    with open(search_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"加载文章: {len(articles)}篇")
    
    # 评分
    scored = []
    for a in articles:
        score = score_article(a)
        a["quality_score"] = score
        a["is_2026"] = a.get("datetime", "").startswith("2026")
        scored.append(a)
    
    # 按评分排序
    scored.sort(key=lambda x: -x["quality_score"])
    
    # 过滤：评分>75
    filtered = [a for a in scored if a["quality_score"] > 75]
    print(f"评分>75: {len(filtered)}篇")
    
    # 进一步过滤：2026年的优先，但也可以接受2025年的
    priority = [a for a in filtered if a["is_2026"]]
    print(f"2026年文章: {len(priority)}篇")
    
    # 如果2026年文章不够50篇，补充2025年的
    if len(priority) < 50:
        older = [a for a in filtered if not a["is_2026"]][:50 - len(priority)]
        filtered = priority + older
    else:
        filtered = priority[:50]
    
    print(f"最终选择: {len(filtered)}篇")
    
    # 保存过滤结果
    filtered_file = r"C:\Users\flyan\.openclaw\workspace\reports\filtered_articles.json"
    with open(filtered_file, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    
    print(f"保存到: {filtered_file}")
    
    # 分类统计
    cats = {"银行业": 0, "金融科技": 0, "AI": 0}
    for a in filtered:
        t = a.get("title", "").lower()
        s = a.get("summary", "").lower()
        if any(k in t or k in s for k in ["银行", "信贷", "存款", "贷款", "网点", "零售", "财富", "风控"]):
            cats["银行业"] += 1
        elif any(k in t or k in s for k in ["支付", "金融科技", "数字人民币", "区块链", "消费金融", "监管"]):
            cats["金融科技"] += 1
        elif any(k in t or k in s for k in ["AI", "大模型", "生成式AI", "机器学习", "人工智能", "智能"]):
            cats["AI"] += 1
        else:
            cats["银行业"] += 1
    
    print(f"\n分类: 银行业{cats['银行业']}篇, 金融科技{cats['金融科技']}篇, AI{cats['AI']}篇")
    
    return len(filtered)

if __name__ == "__main__":
    main()