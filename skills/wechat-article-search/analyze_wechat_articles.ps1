# 微信文章质量评估完整流程脚本 (PowerShell)
# 使用方法: .\analyze_wechat_articles.ps1 -Keyword "搜索关键词" -Count 20

param(
    [string]$Keyword = "金融科技",
    [int]$Count = 20,
    [switch]$ShowDetails = $false
)

$SkillDir = "C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ResultsFile = "wechat_search_results_$Timestamp.json"
$AnalysisFile = "wechat_analysis_$Timestamp.json"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "微信文章质量评估系统" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 搜索参数:" -ForegroundColor Yellow
Write-Host "  关键词: $Keyword"
Write-Host "  数量: $Count"
Write-Host ""

# 第一步：搜索文章
Write-Host "第一步: 搜索微信文章..." -ForegroundColor Green
Write-Host "命令: node scripts/search_wechat.js `"$Keyword`" -n $Count -r -o $ResultsFile"
Write-Host ""

Push-Location $SkillDir

try {
    & node scripts/search_wechat.js $Keyword -n $Count -r -o $ResultsFile
    
    if (-not (Test-Path $ResultsFile)) {
        Write-Host "❌ 搜索失败" -ForegroundColor Red
        exit 1
    }
    
    $searchResult = Get-Content $ResultsFile | ConvertFrom-Json
    $totalArticles = $searchResult.total
    
    Write-Host "✅ 搜索完成，找到 $totalArticles 篇文章" -ForegroundColor Green
    Write-Host ""
    
    # 第二步：分析质量
    Write-Host "第二步: 分析文章质量..." -ForegroundColor Green
    Write-Host "命令: python analyze_quality.py $ResultsFile --output $AnalysisFile"
    Write-Host ""
    
    & python analyze_quality.py $ResultsFile --output $AnalysisFile
    
    if (-not (Test-Path $AnalysisFile)) {
        Write-Host "❌ 分析失败" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ 分析完成" -ForegroundColor Green
    Write-Host ""
    
    # 第三步：显示结果
    Write-Host "第三步: 显示分析结果..." -ForegroundColor Green
    Write-Host ""
    
    $analysisResult = Get-Content $AnalysisFile | ConvertFrom-Json
    
    # 显示摘要
    Write-Host "📊 统计摘要" -ForegroundColor Yellow
    Write-Host ("-" * 80)
    Write-Host "平均内容质量分: $($analysisResult.summary.average_content_score)/100"
    Write-Host "平均来源信誉分: $($analysisResult.summary.average_credibility_score)/100"
    Write-Host "平均综合评分: $($analysisResult.summary.average_overall_score)/100"
    Write-Host ""
    
    # 显示排名前3
    Write-Host "🏆 排名前3的文章" -ForegroundColor Yellow
    Write-Host ("-" * 80)
    $i = 1
    foreach ($article in $analysisResult.summary.top_3_articles) {
        Write-Host "$i. $($article.title)"
        Write-Host "   来源: $($article.account)"
        Write-Host "   评分: $($article.score)/100"
        Write-Host ""
        $i++
    }
    
    # 显示详细列表
    if ($ShowDetails) {
        Write-Host "📋 详细分析结果" -ForegroundColor Yellow
        Write-Host ("-" * 80)
        
        $i = 1
        foreach ($article in $analysisResult.articles) {
            Write-Host ""
            Write-Host "$i. $($article.title)" -ForegroundColor Cyan
            Write-Host "   来源: $($article.account_name)"
            Write-Host "   发布: $($article.publish_time)"
            Write-Host "   内容质量: $($article.scores.content_quality)/100"
            Write-Host "   来源信誉: $($article.scores.source_credibility)/100"
            Write-Host "   综合评分: $($article.scores.overall)/100"
            Write-Host "   推荐: $($article.recommendation.stars) $($article.recommendation.level)"
            Write-Host "   理由: $($article.recommendation.reason)"
            
            # 内容分析
            $content = $article.details.content
            Write-Host "   内容分析:"
            Write-Host "     - 字数: $($content.word_count.actual) ($($content.word_count.level))"
            Write-Host "     - 数据: $($content.data_references.count) 个 ($($content.data_references.level))"
            Write-Host "     - 结构: $($content.structure.completeness) ($($content.structure.items -join ', '))"
            
            # 信誉分析
            $credibility = $article.details.credibility
            Write-Host "   信誉分析:"
            Write-Host "     - 认证: $($credibility.certification.status)"
            Write-Host "     - 粉丝: $($credibility.follower_influence.level)"
            Write-Host "     - 更新: $($credibility.update_frequency.frequency)"
            Write-Host "     - 类型: $($credibility.institution_type.type)"
            
            $i++
        }
    }
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "✅ 完成！" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📁 文件位置:" -ForegroundColor Yellow
    Write-Host "  搜索结果: $(Resolve-Path $ResultsFile)"
    Write-Host "  分析报告: $(Resolve-Path $AnalysisFile)"
    Write-Host ""
    Write-Host "💡 提示: 使用 -ShowDetails 参数查看完整分析结果"
    Write-Host "  示例: .\analyze_wechat_articles.ps1 -Keyword '金融科技' -Count 20 -ShowDetails"
    Write-Host ""
    
}
finally {
    Pop-Location
}
