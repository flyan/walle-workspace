#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文章质量评估系统
综合分析内容质量和来源信誉
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class ArticleQualityAnalyzer:
    """文章质量分析器"""
    
    def __init__(self):
        self.content_weights = {
            'word_count': 0.30,
            'data_references': 0.30,
            'structure': 0.20,
            'professionalism': 0.20
        }
        self.credibility_weights = {
            'certification': 0.20,
            'follower_influence': 0.20,
            'update_frequency': 0.20,
            'institution_type': 0.40
        }
    
    def analyze_content_quality(self, article: Dict) -> Tuple[int, Dict]:
        """
        分析内容质量
        返回: (总分, 详细分数)
        """
        details = {}
        
        # 1. 字数深度分析
        content = article.get('summary', '') + article.get('msg_content', '')
        word_count = len(content)
        
        if word_count >= 3000:
            word_score = 30
            word_level = '深度分析'
        elif word_count >= 2000:
            word_score = 20
            word_level = '中等深度'
        elif word_count >= 1000:
            word_score = 10
            word_level = '快讯/观点'
        else:
            word_score = 0
            word_level = '内容过短'
        
        details['word_count'] = {
            'score': word_score,
            'level': word_level,
            'actual': word_count
        }
        
        # 2. 数据引用分析
        # 检查是否包含数字、百分比、金额等
        data_patterns = [
            r'\d+%',  # 百分比
            r'¥\d+',  # 金额
            r'\d+\.\d+',  # 小数
            r'第\d+',  # 序号
            r'\d{4}年',  # 年份
        ]
        
        data_count = sum(len(re.findall(pattern, content)) for pattern in data_patterns)
        
        if data_count >= 10:
            data_score = 30
            data_level = '数据充分'
        elif data_count >= 5:
            data_score = 20
            data_level = '有数据支撑'
        elif data_count >= 1:
            data_score = 10
            data_level = '部分数据'
        else:
            data_score = 0
            data_level = '无数据引用'
        
        details['data_references'] = {
            'score': data_score,
            'level': data_level,
            'count': data_count
        }
        
        # 3. 结构完整性分析
        structure_score = 0
        structure_items = []
        
        if article.get('msg_title'):
            structure_score += 5
            structure_items.append('标题')
        if article.get('summary'):
            structure_score += 5
            structure_items.append('摘要')
        if article.get('msg_content'):
            structure_score += 5
            structure_items.append('正文')
        if article.get('msg_author'):
            structure_score += 5
            structure_items.append('作者')
        
        details['structure'] = {
            'score': structure_score,
            'items': structure_items,
            'completeness': f"{len(structure_items)}/4"
        }
        
        # 4. 专业性指标
        professional_score = 0
        professional_markers = []
        
        # 检查专业术语
        professional_terms = [
            '数据', '分析', '研究', '报告', '指数', '指标',
            '趋势', '预测', '模型', '框架', '策略', '方案'
        ]
        
        if any(term in content for term in professional_terms):
            professional_score += 10
            professional_markers.append('专业术语')
        
        # 检查是否有引用或参考
        if '引用' in content or '参考' in content or '来源' in content:
            professional_score += 5
            professional_markers.append('有引用')
        
        # 检查是否有图表描述
        if '图' in content or '表' in content or '图表' in content:
            professional_score += 5
            professional_markers.append('有图表')
        
        details['professionalism'] = {
            'score': professional_score,
            'markers': professional_markers
        }
        
        # 计算内容质量总分
        total_content_score = (
            word_score * self.content_weights['word_count'] +
            data_score * self.content_weights['data_references'] +
            structure_score * self.content_weights['structure'] +
            professional_score * self.content_weights['professionalism']
        )
        
        return int(total_content_score), details
    
    def analyze_source_credibility(self, article: Dict) -> Tuple[int, Dict]:
        """
        分析来源信誉
        返回: (总分, 详细分数)
        """
        details = {}
        
        # 1. 认证状态
        account_desc = article.get('account_description', '')
        account_name = article.get('account_name', '')
        
        cert_score = 0
        cert_status = '未认证'
        
        if '认证' in account_desc or '官方' in account_desc or '✓' in account_name:
            cert_score = 20
            cert_status = '已认证'
        
        details['certification'] = {
            'score': cert_score,
            'status': cert_status
        }
        
        # 2. 粉丝影响力（通过公众号名称和描述推断）
        follower_score = 0
        follower_level = '未知'
        
        # 根据公众号类型推断粉丝量
        major_media = ['日报', '周刊', '新闻', '中国', '人民', '新华', '央视', '财经']
        large_account = ['研究院', '学会', '协会', '大学', '集团', '公司']
        
        if any(keyword in account_name for keyword in major_media):
            follower_score = 20
            follower_level = '100w+ 粉丝'
        elif any(keyword in account_name for keyword in large_account):
            follower_score = 15
            follower_level = '10w-100w 粉丝'
        else:
            follower_score = 10
            follower_level = '1w-10w 粉丝'
        
        details['follower_influence'] = {
            'score': follower_score,
            'level': follower_level
        }
        
        # 3. 更新频率（通过发布时间推断）
        pub_time_str = article.get('datetime', '')
        update_score = 0
        update_frequency = '未知'
        
        try:
            pub_time = datetime.strptime(pub_time_str, '%Y-%m-%d %H:%M:%S')
            days_old = (datetime.now() - pub_time).days
            
            if days_old <= 1:
                update_score = 20
                update_frequency = '日更'
            elif days_old <= 7:
                update_score = 15
                update_frequency = '周更'
            elif days_old <= 30:
                update_score = 10
                update_frequency = '月更'
            else:
                update_score = 5
                update_frequency = '不定期'
        except:
            update_score = 5
            update_frequency = '无法判断'
        
        details['update_frequency'] = {
            'score': update_score,
            'frequency': update_frequency,
            'days_old': days_old if 'days_old' in locals() else None
        }
        
        # 4. 机构类型
        institution_score = 0
        institution_type = '个人博客'
        
        official_keywords = ['日报', '周刊', '新闻', '中国', '人民', '新华', '央视', '财经', '经济']
        research_keywords = ['研究', '学院', '中心', '研究院', '学会', '协会', '大学']
        enterprise_keywords = ['公司', '集团', '银行', '基金', '证券', '保险']
        
        if any(keyword in account_name for keyword in official_keywords):
            institution_score = 40
            institution_type = '官方媒体'
        elif any(keyword in account_name for keyword in research_keywords):
            institution_score = 30
            institution_type = '研究机构'
        elif any(keyword in account_name for keyword in enterprise_keywords):
            institution_score = 20
            institution_type = '企业官号'
        else:
            institution_score = 10
            institution_type = '个人博客'
        
        details['institution_type'] = {
            'score': institution_score,
            'type': institution_type
        }
        
        # 计算信誉总分
        total_credibility_score = (
            cert_score * self.credibility_weights['certification'] +
            follower_score * self.credibility_weights['follower_influence'] +
            update_score * self.credibility_weights['update_frequency'] +
            institution_score * self.credibility_weights['institution_type']
        )
        
        return int(total_credibility_score), details
    
    def calculate_overall_score(self, content_score: int, credibility_score: int) -> int:
        """计算综合评分"""
        return int(content_score * 0.5 + credibility_score * 0.5)
    
    def get_recommendation(self, overall_score: int) -> Tuple[str, str]:
        """根据评分获取推荐等级和理由"""
        if overall_score >= 85:
            stars = '⭐⭐⭐⭐⭐'
            recommendation = '强烈推荐'
            reason = '优质内容，来源可信'
        elif overall_score >= 70:
            stars = '⭐⭐⭐⭐'
            recommendation = '推荐'
            reason = '内容不错，值得阅读'
        elif overall_score >= 55:
            stars = '⭐⭐⭐'
            recommendation = '可读'
            reason = '内容一般，可参考'
        elif overall_score >= 40:
            stars = '⭐⭐'
            recommendation = '参考'
            reason = '内容较弱，仅供参考'
        else:
            stars = '⭐'
            recommendation = '不推荐'
            reason = '质量较差，不建议阅读'
        
        return stars, recommendation, reason
    
    def analyze_article(self, article: Dict) -> Dict:
        """分析单篇文章"""
        content_score, content_details = self.analyze_content_quality(article)
        credibility_score, credibility_details = self.analyze_source_credibility(article)
        overall_score = self.calculate_overall_score(content_score, credibility_score)
        stars, recommendation, reason = self.get_recommendation(overall_score)
        
        return {
            'title': article.get('title', ''),
            'account_name': article.get('source', ''),
            'publish_time': article.get('datetime', ''),
            'url': article.get('url', ''),
            'summary': article.get('summary', '')[:100] + '...',
            'scores': {
                'content_quality': content_score,
                'source_credibility': credibility_score,
                'overall': overall_score
            },
            'details': {
                'content': content_details,
                'credibility': credibility_details
            },
            'recommendation': {
                'stars': stars,
                'level': recommendation,
                'reason': reason
            }
        }
    
    def analyze_batch(self, articles: List[Dict]) -> List[Dict]:
        """批量分析文章"""
        results = []
        for article in articles:
            try:
                result = self.analyze_article(article)
                results.append(result)
            except Exception as e:
                print(f"分析文章失败: {article.get('title', 'Unknown')} - {str(e)}", file=sys.stderr)
                continue
        
        # 按综合评分排序
        results.sort(key=lambda x: x['scores']['overall'], reverse=True)
        return results


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python analyze_quality.py <input_file> [--output <output_file>]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = None
    
    # 解析命令行参数
    if '--output' in sys.argv:
        output_idx = sys.argv.index('--output')
        if output_idx + 1 < len(sys.argv):
            output_file = sys.argv[output_idx + 1]
    
    # 读取输入文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    # 提取文章列表
    articles = data.get('articles', [])
    if not articles:
        print("未找到文章数据", file=sys.stderr)
        sys.exit(1)
    
    # 分析文章
    analyzer = ArticleQualityAnalyzer()
    results = analyzer.analyze_batch(articles)
    
    # 生成报告
    report = {
        'total_articles': len(articles),
        'analyzed_articles': len(results),
        'analysis_time': datetime.now().isoformat(),
        'articles': results,
        'summary': {
            'average_content_score': int(sum(r['scores']['content_quality'] for r in results) / len(results)) if results else 0,
            'average_credibility_score': int(sum(r['scores']['source_credibility'] for r in results) / len(results)) if results else 0,
            'average_overall_score': int(sum(r['scores']['overall'] for r in results) / len(results)) if results else 0,
            'top_3_articles': [
                {
                    'title': r['title'],
                    'account': r['account_name'],
                    'score': r['scores']['overall']
                }
                for r in results[:3]
            ]
        }
    }
    
    # 输出结果
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"分析完成，结果已保存到: {output_file}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        # 打印到控制台
        print_report(report)


def print_report(report: Dict):
    """打印分析报告"""
    import sys
    import io
    
    # 设置 UTF-8 输出
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "="*80)
    print("微信文章质量分析报告")
    print("="*80)
    print(f"分析时间: {report['analysis_time']}")
    print(f"总文章数: {report['total_articles']}")
    print(f"成功分析: {report['analyzed_articles']}")
    print()
    
    # 摘要统计
    summary = report['summary']
    print("[统计摘要]")
    print("-" * 80)
    print(f"平均内容质量分: {summary['average_content_score']}/100")
    print(f"平均来源信誉分: {summary['average_credibility_score']}/100")
    print(f"平均综合评分: {summary['average_overall_score']}/100")
    print()
    
    # 排名前3
    print("[排名前3的文章]")
    print("-" * 80)
    for i, article in enumerate(summary['top_3_articles'], 1):
        print(f"{i}. {article['title']}")
        print(f"   来源: {article['account']}")
        print(f"   评分: {article['score']}/100")
    print()
    
    # 详细列表
    print("[详细分析结果]")
    print("-" * 80)
    for i, article in enumerate(report['articles'], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源: {article['account_name']}")
        print(f"   发布: {article['publish_time']}")
        print(f"   内容质量: {article['scores']['content_quality']}/100")
        print(f"   来源信誉: {article['scores']['source_credibility']}/100")
        print(f"   综合评分: {article['scores']['overall']}/100")
        print(f"   推荐: {article['recommendation']['stars']} {article['recommendation']['level']}")
        print(f"   理由: {article['recommendation']['reason']}")
        
        # 详细分析
        content = article['details']['content']
        print(f"   内容分析:")
        print(f"     - 字数: {content['word_count']['actual']} ({content['word_count']['level']})")
        print(f"     - 数据: {content['data_references']['count']} 个 ({content['data_references']['level']})")
        print(f"     - 结构: {content['structure']['completeness']} ({', '.join(content['structure']['items'])})")
        
        credibility = article['details']['credibility']
        print(f"   信誉分析:")
        print(f"     - 认证: {credibility['certification']['status']}")
        print(f"     - 粉丝: {credibility['follower_influence']['level']}")
        print(f"     - 更新: {credibility['update_frequency']['frequency']}")
        print(f"     - 类型: {credibility['institution_type']['type']}")


if __name__ == '__main__':
    main()
