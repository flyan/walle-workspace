# OpenClaw 模型可用性报告

## 测试时间
2026年3月22日 22:18

## 测试结果

### ✅ 确认可用的模型
1. **deepseek/deepseek-chat** (别名: deepseek)
   - 类型: fallback
   - 状态: **确认可用** (我当前正在使用此模型)

### ❓ 状态未知的模型 (需要API密钥验证)

#### 主要模型 (Primary)
1. **anthropic/claude-haiku-4-5-20251001** (别名: haiku)

#### 备用模型 (Fallbacks)
2. **gemini/[L]gemini-3-flash-preview** (别名: gemini3f)
3. **gemini/[L]gemini-3-pro-preview-search** (别名: gemini3search)
4. **qwen/qwen3-next-80b-a3b-instruct:free**
5. **openrouter/free**
6. **nvidia/nemotron-3-super-120b-a12b:free**
7. **healer-alpha:free**
8. **nvidia/nemotron-3-nano-30b-a3b:free**
9. **openrouter/hunter-alpha:free**

#### 其他配置模型
10. **anthropic/claude-sonnet-4-6** (别名: sonnet)
11. **anthropic/claude-opus-4-6** (别名: opus)
12. **deepseek/deepseek-reasoner** (别名: deepseek-r1)
13. **gemini/[L]gemini-3-pro-preview** (别名: gemini3)

## 统计摘要
- **总共配置模型**: 14个
- **确认可用**: 1个 (deepseek/deepseek-chat)
- **状态未知**: 13个
- **需要API密钥验证**: 13个

## 模型分类

### Anthropic 系列
- ✅ **Claude Haiku** (haiku) - 主要模型 (状态未知)
- ❓ **Claude Sonnet** (sonnet) - 状态未知
- ❓ **Claude Opus** (opus) - 状态未知

### Google Gemini 系列
- ❓ **Gemini 3 Flash** (gemini3f) - 状态未知
- ❓ **Gemini 3 Pro** (gemini3) - 状态未知
- ❓ **Gemini 3 Pro Search** (gemini3search) - 状态未知

### DeepSeek 系列
- ✅ **DeepSeek Chat** (deepseek) - **确认可用**
- ❓ **DeepSeek Reasoner** (deepseek-r1) - 状态未知

### 免费模型 (OpenRouter)
- ❓ **openrouter/free** - 状态未知
- ❓ **openrouter/hunter-alpha:free** - 状态未知
- ❓ **healer-alpha:free** - 状态未知

### NVIDIA 系列
- ❓ **Nemotron-3 Super 120B** - 状态未知
- ❓ **Nemotron-3 Nano 30B** - 状态未知

### 其他
- ❓ **Qwen 3 Next 80B** - 状态未知

## 测试方法说明
1. **直接验证**: deepseek/deepseek-chat 通过实际使用验证为可用
2. **间接推断**: 其他模型需要API密钥和网络连接验证
3. **测试限制**: 之前的自动化测试脚本因权限问题失败

## 建议操作

### 立即可用的
1. **继续使用 deepseek/deepseek-chat** - 已确认工作正常

### 需要验证的
1. **检查API密钥**:
   - Anthropic API密钥 (用于Claude系列)
   - Google Gemini API密钥
   - DeepSeek API密钥 (已确认有效)

2. **测试其他模型**:
   - 使用 `/model` 命令切换模型测试
   - 检查网络连接和API配额

3. **配置优化**:
   - 确保所有API密钥正确配置
   - 检查网络代理设置
   - 验证免费模型的可用性

## 结论
- **当前工作模型**: deepseek/deepseek-chat ✅
- **主要模型状态**: anthropic/claude-haiku-4-5-20251001 (需要验证)
- **备用模型**: 9个 (都需要API密钥验证)
- **建议**: 先使用确认可用的deepseek模型，逐步验证其他模型

---
*报告生成时间: 2026-03-22 22:18*