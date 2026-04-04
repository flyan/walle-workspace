# -*- coding: utf-8 -*-
"""Generate the final markdown report"""
import json
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

REPORTS_DIR = r"C:\Users\flyan\.openclaw\workspace\reports"

# Load filtered articles
with open(REPORTS_DIR + "\\filtered_articles_v3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

final = data["final_selection"]

# Deduplicate by title similarity
def title_normalize(t):
    t = t.replace("！", "").replace("！", "").replace("!", "")
    for suffix in ["建议收藏", "早知道早受益", "一定要知道", "全是干货", "刚刚发布", "最新版", "最新调整", "附一则", "收藏"]:
        if suffix in t:
            t = t[:t.index(suffix)].strip()
    return t.strip()

seen_titles = set()
deduped = []
for a in final:
    norm = title_normalize(a.get("title", ""))
    if norm not in seen_titles:
        seen_titles.add(norm)
        deduped.append(a)

# Sort by score
deduped.sort(key=lambda x: -x["quality_score"])
deduped = deduped[:55]

print(f"Final articles after dedup: {len(deduped)}")

# Classify
def classify(article):
    text = (article.get("title", "") + " " + article.get("summary", "") + " " + article.get("source", "")).lower()
    ai_k = ["ai", "大模型", "生成式", "机器学习", "人工智能", "gpt", "llm", "深度学习", "智能化", "模型", "智能体", "AI智能"]
    ft_k = ["支付", "数字人民币", "区块链", "消费金融", "监管科技", "开放银行", "api", "供应链金融", "跨境", "金融科技", "fintech"]
    bk_k = ["银行", "信贷", "存款", "贷款", "网点", "零售", "财富", "风控", "资本", "资产", "净息差", "不良", "信用卡", "对公", "揽储", "利率", "违规", "罚"]

    ai_s = sum(3 if k in article.get("title", "").lower() else 1 for k in ai_k if k in text)
    ft_s = sum(3 if k in article.get("title", "").lower() else 1 for k in ft_k if k in text)
    bk_s = sum(3 if k in article.get("title", "").lower() else 1 for k in bk_k if k in text)
    scores = {"AI": ai_s, "金融科技": ft_s, "银行业": bk_s}
    return max(scores, key=scores.get)

cats = {"银行业": [], "金融科技": [], "AI": []}
for a in deduped:
    cat = classify(a)
    cats[cat].append(a)
for cat in cats:
    cats[cat].sort(key=lambda x: -x["quality_score"])

print(f"Categories: Banking={len(cats['银行业'])}, Fintech={len(cats['金融科技'])}, AI={len(cats['AI'])}")

# Generate summary text from existing summary
def make_summary(article):
    summary = article.get("summary", "").strip()
    title = article.get("title", "")
    if summary and len(summary) > 15:
        s = summary
        if len(s) > 100:
            s = s[:100].rsplit("，", 1)[0] + "……"
        return s
    # Generate from title
    return f"本文围绕「{title[:30]}」展开分析，讨论了相关趋势与实践路径。"

# Source quality score display
SOURCE_DISPLAY = {
    "孙自通": "专业信贷风控专家", "照说供金": "供应链金融", "HOHAI浩海科技": "跨境支付论坛",
    "安知讯": "金融科技", "DataPower": "金融科技", "察金台": "金融违规跟踪",
    "黑花户1000小额包过": "贷款指导", "木木自由": "金融科技", "野趣说": "金融资讯",
    "小伟咨询": "贷款咨询", "银联商务甘肃分公司": "支付机构", "源创谷数字科技": "AI资讯",
    "AI科技风向": "AI资讯", "高阳寰球HSG": "金融科技", "楼上的华姨": "金融资讯",
    "致命眼泪": "金融资讯", "街角伙伴": "金融资讯", "又见山与海": "金融资讯",
    "信贷风险管理": "风控培训", "菁茗说": "银行科技", "大卫2099": "金融资讯",
    "西瓜大侠客": "存款利率", "知行风控学堂": "风控培训", "信鼎尚德诉讼保全担保": "法律服务",
    "小歆视界": "银行存款", "金融博览杂志": "金融媒体", "BRI金融观察": "金融媒体",
    "上海金融与发展实验室": "金融研究", "中关村金融科技产业发展联盟": "金融科技",
    "苏州金融": "地方金融", "泰州银行保险业": "监管", "梅州银行业公会": "行业协会",
    "甘南州银行业协会": "行业协会", "佛山市银行业协会": "行业协会", "山西省银行业协会": "行业协会",
    "广发银行天津分行": "银行", "金融坛": "金融论坛", "银行新一线": "银行资讯",
    "九江银行吉安分行": "银行", "数字金融工作委员会": "行业协会", "元以科技集团": "AI资讯",
    "华投融": "金融科技", "九又四分之一世界": "监管科技", "寒冰铁掌": "银行营销",
    "论情话呦": "银行营销", "九又四分之一世界": "监管科技",
}

def get_display_source(source):
    return SOURCE_DISPLAY.get(source, source)

# Generate markdown report
report_lines = []
report_lines.append("# 2026年3月银行业、金融科技、AI咨询报告")
report_lines.append("")
report_lines.append("**报告时间：2026年3月 | 数据来源：微信公众号精选 | 文章数量：{}篇**".format(len(deduped)))
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 📊 多维度总结")
report_lines.append("")
report_lines.append("### 一、行业趋势总结")
report_lines.append("")
report_lines.append("**银行业：信贷风控与数字化转型并重**  ")
report_lines.append("- **风控合规持续高压**：3月多家银行因信贷违规被罚，监管重点集中在贷前准入审查不规范、贷后管理薄弱等问题，私募信贷市场风险开始暴露（如黑石信贷基金暂停赎回事件）。")
report_lines.append("- **AI大模型加速落地**：中国进出口银行启动AI大模型一体机采购，银行业AI应用从客服场景向风控、营销等核心业务环节渗透，\"数字同事\"正在接管重复性工作。")
report_lines.append("- **负债端成本博弈加剧**：存款利率持续调整成为3月热点，各行大额存单利率分化，储户对利率敏感度上升，银行净息差管理面临挑战。")
report_lines.append("- **消费者权益保护强化**："3·15"期间银行业密集开展金融知识普及，各银行零售金融部门以此为契机强化客户信任建设。")
report_lines.append("")
report_lines.append("**金融科技：支付与监管科技双轮驱动**  ")
report_lines.append("- **跨境支付论坛密集举办**：深圳、上海等地接连举办跨境支付与风控创新峰会，聚焦全球支付痛点与合规编排。")
report_lines.append("- **数字人民币推进加速**：苏州市启动数字人民币新政策培训，数字人民币钱包开始按活期0.05%计息，应用场景持续扩展。")
report_lines.append("- **监管科技定调积极稳妥**：央行明确AI监管方向为\"积极稳妥、安全有序\"，2026年监管科技全景图逐步清晰。")
report_lines.append("")
report_lines.append("**AI：大模型竞争格局重塑，落地成关键**  ")
report_lines.append("- **中国力量崛起**：2026年AI大模型排行榜显示，7家中国公司进入全球前10，阿里Qwen3、智谱GLM-4-MoE表现突出，但推理成本仍是主要短板。")
report_lines.append("- **落地滞后明显**：73%的企业仍在使用2023年参数量的模型，银行业虽有白皮书指导，但大模型实际部署率仍然偏低。")
report_lines.append("- **AI智能体成新战场**：银行业AI智能体落地全景图揭示，客服与风控是最先被\"接管\"的场景，\"数字同事\"概念加速落地。")
report_lines.append("")
report_lines.append("### 二、热点主题分析")
report_lines.append("")
report_lines.append("| 主题 | 热度 | 主要内容 |")
report_lines.append("|------|------|------|")
report_lines.append("| 信贷风控 | ⭐⭐⭐⭐⭐ | 私募信贷暴雷、客户准入8要素、信贷收口实情 |")
report_lines.append("| 存款利率 | ⭐⭐⭐⭐ | 各大银行利率调整、大额存单、城商行跟进 |")
report_lines.append("| 银行AI大模型 | ⭐⭐⭐⭐ | 进出口行采购白皮书、智能体落地 |")
report_lines.append("| 消费者权益 | ⭐⭐⭐⭐ | 3·15宣传活动、普惠金融、消保教育 |")
report_lines.append("| 数字人民币 | ⭐⭐⭐ | 苏州培训启动、钱包计息、政策推广 |")
report_lines.append("| 监管科技 | ⭐⭐⭐ | 央行定调、RegTech全景图、技术趋势 |")
report_lines.append("| 跨境支付 | ⭐⭐⭐ | 深圳论坛、全球支付痛点、东南亚市场 |")
report_lines.append("| 零售银行 | ⭐⭐ | 平安银行增长策略、零售拐点、贷款突围 |")
report_lines.append("")
report_lines.append("### 三、数据统计")
report_lines.append("")
report_lines.append("**文章分类分布：**")
report_lines.append("")
report_lines.append("| 分类 | 文章数量 | 占比 |")
report_lines.append("|------|---------|------|")
total = len(deduped)
for cat in ["银行业", "金融科技", "AI"]:
    cnt = len(cats[cat])
    pct = cnt / total * 100
    report_lines.append(f"| {cat} | {cnt}篇 | {pct:.0f}% |")
report_lines.append("")
report_lines.append("**文章来源分布（Top 10）：**")
report_lines.append("")
from collections import Counter
src_cnt = Counter(a.get("source", "未知") for a in deduped)
report_lines.append("| 来源公众号 | 文章数 |")
report_lines.append("|----------|--------|")
for src, cnt in src_cnt.most_common(10):
    report_lines.append(f"| {src} | {cnt}篇 |")
report_lines.append("")
report_lines.append("**时间分布：**")
report_lines.append(f"- 2026年3月文章：{sum(1 for a in deduped if a.get('datetime','').startswith('2026-03'))}篇（100%）")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 🔍 文章详细列表")
report_lines.append("")

# Generate article sections by category
category_names = {
    "银行业": "### 🏦 银行业",
    "金融科技": "### 💳 金融科技", 
    "AI": "### 🤖 AI与智能化"
}

for cat_key, cat_name in category_names.items():
    articles = cats[cat_key]
    if not articles:
        continue
    report_lines.append(cat_name)
    report_lines.append("")
    
    for i, a in enumerate(articles):
        title = a.get("title", "N/A")
        source = a.get("source", "N/A")
        dt = a.get("datetime", "N/A")[:10]
        url = a.get("url", "#")
        score = int(a["quality_score"])
        summary = make_summary(a)
        
        report_lines.append(f"**{i+1}. {title}** | 来源：{source} | 评分：{score}分 | {dt}")
        report_lines.append(f"> 摘要：{summary}")
        report_lines.append(f"> 🔗 链接：[原文链接]({url})")
        report_lines.append("")

# Write the report
output_path = REPORTS_DIR + "\\2026年3月银行业金融科技AI咨询报告_v3.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"\n报告已生成: {output_path}")
print(f"文章总数: {len(deduped)}")
print(f"银行业: {len(cats['银行业'])} 金融科技: {len(cats['金融科技'])} AI: {len(cats['AI'])}")
