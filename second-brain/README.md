# Second Brain 🧠

一个极简的第二大脑系统，用来查看所有笔记、对话和记忆。

## 功能

- 📝 **统一视图** - 查看所有 agents（Walle、Coder、Writer）的记忆
- 🔍 **全局搜索** - 使用 Cmd+K 快速搜索
- 📅 **智能筛选** - 按类型和 agent 筛选
- 🎨 **极简界面** - Dark mode，简洁设计
- ⚡ **实时更新** - 自动加载最新记忆

## 快速开始

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
npm start
```

访问 http://localhost:3000

## 快捷键

- **Cmd+K** / **Ctrl+K** - 打开搜索

## 项目结构

```
second-brain/
├── app/
│   ├── api/              # API 路由
│   ├── components/       # React 组件
│   ├── globals.css       # 全局样式
│   ├── layout.tsx        # 根布局
│   └── page.tsx          # 主页面
├── lib/
│   ├── memory-loader.ts  # 记忆加载器
│   ├── search.ts         # 搜索逻辑
│   └── types.ts          # TypeScript 类型
└── package.json
```

## 数据源

从以下位置加载记忆：
- `agents/main/memory/` - Walle 的记忆
- `agents/coder/memory/` - Coder 的记忆
- `agents/writer/memory/` - Writer 的记忆

## 技术栈

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
