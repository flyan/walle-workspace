# sync-and-push.ps1
# 自动同步所有 agent 工作目录到主仓库，然后提交和推送到 GitHub

param(
    [string]$CommitMessage = "Auto-sync: Update agents workspaces"
)

$ErrorActionPreference = "Stop"

# 定义路径
$WorkspaceRoot = "C:\Users\flyan\.openclaw\workspace"
$AgentsWorkspacesDir = "$WorkspaceRoot\agents-workspaces"
$WriterExternal = "C:\Users\flyan\.openclaw\workspace-writer"
$CoderExternal = "C:\Users\flyan\.openclaw\workspace-coder"

Write-Host "🔄 开始同步 agents 工作目录..." -ForegroundColor Cyan

# 同步 writer
if (Test-Path $WriterExternal) {
    Write-Host "  📁 同步 writer..." -ForegroundColor Yellow
    $WriterTarget = "$AgentsWorkspacesDir\writer"
    
    if (Test-Path $WriterTarget) {
        Remove-Item "$WriterTarget\*" -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        New-Item -ItemType Directory -Path $WriterTarget -Force | Out-Null
    }
    
    Get-ChildItem -Path $WriterExternal -Exclude ".git" -Force | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $WriterTarget -Recurse -Force
    }
    
    Write-Host "    ✓ writer 同步完成" -ForegroundColor Green
}

# 同步 coder
if (Test-Path $CoderExternal) {
    Write-Host "  📁 同步 coder..." -ForegroundColor Yellow
    $CoderTarget = "$AgentsWorkspacesDir\coder"
    
    if (Test-Path $CoderTarget) {
        Remove-Item "$CoderTarget\*" -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        New-Item -ItemType Directory -Path $CoderTarget -Force | Out-Null
    }
    
    Get-ChildItem -Path $CoderExternal -Exclude ".git" -Force | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $CoderTarget -Recurse -Force
    }
    
    Write-Host "    ✓ coder 同步完成" -ForegroundColor Green
}

Write-Host ""
Write-Host "📊 检查 git 状态..." -ForegroundColor Cyan

# 进入工作目录
Set-Location $WorkspaceRoot

# 检查是否有变更
$status = git status --short
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "✓ 没有新的变更，无需提交" -ForegroundColor Green
    exit 0
}

Write-Host "发现以下变更:" -ForegroundColor Yellow
Write-Host $status

Write-Host ""
Write-Host "📝 添加文件到 git..." -ForegroundColor Cyan

# 添加所有变更
git add -A
Write-Host "✓ 文件已添加" -ForegroundColor Green

Write-Host ""
Write-Host "💾 提交变更..." -ForegroundColor Cyan

# 提交
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$fullMessage = "$CommitMessage ($timestamp)"
git commit -m $fullMessage
Write-Host "✓ 提交完成: $fullMessage" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 推送到 GitHub..." -ForegroundColor Cyan

# 推送
git push origin main
Write-Host "✓ 推送完成" -ForegroundColor Green

Write-Host ""
Write-Host "✅ 同步和推送完成！" -ForegroundColor Green

# 显示最新的 commit 信息
Write-Host ""
Write-Host "📌 最新 commit:" -ForegroundColor Cyan
git log --oneline -1
