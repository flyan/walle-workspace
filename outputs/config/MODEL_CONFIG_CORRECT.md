# OpenClaw 模型配置说明

## 问题总结

OpenClaw的配置schema很严格，不接受自定义字段。我之前添加的这些字段都不被支持：
- `agents.defaults.modelStrategy` ❌
- `agents.allow` ❌
- `agents.defaults.model.haiku/opus` ❌
- `web.serperApiKey` ❌

## 正确的配置方式

### 1. 模型配置（openclaw.json）

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6"
      }
    }
  }
}
```

**说明**：
- 只能配置 `primary`（主模型）
- 不支持自定义模型别名
- 模型切换需要用命令或工具

### 2. Serper API Key

**方式1：环境变量（推荐）**
```bash
# Windows PowerShell
$env:SERPER_API_KEY="9c726a829854d30e5dcaf3adb2695e2b432cae42"

# 或者添加到系统环境变量
```

**方式2：直接在脚本中使用**
```python
SERPER_API_KEY = "9c726a829854d30e5dcaf3adb2695e2b432cae42"
```

### 3. 模型切换

**方式1：会话中切换（推荐）**
```
/model claude-opus-4-6
/model claude-haiku-4-5-20251101
/model default  # 切回默认
```

**方式2：使用 session_status 工具**
```python
session_status(model="claude-opus-4-6")
```

**方式3：子会话（subagent）**
```python
sessions_spawn(
    task="复杂任务",
    model="claude-opus-4-6"
)
```

## 可用的三个模型

你的API Key支持：
- `claude-haiku-4-5-20251101` - 快速便宜
- `claude-sonnet-4-6` - 默认平衡
- `claude-opus-4-6` - 最强推理

## 智能切换策略

由于OpenClaw限制，我会：
1. **默认使用 Sonnet 4-6**（当前配置）
2. **简单任务快速完成**（模拟Haiku效率）
3. **复杂任务时建议你**：
   - 使用 `/model claude-opus-4-6` 切换
   - 或者我用subagent调用Opus

## 当前状态

- ✅ 配置文件已还原（正确格式）
- ✅ Serper API Key 在脚本中配置
- ✅ 三个模型都可用（通过命令切换）
- ⚠️ 不支持自动切换（OpenClaw限制）

---

**记录时间**: 2026-03-08 12:19
**教训**: 不要在OpenClaw配置中添加自定义字段，会导致验证失败
