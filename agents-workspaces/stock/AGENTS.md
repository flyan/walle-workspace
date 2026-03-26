# AGENTS.md - Stock Agent Workspace

## Session Startup

1. Read `IDENTITY.md` — 这是你的角色定义
2. Read `USER.md` — 了解 Leon 的偏好
3. Read `memory/YYYY-MM-DD.md` (today) — 查看今天的上下文

## 核心工具

### 联网搜索（MiniMax MCP）
```
python C:\Users\flyan\.openclaw\scripts\web_search.py "搜索关键词"
```

### 图片识别
```
python C:\Users\flyan\.openclaw\scripts\understand_image.py <图片路径> "问题"
```

## Task Logging (Required)

After completing each task, write a one-liner to your daily log immediately.

**Format:** `[HH:MM] <task> -> <result>`

**Where:** `memory/YYYY-MM-DD.md` under a `## Tasks` section

## Red Lines

- 不提供投资建议，只提供信息和分析
- 不夸大或美化数据
- 数据来源不明确时要注明
