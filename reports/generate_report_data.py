# -*- coding: utf-8 -*-
"""Generate final report with summaries"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

REPORTS_DIR = r"C:\Users\flyan\.openclaw\workspace\reports"

# Load filtered articles
with open(REPORTS_DIR + "\\filtered_articles_v3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

final = data["final_selection"]

# Deduplicate by title similarity
def title_normalize(t):
    """Remove common clickbait phrases"""
    t = t.replace("!", "").replace("，", ",").replace("。", ".")
    # Remove common suffixes
    for suffix in ["建议收藏", "早知道早受益", "一定要知道", "全是干货", "刚刚发布", "最新版", "最新调整"]:
        if suffix in t:
            t = t[:t.index(suffix)]
    return t.strip()

seen_titles = set()
deduped = []
for a in final:
    norm = title_normalize(a.get("title", ""))
    if norm not in seen_titles:
        seen_titles.add(norm)
        deduped.append(a)

print(f"After dedup: {len(deduped)} articles")

# Now generate report
# We need to write summaries - use the existing summary or generate one
report_articles = []
for a in deduped:
    title = a.get("title", "N/A")
    source = a.get("source", "N/A")
    dt = a.get("datetime", "N/A")[:10]
    url = a.get("url", "#")
    summary = a.get("summary", "")
    score = a["quality_score"]
    
    # Generate summary from existing summary
    if summary and len(summary) > 20:
        # Clean up summary
        clean_summary = summary.strip()
        if len(clean_summary) > 100:
            clean_summary = clean_summary[:100] + "..."
    else:
        # Generate from title
        clean_summary = f"本文探讨了{title.replace('!','').replace('？','')}相关内容。"
    
    report_articles.append({
        "title": title,
        "source": source,
        "datetime": dt,
        "url": url,
        "summary": clean_summary,
        "score": score,
        "is_march": a.get("is_march_2026", True)
    })

# Sort by score
report_articles.sort(key=lambda x: -x["score"])

# Take top 55
report_articles = report_articles[:55]

# Print for review
for i, a in enumerate(report_articles):
    print(f"{i+1:2d}. [{a['score']:.0f}] {a['datetime']} | {a['source'][:15]:15s} | {a['title'][:60]}")

# Save report data
with open(REPORTS_DIR + "\\report_articles_v3.json", "w", encoding="utf-8") as f:
    json.dump(report_articles, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(report_articles)} articles to report_articles_v3.json")
