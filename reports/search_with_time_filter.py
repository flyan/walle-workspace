#!/usr/bin/env python3
"""
优化的微信文章搜索脚本 - 支持时间过滤
搜索最近 N 天内的文章，并返回结构化数据
"""

import json
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def parse_date(date_str):
    """解析多种日期格式"""
    formats = [
        "%Y-%m-%d",
        "%Y年%m月%d日",
        "%m-%d",
        "%m月%d日",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def filter_by_date(articles, days=7):
    """
    按发布时间过滤文章
    
    Args:
        articles: 文章列表
        days: 保留最近 N 天的文章（默认 7 天）
    
    Returns:
        过滤后的文章列表
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered = []
    
    for article in articles:
        pub_time = article.get('datetime', '')
        if not pub_time:
            continue
        
        # 尝试解析发布时间
        parsed_date = parse_date(pub_time)
        if parsed_date and parsed_date >= cutoff_date:
            filtered.append(article)
    
    return filtered

def search_wechat(keyword, num=20, days=7, resolve_url=True):
    """
    搜索微信文章并按时间过滤
    
    Args:
        keyword: 搜索关键词
        num: 返回数量
        days: 保留最近 N 天的文章
        resolve_url: 是否解析真实链接
    
    Returns:
        过滤后的文章列表
    """
    try:
        # 调用原始搜索脚本
        cmd = [
            'node',
            'skills/wechat-article-search/scripts/search_wechat.js',
            keyword,
            '-n', str(num),
        ]
        
        if resolve_url:
            cmd.append('-r')
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"搜索失败: {result.stderr}", file=sys.stderr)
            return []
        
        # 解析 JSON 输出
        try:
            data = json.loads(result.stdout)
            articles = data if isinstance(data, list) else data.get('articles', [])
        except json.JSONDecodeError:
            print(f"JSON 解析失败", file=sys.stderr)
            return []
        
        # 按时间过滤
        filtered = filter_by_date(articles, days)
        
        return filtered
    
    except subprocess.TimeoutExpired:
        print(f"搜索超时", file=sys.stderr)
        return []
    except Exception as e:
        print(f"搜索异常: {e}", file=sys.stderr)
        return []

def main():
    if len(sys.argv) < 2:
        print("用法: python search_with_time_filter.py <keyword> [--num N] [--days D] [--output FILE]")
        sys.exit(1)
    
    keyword = sys.argv[1]
    num = 20
    days = 7
    output_file = None
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--num':
            num = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--days':
            days = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--output':
            output_file = sys.argv[i+1]
            i += 2
        else:
            i += 1
    
    # 执行搜索
    print(f"搜索: {keyword} (最近 {days} 天, 最多 {num} 篇)")
    articles = search_wechat(keyword, num, days)
    
    print(f"找到 {len(articles)} 篇文章")
    
    # 输出结果
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"已保存到: {output_file}")
    else:
        print(json.dumps(articles, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
