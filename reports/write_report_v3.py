# -*- coding: utf-8 -*-
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

REPORTS_DIR = r"C:\Users\flyan\.openclaw\workspace\reports"
OUT_FILE = os.path.join(REPORTS_DIR, "report_out.md")

with open(os.path.join(REPORTS_DIR, "report_articles_v3.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

deduped = data["deduped"]
cats = data["cats"]

def s8(t):
    if not t:
        return t
    if len(t) > 85:
        for sep in ['\uff0c', '\u3002', '\uff01', '\uff1f']:
            idx = t.rfind(sep, 0, 80)
            if idx > 40:
                return t[:idx+1] + "\u2026"
        return t[:80] + "\u2026"
    return t

lines = []
lines.append("# 2026\u5e743\u6708\u94f6\u884c\u4e1a\u3001\u91d1\u878d\u79d1\u6280\u3001AI\u54a8\u8be2\u62a5\u544a")
lines.append("")
lines.append("---\n")
lines.append("[\u62a5\u544a\u6458\u8981]\u672c\u62a5\u544a\u6570\u636e\u6765\u6e90\uff1a\u5fae\u4fe1\u516c\u4f17\u53f7\u641c\u7d22\uff0c\u65f6\u95f4\u8303\u56f4\uff1a2026\u5e743\u6708\uff0c\u6587\u7ae0\u6570\uff1a%d\u7bc7\uff08\u94f6\u884c\u4e1a%d\u3001\u91d1\u878d\u79d1\u6280%d\u3001AI%d\uff09" % (
    len(deduped), len(cats.get("\u94f6\u884c\u4e1a",[])), len(cats.get("\u91d1\u878d\u79d1\u6280",[])), len(cats.get("AI",[]))))
lines.append("")
lines.append("## 1. \u884c\u4e1a\u8d8b\u52bf\u5206\u6790")
lines.append("")

# Banking section
lines.append("### 1.1 \u94f6\u884c\u4e1a\u70ed\u70b9")
lines.append("")
bank_cats_items = cats.get("\u94f6\u884c\u4e1a", [])
bank_themes = {
    "\u4fe1\u8d37\u98ce\u63a7": [],
    "\u5b58\u6b3e\u5229\u7387": [],
    "\u6570\u5b57\u5316\u8f6c\u578b": [],
    "\u94f6\u884cAI": [],
    "\u6d88\u8d39\u8005\u6743\u76ca": [],
    "\u5176\u4ed6": [],
}
for a in bank_cats_items:
    t = a.get("title","").lower()
    if any(k in t for k in ["\u4fe1\u8d37","\u8fdd\u89c4","\u7f6e","\u7b79","\u4fe1\u8d37\u9879\u76ee"]):
        bank_themes["\u4fe1\u8d37\u98ce\u63a7"].append(a)
    elif any(k in t for k in ["\u5b58\u6b3e","\u5229\u7387","\u5927\u989d","\u50a8\u84c4","\u50a8\u6237"]):
        bank_themes["\u5b58\u6b3e\u5229\u7387"].append(a)
    elif any(k in t for k in ["\u6570\u5b57\u8f6c\u578b","\u6570\u5b57\u5316","\u516c\u53f8","\u6570\u5b57\u4eba\u6c11\u5e01"]):
        bank_themes["\u6570\u5b57\u5316\u8f6c\u578b"].append(a)
    elif any(k in t for k in ["ai","\u5927\u6a21\u578b","\u667a\u80fd","\u667a\u80fd\u4f53","\u667a\u80fd\u4f53"]):
        bank_themes["\u94f6\u884cAI"].append(a)
    elif any(k in t for k in ["3\u00b715","\u6d88\u8d39","\u6d88\u4fdd","\u6d88\u8d39\u8005"]):
        bank_themes["\u6d88\u8d39\u8005\u6743\u76ca"].append(a)
    else:
        bank_themes["\u5176\u4ed6"].append(a)

for theme, articles in bank_themes.items():
    if not articles:
        continue
    lines.append("[%s] %d\u7bc7" % (theme, len(articles)))
    for a in articles[:2]:
        lines.append("  - %s [%s]" % (a.get("title","")[:55], a.get("datetime","")[:10]))
    lines.append("")

# Fintech
lines.append("### 1.2 \u91d1\u878d\u79d1\u6280")
lines.append("")
for a in cats.get("\u91d1\u878d\u79d1\u6280", []):
    lines.append("- %s [%s]" % (a.get("title","")[:60], a.get("datetime","")[:10]))
lines.append("")

# AI
lines.append("### 1.3 AI\u4e0e\u667a\u80fd\u5316")
lines.append("")
for a in cats.get("AI", []):
    lines.append("- %s [%s]" % (a.get("title","")[:60], a.get("datetime","")[:10]))
lines.append("")

# Hot topics
lines.append("## 2. \u70ed\u70b9\u4e3b\u9898\u5206\u6790")
lines.append("")
lines.append("|\u4e3b\u9898|\u70ed\u5ea6|\u5173\u6ce8\u5ea6|")
lines.append("|------|------|------|")
hot_data = [
    ("\u4fe1\u8d37\u98ce\u63a7", "\u9ad8", "\u79c1\u52df\u4fe1\u8d37\u66b4\u96f7\u3001\u8fdd\u89c4\u5904\u7f6e"),
    ("\u94f6\u884cAI\u5927\u6a21\u578b", "\u9ad8", "\u8fdb\u51fa\u53e3\u884c\u91c7\u8d2d\u3001\u667a\u80fd\u4f53\u843d\u5730"),
    ("\u5b58\u6b3e\u5229\u7387\u8c03\u6574", "\u4e2d", "\u5927\u989d\u5b58\u5355\u5206\u5316\u3001\u50a8\u6237\u9009\u62e9"),
    ("\u6570\u5b57\u4eba\u6c11\u5e01", "\u4e2d", "\u82cf\u5dde\u57f9\u8bad\u3001\u94b1\u5305\u8ba1\u606f"),
    ("\u76d1\u7ba1\u79d1\u6280", "\u4e2d", "RegTech\u5168\u666f\u3001\u5a92\u884c\u6307\u9488"),
    ("\u8de8\u5883\u652f\u4ed8", "\u4e2d", "\u8bba\u575b\u5bc6\u96c6\u3001\u5168\u7403\u5316"),
]
for row in hot_data:
    lines.append("|%s|%s|%s|" % row)
lines.append("")
lines.append("## 3. \u6570\u636e\u7edf\u8ba1")
lines.append("")
lines.append("\u6587\u7ae0\u5206\u7c7b\uff1a")
lines.append("")
lines.append("|\u5206\u7c7b|\u6570\u91cf|\u5360\u6bd4|")
lines.append("|------|---------|------|")
total = len(deduped)
for cat in ["\u94f6\u884c\u4e1a", "\u91d1\u878d\u79d1\u6280", "AI"]:
    cnt = len(cats.get(cat, []))
    pct = int(cnt/total*100) if total > 0 else 0
    lines.append("|%s|%d\u7bc7|%d%%|" % (cat, cnt, pct))
lines.append("")
lines.append("\u6587\u7ae0\u6765\u6e90Top8\uff1a")
lines.append("")
from collections import Counter
src_cnt = Counter(a.get("source","\u672a\u77e5") for a in deduped)
lines.append("|\u6765\u6e90|\u6570\u91cf|")
lines.append("|----------|--------|")
for src, cnt in src_cnt.most_common(8):
    lines.append("|%s|%d\u7bc7|" % (src, cnt))
lines.append("")
lines.append("---\n")
lines.append("## 4. \u6587\u7ae0\u8be6\u7ec6\u5217\u8868")
lines.append("")
lines.append("\u672c\u62a5\u544a\u6240\u6709\u6587\u7ae0\u5747\u6765\u81ea2026\u5e743\u6708\u5fae\u4fe1\u516c\u4f17\u53f7\uff0c\u6309\u8d44\u6e90\u8d4b\u5206\u4e0e\u65f6\u6548\u6027\u7b5d\u9009\u3002\u6587\u7ae0\u6458\u8981\u57fa\u4e8e\u539f\u6587\u6982\u8981\u81ea\u52a0\u5de5\u3002")
lines.append("")

article_num = 0
cat_order = ["\u94f6\u884c\u4e1a", "\u91d1\u878d\u79d1\u6280", "AI"]
cat_names = {"\u94f6\u884c\u4e1a": "4.1 \u94f6\u884c\u4e1a\u6587\u7ae0", "\u91d1\u878d\u79d1\u6280": "4.2 \u91d1\u878d\u79d1\u6280\u6587\u7ae0", "AI": "4.3 AI\u4e0e\u667a\u80fd\u5316\u6587\u7ae0"}

for cat_key in cat_order:
    articles = cats.get(cat_key, [])
    if not articles:
        continue
    lines.append("### %s" % cat_names[cat_key])
    lines.append("")
    for a in articles:
        article_num += 1
        title = a.get("title", "N/A")
        source = a.get("source", "N/A")
        dt = a.get("datetime", "N/A")[:10]
        url = a.get("url", "#")
        score = int(a["quality_score"])

        raw_summary = a.get("summary", "").strip()
        if raw_summary and len(raw_summary) > 15:
            summary = s8(raw_summary)
        else:
            summary = "\u8be5\u6587\u7ae0\u8b8a\u8fba\u4e86" + title[:35] + "\u7684\u5b9e\u8df5\u4e0e\u601d\u8003\u3002"

        lines.append("\u25cf [%d] **%s**  " % (article_num, title))
        lines.append("> \u6765\u6e90\uff1a%s | \u8bc4\u5206\uff1a%d\u5206 | %s" % (source, score, dt))
        lines.append("> \u6458\u8981\uff1a%s" % summary)
        lines.append("> \u94fe\u63a5\uff1a[%s](%s)" % (title[:40]+"\u2026" if len(title)>40 else title, url))
        lines.append("")
    lines.append("")

lines.append("---\n")
lines.append("\u3010\u62a5\u544a\u8bf4\u660e\u3011")
lines.append("1. \u672c\u62a5\u544a\u6240\u6709\u6587\u7ae0\u5747\u6765\u81ea\u5fae\u4fe1\u516c\u4f17\u53f7\uff0c\u7b5d\u9009\u8d77\u6e90\u4e8e2026\u5e743\u6708\u641c\u7d22\uff0c\u6309\u6765\u6e90\u4e13\u4e1a\u5ea6\u4e0e\u65f6\u6548\u6027\u7b5d\u9009")
lines.append("2. \u6587\u7ae0\u6570\uff1a%d\u7bc7 | \u65f6\u95f4\uff1a2026\u5e743\u6708" % article_num)
lines.append("3. \u6570\u636e\u8303\u56f4\uff1a\u94f6\u884c\u4e1a\u3001\u91d1\u878d\u79d1\u6280\u3001AI\u4e0e\u667a\u80fd\u5316")

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Done: " + OUT_FILE)
print("Articles: " + str(article_num))
