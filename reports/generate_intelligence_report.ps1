# 微信文章情报报告生成 - 一键执行脚本
# 用法: .\generate_intelligence_report.ps1 -Keyword "金融科技" -Days 7 -MinScore 70

param(
    [Parameter(Mandatory=$true)]
    [string]$Keyword,
    
    [int]$Days = 7,
    [int]$Count = 50,
    [int]$MinScore = 70,
    [switch]$ShowDetails
)

# 配置
$WorkspaceRoot = "C:\Users\flyan\.openclaw\workspace"
$ReportsDir = "$WorkspaceRoot\reports"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$SearchResultFile = "$ReportsDir\search_results_$Timestamp.json"
$ReportFile = "$ReportsDir\intelligence_report_$Timestamp.txt"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "微信文章情报报告生成系统" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 第一步：搜索文章
Write-Host "[第一步] 搜索微信文章..." -ForegroundColor Yellow
Write-Host "关键词: $Keyword"
Write-Host "时间范围: 最近 $Days 天"
Write-Host "数量限制: 最多 $Count 篇"
Write-Host ""

try {
    # 调用搜索脚本
    $SearchCmd = @(
        "python",
        "$ReportsDir\search_with_time_filter.py",
        $Keyword,
        "--num", $Count,
        "--days", $Days,
        "--output", $SearchResultFile
    )
    
    & $SearchCmd[0] $SearchCmd[1..($SearchCmd.Length-1)]
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "搜索失败" -ForegroundColor Red
        exit 1
    }
    
    # 检查结果
    if (-not (Test-Path $SearchResultFile)) {
        Write-Host "搜索结果文件不存在" -ForegroundColor Red
        exit 1
    }
    
    $SearchResults = Get-Content $SearchResultFile | ConvertFrom-Json
    $ArticleCount = $SearchResults.Count
    
    Write-Host "✓ 搜索完成，找到 $ArticleCount 篇文章" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "搜索异常: $_" -ForegroundColor Red
    exit 1
}

# 第二步：质量评分和报告生成
Write-Host "[第二步] 质量评分和报告生成..." -ForegroundColor Yellow
Write-Host "最低评分阈值: $MinScore"
Write-Host ""

try {
    $ReportCmd = @(
        "python",
        "$ReportsDir\generate_report.py",
        $SearchResultFile,
        "--min-score", $MinScore,
        "--output", $ReportFile
    )
    
    & $ReportCmd[0] $ReportCmd[1..($ReportCmd.Length-1)]
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "报告生成失败" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ 报告生成完成" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "报告生成异常: $_" -ForegroundColor Red
    exit 1
}

# 第三步：显示报告
Write-Host "[第三步] 报告内容" -ForegroundColor Yellow
Write-Host ""

if (Test-Path $ReportFile) {
    $ReportContent = Get-Content $ReportFile -Raw
    Write-Host $ReportContent
}

# 第四步：总结
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ 情报报告生成完成" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "输出文件:"
Write-Host "  搜索结果: $SearchResultFile"
Write-Host "  文本报告: $ReportFile"
Write-Host "  JSON报告: $($ReportFile -replace '\.txt$', '.json')"
Write-Host ""

# 可选：显示详细信息
if ($ShowDetails) {
    Write-Host "[详细信息]" -ForegroundColor Yellow
    Write-Host ""
    
    $JsonReport = Get-Content ($ReportFile -replace '\.txt$', '.json') | ConvertFrom-Json
    
    foreach ($article in $JsonReport) {
        Write-Host "标题: $($article.title)" -ForegroundColor Cyan
        Write-Host "来源: $($article.source)"
        Write-Host "评分: $($article.scores.overall)/100 $($article.recommendation.stars)"
        Write-Host "推荐: $($article.recommendation.level)"
        Write-Host "链接: $($article.url)"
        Write-Host ""
    }
}

# 可选：自动提交到 GitHub
Write-Host "[可选] 提交到 GitHub..." -ForegroundColor Yellow
Write-Host ""

try {
    Push-Location $WorkspaceRoot
    
    git add "reports/search_results_$Timestamp.json"
    git add "reports/intelligence_report_$Timestamp.txt"
    git add "reports/intelligence_report_$Timestamp.json"
    
    git commit -m "情报报告: $Keyword ($Timestamp)"
    git push origin main
    
    Write-Host "✓ 已提交到 GitHub" -ForegroundColor Green
    
    Pop-Location
}
catch {
    Write-Host "⚠ GitHub 提交失败 (可选): $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "完成！" -ForegroundColor Green
