# 待办事项提醒

## 重要待办事项

### 1. 配置 Gemini 模型
**状态**: 待处理
**优先级**: 高
**创建时间**: 2026-03-14
**详情**: 
- 需要从 Google AI Studio 获取 Gemini API 密钥
- 需要在 openclaw.json 中添加 Gemini 模型配置
- 需要测试 Gemini 模型是否正常工作

### 2. 配置多个 agent
**状态**: 待处理
**优先级**: 中
**创建时间**: 2026-03-14
**详情**:
- 设计多个 agent 的工作流程
- 配置不同的 agent 角色（如：编码专家、文档助手、研究助手等）
- 设置 agent 间的协作机制

## 检查清单

### Gemini 配置步骤：
- [ ] 访问 https://aistudio.google.com/ 获取 API 密钥
- [ ] 在 openclaw.json 的 auth.profiles 中添加 Gemini 配置
- [ ] 在 agents.defaults.models 中添加 Gemini 模型
- [ ] 测试模型：`openclaw chat --model gemini`

### 多 agent 配置步骤：
- [ ] 确定需要哪些类型的 agent
- [ ] 为每个 agent 配置不同的模型或参数
- [ ] 设置 agent 间的通信机制
- [ ] 创建示例工作流程

## 下次提醒
请在下次会话时检查此文件，并开始处理这些待办事项。