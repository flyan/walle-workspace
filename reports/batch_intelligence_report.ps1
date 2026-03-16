# 批量情报搜索和报告生成
# 用法: .\batch_intelligence_report.ps1 -Strategy "ai_frontier" -Days 7

param(
    [Parameter(Mandatory=$false)]
    [string]$Strategy,
    
    [string[]]$Keywords,
    [string[]]$Accounts,
    [int]$Days = 7,
    [int]$Count = 50,
    [int]$MinScore = 70,
    [switch]$ShowDetails,
    [switch]$NoCommit
)

# 配置
$WorkspaceRoot = "C:\Users\flyan\.openclaw\workspace"
$ReportsDir = "$WorkspaceRoot\reports"
$ConfigFile = "$ReportsDir\config.json"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "批量情报搜索和报告生成系统" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 加载配置
if (Test-Path $ConfigFile) {
    $Config = Get-Content $ConfigFile | ConvertFrom-Json
    Write-Host "✓ 配置已加载" -ForegroundColor Green
}
else {
    Write-Host "⚠ 配置文件不存在: $ConfigFile" -ForegroundColor Yellow
    $Config = $null
}

# 确定搜索策略
if ($Strategy -and $Config) {
    if ($Config.search_strategies.PSObject.Properties.Name -contains $Strategy) {
        $StrategyConfig = $Config.search_strategies.$Strategy
        $Keywords = $StrategyConfig.keywords
        $Accounts = $StrategyConfig.accounts
        Write-Host "使用策略: $Strategy" -ForegroundColor Yellow
        Write-Host "关键词: $($Keywords -join ', ')"
        Write-Host "公众号: $($Accounts -join ', ')"
        Write-Host ""
    }
    else {
        Write-Host "⚠ 策略不存在: $Strategy" -ForegroundColor Yellow
    }
}

# 如果没有指定关键词，使用默认
if (-not $Keywords) {
    $Keywords = @("金融科技", "AI", "银行")
}

# 执行搜索
$AllResults = @()
$ReportFiles = @()

foreach ($Keyword in $Keywords) {
    Write-Host "[搜索] $Keyword" -ForegroundColor Yellow
    
    $SearchResultFile = "$ReportsDir\search_results_${Keyword}_$Timestamp.json"
    $ReportFile = "$ReportsDir\intelligence_report_${Keyword}_$Timestamp.txt"
    
    try {
        # 搜索
        $SearchCmd = @(
            "python",
            "$ReportsDir\search_with_time_filter.py",
            $Keyword,
            "--num", $Count,
            "--days", $Days,
            "--output", $SearchResultFile
        )
        
        & $SearchCmd[0] $SearchCmd[1..($SearchCmd.Length-1)] | Out-Null
        
        if (-not (Test-Path $SearchResultFile)) {
            Write-Host "  ⚠ 搜索失败" -ForegroundColor Yellow
            continue
        }
        
        $SearchResults = Get-Content $SearchResultFile | ConvertFrom-Json
        $ArticleCount = $SearchResults.Count
        
        Write-Host "  ✓ 找到 $ArticleCount 篇文章" -ForegroundColor Green
        
        # 生成报告
        $ReportCmd = @(
            "python",
            "$ReportsDir\generate_report.py",
            $SearchResultFile,
            "--min-score", $MinScore,
            "--output", $ReportFile
        )
        
        & $ReportCmd[0] $ReportCmd[1..($ReportCmd.Length-1)] | Out-Null
        
        if (Test-Path $ReportFile) {
            Write-Host "  ✓ 报告已生成" -ForegroundColor Green
            $ReportFiles += $ReportFile
        }
        
        $AllResults += @{
            Keyword = $Keyword
            Count = $ArticleCount
            ReportFile = $ReportFile
        }
    }
    catch {
        Write-Host "  ✗ 异常: $_" -ForegroundColor Red
    }
    
    Write-Host ""
}

# 生成汇总报告
Write-Host "[汇总] 生成综合报告..." -ForegroundColor Yellow
Write-Host ""

$SummaryFile = "$ReportsDir\intelligence_summary_$Timestamp.txt"
$SummaryContent = @()

$SummaryContent += "=" * 80
$SummaryContent += "微信文章情报汇总报告"
$SummaryContent += "=" * 80
$SummaryContent += "生成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$SummaryContent += "搜索关键词: $($Keywords -join ', ')"
$SummaryContent += "时间范围: 最近 $Days 天"
$SummaryContent += ""

$SummaryContent += "[搜索统计]"
foreach ($Result in $AllResults) {
    $SummaryContent += "$($Result.Keyword): $($Result.Count) 篇文章"
}
$SummaryContent += ""

$SummaryContent += "[报告文件]"
foreach ($ReportFile in $ReportFiles) {
    $SummaryContent += "- $(Split-Path $ReportFile -Leaf)"
}
$SummaryContent += ""

$SummaryContent += "[详细报告内容]"
$SummaryContent += ""

foreach ($ReportFile in $ReportFiles) {
    if (Test-Path $ReportFile) {
        $SummaryContent += "---"
        $SummaryContent += "$(Split-Path $ReportFile -Leaf)"
        $SummaryContent += "---"
        $SummaryContent += ""
        $SummaryContent += Get-Content $ReportFile
        $SummaryContent += ""
    }
}

$SummaryContent | Out-File $SummaryFile -Encoding UTF8

Write-Host "✓ 汇总报告已生成: $SummaryFile" -ForegroundColor Green
Write-Host ""

# 显示汇总
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ 批量搜索完成" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "输出文件:"
Write-Host "  汇总报告: $SummaryFile"
foreach ($ReportFile in $ReportFiles) {
    Write-Host "  详细报告: $(Split-Path $ReportFile -Leaf)"
}
Write-Host ""

# 可选：自动提交到 GitHub
if (-not $NoCommit) {
    Write-Host "[可选] 提交到 GitHub..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        Push-Location $WorkspaceRoot
        
        git add "reports/search_results_*_$Timestamp.json"
        git add "reports/intelligence_report_*_$Timestamp.txt"
        git add "reports/intelligence_report_*_$Timestamp.json"
        git add "reports/intelligence_summary_$Timestamp.txt"
        
        git commit -m "批量情报报告: $($Keywords -join ', ') ($Timestamp)"
        git push origin main
        
        Write-Host "✓ 已提交到 GitHub" -ForegroundColor Green
        
        Pop-Location
    }
    catch {
        Write-Host "⚠ GitHub 提交失败 (可选): $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "完成！" -ForegroundColor Green
