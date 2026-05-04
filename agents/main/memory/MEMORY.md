# Long-term Memory

## Skills 安装偏好
- **公共技能目录**: `~/.agents/skills/` (`C:\Users\flyan\.agents\skills\`)
- 所有 agents 共享此目录，安装时使用 `--dir $env:USERPROFILE\.agents\skills`
- Leon 明确要求：以后安装 skills 都装到公共目录，而不是 `~/.openclaw/workspace/skills/`
- 日期: 2026-03-21

## Skillhub CLI
- 安装路径: `~/.skillhub/skills_store_cli.py`
- Wrapper: `~/.local/bin/skillhub.bat`
- 命令: `python "$env:USERPROFILE\.skillhub\skills_store_cli.py" --dir "$env:USERPROFILE\.agents\skills" install <slug>`
- 版本: 2026.3.18

## GitHub 仓库与 Agent 提交流程
- **仓库**: `flyan/walle-workspace` (`git@github.com:flyan/walle-workspace.git`)
- **Agent workspace 存放路径**: `agents-workspaces/`（与 writer/coder 平级）
  - `agents-workspaces/secretary/` — secretary workspace
  - `agents-workspaces/writer/` — writer workspace
  - `agents-workspaces/coder/` — coder workspace
- **Agent 配置存放路径**: `agents/`（agent models.json、sessions 等）
  - `agents/secretary/agent/models.json`
  - `agents/main/` — main agent 配置
- **敏感文件**（gitignore，不上传）: `auth-profiles.json`

### 上传 Agent 到 GitHub 的标准流程
当 Leon 要求上传 agents/workspace 到 GitHub 时，执行以下步骤：

1. **确认目录位置**：
   - workspace 文件 → 放在 `agents-workspaces/<name>/` 下（与 writer/coder 平级）
   - agent 配置 → 放在 `agents/<name>/` 下

2. **提交 git**：
   ```
   git add agents/<name>/ agents-workspaces/<name>/
   git commit -m "feat: add <name> agent"
   git push origin main
   ```

3. **不需要开 PR 分支**：直接 push 到 main（仓库目前是单人或小团队使用，直接推 main 更高效）

4. **openclaw.json 更新**：如果修改了配置，确保路径指向正确的 workspace 目录后同步更新 git

日期: 2026-03-25

## 已安装的 Skywork 技能（公共目录）
- skywork-document（安装到了 workspace/skills，后续需要迁移）
- skywork-music-maker
- skywork-excel
- skywork-ppt
- skywork-design
- skywork-search

## Hermes 配置修复
- **Hermes 路径**: WSL Ubuntu 里 `/home/flyan/.hermes/config.yaml`
- **问题**: `model.provider` 被设成 `claude-thirdparty`（第三方代理），导致 Claude 模型调用失败
- **修复方法**: 改 `model.provider: minimax-cn`
- **读取命令**: `wsl -e bash -c "cat /home/flyan/.hermes/config.yaml"`
- **写入命令**: `wsl -e bash -c "cat > /home/flyan/.hermes/config.yaml << 'EOF'\n<内容>\nEOF"`
- **核心改动**:
  ```yaml
  model:
    default: claaude-sonnet-4-6
    provider: minimax-cn  # 从 claude-thirdparty 改为 minimax-cn
    base_url: https://api.minimaxi.com/anthropic
  ```
- **生效方式**: 修改后需重启 Hermes（`systemctl --user restart hermes-gateway`）
- 日期: 2026-04-20
