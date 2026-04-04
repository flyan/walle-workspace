#!/usr/bin/env python3
"""
银行业、金融科技、AI专题搜索脚本
搜索关键词：银行业、金融科技、AI（含国内外）
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

def search_wechat(keyword, num=20):
    """搜索微信文章"""
    try:
        cmd = [
            'node',
            r'C:\Users\flyan\.agents\skills\wechat-article-search\scripts\search_wechat.js',
            keyword,
            '-n', str(num),
        ]
        
        print(f"搜索关键词: {keyword}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"搜索失败: {result.stderr}")
            return []
        
        data = json.loads(result.stdout)
        return data.get('articles', [])
        
    except Exception as e:
        print(f"搜索异常: {e}")
        return []

def filter_recent_articles(articles, days=7):
    """过滤最近N天的文章"""
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered = []
    
    for article in articles:
        pub_time_str = article.get('datetime', '')
        if not pub_time_str:
            continue
            
        try:
            # 解析时间格式：2026-03-22 17:48:33
            pub_time = datetime.strptime(pub_time_str, '%Y-%m-%d %H:%M:%S')
            if pub_time >= cutoff_date:
                filtered.append(article)
        except ValueError:
            continue
    
    return filtered

def search_multiple_keywords(keywords, num_per_keyword=15, days=7):
    """搜索多个关键词"""
    all_articles = []
    seen_titles = set()
    
    for keyword in keywords:
        print(f"\n{'='*50}")
        print(f"正在搜索: {keyword}")
        print(f"{'='*50}")
        
        articles = search_wechat(keyword, num_per_keyword)
        recent_articles = filter_recent_articles(articles, days)
        
        # 去重
        for article in recent_articles:
            title = article.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                all_articles.append(article)
        
        print(f"找到 {len(recent_articles)} 篇文章（去重后新增 {len([a for a in recent_articles if a.get('title', '') not in seen_titles])} 篇）")
    
    # 按时间排序
    all_articles.sort(key=lambda x: x.get('datetime', ''), reverse=True)
    
    return all_articles

def categorize_articles(articles):
    """分类文章"""
    categories = {
        'banking': [],      # 银行业
        'fintech': [],      # 金融科技
        'ai': [],           # AI
        'international': [], # 国际
        'other': []         # 其他
    }
    
    banking_keywords = ['银行', '银行业', '商业银行', '零售银行', '数字银行']
    fintech_keywords = ['金融科技', 'FinTech', 'fintech', '科技金融']
    ai_keywords = ['AI', '人工智能', '大模型', '生成式AI', '机器学习']
    intl_keywords = ['国际', '海外', '美国', '欧洲', '英国', '新加坡', '香港']
    
    for article in articles:
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        source = article.get('source', '')
        
        # 检查分类
        categorized = False
        
        # 国际类
        if any(keyword in title or keyword in summary for keyword in intl_keywords):
            categories['international'].append(article)
            categorized = True
        
        # 银行业
        if any(keyword in title or keyword in summary for keyword in banking_keywords):
            categories['banking'].append(article)
            categorized = True
        
        # 金融科技
        if any(keyword in title or keyword in summary for keyword in fintech_keywords):
            categories['fintech'].append(article)
            categorized = True
        
        # AI
        if any(keyword in title or keyword in summary for keyword in ai_keywords):
            categories['ai'].append(article)
            categorized = True
        
        # 其他
        if not categorized:
            categories['other'].append(article)
    
    return categories

def generate_markdown_report(categories, output_file):
    """生成Markdown报告"""
    total_articles = sum(len(articles) for articles in categories.values())
    
    content = f"""# 银行业、金融科技与AI科技咨询情报
## {datetime.now().strftime('%Y年%m月%d日')} 精选报告

---

## 📊 报告概览

- **报告日期**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
- **覆盖周期**: 最近7天
- **文章总数**: {total_articles}篇
- **搜索关键词**: 银行业、金融科技、AI（含国内外）
- **数据来源**: 微信公众号文章搜索

---

## 📈 分类统计

| 类别 | 文章数量 | 占比 |
|------|----------|------|
| 银行业 | {len(categories['banking'])} | {len(categories['banking'])/total_articles*100:.1f}% |
| 金融科技 | {len(categories['fintech'])} | {len(categories['fintech'])/total_articles*100:.1f}% |
| AI | {len(categories['ai'])} | {len(categories['ai'])/total_articles*100:.1f}% |
| 国际动态 | {len(categories['international'])} | {len(categories['international'])/total_articles*100:.1f}% |
| 其他 | {len(categories['other'])} | {len(categories['other'])/total_articles*100:.1f}% |

---

"""

    # 银行业
    if categories['banking']:
        content += "## 🏦 银行业动态\n\n"
        for i, article in enumerate(categories['banking'][:10], 1):
            content += f"### {i}. {article.get('title', '无标题')}\n"
            content += f"- **来源**: {article.get('source', '未知')}\n"
            content += f"- **时间**: {article.get('datetime', '未知时间')} ({article.get('date_description', '')})\n"
            content += f"- **摘要**: {article.get('summary', '无摘要')}\n"
            content += f"- **链接**: {article.get('url', '')}\n\n"
    
    # 金融科技
    if categories['fintech']:
        content += "## 💰 金融科技动态\n\n"
        for i, article in enumerate(categories['fintech'][:10], 1):
            content += f"### {i}. {article.get('title', '无标题')}\n"
            content += f"- **来源**: {article.get('source', '未知')}\n"
            content += f"- **时间**: {article.get('datetime', '未知时间')} ({article.get('date_description', '')})\n"
            content += f"- **摘要**: {article.get('summary', '无摘要')}\n"
            content += f"- **链接**: {article.get('url', '')}\n\n"
    
    # AI
    if categories['ai']:
        content += "## 🤖 AI技术动态\n\n"
        for i, article in enumerate(categories['ai'][:10], 1):
            content += f"### {i}. {article.get('title', '无标题')}\n"
            content += f"- **来源**: {article.get('source', '未知')}\n"
            content += f"- **时间**: {article.get('datetime', '未知时间')} ({article.get('date_description', '')})\n"
            content += f"- **摘要**: {article.get('summary', '无摘要')}\n"
            content += f"- **链接**: {article.get('url', '')}\n\n"
    
    # 国际动态
    if categories['international']:
        content += "## 🌍 国际动态\n\n"
        for i, article in enumerate(categories['international'][:10], 1):
            content += f"### {i}. {article.get('title', '无标题')}\n"
            content += f"- **来源**: {article.get('source', '未知')}\n"
            content += f"- **时间**: {article.get('datetime', '未知时间')} ({article.get('date_description', '')})\n"
            content += f"- **摘要**: {article.get('summary', '无摘要')}\n"
            content += f"- **链接**: {article.get('url', '')}\n\n"
    
    # 其他
    if categories['other']:
        content += "## 📰 其他相关资讯\n\n"
        for i, article in enumerate(categories['other'][:5], 1):
            content += f"### {i}. {article.get('title', '无标题')}\n"
            content += f"- **来源**: {article.get('source', '未知')}\n"
            content += f"- **时间**: {article.get('datetime', '未知时间')} ({article.get('date_description', '')})\n"
            content += f"- **摘要**: {article.get('summary', '无摘要')}\n"
            content += f"- **链接**: {article.get('url', '')}\n\n"
    
    # 总结
    content += f"""---

## 🎯 核心洞察

### 1. 银行业趋势
- 数字化转型加速
- 零售银行创新
- 风险管理加强

### 2. 金融科技发展
- 技术应用深化
- 监管科技兴起
- 跨境支付突破

### 3. AI技术应用
- 大模型在金融领域应用
- 智能风控系统
- 自动化客户服务

### 4. 国际对标
- 全球金融科技趋势
- 国际监管动态
- 跨境合作机会

---

## 📝 下一步建议

1. **持续监测**: 建立定期搜索机制
2. **深度分析**: 对重点领域进行专题研究
3. **趋势预测**: 基于数据预测行业发展
4. **决策支持**: 为投资和战略提供数据支持

---

**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据更新建议**: 每日更新，每周汇总
**报告格式**: Markdown + PDF

---
*本报告基于微信公众号公开文章整理，仅供参考。*
"""
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Markdown报告已生成: {output_file}")
    return content

def main():
    """主函数"""
    # 搜索关键词
    keywords = [
        "银行业",
        "金融科技", 
        "AI",
        "人工智能",
        "银行科技",
        "数字银行",
        "FinTech",
        "大模型",
        "生成式AI",
        "跨境支付",
        "监管科技",
        "智能风控"
    ]
    
    print("开始搜索银行业、金融科技、AI相关文章...")
    print(f"搜索关键词: {', '.join(keywords)}")
    
    # 搜索文章
    articles = search_multiple_keywords(keywords, num_per_keyword=15, days=7)
    
    if not articles:
        print("未找到相关文章")
        return
    
    print(f"\n总共找到 {len(articles)} 篇文章")
    
    # 分类文章
    categories = categorize_articles(articles)
    
    print("\n分类统计:")
    for category, items in categories.items():
        print(f"  {category}: {len(items)}篇")
    
    # 生成Markdown报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    md_file = f'银行业金融科技AI情报_{timestamp}.md'
    pdf_file = f'银行业金融科技AI情报_{timestamp}.pdf'
    
    md_content = generate_markdown_report(categories, md_file)
    
    print(f"\n报告生成完成!")
    print(f"- Markdown文件: {md_file}")
    print(f"- 建议PDF文件: {pdf_file}")
    
    # 保存原始数据
    data_file = f'search_results_{timestamp}.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_time': datetime.now().isoformat(),
            'keywords': keywords,
            'total_articles': len(articles),
            'categories': {k: len(v) for k, v in categories.items()},
            'articles': articles
        }, f, ensure_ascii=False, indent=2)
    
    print(f"- 原始数据: {data_file}")
    
    return md_file, articles

if __name__ == '__main__':
    main()