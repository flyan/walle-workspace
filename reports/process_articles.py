# -*- coding: utf-8 -*-
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

REPORTS_DIR = r"C:\Users\flyan\.openclaw\workspace\reports"

with open(REPORTS_DIR + "\\filtered_articles_v3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

final = data["final_selection"]

def title_norm(t):
    for old, new in [("\u3000", " "), ("\u00a0", " "), ("\uff08", "("), ("\uff09", ")"), ("[", "("), ("]", ")")]:
        t = t.replace(old, new)
    for suffix in ["\u5efa\u8bae\u6536\u85cf", "\u65e9\u77e5\u9053\u65e9\u53d7\u76ca",
                   "\u4e00\u5b9a\u8981\u77e5\u9053", "\u5168\u662f\u5e72\u8d27",
                   "\u521a\u521a\u53d1\u5e03", "\u6700\u65b0\u7248", "\u6700\u65b0\u8c03\u6574"]:
        idx = t.find(suffix)
        if idx >= 0:
            t = t[:idx].strip()
    return t.strip()

seen = set()
deduped = []
for a in final:
    n = title_norm(a.get("title", ""))
    if n not in seen:
        seen.add(n)
        deduped.append(a)

deduped.sort(key=lambda x: -x["quality_score"])
deduped = deduped[:55]
print("Deduped:", len(deduped))

# classify
def classify(a):
    text = (a.get("title", "") + " " + a.get("summary", "") + " " + a.get("source", "")).lower()
    ai_k = ["ai", "\u5927\u6a21\u578b", "\u751f\u6210\u5f0f", "\u673a\u5668\u5b66\u4e60",
            "\u4eba\u5de5\u667a\u80fd", "gpt", "llm", "\u6df1\u5ea6\u5b66\u4e60",
            "\u667a\u80fd\u5316", "\u6a21\u578b", "\u667a\u80fd\u4f53"]
    ft_k = ["\u652f\u4ed8", "\u6570\u5b57\u4eba\u6c11\u5e01", "\u533a\u5757\u94fe",
            "\u6d88\u8d39\u91d1\u878d", "\u76d1\u7ba1\u79d1\u6280", "\u5f00\u653e\u94f6\u884c",
            "api", "\u4f9b\u5e94\u94fe\u91d1\u878d", "\u8de8\u5883", "\u91d1\u878d\u79d1\u6280"]
    bk_k = ["\u94f6\u884c", "\u4fe1\u8d37", "\u5b58\u6b3e", "\u8d37\u6b3e", "\u7f51\u70b9",
            "\u96f6\u552e", "\u8d22\u5bcc", "\u98ce\u63a7", "\u8d44\u672c", "\u8d44\u4ea7",
            "\u51c0\u606f\u5dee", "\u4e0d\u826f", "\u4fe1\u7528\u5361", "\u5bf9\u516c",
            "\u63a5\u50a8", "\u5229\u7387"]
    def score_it(kws):
        s = 0
        title_l = a.get("title", "").lower()
        for k in kws:
            if k in title_l:
                s += 3
            if k in text:
                s += 1
        return s
    ai_s = score_it(ai_k)
    ft_s = score_it(ft_k)
    bk_s = score_it(bk_k)
    if ai_s >= max(ai_s, ft_s, bk_s):
        return "AI"
    elif ft_s >= bk_s:
        return "\u91d1\u878d\u79d1\u6280"
    else:
        return "\u94f6\u884c\u4e1a"

cats = {"\u94f6\u884c\u4e1a": [], "\u91d1\u878d\u79d1\u6280": [], "AI": []}
for a in deduped:
    cats[classify(a)].append(a)
for c in cats:
    cats[c].sort(key=lambda x: -x["quality_score"])

print("Categories: Banking=%d FinTech=%d AI=%d" % (
    len(cats["\u94f6\u884c\u4e1a"]), len(cats["\u91d1\u878d\u79d1\u6280"]), len(cats["AI"])))

# Save intermediate
with open(REPORTS_DIR + "\\report_articles_v3.json", "w", encoding="utf-8") as f:
    json.dump({"deduped": deduped, "cats": cats}, f, ensure_ascii=False, indent=2)
print("Saved report_articles_v3.json")
