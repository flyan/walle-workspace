#!/bin/bash
# 微信文章质量评估完整流程脚本
# 使用方法: bash analyze_wechat_articles.sh "搜索关键词" [数量]

set -e

KEYWORD="${1:-金融科技}"
NUM="${2:-20}"
SKILL_DIR="C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search"
RESULTS_FILE="wechat_search_results_$(date +%Y%m%d_%H%M%S).json"
ANALYSIS_FILE="wechat_analysis_$(date +%Y%m%d_%H%M%S).json"

echo "=========================================="
echo "微信文章质量评估系统"
echo "=========================================="
echo ""
echo "📝 搜索参数:"
echo "  关键词: $KEYWORD"
echo "  数量: $NUM"
echo ""

# 第一步：搜索文章
echo "第一步: 搜索微信文章..."
echo "命令: node scripts/search_wechat.js \"$KEYWORD\" -n $NUM -r -o $RESULTS_FILE"
echo ""

cd "$SKILL_DIR"
node scripts/search_wechat.js "$KEYWORD" -n $NUM -r -o "$RESULTS_FILE"

if [ ! -f "$RESULTS_FILE" ]; then
    echo "❌ 搜索失败"
    exit 1
fi

echo "✅ 搜索完成，找到 $(jq '.total' $RESULTS_FILE) 篇文章"
echo ""

# 第二步：分析质量
echo "第二步: 分析文章质量..."
echo "命令: python analyze_quality.py $RESULTS_FILE --output $ANALYSIS_FILE"
echo ""

python analyze_quality.py "$RESULTS_FILE" --output "$ANALYSIS_FILE"

if [ ! -f "$ANALYSIS_FILE" ]; then
    echo "❌ 分析失败"
    exit 1
fi

echo "✅ 分析完成"
echo ""

# 第三步：显示结果
echo "第三步: 显示分析结果..."
echo ""

python analyze_quality.py "$RESULTS_FILE"

echo ""
echo "=========================================="
echo "✅ 完成！"
echo "=========================================="
echo ""
echo "📁 文件位置:"
echo "  搜索结果: $RESULTS_FILE"
echo "  分析报告: $ANALYSIS_FILE"
echo ""
