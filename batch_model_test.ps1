#!/usr/bin/env pwsh
<#
OpenClaw 模型批量测试脚本
测试所有配置的模型可用性
#>

# 设置执行策略（如果需要）
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

$startTime = Get-Date
Write-Host "🚀 OpenClaw 模型批量测试开始" -ForegroundColor Green
Write-Host "开始时间: $startTime"
Write-Host "=" * 60

# 1. 获取所有配置的模型
Write-Host "📋 获取模型配置..." -ForegroundColor Cyan
$modelStatus = openclaw models status --plain
$models = @()

# 从输出中解析模型列表
$lines = $modelStatus -split "`n"
$inModelsSection = $false

foreach ($line in $lines) {
    if ($line -match "Configured models") {
        $inModelsSection = $true
        continue
    }
    
    if ($inModelsSection) {
        if ($line.Trim() -match "^[\w\-\.\/\[\]:]+$") {
            $models += $line.Trim()
        } elseif ([string]::IsNullOrWhiteSpace($line) -and $models.Count -gt 0) {
            break
        }
    }
}

if ($models.Count -eq 0) {
    # 如果解析失败，使用硬编码列表
    $models = @(
        "anthropic/claude-haiku-4-5-20251001",
        "gemini/[L]gemini-3-flash-preview",
        "gemini/[L]gemini-3-pro-preview-search",
        "deepseek/deepseek-chat",
        "deepseek/deepseek-reasoner",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "openrouter/free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "healer-alpha:free",
        "nvidia/nemotron-3-nano-30b-a3b:free",
        "openrouter/hunter-alpha:free",
        "anthropic/claude-sonnet-4-6",
        "anthropic/claude-opus-4-6",
        "gemini/[L]gemini-3-pro-preview"
    )
}

Write-Host "找到 $($models.Count) 个配置模型" -ForegroundColor Green

# 2. 准备测试结果存储
$results = @()
$testCount = 0

# 3. 批量测试函数
function Test-Model {
    param(
        [string]$modelName,
        [int]$timeoutSeconds = 30
    )
    
    $testCount++
    Write-Host "`n[$testCount/$($models.Count)] 测试模型: $modelName" -ForegroundColor Yellow
    
    # 创建临时会话ID
    $sessionId = "test-session-$([Guid]::NewGuid().ToString().Substring(0,8))"
    
    # 准备测试命令
    $env:OPENCLAW_MODEL = $modelName
    
    # 简单的测试消息
    $testMessage = "请回复'TEST_OK'以确认模型正常工作。当前时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    
    # 执行测试
    $startTest = Get-Date
    $success = $false
    $errorMessage = ""
    $responseTime = 0
    
    try {
        # 使用超时机制
        $job = Start-Job -ScriptBlock {
            param($model, $msg, $sid)
            $env:OPENCLAW_MODEL = $model
            $result = openclaw agent --local --agent main --message $msg --session-id $sid --json 2>&1
            return $result
        } -ArgumentList $modelName, $testMessage, $sessionId
        
        # 等待结果，带超时
        $jobResult = $job | Wait-Job -Timeout $timeoutSeconds
        
        if ($jobResult) {
            $output = $job | Receive-Job
            
            # 分析结果
            if ($output -match '"content"' -or $output -match 'TEST_OK' -or $output -match '"finishReason":"stop"') {
                $success = $true
                Write-Host "  ✅ 模型响应正常" -ForegroundColor Green
            } else {
                # 检查常见错误
                if ($output -match 'rate limit' -or $output -match 'quota') {
                    $errorMessage = "API配额不足"
                } elseif ($output -match 'timeout' -or $output -match 'timed out') {
                    $errorMessage = "请求超时"
                } elseif ($output -match 'auth' -or $output -match '403' -or $output -match '401') {
                    $errorMessage = "认证失败"
                } elseif ($output -match 'model not found' -or $output -match 'unknown model') {
                    $errorMessage = "模型未找到"
                } else {
                    $errorMessage = "未知错误: $($output | Select-String -Pattern 'error|Error|ERROR' -First 1)"
                }
                Write-Host "  ❌ 模型不可用: $errorMessage" -ForegroundColor Red
            }
            
            # 清理作业
            $job | Remove-Job -Force
        } else {
            # 超时
            $job | Stop-Job -Force
            $job | Remove-Job -Force
            $errorMessage = "测试超时 ($timeoutSeconds秒)"
            Write-Host "  ⏱️  测试超时" -ForegroundColor Yellow
        }
        
        $responseTime = ((Get-Date) - $startTest).TotalSeconds
        
    } catch {
        $errorMessage = "测试异常: $_"
        Write-Host "  ❌ 测试异常: $_" -ForegroundColor Red
    }
    
    # 清理环境变量
    Remove-Item Env:\OPENCLAW_MODEL -ErrorAction SilentlyContinue
    
    # 返回结果
    return @{
        Model = $modelName
        Success = $success
        Error = $errorMessage
        ResponseTime = [math]::Round($responseTime, 2)
        TestTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    }
}

# 4. 执行批量测试
Write-Host "`n🧪 开始批量测试..." -ForegroundColor Cyan
Write-Host "=" * 60

$availableModels = @()
$unavailableModels = @()

foreach ($model in $models) {
    $result = Test-Model -modelName $model -timeoutSeconds 15
    
    $results += $result
    
    if ($result.Success) {
        $availableModels += $result
    } else {
        $unavailableModels += $result
    }
    
    # 短暂延迟，避免API限流
    Start-Sleep -Seconds 2
}

# 5. 生成测试报告
Write-Host "`n📊 测试完成，生成报告..." -ForegroundColor Cyan
Write-Host "=" * 60

$endTime = Get-Date
$totalDuration = [math]::Round(($endTime - $startTime).TotalMinutes, 2)

Write-Host "测试统计:" -ForegroundColor Green
Write-Host "  总共测试: $($models.Count) 个模型"
Write-Host "  可用模型: $($availableModels.Count) 个"
Write-Host "  不可用模型: $($unavailableModels.Count) 个"
Write-Host "  总耗时: $totalDuration 分钟"
Write-Host ""

# 可用模型详情
if ($availableModels.Count -gt 0) {
    Write-Host "✅ 可用模型列表:" -ForegroundColor Green
    $availableModels | Sort-Object ResponseTime | ForEach-Object {
        Write-Host "  - $($_.Model)" -ForegroundColor Green
        Write-Host "    响应时间: $($_.ResponseTime)秒 | 测试时间: $($_.TestTime)"
    }
    Write-Host ""
}

# 不可用模型详情
if ($unavailableModels.Count -gt 0) {
    Write-Host "❌ 不可用模型列表:" -ForegroundColor Red
    $unavailableModels | Sort-Object Model | ForEach-Object {
        Write-Host "  - $($_.Model)" -ForegroundColor Red
        Write-Host "    错误: $($_.Error)"
    }
    Write-Host ""
}

# 6. 保存详细报告
$reportContent = @"
# OpenClaw 模型可用性批量测试报告

## 测试概览
- **测试开始**: $startTime
- **测试结束**: $endTime
- **总耗时**: $totalDuration 分钟
- **测试模型数**: $($models.Count)
- **可用模型**: $($availableModels.Count)
- **不可用模型**: $($unavailableModels.Count)

## 可用模型详情 ($($availableModels.Count))
$($availableModels | Sort-Object ResponseTime | ForEach-Object { 
"- **$($_.Model)**\n  - 响应时间: $($_.ResponseTime)秒\n  - 测试时间: $($_.TestTime)"
} | Out-String)

## 不可用模型详情 ($($unavailableModels.Count))
$($unavailableModels | Sort-Object Model | ForEach-Object {
"- **$($_.Model)**\n  - 错误: $($_.Error)"
} | Out-String)

## 测试配置
- 测试命令: `openclaw agent --local --agent main --message "TEST"`
- 超时设置: 15秒
- 测试环境: Windows PowerShell
- OpenClaw版本: $(openclaw --version 2>$null | Select-String 'OpenClaw')

## 建议
1. **立即可用的模型**: $($availableModels.Count -join ', ')
2. **需要修复的模型**: 检查API密钥和配额
3. **配置问题**: 更新错误的模型路径
4. **网络问题**: 检查网络连接和代理设置

---
*报告生成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')*
"@

$reportPath = "$env:USERPROFILE\.openclaw\workspace\model_batch_test_report.md"
$reportContent | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "📄 详细报告已保存至: $reportPath" -ForegroundColor Cyan

# 7. 总结和建议
Write-Host "`n💡 建议操作:" -ForegroundColor Yellow

if ($availableModels.Count -gt 0) {
    Write-Host "  1. 优先使用以下模型:" -ForegroundColor Green
    $fastestModel = $availableModels | Sort-Object ResponseTime | Select-Object -First 1
    Write-Host "     - $($fastestModel.Model) (最快, $($fastestModel.ResponseTime)秒)" -ForegroundColor Green
}

if ($unavailableModels.Count -gt 0) {
    Write-Host "  2. 需要修复的模型:" -ForegroundColor Yellow
    $unavailableModels | ForEach-Object {
        Write-Host "     - $($_.Model): $($_.Error)" -ForegroundColor Yellow
    }
}

Write-Host "`n✅ 批量测试完成!" -ForegroundColor Green