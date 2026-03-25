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

## 已安装的 Skywork 技能（公共目录）
- skywork-document（安装到了 workspace/skills，后续需要迁移）
- skywork-music-maker
- skywork-excel
- skywork-ppt
- skywork-design
- skywork-search
