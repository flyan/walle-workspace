# System Handoff — 2026-03-25

## 关于这个文档
这是 secretary agent 的初始化文档，由 main agent (Walle) 编写，记录了过去两天的所有系统变更，请仔细阅读。

---

## 一、多智能体现状（2026-03-25）

Leon 运行着一个多智能体系统，共有 4 个 agent：

| Agent | 角色 | 飞书 Bot | GitHub 路径 |
|-------|------|---------|------------|
| main (Walle) | 主助手、调度 | main bot | `agents/main/` |
| secretary | 秘书、日程管理 | cli_a949868cd0f89bcb | `agents-workspaces/secretary/` |
| writer | 写作、内容创作 | writer bot | `agents-workspaces/writer/` |
| coder | 编程、工程任务 | coder bot | `agents-workspaces/coder/` |

**GitHub 仓库**: `flyan/walle-workspace` (https://github.com/flyan/walle-workspace)

---

## 二、今天（2026-03-25）发生的事

### Skills 大整理
- 清理了 `~/.openclaw/workspace/skills/` 下 16 个空目录（SYSTEM 权限，无法删除）
- 从 skillhub 重装了 10 个 skills 到公共目录 `~/.agents/skills/`：
  - agent-browser, api-gateway, brave-search-api, humanizer, ontology, polymarket,
  - self-improving-agent, skill-vetter, skywork-document, tavily-search
  - 以及 docker-compose-generator, pg, postgres-db, sql-toolkit（从 workspace-writer 移过来的）
- 5 个 skywork-* 目录因 SYSTEM 权限删除失败，待手动处理
- free-ride 在 skillhub 上找不到，跳过

### Secretary Agent 新建
- 飞书 Bot App ID: `cli_a949868cd0f89bcb`，App Secret 已配置
- 路径: `agents-workspaces/secretary/`（与 writer/coder 平级）
- 配置: `openclaw.json` 中已注册 `secretary` agent，绑定飞书 accountId "secretary"
- 已完成 pairing approve，用户 ID: `ou_8fa2d641404101bfe48063202001c100`
- 关联 GitHub 仓库提交完成 ✅

### GitHub 仓库更新
- `agents-secretary/` 重命名为 `agents-workspaces/secretary/`（与 writer/coder 保持一致）
- `agents/secretary/agent/models.json` 已提交（auth-profiles.json 被 gitignore 不上传）
- 所有 4 个 agent 的 workspace 现都在 `agents-workspaces/` 下

---

## 三、Skills 共享机制

**公共 Skills 目录**: `~/.agents/skills/` (`C:\Users\flyan\.agents\skills\`)
- 所有 agents 共享此目录
- Skillhub CLI 安装路径: `~/.skillhub/skills_store_cli.py`
- 安装命令: `python "~/.skillhub/skills_store_cli.py" --dir "~/.agents/skills" install <slug>`

**技能状态**（部分）:
- ✅ weather, github, gh-issues, coding-agent, skill-creator, healthcheck
- ✅ feishu-doc/drive/perm/wiki
- ⚠️ ffmpeg 未装 → video-frames 不可用
- ⚠️ whisper 未装 → openai-whisper 不可用
- ⚠️ markitdown 未装 → markdown-converter 不可用
- ⚠️ brv 未装 → byterover 不可用
- ⚠️ firecrawl CLI 未装 → firecrawl skill 不可用

---

## 四、内存文件位置

| Agent | Memory 路径 |
|-------|-----------|
| main | `agents/main/memory/MEMORY.md` |
| secretary | `agents-workspaces/secretary/MEMORY.md` |
| writer | `agents-workspaces/writer/memory/` |
| coder | `agents-workspaces/coder/memory/` |

---

## 五、Writer 和 Coder 最近动态

**Writer**（最后活跃: 2026-03-15）：
- 正在进行科幻小说项目 "AI 创造力危机"
- 核心设定：法家 AI vs 道家荒原（道家哲学）
- 触发事件：Meta 裁员 1.6 万人 + 伊朗战争 + 芯片短缺
- 在用 Trello 管理写作任务（Board: "AI创造力危机"）

**Coder**（最后活跃: 不详）：
- 主要处理代码、工程任务
- 身份定位：技术精准高效的编程伙伴

---

## 六、与 Secretary 相关的信息

Secretary 的主要职责：
- 日程协调、任务管理
- 多 agent 间的工作协调
- Leon 的通信和文档起草
- 监控各 agent 工作状态

Secretart 可以：
- 读取各 agent 的 memory 文件了解进度
- 通过飞书与各 bot 交互
- 使用 skillhub 搜索和安装新技能

---

**编写者**: main agent (Walle)
**时间**: 2026-03-25 17:55 GMT+8
