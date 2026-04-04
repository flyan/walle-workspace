#!/usr/bin/env python3
"""
分阶段报告生成器
Stage 1: 批量搜索并保存中间结果
"""

import json
import subprocess
import time
import sys

SEARCH_SCRIPT = r"C:\Users\flyan\.agents\skills\wechat-article-search\scripts\search_wechat.js"

# 分批关键词
BATCH_KEYWORDS = [
    # 第一批：银行业核心
    ["银行业数字化转型", "银行大模型", "数字人民币试点", "智能风控银行"],
    # 第二批：金融科技
    ["金融科技趋势", "AI客服银行", "开放银行", "供应链金融"],
    # 第三批：AI应用
    ["AI大模型金融", "生成式AI银行", "银行智能投顾", "数字银行卡"],
    # 第四批：技术基础设施
    ["金融云", "银行API", "区块链供应链", "跨境金融科技"],
    # 第五批：监管与合规
    ["金融监管科技", "银行IT建设", "信贷科技", "财富管理AI"],
]

def run_search(keyword, num=20):
    """搜索单个关键词"""
    try:
        result = subprocess.run(
            ["node", SEARCH_SCRIPT, keyword, "-n", str(num)],
            capture_output=True, text=True, encoding='utf-8', timeout=30
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return data.get("articles", [])
            except:
                return []
    except:
        pass
    return []

def main():
    all_articles = []
    seen_urls = set()
    
    for batch_idx, keywords in enumerate(BATCH_KEYWORDS):
        print(f"\n=== 处理批次 {batch_idx+1}/{len(BATCH_KEYWORDS)} ===")
        
        for kw in keywords:
            arts = run_search(kw, 15)
            print(f"  {kw}: {len(arts)}篇")
            
            for a in arts:
                url = a.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    a["keyword"] = kw
                    all_articles.append(a)
            
            time.sleep(0.5)
        
        # 保存中间结果
        interim_file = f"C:/Users/flyan/.openclaw/workspace/reports/interim_{batch_idx+1}.json"
        with open(interim_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
        print(f"  已保存{len(all_articles)}篇到 {interim_file}")
    
    # 保存最终搜索结果
    final_file = r"C:\Users\flyan\.openclaw\workspace\reports\search_results_batch.json"
    with open(final_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 搜索完成 ===")
    print(f"总计收集: {len(all_articles)}篇")
    print(f"保存到: {final_file}")
    
    return len(all_articles)

if __name__ == "__main__":
    main()