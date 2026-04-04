# -*- coding: utf-8 -*-
import json, os, re

BASE = r\"C:\\Users\\flyan\\.openclaw\\workspace\\reports\"

with open(os.path.join(BASE, 'top20_march2026.json'), encoding='utf-8') as f:
    arts = json.load(f)

# Clean summaries: remove embedded URL lines
def clean_summary(s):
    # Remove lines starting with '> 🔗 链接:' or containing URLs
    lines = s.split('\
')
    clean = [l for l in lines if not l.strip().startswith('🔗') and 'weixin.sogou.com' not in l and 'http' not in l]
    return ' '.join(' '.join(clean).split()).strip()

for a in arts:
    a['summary'] = clean_summary(a['summary'])

# Manual categorization based on titles
def categorize(title, source):
    t = title + source
    if any(k in t for k in ['数字人民币', '跨境支付', 'CIPS', '稳定币', 'RedotPay', 'Omise', '货币桥', '双轮驱动']):
        return 'digital_rmb'
    if any(k in t for k in ['消费金融', '消金', '催收', '微众', '马上消费', '持牌', '华道']):
        return 'consumer_finance'
    if any(k in t for k in ['信创', 'ARM', '宇信']):
        return 'xinchuan'
    if any(k in t for k in ['绿色', '双碳', '生态', '南京银行', '渤海银行', '蒙商']):
        return 'green'
    if any(k in t for k in ['AI', '大模型', '风控', '金融科技', 'FinTech', 'CB Insights', '毕马威', 'KPMG', '嵌入式', '数字金融']):
        return 'ai_bank'
    return 'ai_bank'

for a in arts:
    a['category'] = categorize(a['title'], a['source'])

categories = {
    'digital_rmb': ('二、数字人民币与跨境支付', []),
    'ai_bank': ('三、AI大模型与银行应用', []),
    'consumer_finance': ('四、消费金融AI应用', []),
    'green': ('五、绿色金融', []),
    'xinchuan': ('六、银行信创', []),
}

for a in arts:
    cat = a['category']
    if cat in categories:
        categories[cat][1].append(a)
    else:
        categories['ai_bank'][1].append(a)

# Print category distribution
for k, (title, lst) in categories.items():
    print(f\"{title}: {len(lst)}篇\")
    for a in lst:
        print(f\"  [{a['score']}] {a['source']}: {a['title'][:35]}\")

# Build report
lines = []
lines.append('# 2026年3月银行业金融科技AI资讯报告')
lines.append('')
lines.append('**生成时间**：2026年3月24日 | **文章总数**：20篇 | **数据来源**：微信搜狗搜索 | **评分门槛**：≥70分')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## 一、多维度总结')
lines.append('')
lines.append('### 1.1 行业趋势总结')
lines.append('')
lines.append('**AI大模型从试点走向核心生产** — 2026年3月，大模型在银行业的应用已深入信贷审批、风控决策、客户服务等核心环节。AI智能体（Agent）对银行传统风控体系形成新挑战，平安银行关闭个人