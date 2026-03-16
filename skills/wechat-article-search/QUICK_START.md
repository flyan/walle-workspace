# 微信文章质量评估系统 - 快速参考

## 🎯 一句话总结
自动搜索微信文章，综合分析内容质量和来源信誉，生成评分和推荐等级。

## ⚡ 最快开始（30秒）

```powershell
cd C:\Users\flyan\.openclaw\workspace\skills\wechat-article-search
.\analyze_wechat_articles.ps1 -Keyword "你的关键词" -Count 20
```

## 📊 评分一览表

| 评分 | 等级 | 推荐 | 说明 |
|------|------|------|------|
| 85+ | ⭐⭐⭐⭐⭐ | 强烈推荐 | 优质内容，来源可信 |
| 70-84 | ⭐⭐⭐⭐ | 推荐 | 内容不错，值得阅读 |
| 55-69 | ⭐⭐⭐ | 可读 | 内容一般，可参考 |
| 40-54 | ⭐⭐ | 参考 | 内容较弱，仅供参考 |
| <40 | ⭐ | 不推荐 | 质量较差，不建议阅读 |

## 🔍 评分构成

```
综合评分 = 内容质量(50%) + 来源信誉(50%)

内容质量 = 字数(30%) + 数据(30%) + 结构(20%) + 专业性(20%)
来源信誉 = 认证(20%) + 粉丝(20%) + 更新(20%) + 机构(40%)
```

## 📝 常用命令

### 基础搜索和分析
```powershell
# 搜索 20 篇文章并分析
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20

# 显示详细分析结果
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20 -ShowDetails

# 自定义数量
.\analyze_wechat_articles.ps1 -Keyword "区块链" -Count 50
```

### 分步执行
```bash
# 只搜索
node scripts/search_wechat.js "金融科技" -n 20 -r -o results.json

# 只分析
python analyze_quality.py results.json --output analysis.json

# 只查看报告
python analyze_quality.py results.json
```

### 批量处理
```powershell
# 分析多个关键词
$keywords = @("金融科技", "区块链", "人工智能", "大数据")
foreach ($keyword in $keywords) {
    .\analyze_wechat_articles.ps1 -Keyword $keyword -Count 15
}
```

## 📂 文件说明

| 文件 | 说明 |
|------|------|
| `analyze_quality.py` | 质量分析引擎（15KB） |
| `analyze_wechat_articles.ps1` | PowerShell 自动化脚本 |
| `QUALITY_ANALYSIS_GUIDE.md` | 完整使用指南 |
| `wechat_search_results_*.json` | 搜索结果（自动生成） |
| `wechat_analysis_*.json` | 分析报告（自动生成） |

## 🎨 输出示例

```
[统计摘要]
平均内容质量分: 72/100
平均来源信誉分: 78/100
平均综合评分: 75/100

[排名前3的文章]
1. 2024年金融科技发展报告
   来源: 中国金融时报
   评分: 92/100 ⭐⭐⭐⭐⭐

2. 金融科技创新趋势分析
   来源: 某研究院
   评分: 85/100 ⭐⭐⭐⭐

3. 区块链在金融中的应用
   来源: 金融科技周刊
   评分: 78/100 ⭐⭐⭐⭐
```

## 💡 使用技巧

### 1. 快速筛选高质量文章
```powershell
# 搜索 50 篇，系统自动排序，前 3 名就是最好的
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 50
```

### 2. 对比不同来源
```powershell
# 分别搜索不同公众号的观点
.\analyze_wechat_articles.ps1 -Keyword "金融科技 央行" -Count 20
.\analyze_wechat_articles.ps1 -Keyword "金融科技 研究院" -Count 20
```

### 3. 定期监控新文章
```powershell
# 每天运行一次，自动保存结果
$date = Get-Date -Format "yyyy-MM-dd"
.\analyze_wechat_articles.ps1 -Keyword "金融科技" -Count 20 | Tee-Object "report_$date.txt"
```

### 4. 导出数据分析
```python
# 将结果导出为 CSV，用 Excel 打开
python -c "
import json, csv
with open('analysis.json') as f:
    data = json.load(f)
with open('analysis.csv', 'w', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['标题', '公众号', '评分', '推荐'])
    for a in data['articles']:
        w.writerow([a['title'], a['account_name'], a['scores']['overall'], a['recommendation']['level']])
"
```

## ⚠️ 常见问题

**Q: 搜索返回空结果？**
A: 尝试更通用的关键词，或等待 10 分钟后重试

**Q: 评分很低？**
A: 摘要类文章本身内容就短，这是正常的。看排名前 3 的文章

**Q: 链接打不开？**
A: 文章可能被删除或过期，尝试在微信中直接搜索

**Q: 如何定期自动运行？**
A: 使用 Windows 任务计划程序，设置每天运行一次脚本

## 🔗 相关技能

- `wechat-article-search` - 微信文章搜索
- `wechat-article-extractor-skill` - 文章内容提取
- `firecrawl-search` - 全网搜索
- `baidu-search` - 百度搜索

## 📚 完整文档

详见：`QUALITY_ANALYSIS_GUIDE.md`

---

**最后更新：2026-03-14 19:33 GMT+8**
