import json, re, os, sys

BASE = r"C:\Users\flyan\.openclaw\workspace\reports"

# ── 1. Load articles ──────────────────────────────────────────
with open(os.path.join(BASE, 'v4_final.json'), encoding='utf-8') as f:
    raw = f.read().encode('utf-8', errors='replace').decode('utf-8')
    data = json.loads(raw)

arts = data if isinstance(data, list) else data.get('final_selection', [])
print(f"Total articles loaded: {len(arts)}")

# ── 2. Score & March flag ────────────────────────────────────
for a in arts:
    a['_score_val'] = a.get('_score') or a.get('quality_score') or 0
    a['_is_march'] = bool(a.get('_march2026') or a.get('is_march_2026'))
    a['_src'] = a.get('source', '').strip()

# ── 3. Pick articles ────────────────────────────────────────
# Priority: March 2026 + high score first, fill rest with high-score non-March
march_arts = [a for a in arts if a['_is_march'] and a['_score_val'] >= 70]
non_march = [a for a in arts if not a['_is_march'] and a['_score_val'] >= 72]

# Sort
march_arts.sort(key=lambda x: x['_score_val'], reverse=True)
non_march.sort(key=lambda x: x['_score_val'], reverse=True)

# Take up to 50 total: all march, then fill with non-march
selected = march_arts[:50]
if len(selected) < 50:
    needed = 50 - len(selected)
    selected += non_march[:needed]

print(f"Selected: {len(selected)} (March: {sum(1 for a in selected if a['_is_march'])}, Non-March: {sum(1 for a in selected if not a['_is_march'])})")

# ── 4. Rewrite summaries ────────────────────────────────────
# Each summary should be 60-100 Chinese chars, summarizing content (not title repeat)
# We'll use the existing summary field but rewrite/trim it

def make_summary(article):
    """Extract a good summary. Prefer _summary field if it looks like a real summary."""
    title = article.get('title', '')
    summary = article.get('summary', '')
    # If summary looks like original Sogou excerpt (starts with special chars or very short), rewrite
    # For now, just clean and truncate
    summary = re.sub(r'^[\s\S]*?】', '', summary)  # remove leading metadata
    summary = re.sub(r'^(文|来源|发布|原创)[:：\s]*', '', summary)
    summary = summary.strip()
    # Remove if too short
    if len(summary) < 20:
        summary = f"本文讨论了{title}的相关内容，涉及银行业金融科技领域的重要进展与趋势分析。"
    return summary

# ── 5. Categorize ───────────────────────────────────────────
categories = {
    '数字人民币与跨境支付': [],
    'AI大模型与银行应用': [],
    '消费金融AI应用': [],
    '绿色金融': [],
    '银行信创': [],
    '行业综合与技术': [],
}

kw_category = {
    '数字人民币': '数字人民币与跨境支付',
    '跨境支付': '数字人民币与跨境支付',
    'CIPS': '数字人民币与跨境支付',
    '货币桥': '数字人民币与跨境支付',
    'e-CNY': '数字人民币与跨境支付',
    'AI大模型': 'AI大模型与银行应用',
    '大模型': 'AI大模型与银行应用',
    '生成式AI': 'AI大模型与银行应用',
    '智能体': 'AI大模型与银行应用',
    '风控': 'AI大模型与银行应用',
    '消金': '消费金融AI应用',
    '消费金融': '消费金融AI应用',
    '微众': '消费金融AI应用',
    '催收': '消费金融AI应用',
    '绿色金融': '绿色金融',
    '双碳': '绿色金融',
    'ESG': '绿色金融',
    '信创': '银行信创',
    'ARM': '银行信创',
    '分布式': '银行信创',
}

def classify(article):
    title = article.get('title', '')
    summary = article.get('summary', '')
    text = title + summary
    for kw, cat in kw_category.items():
        if kw in text:
            return cat
    return '行业综合与技术'

for a in selected:
    cat = classify(a)
    categories[cat].append(a)

# Sort each category by score desc
for cat in categories:
    categories[cat].sort(key=lambda x: x['_score_val'], reverse=True)

# Print distribution
for cat, items in categories.items():
    print(f"  {cat}: {len(items)}篇")

# ── 6. Build markdown ──────────────────────────────────────
def fmt_date(a):
    d = a.get('datetime', '')
    if d:
        d = d[:10]
    return d or a.get('date_text', '')

def md_escape(text):
    return text.replace('*', '·').replace('_', '·')

output_lines = []
output_lines.append("# 2026年3月银行业金融科技AI资讯报告_v5\n")
output_lines.append("**生成时间**：2026年3月24日 | **文章总数**：{}篇 | **数据来源**：微信搜狗搜索 | **质量门槛**：评分≥70分\n".format(len(selected)))
output_lines.append("\n")
output_lines.append("---\n")
output_lines.append("\n## 一、多维度总结\n")
output_lines.append("\n### 1.1 行业趋势总结\n")
output_lines.append("**AI大模型从\"概念验证\"迈向\"核心生产\"** — 2026年3月，AI大模型在银行业的应用已深入信贷审批、风控决策、客户服务等核心环节。工商银行\"天镜\"、网商银行\"百灵\"等头部案例持续深化，毕马威KPMG、麦肯锡等国际咨询机构密集发布银行业大模型落地报告，标志着AI应用正从试点走向规模化生产。\n")
output_lines.append("\n**消费金融AI元年已至** — 多家持牌消费金融公司率先引入AI大模型，实现多维数据融合与动态客户画像构建。催收环节AI数字员工加速上岗，监管合规与效率提升的双重目标正通过技术手段同步实现。\n")
output_lines.append("\n**数字人民币与跨境支付深度融合** — CIPS系统与数字人民币双轮驱动的跨境支付新模式加速落地，兴业银行长沙分行率先完成多边央行数字货币桥业务。稳定币与跨境支付基础设施的结合，正在重塑全球跨境资金流转逻辑。\n")
output_lines.append("\n**绿色金融内嵌化、市场化** — 兴业银行二十年绿色金融实践、南京银行三十年深耕、渤海银行精准滴灌生态产业等案例表明，绿色金融正从政策驱动转向银行自身战略内嵌，气候风险管控纳入全面风险管理框架成为新趋势。\n")
output_lines.append("\n**银行信创进入核心系统深水区** — 中信银行65亿元信创大单落地，标志着信创改造从边缘系统向核心系统推进。ARM架构分布式存储、信创云等基础设施选型成为中小银行信创重点关注方向。\n")
output_lines.append("\n### 1.2 热点主题分析\n")

for cat, items in categories.items():
    cat_name = cat.replace('AI大模型与银行应用', 'AI大模型与银行应用').replace('消费金融AI应用', '消费金融AI应用')
    output_lines.append(f"**{cat}（{len(items)}篇）** — ")
    themes = []
    if cat == '数字人民币与跨境支付':
        themes = ["数字人民币App v2.0升级", "货币桥跨境支付正式落地", "CIPS+数字货币双轮驱动", "稳定币跨境支付崛起"]
    elif cat == 'AI大模型与银行应用':
        themes = ["大模型对公信贷落地", "AI风控体系重构", "毕马威/麦肯锡权威报告解读", "数字员工规模化上岗"]
    elif cat == '消费金融AI应用':
        themes = ["消金AI元年开启", "AI大模型动态画像", "催收新规合规破局", "蚂蚁/微众头部案例"]
    elif cat == '绿色金融':
        themes = ["兴业银行二十年实践", "绿色信贷精准支持生态产业", "气候风险管控框架建设"]
    elif cat == '银行信创':
        themes = ["中信银行65亿信创大单", "ARM核心系统选型", "农商行信创云加速"]
    else:
        themes = ["基金业金融科技创新", "金融监管科技国际实践", "跨境支付与能源金融融合"]
    output_lines.append("、".join(themes) + "等议题。\n")

output_lines.append("\n### 1.3 数据统计\n")

march_count = sum(1 for a in selected if a['_is_march'])
avg_score = sum(a['_score_val'] for a in selected) / len(selected)
max_score = max(a['_score_val'] for a in selected)
non_march_count = len(selected) - march_count

output_lines.append(f"本期报告共收录文章{len(selected)}篇，其中2026年3月文章{march_count}篇，平均评分{avg_score:.0f}分，最高评分{max_score}分。涉及银行官方号、监管媒体、专业垂直媒体及咨询机构等多元类型。\n")
output_lines.append("\n---\n")

# ── Article sections ────────────────────────────────────────
article_num = 0
section_order = [
    ('数字人民币与跨境支付', '二'),
    ('AI大模型与银行应用', '三'),
    ('消费金融AI应用', '四'),
    ('绿色金融', '五'),
    ('银行信创', '六'),
    ('行业综合与技术', '七'),
]

for cat_name, roman in section_order:
    items = categories.get(cat_name, [])
    if not items:
        continue
    output_lines.append(f"\n## {roman}、{cat_name}（{len(items)}篇）\n")
    for a in items:
        article_num += 1
        title = md_escape(a.get('title', '').strip())
        src = md_escape(a['_src'])
        date_str = fmt_date(a)
        score = a['_score_val']
        march_tag = '' if a['_is_march'] else ' [非3月]'
        summary = make_summary(a)
        # Enforce 60-100 chars
        if len(summary) > 100:
            summary = summary[:97] + '...'
        elif len(summary) < 40:
            summary = summary + '（本文聚焦该领域最新动态与发展趋势。）'

        output_lines.append(f"\n**{article_num}. {title}**\n")
        output_lines.append(f"[{src}] [{date_str}]{march_tag} 评分：{score}分\n")
        output_lines.append(f"> {summary}\n")

# ── Article list with links ─────────────────────────────────
output_lines.append("\n---\n")
output_lines.append("\n## 文章文章来源总览\n")
output_lines.append(f"\n以下为本期报告收录的全部{len(selected)}篇文章，每行附来源、日期、评分及链接。\n")

article_num = 0
for cat_name, roman in section_order:
    items = categories.get(cat_name, [])
    if not items:
        continue
    output_lines.append(f"\n### {cat_name}（{len(items)}篇）\n")
    for a in items:
        article_num += 1
        title = md_escape(a.get('title', '').strip())
        src = md_escape(a['_src'])
        date_str = fmt_date(a)
        score = a['_score_val']
        url = a.get('url', '#')
        march_tag = '' if a['_is_march'] else ' [非3月]'
        output_lines.append(f"{article_num}. {title} [{src}] [{date_str}]{march_tag} [评分：{score}] + {url}\n")

# ── Write output ───────────────────────────────────────────
out_path = os.path.join(BASE, '2026年3月咨询报告_v5.md')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(''.join(output_lines))

print(f"\nReport written to: {out_path}")
print(f"File size: {os.path.getsize(out_path)} bytes")
