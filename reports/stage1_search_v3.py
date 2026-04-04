#!/usr/bin/env python3
"""
Stage 1 v2: 批量搜索2026年3月银行业金融科技AI文章
"""

import json
import subprocess
import time
import os

SEARCH_SCRIPT = r"C:\Users\flyan\.agents\skills\wechat-article-search\scripts\search_wechat.js"
REPORTS_DIR = r"C:\Users\flyan\.openclaw\workspace\reports"

# 分批关键词 - 2026年3月
BATCH_KEYWORDS = [
    # 批次1
    ["银行业数字化转型 2026年3月", "AI大模型银行 2026年3月", "金融科技创新 2026年3月", "银行风险控制 2026年3月"],
    # 批次2
    ["数字人民币 2026年3月", "支付创新 2026年3月", "银行科技 2026年3月", "互联网金融 2026年3月"],
    # 批次3
    ["生成式AI金融 2026年3月", "银行客服智能化 2026年3月", "信贷风控 2026年3月", "监管科技 2026年3月"],
    # 批次4
    ["移动支付 2026年3月", "银行数字化 2026年3月", "金融大模型 2026年3月", "银行零售 2026年3月"],
    # 批次5
    ["AI应用银行 2026年3月", "金融业人工智能 2026年3月", "银行业趋势 2026年3月", "银行科技投入 2026年3月"],
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
            except Exception as e:
                print(f"    JSON解析失败: {e}")
                return []
        else:
            print(f"    返回码: {result.returncode}, stderr: {result.stderr[:100]}")
    except Exception as e:
        print(f"    异常: {e}")
    return []

def main():
    all_articles = []
    seen_urls = set()
    
    for batch_idx, keywords in enumerate(BATCH_KEYWORDS):
        print(f"\n=== 处理批次 {batch_idx+1}/{len(BATCH_KEYWORDS)} ===")
        batch_file = os.path.join(REPORTS_DIR, f"interim_batch_{batch_idx+1}.json")
        
        for kw in keywords:
            print(f"  搜索: {kw}", end=" ... ", flush=True)
            arts = run_search(kw, 20)
            print(f"{len(arts)}篇")
            
            for a in arts:
                url = a.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    a["keyword"] = kw
                    all_articles.append(a)
            
            time.sleep(0.8)
        
        # 保存中间结果
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
        print(f"  已保存累计{len(all_articles)}篇到 {batch_file}")
    
    # 保存最终搜索结果
    final_file = os.path.join(REPORTS_DIR, "search_results_2026_v3.json")
    with open(final_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 搜索完成 ===")
    print(f"总计收集: {len(all_articles)}篇")
    print(f"保存到: {final_file}")
    
    return len(all_articles)

if __name__ == "__main__":
    main()
