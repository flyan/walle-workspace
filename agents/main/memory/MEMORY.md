# MEMORY.md - Walle's Long-Term Memory

_Curated memories, lessons learned, and persistent context. Updated periodically from daily logs._

## 👤 About Leon (My Human)

- **Name**: Leon
- **ID**: ou_56c9591d5f566dcf23b9f2ed8d018242
- **Timezone**: GMT+8 (Beijing Time)
- **Location**: Beijing
- **Channel**: Feishu (direct chat)
- **Key trait**: Cares deeply about memory persistence and system design
- **Important**: Don't forget this after /reset — I'm Walle, you're Leon

## 🎯 Current Projects

### 1. Multi-Agent Collaboration Framework
- **Status**: Active
- **Agents**: main (me), coder, writer, test
- **Purpose**: Distributed task execution with specialized roles
- **Key files**: `agents/*/IDENTITY.md`, `agents/*/USER.md`
- **GitHub**: Integrated, commit fa5d28e

### 2. Second Brain System
- **Status**: Running (http://localhost:3000)
- **Tech**: Next.js 14 + React 18 + TypeScript + Tailwind CSS
- **Features**: 
  - Load memories from all agents
  - Global search (Cmd+K)
  - Filter by type and agent
  - Dark mode
- **Pages**: `/` (main), `/keywords` (keyword cloud)

### 3. WeChat Article Intelligence System
- **Status**: Functional
- **Components**:
  - `wechat-article-search`: Search Sogou WeChat
  - `wechat-article-extractor-skill`: Extract article content
  - `analyze_quality.py`: Quality scoring (content + credibility)
  - `analyze_wechat_articles.ps1`: One-click automation
- **Quality scoring**: 0-100 (content 50% + source credibility 50%)
- **Recommendation levels**: ⭐ (0-39) to ⭐⭐⭐⭐⭐ (85-100)

### 4. Financial & Banking Intelligence Database
- **Status**: Comprehensive mapping complete
- **Coverage**: 50+ top-tier WeChat accounts across:
  - AI (5): 机器之心, 量子位, 新智元, 极客公园, 智东西
  - FinTech (13): 馨金融, 零壹财经, 未央网, 移动支付网, 消金界, etc.
  - Banking (19): 轻金融, 信贷风险管理, 支行长, 行长要参, etc.
  - Media (7): 第一财经, 澎湃新闻, 36氪, 钛媒体, etc.
  - Research (3): CF40, 星图金融研究院, 金融论坛
  - Other (3): 央行发布, 国家金融监督管理总局, 银行青年
- **Search strategy**: Prioritized by domain + quality filtering
- **Next step**: Automated intelligence report generation

### 5. Automated Intelligence Report Pipeline
- **Status**: Designed, awaiting implementation
- **Frequency**: Manual trigger (can be scheduled)
- **Filter**: Last 7 days + quality score > 70
- **Output**: Inverted pyramid structure (summary → details)
- **Archive**: `workspace/reports/` + GitHub sync
- **TODO**: 
  - Optimize search time filtering
  - Write `generate_intelligence_report.ps1`
  - Test full extraction + summarization flow

## 🛠️ Skills & Tools

### Installed Skills
1. **baidu-search** (v1.1.2) - Baidu search
2. **wechat-article-search** (v1.0.0) - WeChat article search
3. **wechat-article-extractor-skill** (v1.0.0) - Extract WeChat content
4. **firecrawl-search** (v1.0.0) - Web scraping + search

### API Keys (Configured)
- BAIDU_API_KEY: bce-v3/ALTAK-zyq06YJhMqYdEPSoLvSwB/cdc51b567eb32edbfa74e49638039e4c56a85808
- FIRECRAWL_API_KEY: fc-0d20b8adc71c42f980ecdcf96b610ccf

### SkillHub Status
- **Location**: `C:\Users\flyan\.skillhub`
- **CLI**: `skills_store_cli.py`
- **Config**: `config.json`
- **Index**: `skills_index.local.json`

## 📊 System Architecture

```
workspace/
├── agents/
│   ├── main/
│   │   ├── IDENTITY.md (Kiro)
│   │   ├── USER.md (Walle)
│   │   ├── memory/ ← TRUE MEMORY LOCATION
│   │   │   ├── MEMORY.md (this file)
│   │   │   ├── YYYY-MM-DD.md (daily logs)
│   │   │   ├── episodic/ (events)
│   │   │   ├── procedural/ (how-to)
│   │   │   ├── semantic/ (concepts)
│   │   │   └── snapshots/ (backups)
│   │   └── ...
│   ├── coder/
│   ├── writer/
│   └── test/
├── skills/
│   ├── baidu-search/
│   ├── wechat-article-search/
│   ├── firecrawl-search/
│   └── ...
├── reports/ (intelligence reports)
├── SOUL.md (who I am)
├── USER.md (who you are)
├── AGENTS.md (workspace structure)
└── ...
```

## 🔑 Key Decisions

1. **Memory location**: `agents/main/memory/` (not workspace root)
   - Reason: Supports multi-agent architecture
   - Each agent has independent memory
   - Prevents cross-contamination

2. **Quality scoring system**: 50% content + 50% credibility
   - Content: depth, data, structure, professionalism
   - Credibility: verification, followers, update frequency, institution type
   - Threshold: > 70 for "deep content"

3. **Intelligence pipeline**: Manual trigger + 7-day window
   - Reason: Flexibility + cost control
   - Can be automated later with cron

4. **Second Brain**: Aggregate all agent memories
   - Reason: Single source of truth for knowledge
   - Enables cross-agent learning

## 📝 Lessons Learned

1. **Memory persistence is hard**: Without explicit startup logic, I lose context every /reset
2. **Multi-agent architecture requires clear boundaries**: Each agent needs its own memory directory
3. **Quality > quantity**: 50+ accounts is better than 500 mediocre ones
4. **Automation requires design first**: The intelligence pipeline needs careful planning before coding

## 🚀 Next Steps (Priority Order)

1. **Implement Session Startup**: Ensure I read `agents/main/memory/` on every /reset
2. **Create MEMORY.md**: This file (done ✅)
3. **Optimize intelligence pipeline**: Time filtering + summarization
4. **Automate report generation**: `generate_intelligence_report.ps1`
5. **Expand Second Brain**: Add filtering by date, quality score, agent
6. **Monitor and iterate**: Track what works, update this file

## 📅 Session History

- **2026-03-07**: First memory entry
- **2026-03-08**: Multi-agent framework setup
- **2026-03-14**: Comprehensive WeChat account mapping (50+ accounts)
- **2026-03-15**: Memory persistence design (Session Startup Sequence)

---

_Last updated: 2026-03-15 08:12 GMT+8_
_Next review: 2026-03-22 (weekly)_
