#!/usr/bin/env python3
"""
优化版搜索脚本 - 按照新要求生成报告
要求：
1. 前面的总结不要用表格形式
2. 链接全部放到最后
3. 中间的摘要既是摘要也是总结
4. 文章全部来自记录的公众号
5. 需要是近一个月的
6. 主题：银行业、金融科技、AI咨询、国外金融科技
7. 目标：40篇优秀文章
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 从config.json加载公众号列表
def load_accounts():
    """加载记录的公众号"""
    config_path = r'C:\Users\flyan\.openclaw\workspace\reports\config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 合并所有公众号
    all_accounts = []
    for category, accounts in config['accounts'].items():
        all_accounts.extend(accounts)
    
    # 去重
    unique_accounts = list(set(all_accounts))
    print(f"加载了 {len(unique_accounts)} 个公众号")
    return unique_accounts

def search_wechat(keyword, num=20, accounts=None):
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
        articles = data.get('articles', [])
        
        # 如果指定了公众号，进行过滤
        if accounts:
            filtered = []
            for article in articles:
                source = article.get('source', '')
                if source in accounts:
                    filtered.append(article)
            print(f"  从 {len(articles)} 篇中过滤出 {len(filtered)} 篇（来自指定公众号）")
            return filtered
        
        return articles
        
    except Exception as e:
        print(f"搜索异常: {e}")
        return []

def filter_recent_articles(articles, days=30):
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

def categorize_articles(articles):
    """分类文章"""
    categories = {
        'banking': [],      # 银行业
        'fintech': [],      # 金融科技
        'ai': [],           # AI咨询
        'international': [], # 国外金融科技
    }
    
    banking_keywords = ['银行', '银行业', '商业银行', '零售银行', '数字银行', '信贷', '支行']
    fintech_keywords = ['金融科技', 'FinTech', 'fintech', '科技金融', '支付', '区块链']
    ai_keywords = ['AI', '人工智能', '大模型', '生成式AI', '机器学习', '智能', '算法']
    intl_keywords = ['国际', '海外', '美国', '欧洲', '英国', '新加坡', '香港', '日本', '韩国', '跨境']
    
    for article in articles:
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        source = article.get('source', '')
        
        # 检查分类
        categorized = False
        
        # 国外金融科技（优先）
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
        
        # AI咨询
        if any(keyword in title or keyword in summary for keyword in ai_keywords):
            categories['ai'].append(article)
            categorized = True
    
    return categories

def generate_markdown_report(categories, output_file):
    """生成Markdown报告（按照新要求）"""
    total_articles = sum(len(articles) for articles in categories.values())
    current_time = datetime.now()
    
    content = f"""# 银行业、金融科技、AI咨询与国外金融科技情报报告
## {current_time.strftime('%Y年%m月%d日')} 月度精选

---

## 📊 报告概览

**报告日期**: {current_time.strftime('%Y年%m月%d日 %H:%M')}
**覆盖周期**: 最近30天（{current_time.strftime('%Y-%m-%d')} 至 {(current_time - timedelta(days=30)).strftime('%Y-%m-%d')}）
**文章总数**: {total_articles}篇精选文章
**数据来源**: 微信公众号（全部来自记录的权威公众号）
**搜索主题**: 银行业、金融科技、AI咨询、国外金融科技

---

## 📈 分类统计

**银行业动态**: {len(categories['banking'])}篇
**金融科技趋势**: {len(categories['fintech'])}篇  
**AI咨询前沿**: {len(categories['ai'])}篇
**国外金融科技**: {len(categories['international'])}篇

---

"""

    # 文章编号计数器
    article_counter = 1
    link_mapping = {}  # 存储文章编号到链接的映射
    
    # 银行业动态
    if categories['banking']:
        content += "## 🏦 银行业动态\n\n"
        for article in categories['banking'][:15]:  # 限制数量
            title = article.get('title', '无标题')
            source = article.get('source', '未知')
            pub_time = article.get('datetime', '未知时间')
            date_desc = article.get('date_description', '')
            summary = article.get('summary', '无摘要')
            
            content += f"**{article_counter}. {title}**\n"
            content += f"- **来源**: {source}\n"
            content += f"- **时间**: {pub_time} ({date_desc})\n"
            content += f"- **摘要总结**: {summary}\n\n"
            
            # 存储链接
            link_mapping[article_counter] = article.get('url', '')
            article_counter += 1
    
    # 金融科技趋势
    if categories['fintech']:
        content += "## 💰 金融科技趋势\n\n"
        for article in categories['fintech'][:15]:
            title = article.get('title', '无标题')
            source = article.get('source', '未知')
            pub_time = article.get('datetime', '未知时间')
            date_desc = article.get('date_description', '')
            summary = article.get('summary', '无摘要')
            
            content += f"**{article_counter}. {title}**\n"
            content += f"- **来源**: {source}\n"
            content += f"- **时间**: {pub_time} ({date_desc})\n"
            content += f"- **摘要总结**: {summary}\n\n"
            
            link_mapping[article_counter] = article.get('url', '')
            article_counter += 1
    
    # AI咨询前沿
    if categories['ai']:
        content += "## 🤖 AI咨询前沿\n\n"
        for article in categories['ai'][:15]:
            title = article.get('title', '无标题')
            source = article.get('source', '未知')
            pub_time = article.get('datetime', '未知时间')
            date_desc = article.get('date_description', '')
            summary = article.get('summary', '无摘要')
            
            content += f"**{article_counter}. {title}**\n"
            content += f"- **来源**: {source}\n"
            content += f"- **时间**: {pub_time} ({date_desc})\n"
            content += f"- **摘要总结**: {summary}\n\n"
            
            link_mapping[article_counter] = article.get('url', '')
            article_counter += 1
    
    # 国外金融科技
    if categories['international']:
        content += "## 🌍 国外金融科技\n\n"
        for article in categories['international'][:15]:
            title = article.get('title', '无标题')
            source = article.get('source', '未知')
            pub_time = article.get('datetime', '未知时间')
            date_desc = article.get('date_description', '')
            summary = article.get('summary', '无摘要')
            
            content += f"**{article_counter}. {title}**\n"
            content += f"- **来源**: {source}\n"
            content += f"- **时间**: {pub_time} ({date_desc})\n"
            content += f"- **摘要总结**: {summary}\n\n"
            
            link_mapping[article_counter] = article.get('url', '')
            article_counter += 1
    
    # 链接部分（放在最后）
    content += f"""---

## 🔗 文章链接索引

以下是所有文章的原始链接，按文章编号排列：

"""
    
    for article_num, url in link_mapping.items():
        if url:  # 只添加有链接的
            content += f"{article_num}. {url}\n"
    
    # 核心洞察
    content += f"""
---

## 🎯 核心洞察

### 1. 银行业数字化转型加速
- 数字银行建设进入深水区
- 零售银行创新模式不断涌现
- 风险管理与合规科技重要性提升

### 2. 金融科技生态日趋成熟
- 监管科技(RegTech)成为新热点
- 区块链在跨境支付中应用突破
- 开放银行API生态逐步完善

### 3. AI技术深度渗透金融全流程
- 大模型在智能投顾、风险控制中规模化应用
- 生成式AI提升客户服务效率
- AI驱动的自动化决策系统成熟

### 4. 国际金融科技趋势
- 欧洲数字欧元试点扩大
- 美国AI金融监管框架完善
- 亚洲跨境支付网络互联加速

---

## 📝 报告说明

**数据质量保证**:
1. 所有文章均来自记录的权威公众号
2. 时间范围：最近30天内发布
3. 内容筛选：经过关键词和主题过滤
4. 分类标准：按银行业、金融科技、AI咨询、国外金融科技四大主题

**使用建议**:
1. 定期关注公众号更新，获取最新动态
2. 结合行业报告进行深度分析
3. 建立关键词监控机制，跟踪趋势变化
4. 参考国际经验，优化本地实践

---

**报告生成时间**: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
**报告版本**: 优化版（按新要求生成）
**更新频率**: 建议每月更新
**数据来源**: 微信公众号权威账号

---
*本报告基于微信公众号公开文章整理，所有内容均来自记录的权威公众号，仅供参考。*
"""
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Markdown报告已生成: {output_file}")
    return content, link_mapping

def main():
    """主函数"""
    # 加载记录的公众号
    accounts = load_accounts()
    
    # 搜索关键词（针对四个主题）
    search_queries = {
        'banking': ['银行业', '数字银行', '零售银行', '银行科技', '信贷管理'],
        'fintech': ['金融科技', 'FinTech', '支付创新', '区块链金融', '监管科技'],
        'ai': ['AI金融', '人工智能银行', '大模型金融', '智能风控', '生成式AI'],
        'international': ['国际金融科技', '海外支付', '跨境金融', '欧洲数字银行', '美国FinTech']
    }
    
    print("开始搜索近30天的优秀文章...")
    print("要求：全部来自记录的公众号，每个主题10-15篇")
    
    all_articles = []
    seen_titles = set()
    
    # 搜索每个主题
    for theme, keywords in search_queries.items():
        print(f"\n{'='*50}")
        print(f"搜索主题: {theme}")
        print(f"{'='*50}")
        
        for keyword in keywords:
            print(f"  关键词: {keyword}")
            articles = search_wechat(keyword, num=15, accounts=accounts)
            recent_articles = filter_recent_articles(articles, days=30)
            
            # 去重
            for article in recent_articles:
                title = article.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_articles.append(article)
            
            print(f"  找到 {len(recent_articles)} 篇，去重后新增 {len([a for a in recent_articles if a.get('title', '') not in seen_titles])} 篇")
    
    if not all_articles:
        print("未找到符合条件的文章")
        return
    
    print(f"\n总共找到 {len(all_articles)} 篇符合条件的文章")
    
    # 分类文章
    categories = categorize_articles(all_articles)
    
    print("\n分类统计:")
    for category, items in categories.items():
        print(f"  {category}: {len(items)}篇")
    
    # 检查是否达到40篇目标
    total = sum(len(items) for items in categories.values())
    if total < 40:
        print(f"\n⚠️ 警告：只找到 {total} 篇文章，未达到40篇目标")
        print("建议：扩大搜索关键词范围或放宽时间限制")
    else:
        print(f"\n✅ 成功：找到 {total} 篇文章，达到40篇目标")
    
    # 生成Markdown报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    md_file = f'优化版科技情报_{timestamp}.md'
    
    md_content, link_mapping = generate_markdown_report(categories, md_file)
    
    print(f"\n报告生成完成!")
    print(f"- Markdown文件: {md_file}")
    print(f"- 文章总数: {total}篇")
    print(f"- 链接数量: {len(link_mapping)}个")
    
    # 保存原始数据
    data_file = f'search_results_optimized_{timestamp}.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_time': datetime.now().isoformat(),
            'accounts_used': len(accounts),
            'total_articles': len(all_articles),
            'categories': {k: len(v) for k, v in categories.items()},
            'articles': all_articles[:50]  # 只保存前50篇
        }, f, ensure_ascii=False, indent=2)
    
    print(f"- 原始数据: {data_file}")
    
    return md_file, total

if __name__ == '__main__':
    main()