#!/usr/bin/env python3
"""
微信文章质量评分和情报报告生成
支持倒金字塔结构输出
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path

class QualityAnalyzer:
    """文章质量分析器"""
    
    def __init__(self):
        self.content_keywords = {
            'data': r'[\d,]+%|[\d,]+亿|[\d,]+万|[\d,]+元|[\d,]+倍',
            'professional': r'(分析|研究|报告|数据|指数|指标|模型|算法|框架)',
            'structure': r'(摘要|总结|结论|建议|展望)',
        }
    
    def analyze_content_quality(self, title, summary, content=''):
        """分析内容质量 (0-50 分)"""
        score = 0
        
        # 字数深度 (0-30)
        text = f"{title}{summary}{content}"
        word_count = len(text)
        if word_count > 2000:
            score += 30
        elif word_count > 1000:
            score += 20
        elif word_count > 500:
            score += 10
        
        # 数据引用 (0-20)
        if re.search(self.content_keywords['data'], text):
            score += 20
        
        # 结构完整性 (0-20)
        if re.search(self.content_keywords['structure'], text):
            score += 10
        
        # 专业性 (0-20)
        if re.search(self.content_keywords['professional'], text):
            score += 10
        
        return min(score, 50)
    
    def analyze_source_credibility(self, source, account_name=''):
        """分析来源信誉 (0-50 分)"""
        score = 0
        
        # 官方认证 (0-20)
        official_keywords = ['央行', '监管', '官方', '中国', '国家', '部门']
        if any(kw in account_name for kw in official_keywords):
            score += 20
        elif '研究院' in account_name or '论坛' in account_name:
            score += 15
        
        # 机构类型 (0-30)
        institution_keywords = {
            '央行': 40,
            '监管': 40,
            '研究院': 35,
            '论坛': 35,
            '媒体': 25,
            '企业': 15,
        }
        
        for kw, pts in institution_keywords.items():
            if kw in account_name:
                score += min(pts, 30)
                break
        
        return min(score, 50)
    
    def get_recommendation(self, overall_score):
        """获取推荐等级"""
        if overall_score >= 85:
            return ('⭐⭐⭐⭐⭐', '强烈推荐')
        elif overall_score >= 70:
            return ('⭐⭐⭐⭐', '推荐')
        elif overall_score >= 55:
            return ('⭐⭐⭐', '可读')
        elif overall_score >= 40:
            return ('⭐⭐', '参考')
        else:
            return ('⭐', '不推荐')
    
    def analyze(self, article):
        """分析单篇文章"""
        title = article.get('title', '')
        summary = article.get('summary', '')
        account_name = article.get('source', '') or article.get('account_name', '')
        
        content_score = self.analyze_content_quality(title, summary)
        credibility_score = self.analyze_source_credibility(article.get('url', ''), account_name)
        overall_score = (content_score * 0.5 + credibility_score * 0.5)
        
        stars, recommendation = self.get_recommendation(overall_score)
        
        return {
            'title': title,
            'source': account_name,
            'url': article.get('url', ''),
            'datetime': article.get('datetime', ''),
            'summary': summary,
            'scores': {
                'content_quality': content_score,
                'source_credibility': credibility_score,
                'overall': round(overall_score, 1),
            },
            'recommendation': {
                'stars': stars,
                'level': recommendation,
            }
        }

def generate_report(articles, min_score=70):
    """
    生成倒金字塔结构的情报报告
    
    Args:
        articles: 文章列表
        min_score: 最低评分阈值
    
    Returns:
        报告文本
    """
    analyzer = QualityAnalyzer()
    
    # 分析所有文章
    analyzed = []
    for article in articles:
        result = analyzer.analyze(article)
        if result['scores']['overall'] >= min_score:
            analyzed.append(result)
    
    # 按评分排序
    analyzed.sort(key=lambda x: x['scores']['overall'], reverse=True)
    
    # 生成报告
    report = []
    report.append("=" * 80)
    report.append("微信文章情报报告")
    report.append("=" * 80)
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"总文章数: {len(articles)}")
    report.append(f"高质量文章: {len(analyzed)} (评分 > {min_score})")
    report.append("")
    
    # 统计摘要
    if analyzed:
        avg_content = sum(a['scores']['content_quality'] for a in analyzed) / len(analyzed)
        avg_credibility = sum(a['scores']['source_credibility'] for a in analyzed) / len(analyzed)
        avg_overall = sum(a['scores']['overall'] for a in analyzed) / len(analyzed)
        
        report.append("[统计摘要]")
        report.append(f"平均内容质量分: {avg_content:.1f}/100")
        report.append(f"平均来源信誉分: {avg_credibility:.1f}/100")
        report.append(f"平均综合评分: {avg_overall:.1f}/100")
        report.append("")
    
    # 排名前 10 的文章
    report.append("[排名前 10 的文章]")
    for i, article in enumerate(analyzed[:10], 1):
        report.append(f"{i}. {article['title']}")
        report.append(f"   来源: {article['source']}")
        report.append(f"   评分: {article['scores']['overall']}/100 {article['recommendation']['stars']}")
        report.append(f"   链接: {article['url']}")
        report.append("")
    
    # 详细索引
    report.append("[详细索引]")
    for i, article in enumerate(analyzed, 1):
        report.append(f"{i}. {article['title']}")
        report.append(f"   来源: {article['source']}")
        report.append(f"   发布: {article['datetime']}")
        report.append(f"   评分: {article['scores']['overall']}/100")
        report.append(f"   推荐: {article['recommendation']['level']}")
        report.append("")
    
    return '\n'.join(report), analyzed

def main():
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <input_json> [--min-score N] [--output FILE]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    min_score = 70
    output_file = None
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--min-score':
            min_score = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--output':
            output_file = sys.argv[i+1]
            i += 2
        else:
            i += 1
    
    # 读取输入
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 生成报告
    report_text, analyzed = generate_report(articles, min_score)
    
    # 输出
    print(report_text)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n已保存到: {output_file}")
        
        # 同时保存 JSON 格式
        json_file = output_file.replace('.txt', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analyzed, f, ensure_ascii=False, indent=2)
        print(f"JSON 已保存到: {json_file}")

if __name__ == '__main__':
    main()
