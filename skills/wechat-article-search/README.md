# 微信文章质量评估系统

> 自动搜索、分析、评分微信公众号文章，帮助你快速识别高质量内容

## 🎯 核心功能

- ✅ **自动搜索** - 搜索微信公众号文章
- ✅ **内容分析** - 评估字数、数据、结构、专业性
- ✅ **信誉评估** - 分析认证、粉丝、更新频率、机构类型
- ✅ **综合评分** - 生成 0-100 的质量评分
- ✅ **推荐等级** - 从 ⭐ 到 ⭐⭐⭐⭐⭐ 的推荐等级
- ✅ **详细报告** - 生成 JSON 格式的分析报告

## 🚀 快速开始

### 最简单的方式（一行命令）

```powershell
cd C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20
```

### 显示详细分析

```powershell
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20 -ShowDetails
```

## 📊 评分体系

### 内容质量（50%）

| 指标 | 满分 | 说明 |
|------|------|------|
| 字数深度 | 30 | 3000+ 字为满分 |
| 数据引用 | 30 | 10+ 个数据点为满分 |
| 结构完整性 | 20 | 标题、摘要、正文、作者 |
| 专业性指标 | 20 | 专业术语、引用、图表 |

### 来源信誉（50%）

| 指标 | 满分 | 说明 |
|------|------|------|
| 认证状态 | 20 | 蓝 V 认证为满分 |
| 粉丝影响力 | 20 | 100w+ 粉丝为满分 |
| 更新频率 | 20 | 日更为满分 |
| 机构类型 | 40 | 官方媒体为满分 |

### 推荐等级

| 评分 | 等级 | 推荐 |
|------|------|------|
| 85-100 | ⭐⭐⭐⭐⭐ | 强烈推荐 |
| 70-84 | ⭐⭐⭐⭐ | 推荐 |
| 55-69 | ⭐⭐⭐ | 可读 |
| 40-54 | ⭐⭐ | 参考 |
| 0-39 | ⭐ | 不推荐 |

## 📁 文件结构

```
wechat-article-search/
├── scripts/
│   └── search_wechat.js          # 搜索脚本
├── analyze_quality.py             # 质量分析引擎（核心）
├── analyze_wechat_articles.ps1    # PowerShell 自动化脚本
├── README.md                      # 本文件
├── QUICK_START.md                 # 快速参考
├── QUALITY_ANALYSIS_GUIDE.md      # 完整使用指南
└── SKILL.md                       # 技能说明
```

## 💻 使用方式

### 方式一：PowerShell 自动化（推荐）

```powershell
# 基础用法
.\analyze_wechat_articles.ps1 -Keyword "关键词" -Count 20

# 显示详细分析
.\analyze_wechat_articles.ps1 -Keyword "关键词" -Count 20 -ShowDetails

# 自定义参数
.\analyze_wechat_articles.ps1 -Keyword "区块链" -Count 50 -ShowDetails
```

### 方式二：分步执行

```bash
# 第一步：搜索文章
node scripts/search_wechat.js "金融科技" -n 20 -r -o results.json

# 第二步：分析质量
python analyze_quality.py results.json --output analysis.json

# 第三步：查看报告
python analyze_quality.py results.json
```

### 方式三：批量处理

```powershell
# 分析多个关键词
$keywords = @("金融科技", "区块链", "人工智能", "大数据")
foreach ($keyword in $keywords) {
    .\analyze_wechat_articles.ps1 -Keyword $keyword -Count 15
}
```

## 📊 输出示例

```
================================================================================
微信文章质量分析报告
================================================================================
分析时间: 2026-03-14T19:27:09
总文章数: 20
成功分析: 20

[统计摘要]
平均内容质量分: 72/100
平均来源信誉分: 78/100
平均综合评分: 75/100

[排名前3的文章]
1. 2024年金融科技发展报告
   来源: 中国金融时报
   评分: 92/100

2. 金融科技创新趋势分析
   来源: 某研究院
   评分: 85/100

3. 区块链在金融中的应用
   来源: 金融科技周刊
   评分: 78/100

[详细分析结果]
1. 2024年金融科技发展报告
   来源: 中国金融时报
   发布: 2026-03-14 10:30:00
   内容质量: 85/100
   来源信誉: 95/100
   综合评分: 90/100
   推荐: ⭐⭐⭐⭐⭐ 强烈推荐
   理由: 优质内容，来源可信
   内容分析:
     - 字数: 3500 (深度分析)
     - 数据: 15 个 (数据充分)
     - 结构: 4/4 (标题, 摘要, 正文, 作者)
   信誉分析:
     - 认证: 已认证
     - 粉丝: 100w+ 粉丝
     - 更新: 日更
     - 类型: 官方媒体
```

## 🔧 高级功能

### 导出 CSV 格式

```python
import json
import csv

with open('analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

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

### 定期自动运行

使用 Windows 任务计划程序：

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天 9:00 AM）
4. 设置操作：
   ```
   程序: powershell.exe
   参数: -ExecutionPolicy Bypass -File "C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search\analyze_wechat_articles.ps1" -Keyword "金融科技" -Count 20
   ```

## 📚 文档

- **快速参考** - 见 `QUICK_START.md`
- **完整指南** - 见 `QUALITY_ANALYSIS_GUIDE.md`
- **技能说明** - 见 `SKILL.md`

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

## 🐛 故障排除

### 搜索返回空结果

**原因**：关键词过于特殊或搜狗限制

**解决**：
- 尝试更通用的关键词
- 等待 10 分钟后重试
- 检查网络连接

### 分析脚本出错

**原因**：Python 环境问题或文件格式错误

**解决**：
```bash
# 检查 Python 版本
python --version

# 验证 JSON 文件
python -m json.tool results.json
```

### 链接无法打开

**原因**：文章被删除或链接过期

**解决**：
- 检查发布时间
- 尝试在微信中直接搜索
- 查看是否有备份链接

## 🔗 相关技能

- `wechat-article-search` - 微信文章搜索
- `wechat-article-extractor-skill` - 文章内容提取
- `firecrawl-search` - 全网搜索
- `baidu-search` - 百度搜索

## 📞 支持

遇到问题？

1. 查看 `QUALITY_ANALYSIS_GUIDE.md` 中的故障排除部分
2. 检查 `QUICK_START.md` 中的常见问题
3. 验证 Python 和 Node.js 环境

## 📝 更新日志

### v1.0.0 (2026-03-14)

- ✅ 完成内容质量分析引擎
- ✅ 完成来源信誉评估系统
- ✅ 完成 PowerShell 自动化脚本
- ✅ 完成完整使用指南
- ✅ 完成快速参考卡片

## 📄 许可证

仅供学习和研究使用。

---

**最后更新：2026-03-14 19:33 GMT+8**

**作者：Kiro AI Assistant**
