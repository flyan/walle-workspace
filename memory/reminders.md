# 待办事项提醒

## 重要待办事项

### 1. 配置 Gemini 模型
**状态**: 进行中
**优先级**: 高
**创建时间**: 2026-03-14
**更新**: 2026-03-21
**详情**: 
- ✅ 在 openclaw.json 的 auth.profiles 中添加 Gemini 配置
- ✅ 在 agents.defaults.models 中添加 Gemini 模型
- ⏳ 需要从 Google AI Studio 获取 Gemini API 密钥
- ⏳ 设置环境变量：GEMINI_API_KEY
- ⏳ 测试模型：`openclaw chat --model gemini3`

### 2. 配置多个 agent
**状态**: 待处理
**优先级**: 中
**创建时间**: 2026-03-14
**详情**:
- 设计多个 agent 的工作流程
- 配置不同的 agent 角色（如：编码专家、文档助手、研究助手等）
- 设置 agent 间的协作机制

## 下一步行动

### Gemini 配置：
1. 访问 https://aistudio.google.com/ 获取 API 密钥
2. 设置环境变量：`export GEMINI_API_KEY=your_key_here` (Linux/Mac) 或 `set GEMINI_API_KEY=your_key_here` (Windows)
3. 测试：`openclaw chat --model gemini3`

### 多 agent 配置：
1. 确定需要哪些类型的 agent
2. 为每个 agent 配置不同的模型或参数
3. 设置 agent 间的通信机制
4. 创建示例工作流程

## 最后更新
2026-03-21