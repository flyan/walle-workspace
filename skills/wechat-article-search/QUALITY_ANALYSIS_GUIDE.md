# 微信文章质量评估系统 - 完整使用指南

## 📋 系统概述

这是一个综合的微信公众号文章质量评估系统，结合了**内容质量分析**和**来源信誉评估**，帮助你快速识别高质量的微信文章。

### 核心功能

- ✅ 自动搜索微信公众号文章
- ✅ 分析文章内容质量（字数、数据、结构、专业性）
- ✅ 评估来源信誉（认证、粉丝、更新频率、机构类型）
- ✅ 生成综合评分和推荐等级
- ✅ 输出详细分析报告

---

## 🚀 快速开始

### 方式一：使用 PowerShell 脚本（推荐）

```powershell
# 基础用法
cd C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20

# 显示详细分析
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20 -ShowDetails

# 自定义参数
.\analyze_wechat_articles.ps1 -Keyword "区块链" -Count 30 -ShowDetails
```

### 方式二：分步执行

```bash
# 第一步：搜索文章
cd C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search
node scripts/search_wechat.js "金融科技" -n 20 -r -o results.json

# 第二步：分析质量
python analyze_quality.py results.json --output analysis.json

# 第三步：查看报告
python analyze_quality.py results.json
```

---

## 📊 评分体系详解

### 内容质量评分（50%）

#### 1. 字数深度（30分）
- **3000+ 字**：30分 - 深度分析
- **2000-3000 字**：20分 - 中等深度
- **1000-2000 字**：10分 - 快讯/观点
- **<1000 字**：0分 - 内容过短

#### 2. 数据引用（30分）
- **10+ 个数据点**：30分 - 数据充分
- **5-10 个数据点**：20分 - 有数据支撑
- **1-5 个数据点**：10分 - 部分数据
- **0 个数据点**：0分 - 无数据引用

数据点包括：百分比、金额、年份、序号、小数等

#### 3. 结构完整性（20分）
- 标题：5分
- 摘要：5分
- 正文：5分
- 作者：5分

#### 4. 专业性指标（20分）
- 有专业术语：10分
- 有引用/参考：5分
- 有图表描述：5分

### 来源信誉评分（50%）

#### 1. 认证状态（20分）
- **已认证**（蓝 V）：20分
- **未认证**：0分

#### 2. 粉丝影响力（20分）
- **100w+ 粉丝**：20分
- **10w-100w 粉丝**：15分
- **1w-10w 粉丝**：10分
- **<1w 粉丝**：0分

#### 3. 更新频率（20分）
- **日更**：20分
- **周更**：15分
- **月更**：10分
- **不定期**：5分

#### 4. 机构类型（40分）
- **官方媒体**（日报、新闻、央视等）：40分
- **研究机构**（研究院、学会、大学等）：30分
- **企业官号**（公司、银行、基金等）：20分
- **个人博客**：10分

### 综合评分

```
综合评分 = 内容质量分 × 50% + 来源信誉分 × 50%
```

#### 推荐等级

| 评分范围 | 等级 | 推荐 | 说明 |
|---------|------|------|------|
| 85-100 | ⭐⭐⭐⭐⭐ | 强烈推荐 | 优质内容，来源可信 |
| 70-84 | ⭐⭐⭐⭐ | 推荐 | 内容不错，值得阅读 |
| 55-69 | ⭐⭐⭐ | 可读 | 内容一般，可参考 |
| 40-54 | ⭐⭐ | 参考 | 内容较弱，仅供参考 |
| 0-39 | ⭐ | 不推荐 | 质量较差，不建议阅读 |

---

## 📁 输出文件说明

### 搜索结果文件 (JSON)

```json
{
  "query": "金融科技",
  "total": 20,
  "articles": [
    {
      "title": "文章标题",
      "url": "https://mp.weixin.qq.com/s?...",
      "summary": "文章摘要",
      "datetime": "2026-03-14 10:30:00",
      "date_text": "2026年03月14日",
      "source": "公众号名称"
    }
  ]
}
```

### 分析报告文件 (JSON)

```json
{
  "total_articles": 20,
  "analyzed_articles": 20,
  "analysis_time": "2026-03-14T19:30:00",
  "summary": {
    "average_content_score": 72,
    "average_credibility_score": 78,
    "average_overall_score": 75,
    "top_3_articles": [...]
  },
  "articles": [
    {
      "title": "文章标题",
      "account_name": "公众号名称",
      "publish_time": "2026-03-14 10:30:00",
      "url": "https://mp.weixin.qq.com/s?...",
      "scores": {
        "content_quality": 85,
        "source_credibility": 90,
        "overall": 87
      },
      "recommendation": {
        "stars": "⭐⭐⭐⭐⭐",
        "level": "强烈推荐",
        "reason": "优质内容，来源可信"
      },
      "details": {
        "content": {...},
        "credibility": {...}
      }
    }
  ]
}
```

---

## 💡 使用示例

### 示例 1：搜索金融科技文章

```powershell
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20 -ShowDetails
```

**输出示例：**
```
==========================================
微信文章质量评估系统
==========================================

📝 搜索参数:
  关键词: 金融科技
  数量: 20

第一步: 搜索微信文章...
✅ 搜索完成，找到 20 篇文章

第二步: 分析文章质量...
✅ 分析完成

📊 统计摘要
────────────────────────────────────────
平均内容质量分: 72/100
平均来源信誉分: 78/100
平均综合评分: 75/100

🏆 排名前3的文章
────────────────────────────────────────
1. 2024年金融科技发展报告
   来源: 中国金融时报
   评分: 92/100

2. 金融科技创新趋势分析
   来源: 某研究院
   评分: 85/100

3. 区块链在金融中的应用
   来源: 金融科技周刊
   评分: 78/100
```

### 示例 2：分步执行

```bash
# 搜索
node scripts/search_wechat.js "区块链" -n 15 -r -o blockchain_results.json

# 分析
python analyze_quality.py blockchain_results.json --output blockchain_analysis.json

# 查看报告
python analyze_quality.py blockchain_results.json
```

---

## 🔧 高级用法

### 批量分析多个关键词

```powershell
$keywords = @("金融科技", "区块链", "人工智能", "大数据")

foreach ($keyword in $keywords) {
    Write-Host "分析: $keyword" -ForegroundColor Green
    .\analyze_wechat_articles.ps1 -Keyword $keyword -Count 15
    Write-Host ""
}
```

### 导出 CSV 格式

```python
import json
import csv

# 读取分析结果
with open('analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 导出为 CSV
with open('analysis.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['标题', '公众号', '发布时间', '内容质量', '来源信誉', '综合评分', '推荐等级'])
    
    for article in data['articles']:
        writer.writerow([
            article['title'],
            article['account_name'],
            article['publish_time'],
            article['scores']['content_quality'],
            article['scores']['source_credibility'],
            article['scores']['overall'],
            article['recommendation']['level']
        ])
```

---

## ⚠️ 注意事项

1. **反爬虫限制**
   - 搜狗微信有严格的反爬虫机制
   - 过度使用可能导致 IP 被封禁
   - 建议每次搜索间隔 5-10 分钟

2. **数据准确性**
   - 评分基于可获取的公开信息
   - 某些数据（如粉丝数）是推断值
   - 建议结合人工审核

3. **链接有效性**
   - 某些文章可能因版权或违规被删除
   - 链接可能过期或无法访问
   - 建议及时保存重要文章

4. **仅供参考**
   - 本系统仅用于学习和研究目的
   - 不用于商业用途或大规模爬取
   - 请遵守相关网站的使用条款

---

## 📞 故障排除

### 问题 1：搜索返回空结果

**原因**：关键词过于特殊或搜狗限制

**解决**：
- 尝试更通用的关键词
- 等待 10 分钟后重试
- 检查网络连接

### 问题 2：分析脚本出错

**原因**：Python 环境问题或文件格式错误

**解决**：
```bash
# 检查 Python 版本
python --version

# 检查依赖
pip list

# 验证 JSON 文件
python -m json.tool results.json
```

### 问题 3：链接无法打开

**原因**：文章被删除或链接过期

**解决**：
- 检查发布时间
- 尝试在微信中直接搜索
- 查看是否有备份链接

---

## 📚 相关资源

- 微信搜索技能：`wechat-article-search`
- 文章提取技能：`wechat-article-extractor-skill`
- 全网搜索技能：`firecrawl-search`、`baidu-search`

---

## 🎯 下一步

1. **集成到 Second Brain**
   - 将高质量文章自动保存到知识库
   - 按评分和主题分类

2. **定期监控**
   - 设置定时任务
   - 自动搜索和分析新文章

3. **数据可视化**
   - 生成评分分布图
   - 显示趋势分析

4. **智能推荐**
   - 基于评分推荐文章
   - 个性化内容筛选

---

**祝你使用愉快！** 🎉
