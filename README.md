# Walle Agent Workspace

🤖 个人 AI 助手 Walle 的工作空间配置与记忆库。

## 📁 目录结构

```
.
├── AGENTS.md           # Agent 运行规则与内存管理指南
├── SOUL.md             # Agent 性格、价值观与边界
├── IDENTITY.md         # Agent 身份信息（名字、风格、emoji）
├── USER.md             # 用户信息与偏好设置
├── TOOLS.md            # 本地工具与系统配置
├── HEARTBEAT.md        # 定期检查任务清单
├── memory/             # 每日记忆日志
│   └── YYYY-MM-DD.md   # 按日期记录的事件与学习
└── .gitignore          # Git 忽略规则
```

## 🎯 核心文件说明

| 文件 | 用途 | 更新频率 |
|------|------|--------|
| **SOUL.md** | 定义 Agent 的性格与行为准则 | 偶尔 |
| **AGENTS.md** | 运行指南与内存管理策略 | 偶尔 |
| **IDENTITY.md** | Agent 的名字、风格、头像 | 很少 |
| **USER.md** | 用户信息与交互偏好 | 很少 |
| **TOOLS.md** | 本地工具、SSH、摄像头等配置 | 按需 |
| **memory/YYYY-MM-DD.md** | 每日事件、决策、学习记录 | 每天 |

## 🧠 记忆系统

- **日记** (`memory/YYYY-MM-DD.md`): 原始日志，记录每天发生的事
- **长期记忆** (`MEMORY.md`): 精选的重要信息与决策（仅在主会话加载）

## 🔐 安全说明

- ✅ 所有配置文件已版本控制
- ❌ 不包含 API keys、tokens、密码
- ❌ 不包含 `~/.openclaw/` 下的敏感信息
- 📝 敏感数据存储在 `~/.openclaw/credentials/` 中

## 🚀 快速开始

### 克隆到新机器

```bash
git clone https://github.com/flyan/walle-workspace.git ~/.openclaw/workspace
cd ~/.openclaw/workspace
openclaw setup --workspace .
```

### 日常更新

```bash
cd ~/.openclaw/workspace
git add .
git commit -m "Update: 描述你的改动"
git push
```

### 回滚到某个版本

```bash
git log --oneline          # 查看历史
git reset --hard <commit>  # 回滚到指定版本
```

## 📊 Agent 信息

- **名字**: Walle (瓦力)
- **风格**: 直接、实用、有个性
- **主要能力**: 日常工作助手、代码协作、系统管理
- **时区**: GMT+8

## 🔗 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/openclaw/openclaw)
- [社区 Discord](https://discord.com/invite/clawd)

---

**最后更新**: 2026-03-10
