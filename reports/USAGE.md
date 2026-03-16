# 微信文章情报系统 - 使用指南

## 系统概述

这是一个完整的微信文章情报搜索、质量评分和报告生成系统。支持：

- ✅ 按时间过滤（最近 N 天）
- ✅ 质量评分（内容 + 信誉）
- ✅ 倒金字塔报告结构
- ✅ 一键执行
- ✅ 批量搜索多个关键词
- ✅ 自动提交 GitHub

## 文件结构

```
reports/
├── config.json                          # 配置文件（公众号、策略、阈值）
├── search_with_time_filter.py          # 优化的搜索脚本（支持时间过滤）
├── generate_report.py                   # 质量评分和报告生成
├── generate_intelligence_report.ps1     # 一键执行脚本
├── batch_intelligence_report.ps1        # 批量搜索脚本
├── USAGE.md                             # 本文件
├── search_results_*.json                # 搜索结果（自动生成）
├── intelligence_report_*.txt            # 文本报告（自动生成）
├── intelligence_report_*.json           # JSON 报告（自动生成）
└── intelligence_summary_*.txt           # 汇总报告（自动生成）
```

## 快速开始

### 方式一：一键执行（推荐）

```powershell
cd C:\Users\flyan\.openclaw\workspace\reports

# 搜索单个关键词
.\generate_intelligence_report.ps1 -Keyword "金融科技" -Days 7 -MinScore 70

# 显示详细信息
.\generate_intelligence_report.ps1 -Keyword "AI" -Days 7 -ShowDetails

# 自定义参数
.\generate_intelligence_report.ps1 -Keyword "银行转型" -Days 14 -Count 100 -MinScore 75
```

### 方式二：批量搜索

```powershell
# 使用预定义策略
.\batch_intelligence_report.ps1 -Strategy "ai_frontier" -Days 7

# 自定义关键词
.\batch_intelligence_report.ps1 -Keywords @("金融科技", "AI", "支付") -Days 7

# 不自动提交 GitHub
.\batch_intelligence_report.ps1 -Strategy "banking_transformation" -NoCommit
```

### 方式三：分步执行

```powershell
# 第一步：搜索
python search_with_time_filter.py "金融科技" --num 50 --days 7 --output results.json

# 第二步：生成报告
python generate_report.py results.json --min-score 70 --output report.txt

# 第三步：查看报告
Get-Content report.txt
```

## 参数说明

### generate_intelligence_report.ps1

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-Keyword` | string | 必填 | 搜索关键词 |
| `-Days` | int | 7 | 保留最近 N 天的文章 |
| `-Count` | int | 50 | 最多搜索 N 篇文章 |
| `-MinScore` | int | 70 | 最低评分阈值 |
| `-ShowDetails` | switch | false | 显示详细信息 |

### batch_intelligence_report.ps1

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-Strategy` | string | 可选 | 使用预定义策略 |
| `-Keywords` | string[] | 可选 | 自定义关键词列表 |
| `-Accounts` | string[] | 可选 | 自定义公众号列表 |
| `-Days` | int | 7 | 保留最近 N 天的文章 |
| `-Count` | int | 50 | 最多搜索 N 篇文章 |
| `-MinScore` | int | 70 | 最低评分阈值 |
| `-ShowDetails` | switch | false | 显示详细信息 |
| `-NoCommit` | switch | false | 不自动提交 GitHub |

## 配置文件 (config.json)

### 公众号分类

```json
{
  "accounts": {
    "ai": ["机器之心", "量子位", "新智元", ...],
    "fintech": ["馨金融", "零壹财经", ...],
    "payment": ["移动支付网", "支付百科"],
    ...
  }
}
```

### 搜索策略

```json
{
  "search_strategies": {
    "ai_frontier": {
      "keywords": ["大模型", "AI前沿", "生成式AI"],
      "accounts": ["机器之心", "量子位", "新智元"],
      "priority": 1
    },
    ...
  }
}
```

### 质量阈值

```json
{
  "quality_thresholds": {
    "high_quality": 85,      # 强烈推荐
    "recommended": 70,       # 推荐
    "acceptable": 55,        # 可读
    "reference": 40          # 参考
  }
}
```

## 质量评分体系

### 内容质量 (0-50 分)

- **字数深度** (0-30 分)
  - > 2000 字: 30 分
  - > 1000 字: 20 分
  - > 500 字: 10 分

- **数据引用** (0-20 分)
  - 包含数字、百分比、金额等: 20 分

- **结构完整性** (0-20 分)
  - 包含摘要、总结、结论等: 10 分

- **专业性** (0-20 分)
  - 包含专业术语、引用等: 10 分

### 来源信誉 (0-50 分)

- **官方认证** (0-20 分)
  - 央行、监管部门等: 20 分
  - 研究院、论坛: 15 分

- **机构类型** (0-30 分)
  - 官方媒体: 40 分
  - 研究机构: 35 分
  - 财经媒体: 25 分
  - 企业: 15 分

### 综合评分

```
总分 = 内容质量 × 50% + 来源信誉 × 50%

85-100: ⭐⭐⭐⭐⭐ 强烈推荐
70-84:  ⭐⭐⭐⭐ 推荐
55-69:  ⭐⭐⭐ 可读
40-54:  ⭐⭐ 参考
0-39:   ⭐ 不推荐
```

## 报告格式

### 倒金字塔结构

1. **统计摘要** - 平均评分、文章数量
2. **排名前 10** - 最高质量的文章
3. **详细索引** - 所有符合条件的文章

### 输出文件

- `intelligence_report_*.txt` - 文本格式报告
- `intelligence_report_*.json` - JSON 格式报告（便于进一步处理）
- `search_results_*.json` - 原始搜索结果

## 预定义策略

### 1. AI 前沿 (ai_frontier)

```powershell
.\batch_intelligence_report.ps1 -Strategy "ai_frontier"
```

关键词: 大模型、AI前沿、生成式AI、AGI
公众号: 机器之心、量子位、新智元

### 2. 支付创新 (payment_innovation)

```powershell
.\batch_intelligence_report.ps1 -Strategy "payment_innovation"
```

关键词: 数字人民币、第三方支付、跨境支付
公众号: 移动支付网、支付百科、十字财经

### 3. 消费金融 (consumer_finance)

```powershell
.\batch_intelligence_report.ps1 -Strategy "consumer_finance"
```

关键词: 风控、助贷、消费金融
公众号: 消金界、第一消费金融、零壹财经

### 4. 银行转型 (banking_transformation)

```powershell
.\batch_intelligence_report.ps1 -Strategy "banking_transformation"
```

关键词: 数字化、开放银行、零售转型
公众号: 金融数字化观察、零售银行、轻金融

### 5. 监管政策 (regulatory_policy)

```powershell
.\batch_intelligence_report.ps1 -Strategy "regulatory_policy"
```

关键词: 监管、政策、罚单、降准
公众号: 央行发布、国家金融监督管理总局、澎湃新闻

### 6. 高管动态 (executive_dynamics)

```powershell
.\batch_intelligence_report.ps1 -Strategy "executive_dynamics"
```

关键词: 人事、高管、战略
公众号: 行长要参、中国银行业杂志

## 常见用法

### 每日情报汇总

```powershell
# 每天早上 8 点运行
.\batch_intelligence_report.ps1 -Strategy "ai_frontier" -Days 1
.\batch_intelligence_report.ps1 -Strategy "regulatory_policy" -Days 1
.\batch_intelligence_report.ps1 -Strategy "banking_transformation" -Days 1
```

### 周度深度分析

```powershell
# 每周一运行
.\batch_intelligence_report.ps1 -Strategy "ai_frontier" -Days 7 -Count 100 -MinScore 75
.\batch_intelligence_report.ps1 -Strategy "fintech" -Days 7 -Count 100 -MinScore 75
```

### 特定主题研究

```powershell
# 研究特定主题
.\generate_intelligence_report.ps1 -Keyword "数字人民币" -Days 30 -Count 200 -MinScore 65
.\generate_intelligence_report.ps1 -Keyword "开放银行" -Days 30 -Count 200 -MinScore 65
```

### 自动化定时任务

在 Windows 任务计划程序中创建定时任务：

```powershell
# 每天 8:00 AM 运行
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\Users\flyan\.openclaw\workspace\reports\batch_intelligence_report.ps1 -Strategy ai_frontier"
$Trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
Register-ScheduledTask -TaskName "DailyIntelligenceReport" -Action $Action -Trigger $Trigger
```

## 故障排除

### 搜索返回空结果

- 检查关键词是否正确
- 尝试更通用的关键词
- 增加 `-Count` 参数
- 检查网络连接

### Python 脚本错误

```powershell
# 检查 Python 版本
python --version

# 检查 JSON 文件格式
python -m json.tool search_results_*.json

# 运行脚本时显示详细错误
python search_with_time_filter.py "关键词" 2>&1
```

### GitHub 提交失败

```powershell
# 检查 Git 配置
git config --list

# 手动提交
cd C:\Users\flyan\.openclaw\workspace
git add reports/
git commit -m "情报报告"
git push origin main
```

## 高级用法

### 自定义质量评分

编辑 `generate_report.py` 中的 `QualityAnalyzer` 类：

```python
def analyze_content_quality(self, title, summary, content=''):
    # 修改评分逻辑
    score = 0
    # ...
    return min(score, 50)
```

### 扩展公众号列表

编辑 `config.json` 中的 `accounts` 部分：

```json
{
  "accounts": {
    "custom_category": [
      "新公众号1",
      "新公众号2"
    ]
  }
}
```

### 添加新的搜索策略

编辑 `config.json` 中的 `search_strategies` 部分：

```json
{
  "search_strategies": {
    "my_strategy": {
      "keywords": ["关键词1", "关键词2"],
      "accounts": ["公众号1", "公众号2"],
      "priority": 1
    }
  }
}
```

## 性能优化

### 减少搜索时间

```powershell
# 减少搜索数量
.\generate_intelligence_report.ps1 -Keyword "金融科技" -Count 20

# 减少时间范围
.\generate_intelligence_report.ps1 -Keyword "金融科技" -Days 3
```

### 并行搜索

```powershell
# 使用 PowerShell 并行处理
$Keywords = @("金融科技", "AI", "支付")
$Keywords | ForEach-Object -Parallel {
    .\generate_intelligence_report.ps1 -Keyword $_ -NoCommit
}
```

## 数据导出

### 导出为 CSV

```powershell
# 从 JSON 转换为 CSV
$Json = Get-Content "intelligence_report_*.json" | ConvertFrom-Json
$Json | Export-Csv "report.csv" -Encoding UTF8 -NoTypeInformation
```

### 导出为 Excel

```powershell
# 需要安装 ImportExcel 模块
Install-Module ImportExcel -Force

$Json = Get-Content "intelligence_report_*.json" | ConvertFrom-Json
$Json | Export-Excel "report.xlsx" -AutoSize
```

## 支持和反馈

如有问题或建议，请：

1. 检查本文档的故障排除部分
2. 查看脚本的注释和文档
3. 检查 GitHub 提交历史
4. 联系系统管理员

---

**最后更新**: 2026-03-15
**版本**: 1.0
